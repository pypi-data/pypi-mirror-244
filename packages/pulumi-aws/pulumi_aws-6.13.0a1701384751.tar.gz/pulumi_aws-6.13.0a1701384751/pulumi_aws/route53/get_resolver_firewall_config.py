# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetResolverFirewallConfigResult',
    'AwaitableGetResolverFirewallConfigResult',
    'get_resolver_firewall_config',
    'get_resolver_firewall_config_output',
]

@pulumi.output_type
class GetResolverFirewallConfigResult:
    """
    A collection of values returned by getResolverFirewallConfig.
    """
    def __init__(__self__, firewall_fail_open=None, id=None, owner_id=None, resource_id=None):
        if firewall_fail_open and not isinstance(firewall_fail_open, str):
            raise TypeError("Expected argument 'firewall_fail_open' to be a str")
        pulumi.set(__self__, "firewall_fail_open", firewall_fail_open)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if owner_id and not isinstance(owner_id, str):
            raise TypeError("Expected argument 'owner_id' to be a str")
        pulumi.set(__self__, "owner_id", owner_id)
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="firewallFailOpen")
    def firewall_fail_open(self) -> str:
        return pulumi.get(self, "firewall_fail_open")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> str:
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> str:
        return pulumi.get(self, "resource_id")


class AwaitableGetResolverFirewallConfigResult(GetResolverFirewallConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResolverFirewallConfigResult(
            firewall_fail_open=self.firewall_fail_open,
            id=self.id,
            owner_id=self.owner_id,
            resource_id=self.resource_id)


def get_resolver_firewall_config(resource_id: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResolverFirewallConfigResult:
    """
    `route53.ResolverFirewallConfig` provides details about a specific a Route 53 Resolver DNS Firewall config.

    This data source allows to find a details about a specific a Route 53 Resolver DNS Firewall config.

    ## Example Usage

    The following example shows how to get a firewall config using the VPC ID.

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.route53.get_resolver_firewall_config(resource_id="vpc-exampleid")
    ```


    :param str resource_id: The ID of the VPC from Amazon VPC that the configuration is for.
           
           The following attribute is additionally exported:
    """
    __args__ = dict()
    __args__['resourceId'] = resource_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:route53/getResolverFirewallConfig:getResolverFirewallConfig', __args__, opts=opts, typ=GetResolverFirewallConfigResult).value

    return AwaitableGetResolverFirewallConfigResult(
        firewall_fail_open=pulumi.get(__ret__, 'firewall_fail_open'),
        id=pulumi.get(__ret__, 'id'),
        owner_id=pulumi.get(__ret__, 'owner_id'),
        resource_id=pulumi.get(__ret__, 'resource_id'))


@_utilities.lift_output_func(get_resolver_firewall_config)
def get_resolver_firewall_config_output(resource_id: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResolverFirewallConfigResult]:
    """
    `route53.ResolverFirewallConfig` provides details about a specific a Route 53 Resolver DNS Firewall config.

    This data source allows to find a details about a specific a Route 53 Resolver DNS Firewall config.

    ## Example Usage

    The following example shows how to get a firewall config using the VPC ID.

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.route53.get_resolver_firewall_config(resource_id="vpc-exampleid")
    ```


    :param str resource_id: The ID of the VPC from Amazon VPC that the configuration is for.
           
           The following attribute is additionally exported:
    """
    ...
