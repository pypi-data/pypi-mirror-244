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

__all__ = ['VpcIpamResourceDiscoveryArgs', 'VpcIpamResourceDiscovery']

@pulumi.input_type
class VpcIpamResourceDiscoveryArgs:
    def __init__(__self__, *,
                 operating_regions: pulumi.Input[Sequence[pulumi.Input['VpcIpamResourceDiscoveryOperatingRegionArgs']]],
                 description: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a VpcIpamResourceDiscovery resource.
        :param pulumi.Input[Sequence[pulumi.Input['VpcIpamResourceDiscoveryOperatingRegionArgs']]] operating_regions: Determines which regions the Resource Discovery will enable IPAM features for usage and monitoring. Locale is the Region where you want to make an IPAM pool available for allocations. You can only create pools with locales that match the operating Regions of the IPAM Resource Discovery. You can only create VPCs from a pool whose locale matches the VPC's Region. You specify a region using the region_name parameter. **You must set your provider block region as an operating_region.**
        :param pulumi.Input[str] description: A description for the IPAM Resource Discovery.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "operating_regions", operating_regions)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="operatingRegions")
    def operating_regions(self) -> pulumi.Input[Sequence[pulumi.Input['VpcIpamResourceDiscoveryOperatingRegionArgs']]]:
        """
        Determines which regions the Resource Discovery will enable IPAM features for usage and monitoring. Locale is the Region where you want to make an IPAM pool available for allocations. You can only create pools with locales that match the operating Regions of the IPAM Resource Discovery. You can only create VPCs from a pool whose locale matches the VPC's Region. You specify a region using the region_name parameter. **You must set your provider block region as an operating_region.**
        """
        return pulumi.get(self, "operating_regions")

    @operating_regions.setter
    def operating_regions(self, value: pulumi.Input[Sequence[pulumi.Input['VpcIpamResourceDiscoveryOperatingRegionArgs']]]):
        pulumi.set(self, "operating_regions", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description for the IPAM Resource Discovery.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _VpcIpamResourceDiscoveryState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ipam_resource_discovery_region: Optional[pulumi.Input[str]] = None,
                 is_default: Optional[pulumi.Input[bool]] = None,
                 operating_regions: Optional[pulumi.Input[Sequence[pulumi.Input['VpcIpamResourceDiscoveryOperatingRegionArgs']]]] = None,
                 owner_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering VpcIpamResourceDiscovery resources.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of IPAM Resource Discovery
        :param pulumi.Input[str] description: A description for the IPAM Resource Discovery.
        :param pulumi.Input[str] ipam_resource_discovery_region: The home region of the Resource Discovery
        :param pulumi.Input[bool] is_default: A boolean to identify if the Resource Discovery is the accounts default resource discovery
        :param pulumi.Input[Sequence[pulumi.Input['VpcIpamResourceDiscoveryOperatingRegionArgs']]] operating_regions: Determines which regions the Resource Discovery will enable IPAM features for usage and monitoring. Locale is the Region where you want to make an IPAM pool available for allocations. You can only create pools with locales that match the operating Regions of the IPAM Resource Discovery. You can only create VPCs from a pool whose locale matches the VPC's Region. You specify a region using the region_name parameter. **You must set your provider block region as an operating_region.**
        :param pulumi.Input[str] owner_id: The account ID for the account that manages the Resource Discovery
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if ipam_resource_discovery_region is not None:
            pulumi.set(__self__, "ipam_resource_discovery_region", ipam_resource_discovery_region)
        if is_default is not None:
            pulumi.set(__self__, "is_default", is_default)
        if operating_regions is not None:
            pulumi.set(__self__, "operating_regions", operating_regions)
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
        Amazon Resource Name (ARN) of IPAM Resource Discovery
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description for the IPAM Resource Discovery.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="ipamResourceDiscoveryRegion")
    def ipam_resource_discovery_region(self) -> Optional[pulumi.Input[str]]:
        """
        The home region of the Resource Discovery
        """
        return pulumi.get(self, "ipam_resource_discovery_region")

    @ipam_resource_discovery_region.setter
    def ipam_resource_discovery_region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ipam_resource_discovery_region", value)

    @property
    @pulumi.getter(name="isDefault")
    def is_default(self) -> Optional[pulumi.Input[bool]]:
        """
        A boolean to identify if the Resource Discovery is the accounts default resource discovery
        """
        return pulumi.get(self, "is_default")

    @is_default.setter
    def is_default(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_default", value)

    @property
    @pulumi.getter(name="operatingRegions")
    def operating_regions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VpcIpamResourceDiscoveryOperatingRegionArgs']]]]:
        """
        Determines which regions the Resource Discovery will enable IPAM features for usage and monitoring. Locale is the Region where you want to make an IPAM pool available for allocations. You can only create pools with locales that match the operating Regions of the IPAM Resource Discovery. You can only create VPCs from a pool whose locale matches the VPC's Region. You specify a region using the region_name parameter. **You must set your provider block region as an operating_region.**
        """
        return pulumi.get(self, "operating_regions")

    @operating_regions.setter
    def operating_regions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VpcIpamResourceDiscoveryOperatingRegionArgs']]]]):
        pulumi.set(self, "operating_regions", value)

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The account ID for the account that manages the Resource Discovery
        """
        return pulumi.get(self, "owner_id")

    @owner_id.setter
    def owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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


class VpcIpamResourceDiscovery(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 operating_regions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VpcIpamResourceDiscoveryOperatingRegionArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides an IPAM Resource Discovery resource. IPAM Resource Discoveries are resources meant for multi-organization customers. If you wish to use a single IPAM across multiple orgs, a resource discovery can be created and shared from a subordinate organization to the management organizations IPAM delegated admin account. For a full deployment example, see `ec2.VpcIpamResourceDiscoveryAssociation` resource.

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_aws as aws

        current = aws.get_region()
        main = aws.ec2.VpcIpamResourceDiscovery("main",
            description="My IPAM Resource Discovery",
            operating_regions=[aws.ec2.VpcIpamResourceDiscoveryOperatingRegionArgs(
                region_name=current.name,
            )],
            tags={
                "Test": "Main",
            })
        ```

        ## Import

        Using `pulumi import`, import IPAMs using the IPAM resource discovery `id`. For example:

        ```sh
         $ pulumi import aws:ec2/vpcIpamResourceDiscovery:VpcIpamResourceDiscovery example ipam-res-disco-0178368ad2146a492
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description for the IPAM Resource Discovery.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VpcIpamResourceDiscoveryOperatingRegionArgs']]]] operating_regions: Determines which regions the Resource Discovery will enable IPAM features for usage and monitoring. Locale is the Region where you want to make an IPAM pool available for allocations. You can only create pools with locales that match the operating Regions of the IPAM Resource Discovery. You can only create VPCs from a pool whose locale matches the VPC's Region. You specify a region using the region_name parameter. **You must set your provider block region as an operating_region.**
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VpcIpamResourceDiscoveryArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an IPAM Resource Discovery resource. IPAM Resource Discoveries are resources meant for multi-organization customers. If you wish to use a single IPAM across multiple orgs, a resource discovery can be created and shared from a subordinate organization to the management organizations IPAM delegated admin account. For a full deployment example, see `ec2.VpcIpamResourceDiscoveryAssociation` resource.

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_aws as aws

        current = aws.get_region()
        main = aws.ec2.VpcIpamResourceDiscovery("main",
            description="My IPAM Resource Discovery",
            operating_regions=[aws.ec2.VpcIpamResourceDiscoveryOperatingRegionArgs(
                region_name=current.name,
            )],
            tags={
                "Test": "Main",
            })
        ```

        ## Import

        Using `pulumi import`, import IPAMs using the IPAM resource discovery `id`. For example:

        ```sh
         $ pulumi import aws:ec2/vpcIpamResourceDiscovery:VpcIpamResourceDiscovery example ipam-res-disco-0178368ad2146a492
        ```

        :param str resource_name: The name of the resource.
        :param VpcIpamResourceDiscoveryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VpcIpamResourceDiscoveryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 operating_regions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VpcIpamResourceDiscoveryOperatingRegionArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VpcIpamResourceDiscoveryArgs.__new__(VpcIpamResourceDiscoveryArgs)

            __props__.__dict__["description"] = description
            if operating_regions is None and not opts.urn:
                raise TypeError("Missing required property 'operating_regions'")
            __props__.__dict__["operating_regions"] = operating_regions
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["ipam_resource_discovery_region"] = None
            __props__.__dict__["is_default"] = None
            __props__.__dict__["owner_id"] = None
            __props__.__dict__["tags_all"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["tagsAll"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(VpcIpamResourceDiscovery, __self__).__init__(
            'aws:ec2/vpcIpamResourceDiscovery:VpcIpamResourceDiscovery',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            ipam_resource_discovery_region: Optional[pulumi.Input[str]] = None,
            is_default: Optional[pulumi.Input[bool]] = None,
            operating_regions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VpcIpamResourceDiscoveryOperatingRegionArgs']]]]] = None,
            owner_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'VpcIpamResourceDiscovery':
        """
        Get an existing VpcIpamResourceDiscovery resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of IPAM Resource Discovery
        :param pulumi.Input[str] description: A description for the IPAM Resource Discovery.
        :param pulumi.Input[str] ipam_resource_discovery_region: The home region of the Resource Discovery
        :param pulumi.Input[bool] is_default: A boolean to identify if the Resource Discovery is the accounts default resource discovery
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VpcIpamResourceDiscoveryOperatingRegionArgs']]]] operating_regions: Determines which regions the Resource Discovery will enable IPAM features for usage and monitoring. Locale is the Region where you want to make an IPAM pool available for allocations. You can only create pools with locales that match the operating Regions of the IPAM Resource Discovery. You can only create VPCs from a pool whose locale matches the VPC's Region. You specify a region using the region_name parameter. **You must set your provider block region as an operating_region.**
        :param pulumi.Input[str] owner_id: The account ID for the account that manages the Resource Discovery
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VpcIpamResourceDiscoveryState.__new__(_VpcIpamResourceDiscoveryState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["description"] = description
        __props__.__dict__["ipam_resource_discovery_region"] = ipam_resource_discovery_region
        __props__.__dict__["is_default"] = is_default
        __props__.__dict__["operating_regions"] = operating_regions
        __props__.__dict__["owner_id"] = owner_id
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return VpcIpamResourceDiscovery(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of IPAM Resource Discovery
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description for the IPAM Resource Discovery.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="ipamResourceDiscoveryRegion")
    def ipam_resource_discovery_region(self) -> pulumi.Output[str]:
        """
        The home region of the Resource Discovery
        """
        return pulumi.get(self, "ipam_resource_discovery_region")

    @property
    @pulumi.getter(name="isDefault")
    def is_default(self) -> pulumi.Output[bool]:
        """
        A boolean to identify if the Resource Discovery is the accounts default resource discovery
        """
        return pulumi.get(self, "is_default")

    @property
    @pulumi.getter(name="operatingRegions")
    def operating_regions(self) -> pulumi.Output[Sequence['outputs.VpcIpamResourceDiscoveryOperatingRegion']]:
        """
        Determines which regions the Resource Discovery will enable IPAM features for usage and monitoring. Locale is the Region where you want to make an IPAM pool available for allocations. You can only create pools with locales that match the operating Regions of the IPAM Resource Discovery. You can only create VPCs from a pool whose locale matches the VPC's Region. You specify a region using the region_name parameter. **You must set your provider block region as an operating_region.**
        """
        return pulumi.get(self, "operating_regions")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        """
        The account ID for the account that manages the Resource Discovery
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

