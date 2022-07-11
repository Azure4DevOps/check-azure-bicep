@description('Specifies region of RG.')
param location string = resourceGroup().location

@description('Storage Account type')
@allowed([
  'Standard_LRS'
  'Standard_GRS'
  'Standard_ZRS'
  'Premium_LRS'
])
param storageAccountType string = 'Standard_LRS'

param instLocation array = [
  'westeurope'
]

param instName array = [
  'euw'
]

@description('Type of environment where this deployment should occur.')
@allowed([
  'pr'
  'dev'
  'prod'
  'jnno'
  'test'
])
param environmentType string = 'dev'

@description('Name of Application.')
param applicationName string = 'ga2022'
param storageConfig object = {
  kind: 'StorageV2'
  accessTier: 'Hot'
  httpsTrafficOnlyEnabled: true
}
param nameConv object = {
  storageAccountName: 'stacc'
  hostingPlanName: 'plan'
  siteName: 'site'
  trafficManagerName: 'tmanager'
  appins: 'appins'
}

var namestorage = '${applicationName}${environmentType}'
var name = '${applicationName}-${environmentType}'

resource namestorage_instName_nameConv_storageAccountName 'Microsoft.Storage/storageAccounts@2021-04-01' = [for (item, i) in instLocation: {
  sku: {
    name: storageAccountType
  }
  kind: storageConfig.kind
  properties: {
    supportsHttpsTrafficOnly: storageConfig.httpsTrafficOnlyEnabled
    accessTier: storageConfig.accessTier
    encryption: {
      services: {
        blob: {
          enabled: true
        }
        file: {
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
  }
  tags: {
    displayName: 'Array Storage Accounts'
  }
  location: item
  name: '${namestorage}${instName[i]}${nameConv.storageAccountName}'
}]

resource name_instName_nameConv_hostingPlanName 'Microsoft.Web/serverfarms@2021-03-01' = [for (item, i) in instLocation: {
  sku: {
    name: 'Y1' //Dynamic
  }
  kind: 'linux'
  location: item
  name: '${name}-${instName[i]}${nameConv.hostingPlanName}'
}]

resource name_instName_nameConv_siteName 'Microsoft.Web/sites@2020-12-01' = [for (item, i) in instLocation: {
  name: '${name}-${instName[i]}${nameConv.siteName}'
  location: item
  dependsOn: [
    name_instName_nameConv_hostingPlanName
  ]
  tags: {
    displayName: 'Array Sites'
  }
  kind: 'functionapp'
  properties: {
    httpsOnly: true
    serverFarmId: resourceId('Microsoft.Web/serverfarms', '${name}-${instName[i]}${nameConv.hostingPlanName}')
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${namestorage}${instName[i]}${nameConv.storageAccountName};AccountKey=${listKeys(namestorage_instName_nameConv_storageAccountName[i].id, namestorage_instName_nameConv_storageAccountName[i].apiVersion).keys[0].value};EndpointSuffix=${environment().suffixes.storage}'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'dotnet'
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: name_global_nameConv_appins.properties.InstrumentationKey
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: 'InstrumentationKey=${name_global_nameConv_appins.properties.InstrumentationKey}'
        }
      ]
    }
  }

}]

resource trafficManagerProfile 'Microsoft.Network/trafficManagerProfiles@2018-08-01' = {
  name: '${name}-global-${nameConv.trafficManagerName}'
  location: 'global'
  dependsOn: [
    name_instName_nameConv_siteName
  ]
  properties: {
    profileStatus: 'Enabled'
    trafficRoutingMethod: 'Priority'
    dnsConfig: {
      relativeName: '${name}-global-${nameConv.trafficManagerName}'
      ttl: 30
    }
    monitorConfig: {
      protocol: 'HTTPS'
      port: 443
      path: '/api/IsAlive'
    }
  }
}

resource trafficManagerAzureEndpoint 'Microsoft.Network/trafficManagerProfiles/azureEndpoints@2018-08-01' = [for (item, i) in instLocation: {
  name: '${name}-${instName[i]}${nameConv.siteName}'
  parent: trafficManagerProfile
  dependsOn: [
    name_instName_nameConv_siteName
  ]
  properties: {
    endpointMonitorStatus: 'Online'
    targetResourceId: resourceId('Microsoft.Web/sites', '${name}-${instName[i]}${nameConv.siteName}')
  }
}]

resource name_global_nameConv_appins 'Microsoft.Insights/components@2020-02-02' = {
  name: '${name}-global-${nameConv.appins}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}
