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

__all__ = ['ReplicatorArgs', 'Replicator']

@pulumi.input_type
class ReplicatorArgs:
    def __init__(__self__, *,
                 kafka_clusters: pulumi.Input[Sequence[pulumi.Input['ReplicatorKafkaClusterArgs']]],
                 replication_info_list: pulumi.Input['ReplicatorReplicationInfoListArgs'],
                 replicator_name: pulumi.Input[str],
                 service_execution_role_arn: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Replicator resource.
        :param pulumi.Input[Sequence[pulumi.Input['ReplicatorKafkaClusterArgs']]] kafka_clusters: A list of Kafka clusters which are targets of the replicator.
        :param pulumi.Input['ReplicatorReplicationInfoListArgs'] replication_info_list: A list of replication configurations, where each configuration targets a given source cluster to target cluster replication flow.
        :param pulumi.Input[str] replicator_name: The name of the replicator.
        :param pulumi.Input[str] service_execution_role_arn: The ARN of the IAM role used by the replicator to access resources in the customer's account (e.g source and target clusters).
        :param pulumi.Input[str] description: A summary description of the replicator.
        """
        pulumi.set(__self__, "kafka_clusters", kafka_clusters)
        pulumi.set(__self__, "replication_info_list", replication_info_list)
        pulumi.set(__self__, "replicator_name", replicator_name)
        pulumi.set(__self__, "service_execution_role_arn", service_execution_role_arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="kafkaClusters")
    def kafka_clusters(self) -> pulumi.Input[Sequence[pulumi.Input['ReplicatorKafkaClusterArgs']]]:
        """
        A list of Kafka clusters which are targets of the replicator.
        """
        return pulumi.get(self, "kafka_clusters")

    @kafka_clusters.setter
    def kafka_clusters(self, value: pulumi.Input[Sequence[pulumi.Input['ReplicatorKafkaClusterArgs']]]):
        pulumi.set(self, "kafka_clusters", value)

    @property
    @pulumi.getter(name="replicationInfoList")
    def replication_info_list(self) -> pulumi.Input['ReplicatorReplicationInfoListArgs']:
        """
        A list of replication configurations, where each configuration targets a given source cluster to target cluster replication flow.
        """
        return pulumi.get(self, "replication_info_list")

    @replication_info_list.setter
    def replication_info_list(self, value: pulumi.Input['ReplicatorReplicationInfoListArgs']):
        pulumi.set(self, "replication_info_list", value)

    @property
    @pulumi.getter(name="replicatorName")
    def replicator_name(self) -> pulumi.Input[str]:
        """
        The name of the replicator.
        """
        return pulumi.get(self, "replicator_name")

    @replicator_name.setter
    def replicator_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "replicator_name", value)

    @property
    @pulumi.getter(name="serviceExecutionRoleArn")
    def service_execution_role_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the IAM role used by the replicator to access resources in the customer's account (e.g source and target clusters).
        """
        return pulumi.get(self, "service_execution_role_arn")

    @service_execution_role_arn.setter
    def service_execution_role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_execution_role_arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A summary description of the replicator.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ReplicatorState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 current_version: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 kafka_clusters: Optional[pulumi.Input[Sequence[pulumi.Input['ReplicatorKafkaClusterArgs']]]] = None,
                 replication_info_list: Optional[pulumi.Input['ReplicatorReplicationInfoListArgs']] = None,
                 replicator_name: Optional[pulumi.Input[str]] = None,
                 service_execution_role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Replicator resources.
        :param pulumi.Input[str] arn: ARN of the Replicator. Do not begin the description with "An", "The", "Defines", "Indicates", or "Specifies," as these are verbose. In other words, "Indicates the amount of storage," can be rewritten as "Amount of storage," without losing any information.
        :param pulumi.Input[str] description: A summary description of the replicator.
        :param pulumi.Input[Sequence[pulumi.Input['ReplicatorKafkaClusterArgs']]] kafka_clusters: A list of Kafka clusters which are targets of the replicator.
        :param pulumi.Input['ReplicatorReplicationInfoListArgs'] replication_info_list: A list of replication configurations, where each configuration targets a given source cluster to target cluster replication flow.
        :param pulumi.Input[str] replicator_name: The name of the replicator.
        :param pulumi.Input[str] service_execution_role_arn: The ARN of the IAM role used by the replicator to access resources in the customer's account (e.g source and target clusters).
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if current_version is not None:
            pulumi.set(__self__, "current_version", current_version)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if kafka_clusters is not None:
            pulumi.set(__self__, "kafka_clusters", kafka_clusters)
        if replication_info_list is not None:
            pulumi.set(__self__, "replication_info_list", replication_info_list)
        if replicator_name is not None:
            pulumi.set(__self__, "replicator_name", replicator_name)
        if service_execution_role_arn is not None:
            pulumi.set(__self__, "service_execution_role_arn", service_execution_role_arn)
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
        ARN of the Replicator. Do not begin the description with "An", "The", "Defines", "Indicates", or "Specifies," as these are verbose. In other words, "Indicates the amount of storage," can be rewritten as "Amount of storage," without losing any information.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="currentVersion")
    def current_version(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "current_version")

    @current_version.setter
    def current_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "current_version", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A summary description of the replicator.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="kafkaClusters")
    def kafka_clusters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ReplicatorKafkaClusterArgs']]]]:
        """
        A list of Kafka clusters which are targets of the replicator.
        """
        return pulumi.get(self, "kafka_clusters")

    @kafka_clusters.setter
    def kafka_clusters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ReplicatorKafkaClusterArgs']]]]):
        pulumi.set(self, "kafka_clusters", value)

    @property
    @pulumi.getter(name="replicationInfoList")
    def replication_info_list(self) -> Optional[pulumi.Input['ReplicatorReplicationInfoListArgs']]:
        """
        A list of replication configurations, where each configuration targets a given source cluster to target cluster replication flow.
        """
        return pulumi.get(self, "replication_info_list")

    @replication_info_list.setter
    def replication_info_list(self, value: Optional[pulumi.Input['ReplicatorReplicationInfoListArgs']]):
        pulumi.set(self, "replication_info_list", value)

    @property
    @pulumi.getter(name="replicatorName")
    def replicator_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the replicator.
        """
        return pulumi.get(self, "replicator_name")

    @replicator_name.setter
    def replicator_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "replicator_name", value)

    @property
    @pulumi.getter(name="serviceExecutionRoleArn")
    def service_execution_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the IAM role used by the replicator to access resources in the customer's account (e.g source and target clusters).
        """
        return pulumi.get(self, "service_execution_role_arn")

    @service_execution_role_arn.setter
    def service_execution_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_execution_role_arn", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
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


