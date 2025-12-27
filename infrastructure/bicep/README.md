# Azure Infrastructure - Bicep with Azure Verified Modules (AVM)

This directory contains Azure infrastructure as code using Bicep templates with Azure Verified Modules (AVM).

## Overview

This infrastructure uses **Azure Verified Modules (AVM)** - pre-built, tested, and validated Bicep modules that follow Azure best practices. AVM modules ensure:

- ✅ Production-ready configurations
- ✅ Security best practices
- ✅ Consistent resource naming and tagging
- ✅ Comprehensive parameter validation
- ✅ Well-documented usage patterns

## Structure

```
infrastructure/bicep/
├── main.bicep                      # Main orchestration template (uses AVM)
├── environments/
│   ├── dev.bicepparam             # Dev environment parameters
│   ├── staging.bicepparam         # Staging environment parameters
│   └── prod.bicepparam            # Production environment parameters
└── README.md                      # This file
```

## Resources Deployed

All resources use AVM modules from the Bicep Public Registry:

| Resource | AVM Module | Version |
|----------|------------|---------|
| Log Analytics | `avm/res/operational-insights/workspace` | 0.9.1 |
| Application Insights | `avm/res/insights/component` | 0.4.2 |
| Container Registry | `avm/res/container-registry/registry` | 0.7.0 |
| Container Apps Environment | `avm/res/app/managed-environment` | 0.8.2 |
| Container App (Airline Service) | `avm/res/app/container-app` | 0.11.0 |
| Key Vault | `avm/res/key-vault/vault` | 0.11.0 |
| Service Bus | `avm/res/service-bus/namespace` | 0.11.1 |

### Resource Details

- **Resource Group**: Container for all environment resources
- **Log Analytics Workspace**: Centralized logging (30-day retention)
- **Application Insights**: Application monitoring and telemetry
- **Container Registry**: Docker image storage with admin user enabled
- **Container Apps Environment**: Hosting environment for microservices
- **Container Apps**: Individual microservice instances (currently: airline-service)
- **Key Vault**: Secrets management with RBAC authorization
- **Service Bus**: Message queue with topics and queues for inter-service communication

## Prerequisites

- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) (latest version)
- [Bicep CLI](https://docs.microsoft.com/en-us/azure/azure-resource-manager/bicep/install) (automatically installed with Azure CLI)
- Azure subscription with appropriate permissions
- Service principal for automated deployments (optional for local dev)

## Deployment

### Validate Bicep Templates

**MANDATORY**: Always validate before deploying:

```bash
# Update Bicep CLI
az bicep upgrade

# Build and validate main template
az bicep build --file main.bicep
```

### Deploy Using Azure CLI

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "your-subscription-id"

# Deploy to dev environment
az deployment sub create \
  --location eastus \
  --template-file main.bicep \
  --parameters environments/dev.bicepparam \
  --name "deploy-dev-$(date +%Y%m%d-%H%M%S)"

# Deploy to staging environment
az deployment sub create \
  --location eastus \
  --template-file main.bicep \
  --parameters environments/staging.bicepparam \
  --name "deploy-staging-$(date +%Y%m%d-%H%M%S)"

# Deploy to production environment
az deployment sub create \
  --location eastus \
  --template-file main.bicep \
  --parameters environments/prod.bicepparam \
  --name "deploy-prod-$(date +%Y%m%d-%H%M%S)"
```

### Deploy Using Azure Developer CLI

```bash
# From the repository root
azd up
```

### What-If Deployment (Preview Changes)

```bash
az deployment sub what-if \
  --location eastus \
  --template-file main.bicep \
  --parameters environments/dev.bicepparam
```

## Environment Configuration

Update the `.bicepparam` files in the `environments/` directory:

### Required Parameters

- `environmentName`: Name of the environment (dev, staging, prod)
- `location`: Azure region (e.g., eastus, westus2)

### Optional Parameters

- `principalId`: Service principal ID for Key Vault access (leave empty for manual setup)

### Tags

All resources are automatically tagged with:
- `Environment`: Environment name
- `ManagedBy`: Bicep
- `Project`: ghcp-training-microservices

## Azure Verified Modules (AVM)

### Module Discovery

- **Bicep Registry**: https://github.com/Azure/bicep-registry-modules
- **AVM Index**: https://azure.github.io/Azure-Verified-Modules/
- **Module Format**: `br/public:avm/res/{service}/{resource}:{version}`

### Using AVM Modules

AVM modules are referenced directly from the Bicep Public Registry:

```bicep
module keyVault 'br/public:avm/res/key-vault/vault:0.11.0' = {
  name: 'keyVault-deployment'
  scope: rg
  params: {
    name: 'kv-${environmentName}-${uniqueSuffix}'
    location: location
    // ... other parameters
  }
}
```

### Benefits

1. **Tested & Validated**: All modules are thoroughly tested
2. **Best Practices**: Follow Azure Well-Architected Framework
3. **Up-to-Date**: Regular updates with latest Azure features
4. **Documentation**: Comprehensive examples and parameter descriptions
5. **Version Control**: Semantic versioning for stability

## Adding New Services

To add a new Container App service:

1. Add a new module block in `main.bicep`:

```bicep
module newService 'br/public:avm/res/app/container-app:0.11.0' = {
  name: 'newService-deployment'
  scope: rg
  params: {
    name: 'ca-newservice-${environmentName}'
    location: location
    environmentResourceId: containerAppsEnvironment.outputs.resourceId
    // ... configure containers, scaling, ingress
  }
}
```

2. Add output for the new service:

```bicep
output newServiceUrl string = newService.outputs.fqdn
```

3. Update parameter files if needed
4. Validate: `az bicep build --file main.bicep`
5. Deploy changes

## Troubleshooting

### Common Issues

1. **Module Version Not Found**
   - Check latest version in [Bicep Registry](https://github.com/Azure/bicep-registry-modules)
   - Update module reference with correct version

2. **Validation Failures**
   - Run `az bicep build --file main.bicep` to see detailed errors
   - Check parameter types and required values

3. **Container App Image Pull Failures**
   - Ensure Container Registry credentials are correct
   - Verify image exists in the registry
   - Check Container App has proper registry configuration

4. **Principal ID for Key Vault**
   - Get service principal ID: `az ad sp show --id <app-id> --query id -o tsv`
   - Update in parameter file or pass during deployment

### Validation Command

```bash
# Always run before committing changes
az bicep build --file main.bicep
```

## CI/CD Integration

This infrastructure is deployed via GitHub Actions:
- `.github/workflows/infrastructure.yml`

Automated actions:
- ✅ Validate on pull requests
- ✅ What-if analysis in PR comments
- ✅ Deploy on merge to main (with approvals for production)

## Maintenance

### Updating AVM Modules

1. Check for new module versions in [Bicep Registry](https://github.com/Azure/bicep-registry-modules)
2. Update module reference: `br/public:avm/res/{service}/{resource}:{new-version}`
3. Review module CHANGELOG for breaking changes
4. Test in dev environment first
5. Validate: `az bicep build --file main.bicep`
6. Deploy to higher environments after verification

### Adding Resources

1. Search for AVM module: https://github.com/Azure/bicep-registry-modules
2. Review module README and examples
3. Add module reference to `main.bicep`
4. Configure required and optional parameters
5. Add outputs as needed
6. Validate and test

## Security Considerations

- ✅ Key Vault uses RBAC authorization
- ✅ Soft delete enabled (90-day retention)
- ✅ Service Bus uses TLS 1.2 minimum
- ✅ Container Registry admin user (for simplicity - consider managed identity for production)
- ⚠️ Purge protection disabled for dev (enable for production)

## Cost Optimization

Development environment uses minimal SKUs:
- Container Registry: Basic
- Service Bus: Standard
- Log Analytics: Pay-as-you-go (30-day retention)
- Container Apps: Consumption-based pricing

Adjust SKUs in production parameter files as needed.

## References

- [Azure Verified Modules](https://azure.github.io/Azure-Verified-Modules/)
- [Bicep Registry Modules](https://github.com/Azure/bicep-registry-modules)
- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Azure Well-Architected Framework](https://learn.microsoft.com/azure/architecture/framework/)
