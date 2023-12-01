# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AvailabilityZoneGroupArgs', 'AvailabilityZoneGroup']

@pulumi.input_type
class AvailabilityZoneGroupArgs:
    def __init__(__self__, *,
                 group_name: pulumi.Input[str],
                 opt_in_status: pulumi.Input[str]):
        """
        The set of arguments for constructing a AvailabilityZoneGroup resource.
        :param pulumi.Input[str] group_name: Name of the Availability Zone Group.
        :param pulumi.Input[str] opt_in_status: Indicates whether to enable or disable Availability Zone Group. Valid values: `opted-in` or `not-opted-in`.
        """
        pulumi.set(__self__, "group_name", group_name)
        pulumi.set(__self__, "opt_in_status", opt_in_status)

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> pulumi.Input[str]:
        """
        Name of the Availability Zone Group.
        """
        return pulumi.get(self, "group_name")

    @group_name.setter
    def group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "group_name", value)

    @property
    @pulumi.getter(name="optInStatus")
    def opt_in_status(self) -> pulumi.Input[str]:
        """
        Indicates whether to enable or disable Availability Zone Group. Valid values: `opted-in` or `not-opted-in`.
        """
        return pulumi.get(self, "opt_in_status")

    @opt_in_status.setter
    def opt_in_status(self, value: pulumi.Input[str]):
        pulumi.set(self, "opt_in_status", value)


@pulumi.input_type
class _AvailabilityZoneGroupState:
    def __init__(__self__, *,
                 group_name: Optional[pulumi.Input[str]] = None,
                 opt_in_status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AvailabilityZoneGroup resources.
        :param pulumi.Input[str] group_name: Name of the Availability Zone Group.
        :param pulumi.Input[str] opt_in_status: Indicates whether to enable or disable Availability Zone Group. Valid values: `opted-in` or `not-opted-in`.
        """
        if group_name is not None:
            pulumi.set(__self__, "group_name", group_name)
        if opt_in_status is not None:
            pulumi.set(__self__, "opt_in_status", opt_in_status)

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Availability Zone Group.
        """
        return pulumi.get(self, "group_name")

    @group_name.setter
    def group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_name", value)

    @property
    @pulumi.getter(name="optInStatus")
    def opt_in_status(self) -> Optional[pulumi.Input[str]]:
        """
        Indicates whether to enable or disable Availability Zone Group. Valid values: `opted-in` or `not-opted-in`.
        """
        return pulumi.get(self, "opt_in_status")

    @opt_in_status.setter
    def opt_in_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "opt_in_status", value)


class AvailabilityZoneGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_name: Optional[pulumi.Input[str]] = None,
                 opt_in_status: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an EC2 Availability Zone Group, such as updating its opt-in status.

        > **NOTE:** This is an advanced resource. The provider will automatically assume management of the EC2 Availability Zone Group without import and perform no actions on removal from configuration.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ec2.AvailabilityZoneGroup("example",
            group_name="us-west-2-lax-1",
            opt_in_status="opted-in")
        ```

        ## Import

        Using `pulumi import`, import EC2 Availability Zone Groups using the group name. For example:

        ```sh
         $ pulumi import aws:ec2/availabilityZoneGroup:AvailabilityZoneGroup example us-west-2-lax-1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group_name: Name of the Availability Zone Group.
        :param pulumi.Input[str] opt_in_status: Indicates whether to enable or disable Availability Zone Group. Valid values: `opted-in` or `not-opted-in`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AvailabilityZoneGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an EC2 Availability Zone Group, such as updating its opt-in status.

        > **NOTE:** This is an advanced resource. The provider will automatically assume management of the EC2 Availability Zone Group without import and perform no actions on removal from configuration.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ec2.AvailabilityZoneGroup("example",
            group_name="us-west-2-lax-1",
            opt_in_status="opted-in")
        ```

        ## Import

        Using `pulumi import`, import EC2 Availability Zone Groups using the group name. For example:

        ```sh
         $ pulumi import aws:ec2/availabilityZoneGroup:AvailabilityZoneGroup example us-west-2-lax-1
        ```

        :param str resource_name: The name of the resource.
        :param AvailabilityZoneGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AvailabilityZoneGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_name: Optional[pulumi.Input[str]] = None,
                 opt_in_status: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AvailabilityZoneGroupArgs.__new__(AvailabilityZoneGroupArgs)

            if group_name is None and not opts.urn:
                raise TypeError("Missing required property 'group_name'")
            __props__.__dict__["group_name"] = group_name
            if opt_in_status is None and not opts.urn:
                raise TypeError("Missing required property 'opt_in_status'")
            __props__.__dict__["opt_in_status"] = opt_in_status
        super(AvailabilityZoneGroup, __self__).__init__(
            'aws:ec2/availabilityZoneGroup:AvailabilityZoneGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            group_name: Optional[pulumi.Input[str]] = None,
            opt_in_status: Optional[pulumi.Input[str]] = None) -> 'AvailabilityZoneGroup':
        """
        Get an existing AvailabilityZoneGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group_name: Name of the Availability Zone Group.
        :param pulumi.Input[str] opt_in_status: Indicates whether to enable or disable Availability Zone Group. Valid values: `opted-in` or `not-opted-in`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AvailabilityZoneGroupState.__new__(_AvailabilityZoneGroupState)

        __props__.__dict__["group_name"] = group_name
        __props__.__dict__["opt_in_status"] = opt_in_status
        return AvailabilityZoneGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> pulumi.Output[str]:
        """
        Name of the Availability Zone Group.
        """
        return pulumi.get(self, "group_name")

    @property
    @pulumi.getter(name="optInStatus")
    def opt_in_status(self) -> pulumi.Output[str]:
        """
        Indicates whether to enable or disable Availability Zone Group. Valid values: `opted-in` or `not-opted-in`.
        """
        return pulumi.get(self, "opt_in_status")

