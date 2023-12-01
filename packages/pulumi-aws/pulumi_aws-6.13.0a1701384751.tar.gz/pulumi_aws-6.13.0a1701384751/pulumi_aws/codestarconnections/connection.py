# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ConnectionArgs', 'Connection']

@pulumi.input_type
class ConnectionArgs:
    def __init__(__self__, *,
                 host_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 provider_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Connection resource.
        :param pulumi.Input[str] host_arn: The Amazon Resource Name (ARN) of the host associated with the connection. Conflicts with `provider_type`
        :param pulumi.Input[str] name: The name of the connection to be created. The name must be unique in the calling AWS account. Changing `name` will create a new resource.
        :param pulumi.Input[str] provider_type: The name of the external provider where your third-party code repository is configured. Valid values are `Bitbucket`, `GitHub` or `GitHubEnterpriseServer`. Changing `provider_type` will create a new resource. Conflicts with `host_arn`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of key-value resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        if host_arn is not None:
            pulumi.set(__self__, "host_arn", host_arn)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if provider_type is not None:
            pulumi.set(__self__, "provider_type", provider_type)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="hostArn")
    def host_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the host associated with the connection. Conflicts with `provider_type`
        """
        return pulumi.get(self, "host_arn")

    @host_arn.setter
    def host_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_arn", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the connection to be created. The name must be unique in the calling AWS account. Changing `name` will create a new resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="providerType")
    def provider_type(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the external provider where your third-party code repository is configured. Valid values are `Bitbucket`, `GitHub` or `GitHubEnterpriseServer`. Changing `provider_type` will create a new resource. Conflicts with `host_arn`
        """
        return pulumi.get(self, "provider_type")

    @provider_type.setter
    def provider_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provider_type", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of key-value resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ConnectionState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 connection_status: Optional[pulumi.Input[str]] = None,
                 host_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 provider_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Connection resources.
        :param pulumi.Input[str] arn: The codestar connection ARN.
        :param pulumi.Input[str] connection_status: The codestar connection status. Possible values are `PENDING`, `AVAILABLE` and `ERROR`.
        :param pulumi.Input[str] host_arn: The Amazon Resource Name (ARN) of the host associated with the connection. Conflicts with `provider_type`
        :param pulumi.Input[str] name: The name of the connection to be created. The name must be unique in the calling AWS account. Changing `name` will create a new resource.
        :param pulumi.Input[str] provider_type: The name of the external provider where your third-party code repository is configured. Valid values are `Bitbucket`, `GitHub` or `GitHubEnterpriseServer`. Changing `provider_type` will create a new resource. Conflicts with `host_arn`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of key-value resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if connection_status is not None:
            pulumi.set(__self__, "connection_status", connection_status)
        if host_arn is not None:
            pulumi.set(__self__, "host_arn", host_arn)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if provider_type is not None:
            pulumi.set(__self__, "provider_type", provider_type)
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
        The codestar connection ARN.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="connectionStatus")
    def connection_status(self) -> Optional[pulumi.Input[str]]:
        """
        The codestar connection status. Possible values are `PENDING`, `AVAILABLE` and `ERROR`.
        """
        return pulumi.get(self, "connection_status")

    @connection_status.setter
    def connection_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_status", value)

    @property
    @pulumi.getter(name="hostArn")
    def host_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the host associated with the connection. Conflicts with `provider_type`
        """
        return pulumi.get(self, "host_arn")

    @host_arn.setter
    def host_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_arn", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the connection to be created. The name must be unique in the calling AWS account. Changing `name` will create a new resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="providerType")
    def provider_type(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the external provider where your third-party code repository is configured. Valid values are `Bitbucket`, `GitHub` or `GitHubEnterpriseServer`. Changing `provider_type` will create a new resource. Conflicts with `host_arn`
        """
        return pulumi.get(self, "provider_type")

    @provider_type.setter
    def provider_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provider_type", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of key-value resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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


