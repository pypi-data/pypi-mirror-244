# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DefaultVpcDhcpOptionsArgs', 'DefaultVpcDhcpOptions']

@pulumi.input_type
class DefaultVpcDhcpOptionsArgs:
    def __init__(__self__, *,
                 owner_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a DefaultVpcDhcpOptions resource.
        :param pulumi.Input[str] owner_id: The ID of the AWS account that owns the DHCP options set.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        """
        if owner_id is not None:
            pulumi.set(__self__, "owner_id", owner_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the AWS account that owns the DHCP options set.
        """
        return pulumi.get(self, "owner_id")

    @owner_id.setter
    def owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _DefaultVpcDhcpOptionsState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 domain_name_servers: Optional[pulumi.Input[str]] = None,
                 netbios_name_servers: Optional[pulumi.Input[str]] = None,
                 netbios_node_type: Optional[pulumi.Input[str]] = None,
                 ntp_servers: Optional[pulumi.Input[str]] = None,
                 owner_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering DefaultVpcDhcpOptions resources.
        :param pulumi.Input[str] arn: The ARN of the DHCP Options Set.
        :param pulumi.Input[str] netbios_name_servers: List of NETBIOS name servers.
        :param pulumi.Input[str] netbios_node_type: The NetBIOS node type (1, 2, 4, or 8). AWS recommends to specify 2 since broadcast and multicast are not supported in their network. For more information about these node types, see [RFC 2132](http://www.ietf.org/rfc/rfc2132.txt).
        :param pulumi.Input[str] owner_id: The ID of the AWS account that owns the DHCP options set.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if domain_name_servers is not None:
            pulumi.set(__self__, "domain_name_servers", domain_name_servers)
        if netbios_name_servers is not None:
            pulumi.set(__self__, "netbios_name_servers", netbios_name_servers)
        if netbios_node_type is not None:
            pulumi.set(__self__, "netbios_node_type", netbios_node_type)
        if ntp_servers is not None:
            pulumi.set(__self__, "ntp_servers", ntp_servers)
        if owner_id is not None:
            pulumi.set(__self__, "owner_id", owner_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the DHCP Options Set.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter(name="domainNameServers")
    def domain_name_servers(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "domain_name_servers")

    @domain_name_servers.setter
    def domain_name_servers(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name_servers", value)

    @property
    @pulumi.getter(name="netbiosNameServers")
    def netbios_name_servers(self) -> Optional[pulumi.Input[str]]:
        """
        List of NETBIOS name servers.
        """
        return pulumi.get(self, "netbios_name_servers")

    @netbios_name_servers.setter
    def netbios_name_servers(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "netbios_name_servers", value)

    @property
    @pulumi.getter(name="netbiosNodeType")
    def netbios_node_type(self) -> Optional[pulumi.Input[str]]:
        """
        The NetBIOS node type (1, 2, 4, or 8). AWS recommends to specify 2 since broadcast and multicast are not supported in their network. For more information about these node types, see [RFC 2132](http://www.ietf.org/rfc/rfc2132.txt).
        """
        return pulumi.get(self, "netbios_node_type")

    @netbios_node_type.setter
    def netbios_node_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "netbios_node_type", value)

    @property
    @pulumi.getter(name="ntpServers")
    def ntp_servers(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "ntp_servers")

    @ntp_servers.setter
    def ntp_servers(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ntp_servers", value)

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the AWS account that owns the DHCP options set.
        """
        return pulumi.get(self, "owner_id")

    @owner_id.setter
    def owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource.
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


class DefaultVpcDhcpOptions(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 owner_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a resource to manage the [default AWS DHCP Options Set](http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_DHCP_Options.html#AmazonDNS)
        in the current region.

        Each AWS region comes with a default set of DHCP options.
        **This is an advanced resource**, and has special caveats to be aware of when
        using it. Please read this document in its entirety before using this resource.

        The `ec2.DefaultVpcDhcpOptions` behaves differently from normal resources, in that
        this provider does not _create_ this resource, but instead "adopts" it
        into management.

        ## Example Usage

        Basic usage with tags:

        ```python
        import pulumi
        import pulumi_aws as aws

        default = aws.ec2.DefaultVpcDhcpOptions("default", tags={
            "Name": "Default DHCP Option Set",
        })
        ```

        ## Import

        Using `pulumi import`, import VPC DHCP Options using the DHCP Options `id`. For example:

        ```sh
         $ pulumi import aws:ec2/defaultVpcDhcpOptions:DefaultVpcDhcpOptions default_options dopt-d9070ebb
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] owner_id: The ID of the AWS account that owns the DHCP options set.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[DefaultVpcDhcpOptionsArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage the [default AWS DHCP Options Set](http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_DHCP_Options.html#AmazonDNS)
        in the current region.

        Each AWS region comes with a default set of DHCP options.
        **This is an advanced resource**, and has special caveats to be aware of when
        using it. Please read this document in its entirety before using this resource.

        The `ec2.DefaultVpcDhcpOptions` behaves differently from normal resources, in that
        this provider does not _create_ this resource, but instead "adopts" it
        into management.

        ## Example Usage

        Basic usage with tags:

        ```python
        import pulumi
        import pulumi_aws as aws

        default = aws.ec2.DefaultVpcDhcpOptions("default", tags={
            "Name": "Default DHCP Option Set",
        })
        ```

        ## Import

        Using `pulumi import`, import VPC DHCP Options using the DHCP Options `id`. For example:

        ```sh
         $ pulumi import aws:ec2/defaultVpcDhcpOptions:DefaultVpcDhcpOptions default_options dopt-d9070ebb
        ```

        :param str resource_name: The name of the resource.
        :param DefaultVpcDhcpOptionsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DefaultVpcDhcpOptionsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 owner_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DefaultVpcDhcpOptionsArgs.__new__(DefaultVpcDhcpOptionsArgs)

            __props__.__dict__["owner_id"] = owner_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["domain_name"] = None
            __props__.__dict__["domain_name_servers"] = None
            __props__.__dict__["netbios_name_servers"] = None
            __props__.__dict__["netbios_node_type"] = None
            __props__.__dict__["ntp_servers"] = None
            __props__.__dict__["tags_all"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["tagsAll"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(DefaultVpcDhcpOptions, __self__).__init__(
            'aws:ec2/defaultVpcDhcpOptions:DefaultVpcDhcpOptions',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            domain_name: Optional[pulumi.Input[str]] = None,
            domain_name_servers: Optional[pulumi.Input[str]] = None,
            netbios_name_servers: Optional[pulumi.Input[str]] = None,
            netbios_node_type: Optional[pulumi.Input[str]] = None,
            ntp_servers: Optional[pulumi.Input[str]] = None,
            owner_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'DefaultVpcDhcpOptions':
        """
        Get an existing DefaultVpcDhcpOptions resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the DHCP Options Set.
        :param pulumi.Input[str] netbios_name_servers: List of NETBIOS name servers.
        :param pulumi.Input[str] netbios_node_type: The NetBIOS node type (1, 2, 4, or 8). AWS recommends to specify 2 since broadcast and multicast are not supported in their network. For more information about these node types, see [RFC 2132](http://www.ietf.org/rfc/rfc2132.txt).
        :param pulumi.Input[str] owner_id: The ID of the AWS account that owns the DHCP options set.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DefaultVpcDhcpOptionsState.__new__(_DefaultVpcDhcpOptionsState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["domain_name"] = domain_name
        __props__.__dict__["domain_name_servers"] = domain_name_servers
        __props__.__dict__["netbios_name_servers"] = netbios_name_servers
        __props__.__dict__["netbios_node_type"] = netbios_node_type
        __props__.__dict__["ntp_servers"] = ntp_servers
        __props__.__dict__["owner_id"] = owner_id
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return DefaultVpcDhcpOptions(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the DHCP Options Set.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter(name="domainNameServers")
    def domain_name_servers(self) -> pulumi.Output[str]:
        return pulumi.get(self, "domain_name_servers")

    @property
    @pulumi.getter(name="netbiosNameServers")
    def netbios_name_servers(self) -> pulumi.Output[str]:
        """
        List of NETBIOS name servers.
        """
        return pulumi.get(self, "netbios_name_servers")

    @property
    @pulumi.getter(name="netbiosNodeType")
    def netbios_node_type(self) -> pulumi.Output[str]:
        """
        The NetBIOS node type (1, 2, 4, or 8). AWS recommends to specify 2 since broadcast and multicast are not supported in their network. For more information about these node types, see [RFC 2132](http://www.ietf.org/rfc/rfc2132.txt).
        """
        return pulumi.get(self, "netbios_node_type")

    @property
    @pulumi.getter(name="ntpServers")
    def ntp_servers(self) -> pulumi.Output[str]:
        return pulumi.get(self, "ntp_servers")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        """
        The ID of the AWS account that owns the DHCP options set.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

