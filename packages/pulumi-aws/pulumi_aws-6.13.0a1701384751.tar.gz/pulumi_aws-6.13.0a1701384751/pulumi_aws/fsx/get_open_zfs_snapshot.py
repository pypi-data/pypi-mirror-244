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

__all__ = [
    'GetOpenZfsSnapshotResult',
    'AwaitableGetOpenZfsSnapshotResult',
    'get_open_zfs_snapshot',
    'get_open_zfs_snapshot_output',
]

@pulumi.output_type
class GetOpenZfsSnapshotResult:
    """
    A collection of values returned by getOpenZfsSnapshot.
    """
    def __init__(__self__, arn=None, creation_time=None, filters=None, id=None, most_recent=None, name=None, snapshot_id=None, snapshot_ids=None, tags=None, volume_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        pulumi.set(__self__, "most_recent", most_recent)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if snapshot_id and not isinstance(snapshot_id, str):
            raise TypeError("Expected argument 'snapshot_id' to be a str")
        pulumi.set(__self__, "snapshot_id", snapshot_id)
        if snapshot_ids and not isinstance(snapshot_ids, list):
            raise TypeError("Expected argument 'snapshot_ids' to be a list")
        pulumi.set(__self__, "snapshot_ids", snapshot_ids)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if volume_id and not isinstance(volume_id, str):
            raise TypeError("Expected argument 'volume_id' to be a str")
        pulumi.set(__self__, "volume_id", volume_id)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        Amazon Resource Name of the snapshot.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> str:
        """
        Time that the resource was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetOpenZfsSnapshotFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="mostRecent")
    def most_recent(self) -> Optional[bool]:
        return pulumi.get(self, "most_recent")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the snapshot.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="snapshotId")
    def snapshot_id(self) -> str:
        """
        ID of the snapshot.
        """
        return pulumi.get(self, "snapshot_id")

    @property
    @pulumi.getter(name="snapshotIds")
    def snapshot_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "snapshot_ids")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        List of Tag values, with a maximum of 50 elements.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> str:
        """
        ID of the volume that the snapshot is of.
        """
        return pulumi.get(self, "volume_id")


class AwaitableGetOpenZfsSnapshotResult(GetOpenZfsSnapshotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOpenZfsSnapshotResult(
            arn=self.arn,
            creation_time=self.creation_time,
            filters=self.filters,
            id=self.id,
            most_recent=self.most_recent,
            name=self.name,
            snapshot_id=self.snapshot_id,
            snapshot_ids=self.snapshot_ids,
            tags=self.tags,
            volume_id=self.volume_id)


def get_open_zfs_snapshot(filters: Optional[Sequence[pulumi.InputType['GetOpenZfsSnapshotFilterArgs']]] = None,
                          most_recent: Optional[bool] = None,
                          name: Optional[str] = None,
                          snapshot_ids: Optional[Sequence[str]] = None,
                          tags: Optional[Mapping[str, str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOpenZfsSnapshotResult:
    """
    Use this data source to get information about an Amazon FSx for OpenZFS Snapshot for use when provisioning new Volumes.

    ## Example Usage
    ### Root volume Example

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.fsx.get_open_zfs_snapshot(filters=[aws.fsx.GetOpenZfsSnapshotFilterArgs(
            name="volume-id",
            values=["fsvol-073a32b6098a73feb"],
        )],
        most_recent=True)
    ```


    :param Sequence[pulumi.InputType['GetOpenZfsSnapshotFilterArgs']] filters: One or more name/value pairs to filter off of. The
           supported names are file-system-id or volume-id.
    :param bool most_recent: If more than one result is returned, use the most recent snapshot.
    :param str name: Name of the snapshot.
    :param Sequence[str] snapshot_ids: Returns information on a specific snapshot_id.
    :param Mapping[str, str] tags: List of Tag values, with a maximum of 50 elements.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['mostRecent'] = most_recent
    __args__['name'] = name
    __args__['snapshotIds'] = snapshot_ids
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:fsx/getOpenZfsSnapshot:getOpenZfsSnapshot', __args__, opts=opts, typ=GetOpenZfsSnapshotResult).value

    return AwaitableGetOpenZfsSnapshotResult(
        arn=pulumi.get(__ret__, 'arn'),
        creation_time=pulumi.get(__ret__, 'creation_time'),
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        most_recent=pulumi.get(__ret__, 'most_recent'),
        name=pulumi.get(__ret__, 'name'),
        snapshot_id=pulumi.get(__ret__, 'snapshot_id'),
        snapshot_ids=pulumi.get(__ret__, 'snapshot_ids'),
        tags=pulumi.get(__ret__, 'tags'),
        volume_id=pulumi.get(__ret__, 'volume_id'))


@_utilities.lift_output_func(get_open_zfs_snapshot)
def get_open_zfs_snapshot_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetOpenZfsSnapshotFilterArgs']]]]] = None,
                                 most_recent: Optional[pulumi.Input[Optional[bool]]] = None,
                                 name: Optional[pulumi.Input[Optional[str]]] = None,
                                 snapshot_ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                 tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOpenZfsSnapshotResult]:
    """
    Use this data source to get information about an Amazon FSx for OpenZFS Snapshot for use when provisioning new Volumes.

    ## Example Usage
    ### Root volume Example

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.fsx.get_open_zfs_snapshot(filters=[aws.fsx.GetOpenZfsSnapshotFilterArgs(
            name="volume-id",
            values=["fsvol-073a32b6098a73feb"],
        )],
        most_recent=True)
    ```


    :param Sequence[pulumi.InputType['GetOpenZfsSnapshotFilterArgs']] filters: One or more name/value pairs to filter off of. The
           supported names are file-system-id or volume-id.
    :param bool most_recent: If more than one result is returned, use the most recent snapshot.
    :param str name: Name of the snapshot.
    :param Sequence[str] snapshot_ids: Returns information on a specific snapshot_id.
    :param Mapping[str, str] tags: List of Tag values, with a maximum of 50 elements.
    """
    ...
