# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['BgpPeerArgs', 'BgpPeer']

@pulumi.input_type
class BgpPeerArgs:
    def __init__(__self__, *,
                 address_family: pulumi.Input[str],
                 bgp_asn: pulumi.Input[int],
                 virtual_interface_id: pulumi.Input[str],
                 amazon_address: Optional[pulumi.Input[str]] = None,
                 bgp_auth_key: Optional[pulumi.Input[str]] = None,
                 customer_address: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BgpPeer resource.
        :param pulumi.Input[str] address_family: The address family for the BGP peer. `ipv4 ` or `ipv6`.
        :param pulumi.Input[int] bgp_asn: The autonomous system (AS) number for Border Gateway Protocol (BGP) configuration.
        :param pulumi.Input[str] virtual_interface_id: The ID of the Direct Connect virtual interface on which to create the BGP peer.
        :param pulumi.Input[str] amazon_address: The IPv4 CIDR address to use to send traffic to Amazon.
               Required for IPv4 BGP peers on public virtual interfaces.
        :param pulumi.Input[str] bgp_auth_key: The authentication key for BGP configuration.
        :param pulumi.Input[str] customer_address: The IPv4 CIDR destination address to which Amazon should send traffic.
               Required for IPv4 BGP peers on public virtual interfaces.
        """
        pulumi.set(__self__, "address_family", address_family)
        pulumi.set(__self__, "bgp_asn", bgp_asn)
        pulumi.set(__self__, "virtual_interface_id", virtual_interface_id)
        if amazon_address is not None:
            pulumi.set(__self__, "amazon_address", amazon_address)
        if bgp_auth_key is not None:
            pulumi.set(__self__, "bgp_auth_key", bgp_auth_key)
        if customer_address is not None:
            pulumi.set(__self__, "customer_address", customer_address)

    @property
    @pulumi.getter(name="addressFamily")
    def address_family(self) -> pulumi.Input[str]:
        """
        The address family for the BGP peer. `ipv4 ` or `ipv6`.
        """
        return pulumi.get(self, "address_family")

    @address_family.setter
    def address_family(self, value: pulumi.Input[str]):
        pulumi.set(self, "address_family", value)

    @property
    @pulumi.getter(name="bgpAsn")
    def bgp_asn(self) -> pulumi.Input[int]:
        """
        The autonomous system (AS) number for Border Gateway Protocol (BGP) configuration.
        """
        return pulumi.get(self, "bgp_asn")

    @bgp_asn.setter
    def bgp_asn(self, value: pulumi.Input[int]):
        pulumi.set(self, "bgp_asn", value)

    @property
    @pulumi.getter(name="virtualInterfaceId")
    def virtual_interface_id(self) -> pulumi.Input[str]:
        """
        The ID of the Direct Connect virtual interface on which to create the BGP peer.
        """
        return pulumi.get(self, "virtual_interface_id")

    @virtual_interface_id.setter
    def virtual_interface_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_interface_id", value)

    @property
    @pulumi.getter(name="amazonAddress")
    def amazon_address(self) -> Optional[pulumi.Input[str]]:
        """
        The IPv4 CIDR address to use to send traffic to Amazon.
        Required for IPv4 BGP peers on public virtual interfaces.
        """
        return pulumi.get(self, "amazon_address")

    @amazon_address.setter
    def amazon_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "amazon_address", value)

    @property
    @pulumi.getter(name="bgpAuthKey")
    def bgp_auth_key(self) -> Optional[pulumi.Input[str]]:
        """
        The authentication key for BGP configuration.
        """
        return pulumi.get(self, "bgp_auth_key")

    @bgp_auth_key.setter
    def bgp_auth_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bgp_auth_key", value)

    @property
    @pulumi.getter(name="customerAddress")
    def customer_address(self) -> Optional[pulumi.Input[str]]:
        """
        The IPv4 CIDR destination address to which Amazon should send traffic.
        Required for IPv4 BGP peers on public virtual interfaces.
        """
        return pulumi.get(self, "customer_address")

    @customer_address.setter
    def customer_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "customer_address", value)


@pulumi.input_type
class _BgpPeerState:
    def __init__(__self__, *,
                 address_family: Optional[pulumi.Input[str]] = None,
                 amazon_address: Optional[pulumi.Input[str]] = None,
                 aws_device: Optional[pulumi.Input[str]] = None,
                 bgp_asn: Optional[pulumi.Input[int]] = None,
                 bgp_auth_key: Optional[pulumi.Input[str]] = None,
                 bgp_peer_id: Optional[pulumi.Input[str]] = None,
                 bgp_status: Optional[pulumi.Input[str]] = None,
                 customer_address: Optional[pulumi.Input[str]] = None,
                 virtual_interface_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BgpPeer resources.
        :param pulumi.Input[str] address_family: The address family for the BGP peer. `ipv4 ` or `ipv6`.
        :param pulumi.Input[str] amazon_address: The IPv4 CIDR address to use to send traffic to Amazon.
               Required for IPv4 BGP peers on public virtual interfaces.
        :param pulumi.Input[str] aws_device: The Direct Connect endpoint on which the BGP peer terminates.
        :param pulumi.Input[int] bgp_asn: The autonomous system (AS) number for Border Gateway Protocol (BGP) configuration.
        :param pulumi.Input[str] bgp_auth_key: The authentication key for BGP configuration.
        :param pulumi.Input[str] bgp_peer_id: The ID of the BGP peer.
        :param pulumi.Input[str] bgp_status: The Up/Down state of the BGP peer.
        :param pulumi.Input[str] customer_address: The IPv4 CIDR destination address to which Amazon should send traffic.
               Required for IPv4 BGP peers on public virtual interfaces.
        :param pulumi.Input[str] virtual_interface_id: The ID of the Direct Connect virtual interface on which to create the BGP peer.
        """
        if address_family is not None:
            pulumi.set(__self__, "address_family", address_family)
        if amazon_address is not None:
            pulumi.set(__self__, "amazon_address", amazon_address)
        if aws_device is not None:
            pulumi.set(__self__, "aws_device", aws_device)
        if bgp_asn is not None:
            pulumi.set(__self__, "bgp_asn", bgp_asn)
        if bgp_auth_key is not None:
            pulumi.set(__self__, "bgp_auth_key", bgp_auth_key)
        if bgp_peer_id is not None:
            pulumi.set(__self__, "bgp_peer_id", bgp_peer_id)
        if bgp_status is not None:
            pulumi.set(__self__, "bgp_status", bgp_status)
        if customer_address is not None:
            pulumi.set(__self__, "customer_address", customer_address)
        if virtual_interface_id is not None:
            pulumi.set(__self__, "virtual_interface_id", virtual_interface_id)

    @property
    @pulumi.getter(name="addressFamily")
    def address_family(self) -> Optional[pulumi.Input[str]]:
        """
        The address family for the BGP peer. `ipv4 ` or `ipv6`.
        """
        return pulumi.get(self, "address_family")

    @address_family.setter
    def address_family(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address_family", value)

    @property
    @pulumi.getter(name="amazonAddress")
    def amazon_address(self) -> Optional[pulumi.Input[str]]:
        """
        The IPv4 CIDR address to use to send traffic to Amazon.
        Required for IPv4 BGP peers on public virtual interfaces.
        """
        return pulumi.get(self, "amazon_address")

    @amazon_address.setter
    def amazon_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "amazon_address", value)

    @property
    @pulumi.getter(name="awsDevice")
    def aws_device(self) -> Optional[pulumi.Input[str]]:
        """
        The Direct Connect endpoint on which the BGP peer terminates.
        """
        return pulumi.get(self, "aws_device")

    @aws_device.setter
    def aws_device(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_device", value)

    @property
    @pulumi.getter(name="bgpAsn")
    def bgp_asn(self) -> Optional[pulumi.Input[int]]:
        """
        The autonomous system (AS) number for Border Gateway Protocol (BGP) configuration.
        """
        return pulumi.get(self, "bgp_asn")

    @bgp_asn.setter
    def bgp_asn(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "bgp_asn", value)

    @property
    @pulumi.getter(name="bgpAuthKey")
    def bgp_auth_key(self) -> Optional[pulumi.Input[str]]:
        """
        The authentication key for BGP configuration.
        """
        return pulumi.get(self, "bgp_auth_key")

    @bgp_auth_key.setter
    def bgp_auth_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bgp_auth_key", value)

    @property
    @pulumi.getter(name="bgpPeerId")
    def bgp_peer_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the BGP peer.
        """
        return pulumi.get(self, "bgp_peer_id")

    @bgp_peer_id.setter
    def bgp_peer_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bgp_peer_id", value)

    @property
    @pulumi.getter(name="bgpStatus")
    def bgp_status(self) -> Optional[pulumi.Input[str]]:
        """
        The Up/Down state of the BGP peer.
        """
        return pulumi.get(self, "bgp_status")

    @bgp_status.setter
    def bgp_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bgp_status", value)

    @property
    @pulumi.getter(name="customerAddress")
    def customer_address(self) -> Optional[pulumi.Input[str]]:
        """
        The IPv4 CIDR destination address to which Amazon should send traffic.
        Required for IPv4 BGP peers on public virtual interfaces.
        """
        return pulumi.get(self, "customer_address")

    @customer_address.setter
    def customer_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "customer_address", value)

    @property
    @pulumi.getter(name="virtualInterfaceId")
    def virtual_interface_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Direct Connect virtual interface on which to create the BGP peer.
        """
        return pulumi.get(self, "virtual_interface_id")

    @virtual_interface_id.setter
    def virtual_interface_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_interface_id", value)


class BgpPeer(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address_family: Optional[pulumi.Input[str]] = None,
                 amazon_address: Optional[pulumi.Input[str]] = None,
                 bgp_asn: Optional[pulumi.Input[int]] = None,
                 bgp_auth_key: Optional[pulumi.Input[str]] = None,
                 customer_address: Optional[pulumi.Input[str]] = None,
                 virtual_interface_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Direct Connect BGP peer resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        peer = aws.directconnect.BgpPeer("peer",
            virtual_interface_id=aws_dx_private_virtual_interface["foo"]["id"],
            address_family="ipv6",
            bgp_asn=65351)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address_family: The address family for the BGP peer. `ipv4 ` or `ipv6`.
        :param pulumi.Input[str] amazon_address: The IPv4 CIDR address to use to send traffic to Amazon.
               Required for IPv4 BGP peers on public virtual interfaces.
        :param pulumi.Input[int] bgp_asn: The autonomous system (AS) number for Border Gateway Protocol (BGP) configuration.
        :param pulumi.Input[str] bgp_auth_key: The authentication key for BGP configuration.
        :param pulumi.Input[str] customer_address: The IPv4 CIDR destination address to which Amazon should send traffic.
               Required for IPv4 BGP peers on public virtual interfaces.
        :param pulumi.Input[str] virtual_interface_id: The ID of the Direct Connect virtual interface on which to create the BGP peer.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BgpPeerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Direct Connect BGP peer resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        peer = aws.directconnect.BgpPeer("peer",
            virtual_interface_id=aws_dx_private_virtual_interface["foo"]["id"],
            address_family="ipv6",
            bgp_asn=65351)
        ```

        :param str resource_name: The name of the resource.
        :param BgpPeerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BgpPeerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address_family: Optional[pulumi.Input[str]] = None,
                 amazon_address: Optional[pulumi.Input[str]] = None,
                 bgp_asn: Optional[pulumi.Input[int]] = None,
                 bgp_auth_key: Optional[pulumi.Input[str]] = None,
                 customer_address: Optional[pulumi.Input[str]] = None,
                 virtual_interface_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BgpPeerArgs.__new__(BgpPeerArgs)

            if address_family is None and not opts.urn:
                raise TypeError("Missing required property 'address_family'")
            __props__.__dict__["address_family"] = address_family
            __props__.__dict__["amazon_address"] = amazon_address
            if bgp_asn is None and not opts.urn:
                raise TypeError("Missing required property 'bgp_asn'")
            __props__.__dict__["bgp_asn"] = bgp_asn
            __props__.__dict__["bgp_auth_key"] = bgp_auth_key
            __props__.__dict__["customer_address"] = customer_address
            if virtual_interface_id is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_interface_id'")
            __props__.__dict__["virtual_interface_id"] = virtual_interface_id
            __props__.__dict__["aws_device"] = None
            __props__.__dict__["bgp_peer_id"] = None
            __props__.__dict__["bgp_status"] = None
        super(BgpPeer, __self__).__init__(
            'aws:directconnect/bgpPeer:BgpPeer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            address_family: Optional[pulumi.Input[str]] = None,
            amazon_address: Optional[pulumi.Input[str]] = None,
            aws_device: Optional[pulumi.Input[str]] = None,
            bgp_asn: Optional[pulumi.Input[int]] = None,
            bgp_auth_key: Optional[pulumi.Input[str]] = None,
            bgp_peer_id: Optional[pulumi.Input[str]] = None,
            bgp_status: Optional[pulumi.Input[str]] = None,
            customer_address: Optional[pulumi.Input[str]] = None,
            virtual_interface_id: Optional[pulumi.Input[str]] = None) -> 'BgpPeer':
        """
        Get an existing BgpPeer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address_family: The address family for the BGP peer. `ipv4 ` or `ipv6`.
        :param pulumi.Input[str] amazon_address: The IPv4 CIDR address to use to send traffic to Amazon.
               Required for IPv4 BGP peers on public virtual interfaces.
        :param pulumi.Input[str] aws_device: The Direct Connect endpoint on which the BGP peer terminates.
        :param pulumi.Input[int] bgp_asn: The autonomous system (AS) number for Border Gateway Protocol (BGP) configuration.
        :param pulumi.Input[str] bgp_auth_key: The authentication key for BGP configuration.
        :param pulumi.Input[str] bgp_peer_id: The ID of the BGP peer.
        :param pulumi.Input[str] bgp_status: The Up/Down state of the BGP peer.
        :param pulumi.Input[str] customer_address: The IPv4 CIDR destination address to which Amazon should send traffic.
               Required for IPv4 BGP peers on public virtual interfaces.
        :param pulumi.Input[str] virtual_interface_id: The ID of the Direct Connect virtual interface on which to create the BGP peer.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BgpPeerState.__new__(_BgpPeerState)

        __props__.__dict__["address_family"] = address_family
        __props__.__dict__["amazon_address"] = amazon_address
        __props__.__dict__["aws_device"] = aws_device
        __props__.__dict__["bgp_asn"] = bgp_asn
        __props__.__dict__["bgp_auth_key"] = bgp_auth_key
        __props__.__dict__["bgp_peer_id"] = bgp_peer_id
        __props__.__dict__["bgp_status"] = bgp_status
        __props__.__dict__["customer_address"] = customer_address
        __props__.__dict__["virtual_interface_id"] = virtual_interface_id
        return BgpPeer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="addressFamily")
    def address_family(self) -> pulumi.Output[str]:
        """
        The address family for the BGP peer. `ipv4 ` or `ipv6`.
        """
        return pulumi.get(self, "address_family")

    @property
    @pulumi.getter(name="amazonAddress")
    def amazon_address(self) -> pulumi.Output[str]:
        """
        The IPv4 CIDR address to use to send traffic to Amazon.
        Required for IPv4 BGP peers on public virtual interfaces.
        """
        return pulumi.get(self, "amazon_address")

    @property
    @pulumi.getter(name="awsDevice")
    def aws_device(self) -> pulumi.Output[str]:
        """
        The Direct Connect endpoint on which the BGP peer terminates.
        """
        return pulumi.get(self, "aws_device")

    @property
    @pulumi.getter(name="bgpAsn")
    def bgp_asn(self) -> pulumi.Output[int]:
        """
        The autonomous system (AS) number for Border Gateway Protocol (BGP) configuration.
        """
        return pulumi.get(self, "bgp_asn")

    @property
    @pulumi.getter(name="bgpAuthKey")
    def bgp_auth_key(self) -> pulumi.Output[str]:
        """
        The authentication key for BGP configuration.
        """
        return pulumi.get(self, "bgp_auth_key")

    @property
    @pulumi.getter(name="bgpPeerId")
    def bgp_peer_id(self) -> pulumi.Output[str]:
        """
        The ID of the BGP peer.
        """
        return pulumi.get(self, "bgp_peer_id")

    @property
    @pulumi.getter(name="bgpStatus")
    def bgp_status(self) -> pulumi.Output[str]:
        """
        The Up/Down state of the BGP peer.
        """
        return pulumi.get(self, "bgp_status")

    @property
    @pulumi.getter(name="customerAddress")
    def customer_address(self) -> pulumi.Output[str]:
        """
        The IPv4 CIDR destination address to which Amazon should send traffic.
        Required for IPv4 BGP peers on public virtual interfaces.
        """
        return pulumi.get(self, "customer_address")

    @property
    @pulumi.getter(name="virtualInterfaceId")
    def virtual_interface_id(self) -> pulumi.Output[str]:
        """
        The ID of the Direct Connect virtual interface on which to create the BGP peer.
        """
        return pulumi.get(self, "virtual_interface_id")

