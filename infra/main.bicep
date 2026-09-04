targetScope = 'subscription'

@description('Short environment name.')
@allowed(['dev', 'test', 'prod'])
param environment string = 'dev'

@description('Azure region approved for the workload.')
param location string = 'westeurope'

@description('Stable workload identifier used in resource names.')
param workloadName string = 'modernization'

@description('Deploy an inexpensive application landing-zone foundation only.')
param deployFoundation bool = true

var suffix = uniqueString(subscription().id, workloadName, environment)
var resourceGroupName = 'rg-${workloadName}-${environment}'

resource workloadResourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = if (deployFoundation) {
  name: resourceGroupName
  location: location
  tags: {
    environment: environment
    workload: workloadName
    managedBy: 'bicep'
    evidenceStatus: 'requires-post-deployment-verification'
  }
}

module platform 'modules/workload-platform.bicep' = if (deployFoundation) {
  name: 'workload-platform-${suffix}'
  scope: workloadResourceGroup
  params: {
    environment: environment
    location: location
    workloadName: workloadName
    suffix: suffix
  }
}

output resourceGroupName string = deployFoundation ? workloadResourceGroup.name : ''
output platformOutputs object = deployFoundation ? platform!.outputs : {}