class Replicator(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 kafka_clusters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ReplicatorKafkaClusterArgs']]]]] = None,
                 replication_info_list: Optional[pulumi.Input[pulumi.InputType['ReplicatorReplicationInfoListArgs']]] = None,
                 replicator_name: Optional[pulumi.Input[str]] = None,
                 service_execution_role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Resource for managing an AWS Managed Streaming for Kafka Replicator.

        ## Example Usage

        ## Import

        Using `pulumi import`, import MSK replicators using the replicator ARN. For example:

        ```sh
         $ pulumi import aws:msk/replicator:Replicator example arn:aws:kafka:us-west-2:123456789012:configuration/example/279c0212-d057-4dba-9aa9-1c4e5a25bfc7-3
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A summary description of the replicator.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ReplicatorKafkaClusterArgs']]]] kafka_clusters: A list of Kafka clusters which are targets of the replicator.
        :param pulumi.Input[pulumi.InputType['ReplicatorReplicationInfoListArgs']] replication_info_list: A list of replication configurations, where each configuration targets a given source cluster to target cluster replication flow.
        :param pulumi.Input[str] replicator_name: The name of the replicator.
        :param pulumi.Input[str] service_execution_role_arn: The ARN of the IAM role used by the replicator to access resources in the customer's account (e.g source and target clusters).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ReplicatorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS Managed Streaming for Kafka Replicator.

        ## Example Usage

        ## Import

        Using `pulumi import`, import MSK replicators using the replicator ARN. For example:

        ```sh
         $ pulumi import aws:msk/replicator:Replicator example arn:aws:kafka:us-west-2:123456789012:configuration/example/279c0212-d057-4dba-9aa9-1c4e5a25bfc7-3
        ```

        :param str resource_name: The name of the resource.
        :param ReplicatorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ReplicatorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 kafka_clusters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ReplicatorKafkaClusterArgs']]]]] = None,
                 replication_info_list: Optional[pulumi.Input[pulumi.InputType['ReplicatorReplicationInfoListArgs']]] = None,
                 replicator_name: Optional[pulumi.Input[str]] = None,
                 service_execution_role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ReplicatorArgs.__new__(ReplicatorArgs)

            __props__.__dict__["description"] = description
            if kafka_clusters is None and not opts.urn:
                raise TypeError("Missing required property 'kafka_clusters'")
            __props__.__dict__["kafka_clusters"] = kafka_clusters
            if replication_info_list is None and not opts.urn:
                raise TypeError("Missing required property 'replication_info_list'")
            __props__.__dict__["replication_info_list"] = replication_info_list
            if replicator_name is None and not opts.urn:
                raise TypeError("Missing required property 'replicator_name'")
            __props__.__dict__["replicator_name"] = replicator_name
            if service_execution_role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'service_execution_role_arn'")
            __props__.__dict__["service_execution_role_arn"] = service_execution_role_arn
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["current_version"] = None
            __props__.__dict__["tags_all"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["tagsAll"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Replicator, __self__).__init__(
            'aws:msk/replicator:Replicator',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            current_version: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            kafka_clusters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ReplicatorKafkaClusterArgs']]]]] = None,
            replication_info_list: Optional[pulumi.Input[pulumi.InputType['ReplicatorReplicationInfoListArgs']]] = None,
            replicator_name: Optional[pulumi.Input[str]] = None,
            service_execution_role_arn: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Replicator':
        """
        Get an existing Replicator resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the Replicator. Do not begin the description with "An", "The", "Defines", "Indicates", or "Specifies," as these are verbose. In other words, "Indicates the amount of storage," can be rewritten as "Amount of storage," without losing any information.
        :param pulumi.Input[str] description: A summary description of the replicator.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ReplicatorKafkaClusterArgs']]]] kafka_clusters: A list of Kafka clusters which are targets of the replicator.
        :param pulumi.Input[pulumi.InputType['ReplicatorReplicationInfoListArgs']] replication_info_list: A list of replication configurations, where each configuration targets a given source cluster to target cluster replication flow.
        :param pulumi.Input[str] replicator_name: The name of the replicator.
        :param pulumi.Input[str] service_execution_role_arn: The ARN of the IAM role used by the replicator to access resources in the customer's account (e.g source and target clusters).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ReplicatorState.__new__(_ReplicatorState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["current_version"] = current_version
        __props__.__dict__["description"] = description
        __props__.__dict__["kafka_clusters"] = kafka_clusters
        __props__.__dict__["replication_info_list"] = replication_info_list
        __props__.__dict__["replicator_name"] = replicator_name
        __props__.__dict__["service_execution_role_arn"] = service_execution_role_arn
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return Replicator(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the Replicator. Do not begin the description with "An", "The", "Defines", "Indicates", or "Specifies," as these are verbose. In other words, "Indicates the amount of storage," can be rewritten as "Amount of storage," without losing any information.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="currentVersion")
    def current_version(self) -> pulumi.Output[str]:
        return pulumi.get(self, "current_version")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A summary description of the replicator.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="kafkaClusters")
    def kafka_clusters(self) -> pulumi.Output[Sequence['outputs.ReplicatorKafkaCluster']]:
        """
        A list of Kafka clusters which are targets of the replicator.
        """
        return pulumi.get(self, "kafka_clusters")

    @property
    @pulumi.getter(name="replicationInfoList")
    def replication_info_list(self) -> pulumi.Output['outputs.ReplicatorReplicationInfoList']:
        """
        A list of replication configurations, where each configuration targets a given source cluster to target cluster replication flow.
        """
        return pulumi.get(self, "replication_info_list")

    @property
    @pulumi.getter(name="replicatorName")
    def replicator_name(self) -> pulumi.Output[str]:
        """
        The name of the replicator.
        """
        return pulumi.get(self, "replicator_name")

    @property
    @pulumi.getter(name="serviceExecutionRoleArn")
    def service_execution_role_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the IAM role used by the replicator to access resources in the customer's account (e.g source and target clusters).
        """
        return pulumi.get(self, "service_execution_role_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

