import pulumi
from pulumi_azure_native import resources

rg = resources.ResourceGroup('agent-rg')
pulumi.export('resource_group', rg.name)