class Connection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 host_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 provider_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a CodeStar Connection.

        > **NOTE:** The `codestarconnections.Connection` resource is created in the state `PENDING`. Authentication with the connection provider must be completed in the AWS Console. See the [AWS documentation](https://docs.aws.amazon.com/dtconsole/latest/userguide/connections-update.html) for details.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_connection = aws.codestarconnections.Connection("exampleConnection", provider_type="Bitbucket")
        example_pipeline = aws.codepipeline.Pipeline("examplePipeline",
            role_arn=aws_iam_role["codepipeline_role"]["arn"],
            artifact_stores=[aws.codepipeline.PipelineArtifactStoreArgs()],
            stages=[
                aws.codepipeline.PipelineStageArgs(
                    name="Source",
                    actions=[aws.codepipeline.PipelineStageActionArgs(
                        name="Source",
                        category="Source",
                        owner="AWS",
                        provider="CodeStarSourceConnection",
                        version="1",
                        output_artifacts=["source_output"],
                        configuration={
                            "ConnectionArn": example_connection.arn,
                            "FullRepositoryId": "my-organization/test",
                            "BranchName": "main",
                        },
                    )],
                ),
                aws.codepipeline.PipelineStageArgs(
                    name="Build",
                    actions=[aws.codepipeline.PipelineStageActionArgs()],
                ),
                aws.codepipeline.PipelineStageArgs(
                    name="Deploy",
                    actions=[aws.codepipeline.PipelineStageActionArgs()],
                ),
            ])
        ```

        ## Import

        Using `pulumi import`, import CodeStar connections using the ARN. For example:

        ```sh
         $ pulumi import aws:codestarconnections/connection:Connection test-connection arn:aws:codestar-connections:us-west-1:0123456789:connection/79d4d357-a2ee-41e4-b350-2fe39ae59448
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] host_arn: The Amazon Resource Name (ARN) of the host associated with the connection. Conflicts with `provider_type`
        :param pulumi.Input[str] name: The name of the connection to be created. The name must be unique in the calling AWS account. Changing `name` will create a new resource.
        :param pulumi.Input[str] provider_type: The name of the external provider where your third-party code repository is configured. Valid values are `Bitbucket`, `GitHub` or `GitHubEnterpriseServer`. Changing `provider_type` will create a new resource. Conflicts with `host_arn`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of key-value resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ConnectionArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a CodeStar Connection.

        > **NOTE:** The `codestarconnections.Connection` resource is created in the state `PENDING`. Authentication with the connection provider must be completed in the AWS Console. See the [AWS documentation](https://docs.aws.amazon.com/dtconsole/latest/userguide/connections-update.html) for details.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_connection = aws.codestarconnections.Connection("exampleConnection", provider_type="Bitbucket")
        example_pipeline = aws.codepipeline.Pipeline("examplePipeline",
            role_arn=aws_iam_role["codepipeline_role"]["arn"],
            artifact_stores=[aws.codepipeline.PipelineArtifactStoreArgs()],
            stages=[
                aws.codepipeline.PipelineStageArgs(
                    name="Source",
                    actions=[aws.codepipeline.PipelineStageActionArgs(
                        name="Source",
                        category="Source",
                        owner="AWS",
                        provider="CodeStarSourceConnection",
                        version="1",
                        output_artifacts=["source_output"],
                        configuration={
                            "ConnectionArn": example_connection.arn,
                            "FullRepositoryId": "my-organization/test",
                            "BranchName": "main",
                        },
                    )],
                ),
                aws.codepipeline.PipelineStageArgs(
                    name="Build",
                    actions=[aws.codepipeline.PipelineStageActionArgs()],
                ),
                aws.codepipeline.PipelineStageArgs(
                    name="Deploy",
                    actions=[aws.codepipeline.PipelineStageActionArgs()],
                ),
            ])
        ```

        ## Import

        Using `pulumi import`, import CodeStar connections using the ARN. For example:

        ```sh
         $ pulumi import aws:codestarconnections/connection:Connection test-connection arn:aws:codestar-connections:us-west-1:0123456789:connection/79d4d357-a2ee-41e4-b350-2fe39ae59448
        ```

        :param str resource_name: The name of the resource.
        :param ConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 host_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 provider_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConnectionArgs.__new__(ConnectionArgs)

            __props__.__dict__["host_arn"] = host_arn
            __props__.__dict__["name"] = name
            __props__.__dict__["provider_type"] = provider_type
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["connection_status"] = None
            __props__.__dict__["tags_all"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["tagsAll"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Connection, __self__).__init__(
            'aws:codestarconnections/connection:Connection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            connection_status: Optional[pulumi.Input[str]] = None,
            host_arn: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            provider_type: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Connection':
        """
        Get an existing Connection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The codestar connection ARN.
        :param pulumi.Input[str] connection_status: The codestar connection status. Possible values are `PENDING`, `AVAILABLE` and `ERROR`.
        :param pulumi.Input[str] host_arn: The Amazon Resource Name (ARN) of the host associated with the connection. Conflicts with `provider_type`
        :param pulumi.Input[str] name: The name of the connection to be created. The name must be unique in the calling AWS account. Changing `name` will create a new resource.
        :param pulumi.Input[str] provider_type: The name of the external provider where your third-party code repository is configured. Valid values are `Bitbucket`, `GitHub` or `GitHubEnterpriseServer`. Changing `provider_type` will create a new resource. Conflicts with `host_arn`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of key-value resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ConnectionState.__new__(_ConnectionState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["connection_status"] = connection_status
        __props__.__dict__["host_arn"] = host_arn
        __props__.__dict__["name"] = name
        __props__.__dict__["provider_type"] = provider_type
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return Connection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The codestar connection ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="connectionStatus")
    def connection_status(self) -> pulumi.Output[str]:
        """
        The codestar connection status. Possible values are `PENDING`, `AVAILABLE` and `ERROR`.
        """
        return pulumi.get(self, "connection_status")

    @property
    @pulumi.getter(name="hostArn")
    def host_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the host associated with the connection. Conflicts with `provider_type`
        """
        return pulumi.get(self, "host_arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the connection to be created. The name must be unique in the calling AWS account. Changing `name` will create a new resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="providerType")
    def provider_type(self) -> pulumi.Output[str]:
        """
        The name of the external provider where your third-party code repository is configured. Valid values are `Bitbucket`, `GitHub` or `GitHubEnterpriseServer`. Changing `provider_type` will create a new resource. Conflicts with `host_arn`
        """
        return pulumi.get(self, "provider_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Map of key-value resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

