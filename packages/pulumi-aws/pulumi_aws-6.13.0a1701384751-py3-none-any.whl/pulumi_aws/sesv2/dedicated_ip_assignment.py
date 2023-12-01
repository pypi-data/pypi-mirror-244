# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DedicatedIpAssignmentArgs', 'DedicatedIpAssignment']

@pulumi.input_type
class DedicatedIpAssignmentArgs:
    def __init__(__self__, *,
                 destination_pool_name: pulumi.Input[str],
                 ip: pulumi.Input[str]):
        """
        The set of arguments for constructing a DedicatedIpAssignment resource.
        :param pulumi.Input[str] destination_pool_name: Dedicated IP address.
        :param pulumi.Input[str] ip: Dedicated IP address.
        """
        pulumi.set(__self__, "destination_pool_name", destination_pool_name)
        pulumi.set(__self__, "ip", ip)

    @property
    @pulumi.getter(name="destinationPoolName")
    def destination_pool_name(self) -> pulumi.Input[str]:
        """
        Dedicated IP address.
        """
        return pulumi.get(self, "destination_pool_name")

    @destination_pool_name.setter
    def destination_pool_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination_pool_name", value)

    @property
    @pulumi.getter
    def ip(self) -> pulumi.Input[str]:
        """
        Dedicated IP address.
        """
        return pulumi.get(self, "ip")

    @ip.setter
    def ip(self, value: pulumi.Input[str]):
        pulumi.set(self, "ip", value)


@pulumi.input_type
class _DedicatedIpAssignmentState:
    def __init__(__self__, *,
                 destination_pool_name: Optional[pulumi.Input[str]] = None,
                 ip: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DedicatedIpAssignment resources.
        :param pulumi.Input[str] destination_pool_name: Dedicated IP address.
        :param pulumi.Input[str] ip: Dedicated IP address.
        """
        if destination_pool_name is not None:
            pulumi.set(__self__, "destination_pool_name", destination_pool_name)
        if ip is not None:
            pulumi.set(__self__, "ip", ip)

    @property
    @pulumi.getter(name="destinationPoolName")
    def destination_pool_name(self) -> Optional[pulumi.Input[str]]:
        """
        Dedicated IP address.
        """
        return pulumi.get(self, "destination_pool_name")

    @destination_pool_name.setter
    def destination_pool_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "destination_pool_name", value)

    @property
    @pulumi.getter
    def ip(self) -> Optional[pulumi.Input[str]]:
        """
        Dedicated IP address.
        """
        return pulumi.get(self, "ip")

    @ip.setter
    def ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip", value)


class DedicatedIpAssignment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_pool_name: Optional[pulumi.Input[str]] = None,
                 ip: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS SESv2 (Simple Email V2) Dedicated IP Assignment.

        This resource is used with "Standard" dedicated IP addresses. This includes addresses [requested and relinquished manually](https://docs.aws.amazon.com/ses/latest/dg/dedicated-ip-case.html) via an AWS support case, or [Bring Your Own IP](https://docs.aws.amazon.com/ses/latest/dg/dedicated-ip-byo.html) addresses. Once no longer assigned, this resource returns the IP to the [`ses-default-dedicated-pool`](https://docs.aws.amazon.com/ses/latest/dg/managing-ip-pools.html), managed by AWS.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sesv2.DedicatedIpAssignment("example",
            destination_pool_name="my-pool",
            ip="0.0.0.0")
        ```

        ## Import

        Using `pulumi import`, import SESv2 (Simple Email V2) Dedicated IP Assignment using the `id`, which is a comma-separated string made up of `ip` and `destination_pool_name`. For example:

        ```sh
         $ pulumi import aws:sesv2/dedicatedIpAssignment:DedicatedIpAssignment example "0.0.0.0,my-pool"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] destination_pool_name: Dedicated IP address.
        :param pulumi.Input[str] ip: Dedicated IP address.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DedicatedIpAssignmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS SESv2 (Simple Email V2) Dedicated IP Assignment.

        This resource is used with "Standard" dedicated IP addresses. This includes addresses [requested and relinquished manually](https://docs.aws.amazon.com/ses/latest/dg/dedicated-ip-case.html) via an AWS support case, or [Bring Your Own IP](https://docs.aws.amazon.com/ses/latest/dg/dedicated-ip-byo.html) addresses. Once no longer assigned, this resource returns the IP to the [`ses-default-dedicated-pool`](https://docs.aws.amazon.com/ses/latest/dg/managing-ip-pools.html), managed by AWS.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sesv2.DedicatedIpAssignment("example",
            destination_pool_name="my-pool",
            ip="0.0.0.0")
        ```

        ## Import

        Using `pulumi import`, import SESv2 (Simple Email V2) Dedicated IP Assignment using the `id`, which is a comma-separated string made up of `ip` and `destination_pool_name`. For example:

        ```sh
         $ pulumi import aws:sesv2/dedicatedIpAssignment:DedicatedIpAssignment example "0.0.0.0,my-pool"
        ```

        :param str resource_name: The name of the resource.
        :param DedicatedIpAssignmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DedicatedIpAssignmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_pool_name: Optional[pulumi.Input[str]] = None,
                 ip: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DedicatedIpAssignmentArgs.__new__(DedicatedIpAssignmentArgs)

            if destination_pool_name is None and not opts.urn:
                raise TypeError("Missing required property 'destination_pool_name'")
            __props__.__dict__["destination_pool_name"] = destination_pool_name
            if ip is None and not opts.urn:
                raise TypeError("Missing required property 'ip'")
            __props__.__dict__["ip"] = ip
        super(DedicatedIpAssignment, __self__).__init__(
            'aws:sesv2/dedicatedIpAssignment:DedicatedIpAssignment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            destination_pool_name: Optional[pulumi.Input[str]] = None,
            ip: Optional[pulumi.Input[str]] = None) -> 'DedicatedIpAssignment':
        """
        Get an existing DedicatedIpAssignment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] destination_pool_name: Dedicated IP address.
        :param pulumi.Input[str] ip: Dedicated IP address.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DedicatedIpAssignmentState.__new__(_DedicatedIpAssignmentState)

        __props__.__dict__["destination_pool_name"] = destination_pool_name
        __props__.__dict__["ip"] = ip
        return DedicatedIpAssignment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="destinationPoolName")
    def destination_pool_name(self) -> pulumi.Output[str]:
        """
        Dedicated IP address.
        """
        return pulumi.get(self, "destination_pool_name")

    @property
    @pulumi.getter
    def ip(self) -> pulumi.Output[str]:
        """
        Dedicated IP address.
        """
        return pulumi.get(self, "ip")

