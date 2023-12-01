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

__all__ = ['InstanceArgs', 'Instance']

@pulumi.input_type
class InstanceArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 fips_enabled: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Instance resource.
        :param pulumi.Input[str] description: A description for the AWS Verified Access Instance.
        :param pulumi.Input[bool] fips_enabled: Enable or disable support for Federal Information Processing Standards (FIPS) on the AWS Verified Access Instance.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if fips_enabled is not None:
            pulumi.set(__self__, "fips_enabled", fips_enabled)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description for the AWS Verified Access Instance.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="fipsEnabled")
    def fips_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable or disable support for Federal Information Processing Standards (FIPS) on the AWS Verified Access Instance.
        """
        return pulumi.get(self, "fips_enabled")

    @fips_enabled.setter
    def fips_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "fips_enabled", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _InstanceState:
    def __init__(__self__, *,
                 creation_time: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 fips_enabled: Optional[pulumi.Input[bool]] = None,
                 last_updated_time: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 verified_access_trust_providers: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceVerifiedAccessTrustProviderArgs']]]] = None):
        """
        Input properties used for looking up and filtering Instance resources.
        :param pulumi.Input[str] creation_time: The time that the Verified Access Instance was created.
        :param pulumi.Input[str] description: A description for the AWS Verified Access Instance.
        :param pulumi.Input[bool] fips_enabled: Enable or disable support for Federal Information Processing Standards (FIPS) on the AWS Verified Access Instance.
        :param pulumi.Input[str] last_updated_time: The time that the Verified Access Instance was last updated.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Sequence[pulumi.Input['InstanceVerifiedAccessTrustProviderArgs']]] verified_access_trust_providers: One or more blocks of providing information about the AWS Verified Access Trust Providers. See verified_access_trust_providers below for details.One or more blocks
        """
        if creation_time is not None:
            pulumi.set(__self__, "creation_time", creation_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if fips_enabled is not None:
            pulumi.set(__self__, "fips_enabled", fips_enabled)
        if last_updated_time is not None:
            pulumi.set(__self__, "last_updated_time", last_updated_time)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if verified_access_trust_providers is not None:
            pulumi.set(__self__, "verified_access_trust_providers", verified_access_trust_providers)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[pulumi.Input[str]]:
        """
        The time that the Verified Access Instance was created.
        """
        return pulumi.get(self, "creation_time")

    @creation_time.setter
    def creation_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "creation_time", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description for the AWS Verified Access Instance.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="fipsEnabled")
    def fips_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable or disable support for Federal Information Processing Standards (FIPS) on the AWS Verified Access Instance.
        """
        return pulumi.get(self, "fips_enabled")

    @fips_enabled.setter
    def fips_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "fips_enabled", value)

    @property
    @pulumi.getter(name="lastUpdatedTime")
    def last_updated_time(self) -> Optional[pulumi.Input[str]]:
        """
        The time that the Verified Access Instance was last updated.
        """
        return pulumi.get(self, "last_updated_time")

    @last_updated_time.setter
    def last_updated_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_updated_time", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter(name="verifiedAccessTrustProviders")
    def verified_access_trust_providers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InstanceVerifiedAccessTrustProviderArgs']]]]:
        """
        One or more blocks of providing information about the AWS Verified Access Trust Providers. See verified_access_trust_providers below for details.One or more blocks
        """
        return pulumi.get(self, "verified_access_trust_providers")

    @verified_access_trust_providers.setter
    def verified_access_trust_providers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceVerifiedAccessTrustProviderArgs']]]]):
        pulumi.set(self, "verified_access_trust_providers", value)


class Instance(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 fips_enabled: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Resource for managing a Verified Access Instance.

        ## Example Usage
        ### Basic

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.verifiedaccess.Instance("example",
            description="example",
            tags={
                "Name": "example",
            })
        ```
        ### With `fips_enabled`

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.verifiedaccess.Instance("example", fips_enabled=True)
        ```

        ## Import

        Using `pulumi import`, import Verified Access Instances using the

        `id`. For example:

        ```sh
         $ pulumi import aws:verifiedaccess/instance:Instance example vai-1234567890abcdef0
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description for the AWS Verified Access Instance.
        :param pulumi.Input[bool] fips_enabled: Enable or disable support for Federal Information Processing Standards (FIPS) on the AWS Verified Access Instance.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[InstanceArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing a Verified Access Instance.

        ## Example Usage
        ### Basic

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.verifiedaccess.Instance("example",
            description="example",
            tags={
                "Name": "example",
            })
        ```
        ### With `fips_enabled`

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.verifiedaccess.Instance("example", fips_enabled=True)
        ```

        ## Import

        Using `pulumi import`, import Verified Access Instances using the

        `id`. For example:

        ```sh
         $ pulumi import aws:verifiedaccess/instance:Instance example vai-1234567890abcdef0
        ```

        :param str resource_name: The name of the resource.
        :param InstanceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstanceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 fips_enabled: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InstanceArgs.__new__(InstanceArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["fips_enabled"] = fips_enabled
            __props__.__dict__["tags"] = tags
            __props__.__dict__["creation_time"] = None
            __props__.__dict__["last_updated_time"] = None
            __props__.__dict__["tags_all"] = None
            __props__.__dict__["verified_access_trust_providers"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["tagsAll"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Instance, __self__).__init__(
            'aws:verifiedaccess/instance:Instance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            creation_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            fips_enabled: Optional[pulumi.Input[bool]] = None,
            last_updated_time: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            verified_access_trust_providers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceVerifiedAccessTrustProviderArgs']]]]] = None) -> 'Instance':
        """
        Get an existing Instance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] creation_time: The time that the Verified Access Instance was created.
        :param pulumi.Input[str] description: A description for the AWS Verified Access Instance.
        :param pulumi.Input[bool] fips_enabled: Enable or disable support for Federal Information Processing Standards (FIPS) on the AWS Verified Access Instance.
        :param pulumi.Input[str] last_updated_time: The time that the Verified Access Instance was last updated.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceVerifiedAccessTrustProviderArgs']]]] verified_access_trust_providers: One or more blocks of providing information about the AWS Verified Access Trust Providers. See verified_access_trust_providers below for details.One or more blocks
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InstanceState.__new__(_InstanceState)

        __props__.__dict__["creation_time"] = creation_time
        __props__.__dict__["description"] = description
        __props__.__dict__["fips_enabled"] = fips_enabled
        __props__.__dict__["last_updated_time"] = last_updated_time
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["verified_access_trust_providers"] = verified_access_trust_providers
        return Instance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        The time that the Verified Access Instance was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description for the AWS Verified Access Instance.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="fipsEnabled")
    def fips_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable or disable support for Federal Information Processing Standards (FIPS) on the AWS Verified Access Instance.
        """
        return pulumi.get(self, "fips_enabled")

    @property
    @pulumi.getter(name="lastUpdatedTime")
    def last_updated_time(self) -> pulumi.Output[str]:
        """
        The time that the Verified Access Instance was last updated.
        """
        return pulumi.get(self, "last_updated_time")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter(name="verifiedAccessTrustProviders")
    def verified_access_trust_providers(self) -> pulumi.Output[Sequence['outputs.InstanceVerifiedAccessTrustProvider']]:
        """
        One or more blocks of providing information about the AWS Verified Access Trust Providers. See verified_access_trust_providers below for details.One or more blocks
        """
        return pulumi.get(self, "verified_access_trust_providers")

