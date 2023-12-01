# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SnapshotScheduleAssociationArgs', 'SnapshotScheduleAssociation']

@pulumi.input_type
class SnapshotScheduleAssociationArgs:
    def __init__(__self__, *,
                 cluster_identifier: pulumi.Input[str],
                 schedule_identifier: pulumi.Input[str]):
        """
        The set of arguments for constructing a SnapshotScheduleAssociation resource.
        :param pulumi.Input[str] cluster_identifier: The cluster identifier.
        :param pulumi.Input[str] schedule_identifier: The snapshot schedule identifier.
        """
        pulumi.set(__self__, "cluster_identifier", cluster_identifier)
        pulumi.set(__self__, "schedule_identifier", schedule_identifier)

    @property
    @pulumi.getter(name="clusterIdentifier")
    def cluster_identifier(self) -> pulumi.Input[str]:
        """
        The cluster identifier.
        """
        return pulumi.get(self, "cluster_identifier")

    @cluster_identifier.setter
    def cluster_identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_identifier", value)

    @property
    @pulumi.getter(name="scheduleIdentifier")
    def schedule_identifier(self) -> pulumi.Input[str]:
        """
        The snapshot schedule identifier.
        """
        return pulumi.get(self, "schedule_identifier")

    @schedule_identifier.setter
    def schedule_identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "schedule_identifier", value)


@pulumi.input_type
class _SnapshotScheduleAssociationState:
    def __init__(__self__, *,
                 cluster_identifier: Optional[pulumi.Input[str]] = None,
                 schedule_identifier: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SnapshotScheduleAssociation resources.
        :param pulumi.Input[str] cluster_identifier: The cluster identifier.
        :param pulumi.Input[str] schedule_identifier: The snapshot schedule identifier.
        """
        if cluster_identifier is not None:
            pulumi.set(__self__, "cluster_identifier", cluster_identifier)
        if schedule_identifier is not None:
            pulumi.set(__self__, "schedule_identifier", schedule_identifier)

    @property
    @pulumi.getter(name="clusterIdentifier")
    def cluster_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The cluster identifier.
        """
        return pulumi.get(self, "cluster_identifier")

    @cluster_identifier.setter
    def cluster_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_identifier", value)

    @property
    @pulumi.getter(name="scheduleIdentifier")
    def schedule_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The snapshot schedule identifier.
        """
        return pulumi.get(self, "schedule_identifier")

    @schedule_identifier.setter
    def schedule_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schedule_identifier", value)


class SnapshotScheduleAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_identifier: Optional[pulumi.Input[str]] = None,
                 schedule_identifier: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        default_cluster = aws.redshift.Cluster("defaultCluster",
            cluster_identifier="tf-redshift-cluster",
            database_name="mydb",
            master_username="foo",
            master_password="Mustbe8characters",
            node_type="dc1.large",
            cluster_type="single-node")
        default_snapshot_schedule = aws.redshift.SnapshotSchedule("defaultSnapshotSchedule",
            identifier="tf-redshift-snapshot-schedule",
            definitions=["rate(12 hours)"])
        default_snapshot_schedule_association = aws.redshift.SnapshotScheduleAssociation("defaultSnapshotScheduleAssociation",
            cluster_identifier=default_cluster.id,
            schedule_identifier=default_snapshot_schedule.id)
        ```

        ## Import

        Using `pulumi import`, import Redshift Snapshot Schedule Association using the `<cluster-identifier>/<schedule-identifier>`. For example:

        ```sh
         $ pulumi import aws:redshift/snapshotScheduleAssociation:SnapshotScheduleAssociation default tf-redshift-cluster/tf-redshift-snapshot-schedule
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_identifier: The cluster identifier.
        :param pulumi.Input[str] schedule_identifier: The snapshot schedule identifier.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SnapshotScheduleAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        default_cluster = aws.redshift.Cluster("defaultCluster",
            cluster_identifier="tf-redshift-cluster",
            database_name="mydb",
            master_username="foo",
            master_password="Mustbe8characters",
            node_type="dc1.large",
            cluster_type="single-node")
        default_snapshot_schedule = aws.redshift.SnapshotSchedule("defaultSnapshotSchedule",
            identifier="tf-redshift-snapshot-schedule",
            definitions=["rate(12 hours)"])
        default_snapshot_schedule_association = aws.redshift.SnapshotScheduleAssociation("defaultSnapshotScheduleAssociation",
            cluster_identifier=default_cluster.id,
            schedule_identifier=default_snapshot_schedule.id)
        ```

        ## Import

        Using `pulumi import`, import Redshift Snapshot Schedule Association using the `<cluster-identifier>/<schedule-identifier>`. For example:

        ```sh
         $ pulumi import aws:redshift/snapshotScheduleAssociation:SnapshotScheduleAssociation default tf-redshift-cluster/tf-redshift-snapshot-schedule
        ```

        :param str resource_name: The name of the resource.
        :param SnapshotScheduleAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SnapshotScheduleAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_identifier: Optional[pulumi.Input[str]] = None,
                 schedule_identifier: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SnapshotScheduleAssociationArgs.__new__(SnapshotScheduleAssociationArgs)

            if cluster_identifier is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_identifier'")
            __props__.__dict__["cluster_identifier"] = cluster_identifier
            if schedule_identifier is None and not opts.urn:
                raise TypeError("Missing required property 'schedule_identifier'")
            __props__.__dict__["schedule_identifier"] = schedule_identifier
        super(SnapshotScheduleAssociation, __self__).__init__(
            'aws:redshift/snapshotScheduleAssociation:SnapshotScheduleAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cluster_identifier: Optional[pulumi.Input[str]] = None,
            schedule_identifier: Optional[pulumi.Input[str]] = None) -> 'SnapshotScheduleAssociation':
        """
        Get an existing SnapshotScheduleAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_identifier: The cluster identifier.
        :param pulumi.Input[str] schedule_identifier: The snapshot schedule identifier.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SnapshotScheduleAssociationState.__new__(_SnapshotScheduleAssociationState)

        __props__.__dict__["cluster_identifier"] = cluster_identifier
        __props__.__dict__["schedule_identifier"] = schedule_identifier
        return SnapshotScheduleAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clusterIdentifier")
    def cluster_identifier(self) -> pulumi.Output[str]:
        """
        The cluster identifier.
        """
        return pulumi.get(self, "cluster_identifier")

    @property
    @pulumi.getter(name="scheduleIdentifier")
    def schedule_identifier(self) -> pulumi.Output[str]:
        """
        The snapshot schedule identifier.
        """
        return pulumi.get(self, "schedule_identifier")

