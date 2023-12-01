# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ChannelArgs', 'Channel']

@pulumi.input_type
class ChannelArgs:
    def __init__(__self__, *,
                 authorized: Optional[pulumi.Input[bool]] = None,
                 latency_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recording_configuration_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Channel resource.
        :param pulumi.Input[bool] authorized: If `true`, channel is private (enabled for playback authorization).
        :param pulumi.Input[str] latency_mode: Channel latency mode. Valid values: `NORMAL`, `LOW`.
        :param pulumi.Input[str] name: Channel name.
        :param pulumi.Input[str] recording_configuration_arn: Recording configuration ARN.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] type: Channel type, which determines the allowable resolution and bitrate. Valid values: `STANDARD`, `BASIC`.
        """
        if authorized is not None:
            pulumi.set(__self__, "authorized", authorized)
        if latency_mode is not None:
            pulumi.set(__self__, "latency_mode", latency_mode)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if recording_configuration_arn is not None:
            pulumi.set(__self__, "recording_configuration_arn", recording_configuration_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def authorized(self) -> Optional[pulumi.Input[bool]]:
        """
        If `true`, channel is private (enabled for playback authorization).
        """
        return pulumi.get(self, "authorized")

    @authorized.setter
    def authorized(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "authorized", value)

    @property
    @pulumi.getter(name="latencyMode")
    def latency_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Channel latency mode. Valid values: `NORMAL`, `LOW`.
        """
        return pulumi.get(self, "latency_mode")

    @latency_mode.setter
    def latency_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "latency_mode", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Channel name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="recordingConfigurationArn")
    def recording_configuration_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Recording configuration ARN.
        """
        return pulumi.get(self, "recording_configuration_arn")

    @recording_configuration_arn.setter
    def recording_configuration_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "recording_configuration_arn", value)

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
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Channel type, which determines the allowable resolution and bitrate. Valid values: `STANDARD`, `BASIC`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class _ChannelState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 authorized: Optional[pulumi.Input[bool]] = None,
                 ingest_endpoint: Optional[pulumi.Input[str]] = None,
                 latency_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 playback_url: Optional[pulumi.Input[str]] = None,
                 recording_configuration_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Channel resources.
        :param pulumi.Input[str] arn: ARN of the Channel.
        :param pulumi.Input[bool] authorized: If `true`, channel is private (enabled for playback authorization).
        :param pulumi.Input[str] ingest_endpoint: Channel ingest endpoint, part of the definition of an ingest server, used when setting up streaming software.
        :param pulumi.Input[str] latency_mode: Channel latency mode. Valid values: `NORMAL`, `LOW`.
        :param pulumi.Input[str] name: Channel name.
        :param pulumi.Input[str] playback_url: Channel playback URL.
        :param pulumi.Input[str] recording_configuration_arn: Recording configuration ARN.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] type: Channel type, which determines the allowable resolution and bitrate. Valid values: `STANDARD`, `BASIC`.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if authorized is not None:
            pulumi.set(__self__, "authorized", authorized)
        if ingest_endpoint is not None:
            pulumi.set(__self__, "ingest_endpoint", ingest_endpoint)
        if latency_mode is not None:
            pulumi.set(__self__, "latency_mode", latency_mode)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if playback_url is not None:
            pulumi.set(__self__, "playback_url", playback_url)
        if recording_configuration_arn is not None:
            pulumi.set(__self__, "recording_configuration_arn", recording_configuration_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the Channel.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def authorized(self) -> Optional[pulumi.Input[bool]]:
        """
        If `true`, channel is private (enabled for playback authorization).
        """
        return pulumi.get(self, "authorized")

    @authorized.setter
    def authorized(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "authorized", value)

    @property
    @pulumi.getter(name="ingestEndpoint")
    def ingest_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        Channel ingest endpoint, part of the definition of an ingest server, used when setting up streaming software.
        """
        return pulumi.get(self, "ingest_endpoint")

    @ingest_endpoint.setter
    def ingest_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ingest_endpoint", value)

    @property
    @pulumi.getter(name="latencyMode")
    def latency_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Channel latency mode. Valid values: `NORMAL`, `LOW`.
        """
        return pulumi.get(self, "latency_mode")

    @latency_mode.setter
    def latency_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "latency_mode", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Channel name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="playbackUrl")
    def playback_url(self) -> Optional[pulumi.Input[str]]:
        """
        Channel playback URL.
        """
        return pulumi.get(self, "playback_url")

    @playback_url.setter
    def playback_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "playback_url", value)

    @property
    @pulumi.getter(name="recordingConfigurationArn")
    def recording_configuration_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Recording configuration ARN.
        """
        return pulumi.get(self, "recording_configuration_arn")

    @recording_configuration_arn.setter
    def recording_configuration_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "recording_configuration_arn", value)

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
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Channel type, which determines the allowable resolution and bitrate. Valid values: `STANDARD`, `BASIC`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class Channel(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorized: Optional[pulumi.Input[bool]] = None,
                 latency_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recording_configuration_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS IVS (Interactive Video) Channel.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ivs.Channel("example")
        ```

        ## Import

        Using `pulumi import`, import IVS (Interactive Video) Channel using the ARN. For example:

        ```sh
         $ pulumi import aws:ivs/channel:Channel example arn:aws:ivs:us-west-2:326937407773:channel/0Y1lcs4U7jk5
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] authorized: If `true`, channel is private (enabled for playback authorization).
        :param pulumi.Input[str] latency_mode: Channel latency mode. Valid values: `NORMAL`, `LOW`.
        :param pulumi.Input[str] name: Channel name.
        :param pulumi.Input[str] recording_configuration_arn: Recording configuration ARN.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] type: Channel type, which determines the allowable resolution and bitrate. Valid values: `STANDARD`, `BASIC`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ChannelArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS IVS (Interactive Video) Channel.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ivs.Channel("example")
        ```

        ## Import

        Using `pulumi import`, import IVS (Interactive Video) Channel using the ARN. For example:

        ```sh
         $ pulumi import aws:ivs/channel:Channel example arn:aws:ivs:us-west-2:326937407773:channel/0Y1lcs4U7jk5
        ```

        :param str resource_name: The name of the resource.
        :param ChannelArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ChannelArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorized: Optional[pulumi.Input[bool]] = None,
                 latency_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recording_configuration_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ChannelArgs.__new__(ChannelArgs)

            __props__.__dict__["authorized"] = authorized
            __props__.__dict__["latency_mode"] = latency_mode
            __props__.__dict__["name"] = name
            __props__.__dict__["recording_configuration_arn"] = recording_configuration_arn
            __props__.__dict__["tags"] = tags
            __props__.__dict__["type"] = type
            __props__.__dict__["arn"] = None
            __props__.__dict__["ingest_endpoint"] = None
            __props__.__dict__["playback_url"] = None
            __props__.__dict__["tags_all"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["tagsAll"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Channel, __self__).__init__(
            'aws:ivs/channel:Channel',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            authorized: Optional[pulumi.Input[bool]] = None,
            ingest_endpoint: Optional[pulumi.Input[str]] = None,
            latency_mode: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            playback_url: Optional[pulumi.Input[str]] = None,
            recording_configuration_arn: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'Channel':
        """
        Get an existing Channel resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the Channel.
        :param pulumi.Input[bool] authorized: If `true`, channel is private (enabled for playback authorization).
        :param pulumi.Input[str] ingest_endpoint: Channel ingest endpoint, part of the definition of an ingest server, used when setting up streaming software.
        :param pulumi.Input[str] latency_mode: Channel latency mode. Valid values: `NORMAL`, `LOW`.
        :param pulumi.Input[str] name: Channel name.
        :param pulumi.Input[str] playback_url: Channel playback URL.
        :param pulumi.Input[str] recording_configuration_arn: Recording configuration ARN.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] type: Channel type, which determines the allowable resolution and bitrate. Valid values: `STANDARD`, `BASIC`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ChannelState.__new__(_ChannelState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["authorized"] = authorized
        __props__.__dict__["ingest_endpoint"] = ingest_endpoint
        __props__.__dict__["latency_mode"] = latency_mode
        __props__.__dict__["name"] = name
        __props__.__dict__["playback_url"] = playback_url
        __props__.__dict__["recording_configuration_arn"] = recording_configuration_arn
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["type"] = type
        return Channel(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the Channel.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def authorized(self) -> pulumi.Output[bool]:
        """
        If `true`, channel is private (enabled for playback authorization).
        """
        return pulumi.get(self, "authorized")

    @property
    @pulumi.getter(name="ingestEndpoint")
    def ingest_endpoint(self) -> pulumi.Output[str]:
        """
        Channel ingest endpoint, part of the definition of an ingest server, used when setting up streaming software.
        """
        return pulumi.get(self, "ingest_endpoint")

    @property
    @pulumi.getter(name="latencyMode")
    def latency_mode(self) -> pulumi.Output[str]:
        """
        Channel latency mode. Valid values: `NORMAL`, `LOW`.
        """
        return pulumi.get(self, "latency_mode")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Channel name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="playbackUrl")
    def playback_url(self) -> pulumi.Output[str]:
        """
        Channel playback URL.
        """
        return pulumi.get(self, "playback_url")

    @property
    @pulumi.getter(name="recordingConfigurationArn")
    def recording_configuration_arn(self) -> pulumi.Output[str]:
        """
        Recording configuration ARN.
        """
        return pulumi.get(self, "recording_configuration_arn")

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
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Channel type, which determines the allowable resolution and bitrate. Valid values: `STANDARD`, `BASIC`.
        """
        return pulumi.get(self, "type")

