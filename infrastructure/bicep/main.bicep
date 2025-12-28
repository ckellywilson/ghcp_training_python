// Main infrastructure orchestration for microservices using Azure Verified Modules (AVM)
targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@sys.description('Name of the environment (e.g., dev, staging, prod)')
param environmentName string

@minLength(1)
@sys.description('Primary location for all resources')
param location string

@sys.description('Id of the principal to assign Key Vault access')
param principalId string = ''

@sys.description('Tags to apply to all resources')
param tags object = {
  Environment: environmentName
  ManagedBy: 'Bicep'
  Project: 'ghcp-training-microservices'
}

// Generate unique suffix for globally unique names
var uniqueSuffix = uniqueString(subscription().id, environmentName)

// Resource group
resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-${environmentName}'
  location: location
  tags: tags
}

// Log Analytics Workspace using AVM
module logAnalytics 'br/public:avm/res/operational-insights/workspace:0.9.1' = {
  name: 'logAnalytics-deployment'
  scope: rg
  params: {
    name: 'log-${environmentName}-${uniqueSuffix}'
    location: location
    skuName: 'PerGB2018'
    dataRetention: 30
    tags: tags
  }
}

// Application Insights using AVM
module appInsights 'br/public:avm/res/insights/component:0.4.2' = {
  name: 'appInsights-deployment'
  scope: rg
  params: {
    name: 'appi-${environmentName}-${uniqueSuffix}'
    location: location
    workspaceResourceId: logAnalytics.outputs.resourceId
    kind: 'web'
    applicationType: 'web'
    tags: tags
  }
}

// Container Registry using AVM
module containerRegistry 'br/public:avm/res/container-registry/registry:0.7.0' = {
  name: 'containerRegistry-deployment'
  scope: rg
  params: {
    name: 'cr${environmentName}${uniqueSuffix}'
    location: location
    acrSku: 'Basic'
    adminUserEnabled: false // Disabled for security - use managed identity instead
    publicNetworkAccess: 'Enabled'
    tags: tags
  }
}

// Container Apps Environment using AVM
module containerAppsEnvironment 'br/public:avm/res/app/managed-environment:0.8.2' = {
  name: 'containerAppsEnv-deployment'
  scope: rg
  params: {
    name: 'cae-${environmentName}-${uniqueSuffix}'
    location: location
    logAnalyticsWorkspaceResourceId: logAnalytics.outputs.resourceId
    infrastructureResourceGroupName: 'rg-${environmentName}-infra'
    internal: false
    tags: tags
  }
}

// Key Vault using AVM
module keyVault 'br/public:avm/res/key-vault/vault:0.11.0' = {
  name: 'keyVault-deployment'
  scope: rg
  params: {
    name: 'kv-${environmentName}-${uniqueSuffix}'
    location: location
    sku: 'standard'
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    enablePurgeProtection: false // Set to true for production
    tags: tags
    roleAssignments: !empty(principalId) ? [
      {
        principalId: principalId
        roleDefinitionIdOrName: 'Key Vault Secrets User'
        principalType: 'ServicePrincipal'
      }
    ] : []
  }
}

// Service Bus Namespace using AVM
module serviceBusNamespace 'br/public:avm/res/service-bus/namespace:0.11.1' = {
  name: 'serviceBus-deployment'
  scope: rg
  params: {
    name: 'sb-${environmentName}-${uniqueSuffix}'
    location: location
    skuObject: {
      name: 'Standard'
    }
    minimumTlsVersion: '1.2'
    tags: tags
    queues: [
      {
        name: 'airline-events'
        lockDuration: 'PT5M'
        maxSizeInMegabytes: 1024
        requiresDuplicateDetection: false
        requiresSession: false
        defaultMessageTimeToLive: 'P14D'
        deadLetteringOnMessageExpiration: true
        enableBatchedOperations: true
      }
    ]
    topics: [
      {
        name: 'booking-events'
        maxSizeInMegabytes: 1024
        defaultMessageTimeToLive: 'P14D'
        enableBatchedOperations: true
      }
    ]
  }
}

// Airline Service Container App using AVM
module airlineService 'br/public:avm/res/app/container-app:0.11.0' = {
  name: 'airlineService-deployment'
  scope: rg
  params: {
    name: 'ca-airline-${environmentName}'
    location: location
    environmentResourceId: containerAppsEnvironment.outputs.resourceId
    tags: tags
    managedIdentities: {
      systemAssigned: true
    }
    containers: [
      {
        name: 'airline-service'
        image: '${containerRegistry.outputs.loginServer}/airline-service:latest'
        resources: {
          cpu: '0.25'
          memory: '0.5Gi'
        }
      }
    ]
    scaleMinReplicas: 1
    scaleMaxReplicas: 10
    scaleRules: [
      {
        name: 'http-scaling'
        http: {
          metadata: {
            concurrentRequests: '10'
          }
        }
      }
    ]
    ingressTargetPort: 8000
    ingressExternal: true
    ingressTransport: 'http'
    ingressAllowInsecure: false
    registries: [
      {
        server: containerRegistry.outputs.loginServer
        identity: 'system'
      }
    ]
  }
}

// Grant the Container App's managed identity permission to pull from ACR
module acrRoleAssignment 'br/public:avm/ptn/authorization/resource-role-assignment:0.1.1' = {
  name: 'acr-role-assignment'
  scope: rg
  params: {
    principalId: airlineService.outputs.systemAssignedMIPrincipalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d') // AcrPull role
    resourceId: containerRegistry.outputs.resourceId
  }
}

// Outputs
output resourceGroupName string = rg.name
output containerRegistryName string = containerRegistry.outputs.name
output containerRegistryLoginServer string = containerRegistry.outputs.loginServer
output keyVaultName string = keyVault.outputs.name
output keyVaultUri string = keyVault.outputs.uri
output serviceBusNamespace string = serviceBusNamespace.outputs.name
output applicationInsightsName string = appInsights.outputs.name
output applicationInsightsConnectionString string = appInsights.outputs.connectionString
output airlineServiceUrl string = airlineService.outputs.fqdn
output logAnalyticsWorkspaceId string = logAnalytics.outputs.resourceId
