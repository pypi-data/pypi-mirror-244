# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetFirewallResult',
    'AwaitableGetFirewallResult',
    'get_firewall',
    'get_firewall_output',
]

@pulumi.output_type
class GetFirewallResult:
    """
    A collection of values returned by getFirewall.
    """
    def __init__(__self__, arn=None, delete_protection=None, description=None, encryption_configurations=None, firewall_policy_arn=None, firewall_policy_change_protection=None, firewall_statuses=None, id=None, name=None, subnet_change_protection=None, subnet_mappings=None, tags=None, update_token=None, vpc_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if delete_protection and not isinstance(delete_protection, bool):
            raise TypeError("Expected argument 'delete_protection' to be a bool")
        pulumi.set(__self__, "delete_protection", delete_protection)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if encryption_configurations and not isinstance(encryption_configurations, list):
            raise TypeError("Expected argument 'encryption_configurations' to be a list")
        pulumi.set(__self__, "encryption_configurations", encryption_configurations)
        if firewall_policy_arn and not isinstance(firewall_policy_arn, str):
            raise TypeError("Expected argument 'firewall_policy_arn' to be a str")
        pulumi.set(__self__, "firewall_policy_arn", firewall_policy_arn)
        if firewall_policy_change_protection and not isinstance(firewall_policy_change_protection, bool):
            raise TypeError("Expected argument 'firewall_policy_change_protection' to be a bool")
        pulumi.set(__self__, "firewall_policy_change_protection", firewall_policy_change_protection)
        if firewall_statuses and not isinstance(firewall_statuses, list):
            raise TypeError("Expected argument 'firewall_statuses' to be a list")
        pulumi.set(__self__, "firewall_statuses", firewall_statuses)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if subnet_change_protection and not isinstance(subnet_change_protection, bool):
            raise TypeError("Expected argument 'subnet_change_protection' to be a bool")
        pulumi.set(__self__, "subnet_change_protection", subnet_change_protection)
        if subnet_mappings and not isinstance(subnet_mappings, list):
            raise TypeError("Expected argument 'subnet_mappings' to be a list")
        pulumi.set(__self__, "subnet_mappings", subnet_mappings)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if update_token and not isinstance(update_token, str):
            raise TypeError("Expected argument 'update_token' to be a str")
        pulumi.set(__self__, "update_token", update_token)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the firewall.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="deleteProtection")
    def delete_protection(self) -> bool:
        """
        Boolean flag indicating whether it is possible to delete the firewall.
        """
        return pulumi.get(self, "delete_protection")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the firewall.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="encryptionConfigurations")
    def encryption_configurations(self) -> Sequence['outputs.GetFirewallEncryptionConfigurationResult']:
        """
        AWS Key Management Service (AWS KMS) encryption settings for the firewall.
        """
        return pulumi.get(self, "encryption_configurations")

    @property
    @pulumi.getter(name="firewallPolicyArn")
    def firewall_policy_arn(self) -> str:
        """
        ARN of the VPC Firewall policy.
        """
        return pulumi.get(self, "firewall_policy_arn")

    @property
    @pulumi.getter(name="firewallPolicyChangeProtection")
    def firewall_policy_change_protection(self) -> bool:
        """
        A boolean flag indicating whether it is possible to change the associated firewall policy.
        """
        return pulumi.get(self, "firewall_policy_change_protection")

    @property
    @pulumi.getter(name="firewallStatuses")
    def firewall_statuses(self) -> Sequence['outputs.GetFirewallFirewallStatusResult']:
        """
        Nested list of information about the current status of the firewall.
        """
        return pulumi.get(self, "firewall_statuses")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Descriptive name of the firewall.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="subnetChangeProtection")
    def subnet_change_protection(self) -> bool:
        """
        A boolean flag indicating whether it is possible to change the associated subnet(s).
        """
        return pulumi.get(self, "subnet_change_protection")

    @property
    @pulumi.getter(name="subnetMappings")
    def subnet_mappings(self) -> Sequence['outputs.GetFirewallSubnetMappingResult']:
        """
        Set of configuration blocks describing the public subnets. Each subnet must belong to a different Availability Zone in the VPC. AWS Network Firewall creates a firewall endpoint in each subnet.
        """
        return pulumi.get(self, "subnet_mappings")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Map of resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="updateToken")
    def update_token(self) -> str:
        """
        String token used when updating a firewall.
        """
        return pulumi.get(self, "update_token")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        Unique identifier of the VPC where AWS Network Firewall should create the firewall.
        """
        return pulumi.get(self, "vpc_id")


class AwaitableGetFirewallResult(GetFirewallResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFirewallResult(
            arn=self.arn,
            delete_protection=self.delete_protection,
            description=self.description,
            encryption_configurations=self.encryption_configurations,
            firewall_policy_arn=self.firewall_policy_arn,
            firewall_policy_change_protection=self.firewall_policy_change_protection,
            firewall_statuses=self.firewall_statuses,
            id=self.id,
            name=self.name,
            subnet_change_protection=self.subnet_change_protection,
            subnet_mappings=self.subnet_mappings,
            tags=self.tags,
            update_token=self.update_token,
            vpc_id=self.vpc_id)


def get_firewall(arn: Optional[str] = None,
                 name: Optional[str] = None,
                 tags: Optional[Mapping[str, str]] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFirewallResult:
    """
    Retrieve information about a firewall.

    ## Example Usage
    ### Find firewall policy by ARN

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.networkfirewall.get_firewall(arn=aws_networkfirewall_firewall["arn"])
    ```
    ### Find firewall policy by Name

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.networkfirewall.get_firewall(name="Test")
    ```
    ### Find firewall policy by ARN and Name

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.networkfirewall.get_firewall(arn=aws_networkfirewall_firewall["arn"],
        name="Test")
    ```


    :param str arn: ARN of the firewall.
    :param str name: Descriptive name of the firewall.
    :param Mapping[str, str] tags: Map of resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
    """
    __args__ = dict()
    __args__['arn'] = arn
    __args__['name'] = name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:networkfirewall/getFirewall:getFirewall', __args__, opts=opts, typ=GetFirewallResult).value

    return AwaitableGetFirewallResult(
        arn=pulumi.get(__ret__, 'arn'),
        delete_protection=pulumi.get(__ret__, 'delete_protection'),
        description=pulumi.get(__ret__, 'description'),
        encryption_configurations=pulumi.get(__ret__, 'encryption_configurations'),
        firewall_policy_arn=pulumi.get(__ret__, 'firewall_policy_arn'),
        firewall_policy_change_protection=pulumi.get(__ret__, 'firewall_policy_change_protection'),
        firewall_statuses=pulumi.get(__ret__, 'firewall_statuses'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        subnet_change_protection=pulumi.get(__ret__, 'subnet_change_protection'),
        subnet_mappings=pulumi.get(__ret__, 'subnet_mappings'),
        tags=pulumi.get(__ret__, 'tags'),
        update_token=pulumi.get(__ret__, 'update_token'),
        vpc_id=pulumi.get(__ret__, 'vpc_id'))


@_utilities.lift_output_func(get_firewall)
def get_firewall_output(arn: Optional[pulumi.Input[Optional[str]]] = None,
                        name: Optional[pulumi.Input[Optional[str]]] = None,
                        tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFirewallResult]:
    """
    Retrieve information about a firewall.

    ## Example Usage
    ### Find firewall policy by ARN

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.networkfirewall.get_firewall(arn=aws_networkfirewall_firewall["arn"])
    ```
    ### Find firewall policy by Name

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.networkfirewall.get_firewall(name="Test")
    ```
    ### Find firewall policy by ARN and Name

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.networkfirewall.get_firewall(arn=aws_networkfirewall_firewall["arn"],
        name="Test")
    ```


    :param str arn: ARN of the firewall.
    :param str name: Descriptive name of the firewall.
    :param Mapping[str, str] tags: Map of resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
    """
    ...
