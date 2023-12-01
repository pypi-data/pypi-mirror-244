# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetServiceResult',
    'AwaitableGetServiceResult',
    'get_service',
    'get_service_output',
]

@pulumi.output_type
class GetServiceResult:
    """
    A collection of values returned by getService.
    """
    def __init__(__self__, arn=None, cluster_arn=None, desired_count=None, id=None, launch_type=None, scheduling_strategy=None, service_name=None, tags=None, task_definition=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if cluster_arn and not isinstance(cluster_arn, str):
            raise TypeError("Expected argument 'cluster_arn' to be a str")
        pulumi.set(__self__, "cluster_arn", cluster_arn)
        if desired_count and not isinstance(desired_count, int):
            raise TypeError("Expected argument 'desired_count' to be a int")
        pulumi.set(__self__, "desired_count", desired_count)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if launch_type and not isinstance(launch_type, str):
            raise TypeError("Expected argument 'launch_type' to be a str")
        pulumi.set(__self__, "launch_type", launch_type)
        if scheduling_strategy and not isinstance(scheduling_strategy, str):
            raise TypeError("Expected argument 'scheduling_strategy' to be a str")
        pulumi.set(__self__, "scheduling_strategy", scheduling_strategy)
        if service_name and not isinstance(service_name, str):
            raise TypeError("Expected argument 'service_name' to be a str")
        pulumi.set(__self__, "service_name", service_name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if task_definition and not isinstance(task_definition, str):
            raise TypeError("Expected argument 'task_definition' to be a str")
        pulumi.set(__self__, "task_definition", task_definition)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the ECS Service
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="clusterArn")
    def cluster_arn(self) -> str:
        return pulumi.get(self, "cluster_arn")

    @property
    @pulumi.getter(name="desiredCount")
    def desired_count(self) -> int:
        """
        Number of tasks for the ECS Service
        """
        return pulumi.get(self, "desired_count")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="launchType")
    def launch_type(self) -> str:
        """
        Launch type for the ECS Service
        """
        return pulumi.get(self, "launch_type")

    @property
    @pulumi.getter(name="schedulingStrategy")
    def scheduling_strategy(self) -> str:
        """
        Scheduling strategy for the ECS Service
        """
        return pulumi.get(self, "scheduling_strategy")

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> str:
        return pulumi.get(self, "service_name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="taskDefinition")
    def task_definition(self) -> str:
        """
        Family for the latest ACTIVE revision or full ARN of the task definition.
        """
        return pulumi.get(self, "task_definition")


class AwaitableGetServiceResult(GetServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceResult(
            arn=self.arn,
            cluster_arn=self.cluster_arn,
            desired_count=self.desired_count,
            id=self.id,
            launch_type=self.launch_type,
            scheduling_strategy=self.scheduling_strategy,
            service_name=self.service_name,
            tags=self.tags,
            task_definition=self.task_definition)


def get_service(cluster_arn: Optional[str] = None,
                service_name: Optional[str] = None,
                tags: Optional[Mapping[str, str]] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceResult:
    """
    The ECS Service data source allows access to details of a specific
    Service within a AWS ECS Cluster.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ecs.get_service(service_name="example",
        cluster_arn=data["aws_ecs_cluster"]["example"]["arn"])
    ```


    :param str cluster_arn: ARN of the ECS Cluster
    :param str service_name: Name of the ECS Service
    :param Mapping[str, str] tags: Resource tags.
    """
    __args__ = dict()
    __args__['clusterArn'] = cluster_arn
    __args__['serviceName'] = service_name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ecs/getService:getService', __args__, opts=opts, typ=GetServiceResult).value

    return AwaitableGetServiceResult(
        arn=pulumi.get(__ret__, 'arn'),
        cluster_arn=pulumi.get(__ret__, 'cluster_arn'),
        desired_count=pulumi.get(__ret__, 'desired_count'),
        id=pulumi.get(__ret__, 'id'),
        launch_type=pulumi.get(__ret__, 'launch_type'),
        scheduling_strategy=pulumi.get(__ret__, 'scheduling_strategy'),
        service_name=pulumi.get(__ret__, 'service_name'),
        tags=pulumi.get(__ret__, 'tags'),
        task_definition=pulumi.get(__ret__, 'task_definition'))


@_utilities.lift_output_func(get_service)
def get_service_output(cluster_arn: Optional[pulumi.Input[str]] = None,
                       service_name: Optional[pulumi.Input[str]] = None,
                       tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServiceResult]:
    """
    The ECS Service data source allows access to details of a specific
    Service within a AWS ECS Cluster.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ecs.get_service(service_name="example",
        cluster_arn=data["aws_ecs_cluster"]["example"]["arn"])
    ```


    :param str cluster_arn: ARN of the ECS Cluster
    :param str service_name: Name of the ECS Service
    :param Mapping[str, str] tags: Resource tags.
    """
    ...
