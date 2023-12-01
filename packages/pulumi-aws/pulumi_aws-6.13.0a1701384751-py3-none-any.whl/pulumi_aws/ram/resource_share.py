# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ResourceShareArgs', 'ResourceShare']

@pulumi.input_type
class ResourceShareArgs:
    def __init__(__self__, *,
                 allow_external_principals: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permission_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ResourceShare resource.
        :param pulumi.Input[bool] allow_external_principals: Indicates whether principals outside your organization can be associated with a resource share.
        :param pulumi.Input[str] name: The name of the resource share.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permission_arns: Specifies the Amazon Resource Names (ARNs) of the RAM permission to associate with the resource share. If you do not specify an ARN for the permission, RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource share. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        if allow_external_principals is not None:
            pulumi.set(__self__, "allow_external_principals", allow_external_principals)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if permission_arns is not None:
            pulumi.set(__self__, "permission_arns", permission_arns)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="allowExternalPrincipals")
    def allow_external_principals(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether principals outside your organization can be associated with a resource share.
        """
        return pulumi.get(self, "allow_external_principals")

    @allow_external_principals.setter
    def allow_external_principals(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_external_principals", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource share.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="permissionArns")
    def permission_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the Amazon Resource Names (ARNs) of the RAM permission to associate with the resource share. If you do not specify an ARN for the permission, RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        """
        return pulumi.get(self, "permission_arns")

    @permission_arns.setter
    def permission_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "permission_arns", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource share. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ResourceShareState:
    def __init__(__self__, *,
                 allow_external_principals: Optional[pulumi.Input[bool]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permission_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering ResourceShare resources.
        :param pulumi.Input[bool] allow_external_principals: Indicates whether principals outside your organization can be associated with a resource share.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the resource share.
        :param pulumi.Input[str] name: The name of the resource share.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permission_arns: Specifies the Amazon Resource Names (ARNs) of the RAM permission to associate with the resource share. If you do not specify an ARN for the permission, RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource share. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if allow_external_principals is not None:
            pulumi.set(__self__, "allow_external_principals", allow_external_principals)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if permission_arns is not None:
            pulumi.set(__self__, "permission_arns", permission_arns)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter(name="allowExternalPrincipals")
    def allow_external_principals(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether principals outside your organization can be associated with a resource share.
        """
        return pulumi.get(self, "allow_external_principals")

    @allow_external_principals.setter
    def allow_external_principals(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_external_principals", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the resource share.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource share.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="permissionArns")
    def permission_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the Amazon Resource Names (ARNs) of the RAM permission to associate with the resource share. If you do not specify an ARN for the permission, RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        """
        return pulumi.get(self, "permission_arns")

    @permission_arns.setter
    def permission_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "permission_arns", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource share. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class ResourceShare(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_external_principals: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permission_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a Resource Access Manager (RAM) Resource Share. To associate principals with the share, see the `ram.PrincipalAssociation` resource. To associate resources with the share, see the `ram.ResourceAssociation` resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ram.ResourceShare("example",
            allow_external_principals=True,
            tags={
                "Environment": "Production",
            })
        ```

        ## Import

        Using `pulumi import`, import resource shares using the `arn` of the resource share. For example:

        ```sh
         $ pulumi import aws:ram/resourceShare:ResourceShare example arn:aws:ram:eu-west-1:123456789012:resource-share/73da1ab9-b94a-4ba3-8eb4-45917f7f4b12
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_external_principals: Indicates whether principals outside your organization can be associated with a resource share.
        :param pulumi.Input[str] name: The name of the resource share.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permission_arns: Specifies the Amazon Resource Names (ARNs) of the RAM permission to associate with the resource share. If you do not specify an ARN for the permission, RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource share. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ResourceShareArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Resource Access Manager (RAM) Resource Share. To associate principals with the share, see the `ram.PrincipalAssociation` resource. To associate resources with the share, see the `ram.ResourceAssociation` resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ram.ResourceShare("example",
            allow_external_principals=True,
            tags={
                "Environment": "Production",
            })
        ```

        ## Import

        Using `pulumi import`, import resource shares using the `arn` of the resource share. For example:

        ```sh
         $ pulumi import aws:ram/resourceShare:ResourceShare example arn:aws:ram:eu-west-1:123456789012:resource-share/73da1ab9-b94a-4ba3-8eb4-45917f7f4b12
        ```

        :param str resource_name: The name of the resource.
        :param ResourceShareArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceShareArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_external_principals: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permission_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceShareArgs.__new__(ResourceShareArgs)

            __props__.__dict__["allow_external_principals"] = allow_external_principals
            __props__.__dict__["name"] = name
            __props__.__dict__["permission_arns"] = permission_arns
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["tagsAll"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(ResourceShare, __self__).__init__(
            'aws:ram/resourceShare:ResourceShare',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            allow_external_principals: Optional[pulumi.Input[bool]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            permission_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'ResourceShare':
        """
        Get an existing ResourceShare resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_external_principals: Indicates whether principals outside your organization can be associated with a resource share.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the resource share.
        :param pulumi.Input[str] name: The name of the resource share.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permission_arns: Specifies the Amazon Resource Names (ARNs) of the RAM permission to associate with the resource share. If you do not specify an ARN for the permission, RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource share. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ResourceShareState.__new__(_ResourceShareState)

        __props__.__dict__["allow_external_principals"] = allow_external_principals
        __props__.__dict__["arn"] = arn
        __props__.__dict__["name"] = name
        __props__.__dict__["permission_arns"] = permission_arns
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return ResourceShare(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowExternalPrincipals")
    def allow_external_principals(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether principals outside your organization can be associated with a resource share.
        """
        return pulumi.get(self, "allow_external_principals")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the resource share.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource share.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="permissionArns")
    def permission_arns(self) -> pulumi.Output[Sequence[str]]:
        """
        Specifies the Amazon Resource Names (ARNs) of the RAM permission to associate with the resource share. If you do not specify an ARN for the permission, RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        """
        return pulumi.get(self, "permission_arns")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource share. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

