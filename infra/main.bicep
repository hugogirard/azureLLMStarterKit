targetScope = 'subscription'

@description('The location where the resources will be created')
param location string

@description('The name of the resource group')
param resourceGroupName string

resource rg 'Microsoft.Resources/resourceGroups@2024-11-01' = {
  name: resourceGroupName
  location: location
}

var suffix = uniqueString(rg.id)

/* Storage needed for upload and training data for the RAG */

module storage 'br/public:avm/res/storage/storage-account:0.19.0' = {
  scope: rg
  params: {
    name: 'str${suffix}'
    allowBlobPublicAccess: true
    blobServices: {
      containers: [
        {
          name: 'upload'
        }
        {
          name: 'training'
        }
      ]
    }
    allowSharedKeyAccess: false
  }
}

/* Hosting for frontend and backend on App Service */

module appserviceplan 'br/public:avm/res/web/serverfarm:0.4.1' = {
  scope: rg
  params: {
    name: 'asp-${suffix}'
    kind: 'linux'
    skuCapacity: 1
    skuName: 'P1mv3'
    location: location
    zoneRedundant: false
  }
}

module backend 'br/public:avm/res/web/site:0.15.1' = {
  scope: rg
  params: {
    name: 'api-${suffix}'
    kind: 'app,linux,container'
    serverFarmResourceId: appserviceplan.outputs.resourceId
  }
}

module frontend 'br/public:avm/res/web/site:0.15.1' = {
  scope: rg
  params: {
    name: 'front-${suffix}'
    kind: 'app,linux,container'
    serverFarmResourceId: appserviceplan.outputs.resourceId
  }
}

/* CosmosDB needed for chat history */
module cosmosdb 'br/public:avm/res/document-db/database-account:0.12.0' = {
  scope: rg
  params: {
    name: 'cosmosdb-${suffix}'
    location: location
    enableMultipleWriteLocations: false
    automaticFailover: false
    locations: [
      {
        failoverPriority: 0
        isZoneRedundant: false
        locationName: location
      }
    ]
    sqlDatabases: [
      {
        name: 'chat'
        containers: [
          {
            name: 'conversation'
            indexingPolicy: {
              automatic: true
            }
            paths: [
              '/username'
              '/sessionId'
            ]
          }
        ]
        throughput: 1000
        autoscaleSettingsMaxThroughput: 1000
      }
    ]
  }
}

/* AI Services */

module openai 'br/public:avm/res/cognitive-services/account:0.10.2' = {
  scope: rg
  params: {
    name: 'openai-${suffix}'
    kind: 'OpenAI'
    location: location
  }
}

module search 'br/public:avm/res/search/search-service:0.7.2' = {
  scope: rg
  params: {
    name: 'search-${suffix}'
    location: location
    managedIdentities: {
      systemAssigned: true
    }
    partitionCount: 1
    replicaCount: 1
    sku: 'standard'
  }
}

/* Output */

output backendResourceName string = backend.outputs.name
output frontEndResourceName string = frontend.outputs.name
output openaiResourceName string = openai.outputs.name
