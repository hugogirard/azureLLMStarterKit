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
