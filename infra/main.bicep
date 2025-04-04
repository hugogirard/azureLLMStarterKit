targetScope = 'subscription'

@description('The location where the resources will be created')
param location string

@description('The name of the resource group')
param resourceGroupName string

module rg 'br/public:avm/res/resources/resource-group:0.4.1' = {
  params: {
    name: resourceGroupName
    location: location
  }
}

var suffix = uniqueString(rg.outputs.resourceId)

/* Storage needed for upload and training data for the RAG */

module storage 'br/public:avm/res/storage/storage-account:0.19.0' = {
  scope: resourceGroup(resourceGroupName)
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
  scope: resourceGroup(resourceGroupName)
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
  scope: resourceGroup(resourceGroupName)
  params: {
    name: 'api-${suffix}'
    kind: 'app,linux,container'
    serverFarmResourceId: appserviceplan.outputs.resourceId
  }
}

module frontend 'br/public:avm/res/web/site:0.15.1' = {
  scope: resourceGroup(resourceGroupName)
  params: {
    name: 'front-${suffix}'
    kind: 'app,linux,container'
    serverFarmResourceId: appserviceplan.outputs.resourceId
  }
}

/* CosmosDB needed for chat history */
module cosmosdb 'br/public:avm/res/document-db/database-account:0.12.0' = {
  scope: resourceGroup(resourceGroupName)
  params: {
    name: 'cosmosdb-${suffix}'
    location: location
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
              'sessionId'
            ]
          }
        ]
        throughput: 1000
        autoscaleSettingsMaxThroughput: 1000
      }
    ]
  }
}

@description('Name ')
output backendResourceName string = backend.outputs.name
