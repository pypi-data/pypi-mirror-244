# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['HostedPrivateVirtualInterfaceAccepterArgs', 'HostedPrivateVirtualInterfaceAccepter']

@pulumi.input_type
class HostedPrivateVirtualInterfaceAccepterArgs:
    def __init__(__self__, *,
                 virtual_interface_id: pulumi.Input[str],
                 dx_gateway_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vpn_gateway_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a HostedPrivateVirtualInterfaceAccepter resource.
        :param pulumi.Input[str] virtual_interface_id: The ID of the Direct Connect virtual interface to accept.
        :param pulumi.Input[str] dx_gateway_id: The ID of the Direct Connect gateway to which to connect the virtual interface.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] vpn_gateway_id: The ID of the virtual private gateway to which to connect the virtual interface.
        """
        pulumi.set(__self__, "virtual_interface_id", virtual_interface_id)
        if dx_gateway_id is not None:
            pulumi.set(__self__, "dx_gateway_id", dx_gateway_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if vpn_gateway_id is not None:
            pulumi.set(__self__, "vpn_gateway_id", vpn_gateway_id)

    @property
    @pulumi.getter(name="virtualInterfaceId")
    def virtual_interface_id(self) -> pulumi.Input[str]:
        """
        The ID of the Direct Connect virtual interface to accept.
        """
        return pulumi.get(self, "virtual_interface_id")

    @virtual_interface_id.setter
    def virtual_interface_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_interface_id", value)

    @property
    @pulumi.getter(name="dxGatewayId")
    def dx_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Direct Connect gateway to which to connect the virtual interface.
        """
        return pulumi.get(self, "dx_gateway_id")

    @dx_gateway_id.setter
    def dx_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dx_gateway_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vpnGatewayId")
    def vpn_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the virtual private gateway to which to connect the virtual interface.
        """
        return pulumi.get(self, "vpn_gateway_id")

    @vpn_gateway_id.setter
    def vpn_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpn_gateway_id", value)


@pulumi.input_type
class _HostedPrivateVirtualInterfaceAccepterState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 dx_gateway_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_interface_id: Optional[pulumi.Input[str]] = None,
                 vpn_gateway_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering HostedPrivateVirtualInterfaceAccepter resources.
        :param pulumi.Input[str] arn: The ARN of the virtual interface.
        :param pulumi.Input[str] dx_gateway_id: The ID of the Direct Connect gateway to which to connect the virtual interface.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] virtual_interface_id: The ID of the Direct Connect virtual interface to accept.
        :param pulumi.Input[str] vpn_gateway_id: The ID of the virtual private gateway to which to connect the virtual interface.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if dx_gateway_id is not None:
            pulumi.set(__self__, "dx_gateway_id", dx_gateway_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if virtual_interface_id is not None:
            pulumi.set(__self__, "virtual_interface_id", virtual_interface_id)
        if vpn_gateway_id is not None:
            pulumi.set(__self__, "vpn_gateway_id", vpn_gateway_id)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the virtual interface.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="dxGatewayId")
    def dx_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Direct Connect gateway to which to connect the virtual interface.
        """
        return pulumi.get(self, "dx_gateway_id")

    @dx_gateway_id.setter
    def dx_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dx_gateway_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

    @property
    @pulumi.getter(name="virtualInterfaceId")
    def virtual_interface_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Direct Connect virtual interface to accept.
        """
        return pulumi.get(self, "virtual_interface_id")

    @virtual_interface_id.setter
    def virtual_interface_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_interface_id", value)

    @property
    @pulumi.getter(name="vpnGatewayId")
    def vpn_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the virtual private gateway to which to connect the virtual interface.
        """
        return pulumi.get(self, "vpn_gateway_id")

    @vpn_gateway_id.setter
    def vpn_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpn_gateway_id", value)


