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
    'GetWorkspaceResult',
    'AwaitableGetWorkspaceResult',
    'get_workspace',
    'get_workspace_output',
]

@pulumi.output_type
class GetWorkspaceResult:
    """
    A collection of values returned by getWorkspace.
    """
    def __init__(__self__, alias=None, arn=None, created_date=None, id=None, prometheus_endpoint=None, status=None, tags=None, workspace_id=None):
        if alias and not isinstance(alias, str):
            raise TypeError("Expected argument 'alias' to be a str")
        pulumi.set(__self__, "alias", alias)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if created_date and not isinstance(created_date, str):
            raise TypeError("Expected argument 'created_date' to be a str")
        pulumi.set(__self__, "created_date", created_date)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if prometheus_endpoint and not isinstance(prometheus_endpoint, str):
            raise TypeError("Expected argument 'prometheus_endpoint' to be a str")
        pulumi.set(__self__, "prometheus_endpoint", prometheus_endpoint)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if workspace_id and not isinstance(workspace_id, str):
            raise TypeError("Expected argument 'workspace_id' to be a str")
        pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter
    def alias(self) -> str:
        """
        Prometheus workspace alias.
        """
        return pulumi.get(self, "alias")

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the Prometheus workspace.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> str:
        """
        Creation date of the Prometheus workspace.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="prometheusEndpoint")
    def prometheus_endpoint(self) -> str:
        """
        Endpoint of the Prometheus workspace.
        """
        return pulumi.get(self, "prometheus_endpoint")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the Prometheus workspace.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Tags assigned to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> str:
        return pulumi.get(self, "workspace_id")


class AwaitableGetWorkspaceResult(GetWorkspaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkspaceResult(
            alias=self.alias,
            arn=self.arn,
            created_date=self.created_date,
            id=self.id,
            prometheus_endpoint=self.prometheus_endpoint,
            status=self.status,
            tags=self.tags,
            workspace_id=self.workspace_id)


def get_workspace(tags: Optional[Mapping[str, str]] = None,
                  workspace_id: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkspaceResult:
    """
    Provides an Amazon Managed Prometheus workspace data source.

    ## Example Usage
    ### Basic configuration

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.amp.get_workspace(workspace_id="ws-41det8a1-2c67-6a1a-9381-9b83d3d78ef7")
    ```


    :param Mapping[str, str] tags: Tags assigned to the resource.
    :param str workspace_id: Prometheus workspace ID.
    """
    __args__ = dict()
    __args__['tags'] = tags
    __args__['workspaceId'] = workspace_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:amp/getWorkspace:getWorkspace', __args__, opts=opts, typ=GetWorkspaceResult).value

    return AwaitableGetWorkspaceResult(
        alias=pulumi.get(__ret__, 'alias'),
        arn=pulumi.get(__ret__, 'arn'),
        created_date=pulumi.get(__ret__, 'created_date'),
        id=pulumi.get(__ret__, 'id'),
        prometheus_endpoint=pulumi.get(__ret__, 'prometheus_endpoint'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'),
        workspace_id=pulumi.get(__ret__, 'workspace_id'))


@_utilities.lift_output_func(get_workspace)
def get_workspace_output(tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                         workspace_id: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWorkspaceResult]:
    """
    Provides an Amazon Managed Prometheus workspace data source.

    ## Example Usage
    ### Basic configuration

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.amp.get_workspace(workspace_id="ws-41det8a1-2c67-6a1a-9381-9b83d3d78ef7")
    ```


    :param Mapping[str, str] tags: Tags assigned to the resource.
    :param str workspace_id: Prometheus workspace ID.
    """
    ...
