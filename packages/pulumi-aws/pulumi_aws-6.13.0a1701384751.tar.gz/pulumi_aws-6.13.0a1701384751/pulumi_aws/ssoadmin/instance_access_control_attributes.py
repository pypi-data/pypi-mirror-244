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
from ._inputs import *

__all__ = ['InstanceAccessControlAttributesArgs', 'InstanceAccessControlAttributes']

@pulumi.input_type
class InstanceAccessControlAttributesArgs:
    def __init__(__self__, *,
                 attributes: pulumi.Input[Sequence[pulumi.Input['InstanceAccessControlAttributesAttributeArgs']]],
                 instance_arn: pulumi.Input[str]):
        """
        The set of arguments for constructing a InstanceAccessControlAttributes resource.
        :param pulumi.Input[Sequence[pulumi.Input['InstanceAccessControlAttributesAttributeArgs']]] attributes: See AccessControlAttribute for more details.
        :param pulumi.Input[str] instance_arn: The Amazon Resource Name (ARN) of the SSO Instance.
        """
        pulumi.set(__self__, "attributes", attributes)
        pulumi.set(__self__, "instance_arn", instance_arn)

    @property
    @pulumi.getter
    def attributes(self) -> pulumi.Input[Sequence[pulumi.Input['InstanceAccessControlAttributesAttributeArgs']]]:
        """
        See AccessControlAttribute for more details.
        """
        return pulumi.get(self, "attributes")

    @attributes.setter
    def attributes(self, value: pulumi.Input[Sequence[pulumi.Input['InstanceAccessControlAttributesAttributeArgs']]]):
        pulumi.set(self, "attributes", value)

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the SSO Instance.
        """
        return pulumi.get(self, "instance_arn")

    @instance_arn.setter
    def instance_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_arn", value)


@pulumi.input_type
class _InstanceAccessControlAttributesState:
    def __init__(__self__, *,
                 attributes: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceAccessControlAttributesAttributeArgs']]]] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 status_reason: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering InstanceAccessControlAttributes resources.
        :param pulumi.Input[Sequence[pulumi.Input['InstanceAccessControlAttributesAttributeArgs']]] attributes: See AccessControlAttribute for more details.
        :param pulumi.Input[str] instance_arn: The Amazon Resource Name (ARN) of the SSO Instance.
        """
        if attributes is not None:
            pulumi.set(__self__, "attributes", attributes)
        if instance_arn is not None:
            pulumi.set(__self__, "instance_arn", instance_arn)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if status_reason is not None:
            pulumi.set(__self__, "status_reason", status_reason)

    @property
    @pulumi.getter
    def attributes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InstanceAccessControlAttributesAttributeArgs']]]]:
        """
        See AccessControlAttribute for more details.
        """
        return pulumi.get(self, "attributes")

    @attributes.setter
    def attributes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceAccessControlAttributesAttributeArgs']]]]):
        pulumi.set(self, "attributes", value)

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the SSO Instance.
        """
        return pulumi.get(self, "instance_arn")

    @instance_arn.setter
    def instance_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_arn", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="statusReason")
    def status_reason(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "status_reason")

    @status_reason.setter
    def status_reason(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status_reason", value)


class InstanceAccessControlAttributes(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attributes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceAccessControlAttributesAttributeArgs']]]]] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Single Sign-On (SSO) ABAC Resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html

        ## Import

        Using `pulumi import`, import SSO Account Assignments using the `instance_arn`. For example:

        ```sh
         $ pulumi import aws:ssoadmin/instanceAccessControlAttributes:InstanceAccessControlAttributes example arn:aws:sso:::instance/ssoins-0123456789abcdef
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceAccessControlAttributesAttributeArgs']]]] attributes: See AccessControlAttribute for more details.
        :param pulumi.Input[str] instance_arn: The Amazon Resource Name (ARN) of the SSO Instance.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InstanceAccessControlAttributesArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Single Sign-On (SSO) ABAC Resource: https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html

        ## Import

        Using `pulumi import`, import SSO Account Assignments using the `instance_arn`. For example:

        ```sh
         $ pulumi import aws:ssoadmin/instanceAccessControlAttributes:InstanceAccessControlAttributes example arn:aws:sso:::instance/ssoins-0123456789abcdef
        ```

        :param str resource_name: The name of the resource.
        :param InstanceAccessControlAttributesArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstanceAccessControlAttributesArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attributes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceAccessControlAttributesAttributeArgs']]]]] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InstanceAccessControlAttributesArgs.__new__(InstanceAccessControlAttributesArgs)

            if attributes is None and not opts.urn:
                raise TypeError("Missing required property 'attributes'")
            __props__.__dict__["attributes"] = attributes
            if instance_arn is None and not opts.urn:
                raise TypeError("Missing required property 'instance_arn'")
            __props__.__dict__["instance_arn"] = instance_arn
            __props__.__dict__["status"] = None
            __props__.__dict__["status_reason"] = None
        super(InstanceAccessControlAttributes, __self__).__init__(
            'aws:ssoadmin/instanceAccessControlAttributes:InstanceAccessControlAttributes',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            attributes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceAccessControlAttributesAttributeArgs']]]]] = None,
            instance_arn: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            status_reason: Optional[pulumi.Input[str]] = None) -> 'InstanceAccessControlAttributes':
        """
        Get an existing InstanceAccessControlAttributes resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceAccessControlAttributesAttributeArgs']]]] attributes: See AccessControlAttribute for more details.
        :param pulumi.Input[str] instance_arn: The Amazon Resource Name (ARN) of the SSO Instance.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InstanceAccessControlAttributesState.__new__(_InstanceAccessControlAttributesState)

        __props__.__dict__["attributes"] = attributes
        __props__.__dict__["instance_arn"] = instance_arn
        __props__.__dict__["status"] = status
        __props__.__dict__["status_reason"] = status_reason
        return InstanceAccessControlAttributes(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def attributes(self) -> pulumi.Output[Sequence['outputs.InstanceAccessControlAttributesAttribute']]:
        """
        See AccessControlAttribute for more details.
        """
        return pulumi.get(self, "attributes")

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the SSO Instance.
        """
        return pulumi.get(self, "instance_arn")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusReason")
    def status_reason(self) -> pulumi.Output[str]:
        return pulumi.get(self, "status_reason")

