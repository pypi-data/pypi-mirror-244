# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EncryptionByDefaultArgs', 'EncryptionByDefault']

@pulumi.input_type
class EncryptionByDefaultArgs:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a EncryptionByDefault resource.
        :param pulumi.Input[bool] enabled: Whether or not default EBS encryption is enabled. Valid values are `true` or `false`. Defaults to `true`.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not default EBS encryption is enabled. Valid values are `true` or `false`. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)


@pulumi.input_type
class _EncryptionByDefaultState:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering EncryptionByDefault resources.
        :param pulumi.Input[bool] enabled: Whether or not default EBS encryption is enabled. Valid values are `true` or `false`. Defaults to `true`.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not default EBS encryption is enabled. Valid values are `true` or `false`. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)


class EncryptionByDefault(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Provides a resource to manage whether default EBS encryption is enabled for your AWS account in the current AWS region. To manage the default KMS key for the region, see the `ebs.DefaultKmsKey` resource.

        > **NOTE:** Removing this resource disables default EBS encryption.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ebs.EncryptionByDefault("example", enabled=True)
        ```

        ## Import

        Using `pulumi import`, import the default EBS encryption state. For example:

        ```sh
         $ pulumi import aws:ebs/encryptionByDefault:EncryptionByDefault example default
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: Whether or not default EBS encryption is enabled. Valid values are `true` or `false`. Defaults to `true`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[EncryptionByDefaultArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage whether default EBS encryption is enabled for your AWS account in the current AWS region. To manage the default KMS key for the region, see the `ebs.DefaultKmsKey` resource.

        > **NOTE:** Removing this resource disables default EBS encryption.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ebs.EncryptionByDefault("example", enabled=True)
        ```

        ## Import

        Using `pulumi import`, import the default EBS encryption state. For example:

        ```sh
         $ pulumi import aws:ebs/encryptionByDefault:EncryptionByDefault example default
        ```

        :param str resource_name: The name of the resource.
        :param EncryptionByDefaultArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EncryptionByDefaultArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EncryptionByDefaultArgs.__new__(EncryptionByDefaultArgs)

            __props__.__dict__["enabled"] = enabled
        super(EncryptionByDefault, __self__).__init__(
            'aws:ebs/encryptionByDefault:EncryptionByDefault',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            enabled: Optional[pulumi.Input[bool]] = None) -> 'EncryptionByDefault':
        """
        Get an existing EncryptionByDefault resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: Whether or not default EBS encryption is enabled. Valid values are `true` or `false`. Defaults to `true`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EncryptionByDefaultState.__new__(_EncryptionByDefaultState)

        __props__.__dict__["enabled"] = enabled
        return EncryptionByDefault(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether or not default EBS encryption is enabled. Valid values are `true` or `false`. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