class HostedPrivateVirtualInterfaceAccepter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dx_gateway_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_interface_id: Optional[pulumi.Input[str]] = None,
                 vpn_gateway_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage the accepter's side of a Direct Connect hosted private virtual interface.
        This resource accepts ownership of a private virtual interface created by another AWS account.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        accepter = aws.Provider("accepter")
        # Accepter's credentials.
        accepter_caller_identity = aws.get_caller_identity()
        # Accepter's side of the VIF.
        vpn_gw = aws.ec2.VpnGateway("vpnGw", opts=pulumi.ResourceOptions(provider=aws["accepter"]))
        # Creator's side of the VIF
        creator = aws.directconnect.HostedPrivateVirtualInterface("creator",
            connection_id="dxcon-zzzzzzzz",
            owner_account_id=accepter_caller_identity.account_id,
            vlan=4094,
            address_family="ipv4",
            bgp_asn=65352,
            opts=pulumi.ResourceOptions(depends_on=[vpn_gw]))
        accepter_hosted_private_virtual_interface_accepter = aws.directconnect.HostedPrivateVirtualInterfaceAccepter("accepterHostedPrivateVirtualInterfaceAccepter",
            virtual_interface_id=creator.id,
            vpn_gateway_id=vpn_gw.id,
            tags={
                "Side": "Accepter",
            },
            opts=pulumi.ResourceOptions(provider=aws["accepter"]))
        ```

        ## Import

        Using `pulumi import`, import Direct Connect hosted private virtual interfaces using the VIF `id`. For example:

        ```sh
         $ pulumi import aws:directconnect/hostedPrivateVirtualInterfaceAccepter:HostedPrivateVirtualInterfaceAccepter test dxvif-33cc44dd
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dx_gateway_id: The ID of the Direct Connect gateway to which to connect the virtual interface.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] virtual_interface_id: The ID of the Direct Connect virtual interface to accept.
        :param pulumi.Input[str] vpn_gateway_id: The ID of the virtual private gateway to which to connect the virtual interface.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: HostedPrivateVirtualInterfaceAccepterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage the accepter's side of a Direct Connect hosted private virtual interface.
        This resource accepts ownership of a private virtual interface created by another AWS account.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        accepter = aws.Provider("accepter")
        # Accepter's credentials.
        accepter_caller_identity = aws.get_caller_identity()
        # Accepter's side of the VIF.
        vpn_gw = aws.ec2.VpnGateway("vpnGw", opts=pulumi.ResourceOptions(provider=aws["accepter"]))
        # Creator's side of the VIF
        creator = aws.directconnect.HostedPrivateVirtualInterface("creator",
            connection_id="dxcon-zzzzzzzz",
            owner_account_id=accepter_caller_identity.account_id,
            vlan=4094,
            address_family="ipv4",
            bgp_asn=65352,
            opts=pulumi.ResourceOptions(depends_on=[vpn_gw]))
        accepter_hosted_private_virtual_interface_accepter = aws.directconnect.HostedPrivateVirtualInterfaceAccepter("accepterHostedPrivateVirtualInterfaceAccepter",
            virtual_interface_id=creator.id,
            vpn_gateway_id=vpn_gw.id,
            tags={
                "Side": "Accepter",
            },
            opts=pulumi.ResourceOptions(provider=aws["accepter"]))
        ```

        ## Import

        Using `pulumi import`, import Direct Connect hosted private virtual interfaces using the VIF `id`. For example:

        ```sh
         $ pulumi import aws:directconnect/hostedPrivateVirtualInterfaceAccepter:HostedPrivateVirtualInterfaceAccepter test dxvif-33cc44dd
        ```

        :param str resource_name: The name of the resource.
        :param HostedPrivateVirtualInterfaceAccepterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(HostedPrivateVirtualInterfaceAccepterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dx_gateway_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_interface_id: Optional[pulumi.Input[str]] = None,
                 vpn_gateway_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = HostedPrivateVirtualInterfaceAccepterArgs.__new__(HostedPrivateVirtualInterfaceAccepterArgs)

            __props__.__dict__["dx_gateway_id"] = dx_gateway_id
            __props__.__dict__["tags"] = tags
            if virtual_interface_id is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_interface_id'")
            __props__.__dict__["virtual_interface_id"] = virtual_interface_id
            __props__.__dict__["vpn_gateway_id"] = vpn_gateway_id
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["tagsAll"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(HostedPrivateVirtualInterfaceAccepter, __self__).__init__(
            'aws:directconnect/hostedPrivateVirtualInterfaceAccepter:HostedPrivateVirtualInterfaceAccepter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            dx_gateway_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            virtual_interface_id: Optional[pulumi.Input[str]] = None,
            vpn_gateway_id: Optional[pulumi.Input[str]] = None) -> 'HostedPrivateVirtualInterfaceAccepter':
        """
        Get an existing HostedPrivateVirtualInterfaceAccepter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the virtual interface.
        :param pulumi.Input[str] dx_gateway_id: The ID of the Direct Connect gateway to which to connect the virtual interface.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] virtual_interface_id: The ID of the Direct Connect virtual interface to accept.
        :param pulumi.Input[str] vpn_gateway_id: The ID of the virtual private gateway to which to connect the virtual interface.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _HostedPrivateVirtualInterfaceAccepterState.__new__(_HostedPrivateVirtualInterfaceAccepterState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["dx_gateway_id"] = dx_gateway_id
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["virtual_interface_id"] = virtual_interface_id
        __props__.__dict__["vpn_gateway_id"] = vpn_gateway_id
        return HostedPrivateVirtualInterfaceAccepter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the virtual interface.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="dxGatewayId")
    def dx_gateway_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the Direct Connect gateway to which to connect the virtual interface.
        """
        return pulumi.get(self, "dx_gateway_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

    @property
    @pulumi.getter(name="virtualInterfaceId")
    def virtual_interface_id(self) -> pulumi.Output[str]:
        """
        The ID of the Direct Connect virtual interface to accept.
        """
        return pulumi.get(self, "virtual_interface_id")

    @property
    @pulumi.getter(name="vpnGatewayId")
    def vpn_gateway_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the virtual private gateway to which to connect the virtual interface.
        """
        return pulumi.get(self, "vpn_gateway_id")

