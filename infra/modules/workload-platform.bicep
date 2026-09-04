param environment string
param location string
param workloadName string
param suffix string

var logName = 'log-${workloadName}-${environment}-${suffix}'
var storageName = take('stmod${environment}${suffix}', 24)

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logName
  location: location
  tags: {
    environment: environment
    workload: workloadName
  }
  properties: {
    retentionInDays: environment == 'prod' ? 90 : 30
    sku: {
      name: 'PerGB2018'
    }
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  tags: {
    environment: environment
    workload: workloadName
  }
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    minimumTlsVersion: 'TLS1_2'
    publicNetworkAccess: 'Enabled'
    supportsHttpsTrafficOnly: true
  }
}

output logAnalyticsWorkspaceId string = logAnalytics.id
output storageAccountId string = storage.id
