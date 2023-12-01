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

__all__ = [
    'KxClusterAutoScalingConfiguration',
    'KxClusterCacheStorageConfiguration',
    'KxClusterCapacityConfiguration',
    'KxClusterCode',
    'KxClusterDatabase',
    'KxClusterDatabaseCacheConfiguration',
    'KxClusterSavedownStorageConfiguration',
    'KxClusterVpcConfiguration',
    'KxEnvironmentCustomDnsConfiguration',
    'KxEnvironmentTransitGatewayConfiguration',
    'KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfiguration',
    'KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationIcmpTypeCode',
    'KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationPortRange',
]

@pulumi.output_type
class KxClusterAutoScalingConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "autoScalingMetric":
            suggest = "auto_scaling_metric"
        elif key == "maxNodeCount":
            suggest = "max_node_count"
        elif key == "metricTarget":
            suggest = "metric_target"
        elif key == "minNodeCount":
            suggest = "min_node_count"
        elif key == "scaleInCooldownSeconds":
            suggest = "scale_in_cooldown_seconds"
        elif key == "scaleOutCooldownSeconds":
            suggest = "scale_out_cooldown_seconds"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KxClusterAutoScalingConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KxClusterAutoScalingConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KxClusterAutoScalingConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 auto_scaling_metric: str,
                 max_node_count: int,
                 metric_target: float,
                 min_node_count: int,
                 scale_in_cooldown_seconds: float,
                 scale_out_cooldown_seconds: float):
        """
        :param str auto_scaling_metric: Metric your cluster will track in order to scale in and out. For example, CPU_UTILIZATION_PERCENTAGE is the average CPU usage across all nodes in a cluster.
        :param int max_node_count: Highest number of nodes to scale. Cannot be greater than 5
        :param float metric_target: Desired value of chosen `auto_scaling_metric`. When metric drops below this value, cluster will scale in. When metric goes above this value, cluster will scale out. Can be set between 0 and 100 percent.
        :param int min_node_count: Lowest number of nodes to scale. Must be at least 1 and less than the `max_node_count`. If nodes in cluster belong to multiple availability zones, then `min_node_count` must be at least 3.
        :param float scale_in_cooldown_seconds: Duration in seconds that FinSpace will wait after a scale in event before initiating another scaling event.
        :param float scale_out_cooldown_seconds: Duration in seconds that FinSpace will wait after a scale out event before initiating another scaling event.
        """
        pulumi.set(__self__, "auto_scaling_metric", auto_scaling_metric)
        pulumi.set(__self__, "max_node_count", max_node_count)
        pulumi.set(__self__, "metric_target", metric_target)
        pulumi.set(__self__, "min_node_count", min_node_count)
        pulumi.set(__self__, "scale_in_cooldown_seconds", scale_in_cooldown_seconds)
        pulumi.set(__self__, "scale_out_cooldown_seconds", scale_out_cooldown_seconds)

    @property
    @pulumi.getter(name="autoScalingMetric")
    def auto_scaling_metric(self) -> str:
        """
        Metric your cluster will track in order to scale in and out. For example, CPU_UTILIZATION_PERCENTAGE is the average CPU usage across all nodes in a cluster.
        """
        return pulumi.get(self, "auto_scaling_metric")

    @property
    @pulumi.getter(name="maxNodeCount")
    def max_node_count(self) -> int:
        """
        Highest number of nodes to scale. Cannot be greater than 5
        """
        return pulumi.get(self, "max_node_count")

    @property
    @pulumi.getter(name="metricTarget")
    def metric_target(self) -> float:
        """
        Desired value of chosen `auto_scaling_metric`. When metric drops below this value, cluster will scale in. When metric goes above this value, cluster will scale out. Can be set between 0 and 100 percent.
        """
        return pulumi.get(self, "metric_target")

    @property
    @pulumi.getter(name="minNodeCount")
    def min_node_count(self) -> int:
        """
        Lowest number of nodes to scale. Must be at least 1 and less than the `max_node_count`. If nodes in cluster belong to multiple availability zones, then `min_node_count` must be at least 3.
        """
        return pulumi.get(self, "min_node_count")

    @property
    @pulumi.getter(name="scaleInCooldownSeconds")
    def scale_in_cooldown_seconds(self) -> float:
        """
        Duration in seconds that FinSpace will wait after a scale in event before initiating another scaling event.
        """
        return pulumi.get(self, "scale_in_cooldown_seconds")

    @property
    @pulumi.getter(name="scaleOutCooldownSeconds")
    def scale_out_cooldown_seconds(self) -> float:
        """
        Duration in seconds that FinSpace will wait after a scale out event before initiating another scaling event.
        """
        return pulumi.get(self, "scale_out_cooldown_seconds")


@pulumi.output_type
class KxClusterCacheStorageConfiguration(dict):
    def __init__(__self__, *,
                 size: int,
                 type: str):
        """
        :param int size: Size of cache in Gigabytes.
               
               Please note that create/update timeouts may have to be adjusted from the default 4 hours depending upon the
               volume of data being cached, as noted in the example configuration.
        :param str type: Type of KDB database. The following types are available:
               * HDB - Historical Database. The data is only accessible with read-only permissions from one of the FinSpace managed KX databases mounted to the cluster.
               * RDB - Realtime Database. This type of database captures all the data from a ticker plant and stores it in memory until the end of day, after which it writes all of its data to a disk and reloads the HDB. This cluster type requires local storage for temporary storage of data during the savedown process. If you specify this field in your request, you must provide the `savedownStorageConfiguration` parameter.
               * GATEWAY - A gateway cluster allows you to access data across processes in kdb systems. It allows you to create your own routing logic using the initialization scripts and custom code. This type of cluster does not require a  writable local storage.
        """
        pulumi.set(__self__, "size", size)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def size(self) -> int:
        """
        Size of cache in Gigabytes.

        Please note that create/update timeouts may have to be adjusted from the default 4 hours depending upon the
        volume of data being cached, as noted in the example configuration.
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of KDB database. The following types are available:
        * HDB - Historical Database. The data is only accessible with read-only permissions from one of the FinSpace managed KX databases mounted to the cluster.
        * RDB - Realtime Database. This type of database captures all the data from a ticker plant and stores it in memory until the end of day, after which it writes all of its data to a disk and reloads the HDB. This cluster type requires local storage for temporary storage of data during the savedown process. If you specify this field in your request, you must provide the `savedownStorageConfiguration` parameter.
        * GATEWAY - A gateway cluster allows you to access data across processes in kdb systems. It allows you to create your own routing logic using the initialization scripts and custom code. This type of cluster does not require a  writable local storage.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class KxClusterCapacityConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "nodeCount":
            suggest = "node_count"
        elif key == "nodeType":
            suggest = "node_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KxClusterCapacityConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KxClusterCapacityConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KxClusterCapacityConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 node_count: int,
                 node_type: str):
        """
        :param int node_count: Number of instances running in a cluster. Must be at least 1 and at most 5.
        :param str node_type: Determines the hardware of the host computer used for your cluster instance. Each node type offers different memory and storage capabilities. Choose a node type based on the requirements of the application or software that you plan to run on your instance.
               
               You can only specify one of the following values:
               * kx.s.large – The node type with a configuration of 12 GiB memory and 2 vCPUs.
               * kx.s.xlarge – The node type with a configuration of 27 GiB memory and 4 vCPUs.
               * kx.s.2xlarge – The node type with a configuration of 54 GiB memory and 8 vCPUs.
               * kx.s.4xlarge – The node type with a configuration of 108 GiB memory and 16 vCPUs.
               * kx.s.8xlarge – The node type with a configuration of 216 GiB memory and 32 vCPUs.
               * kx.s.16xlarge – The node type with a configuration of 432 GiB memory and 64 vCPUs.
               * kx.s.32xlarge – The node type with a configuration of 864 GiB memory and 128 vCPUs.
        """
        pulumi.set(__self__, "node_count", node_count)
        pulumi.set(__self__, "node_type", node_type)

    @property
    @pulumi.getter(name="nodeCount")
    def node_count(self) -> int:
        """
        Number of instances running in a cluster. Must be at least 1 and at most 5.
        """
        return pulumi.get(self, "node_count")

    @property
    @pulumi.getter(name="nodeType")
    def node_type(self) -> str:
        """
        Determines the hardware of the host computer used for your cluster instance. Each node type offers different memory and storage capabilities. Choose a node type based on the requirements of the application or software that you plan to run on your instance.

        You can only specify one of the following values:
        * kx.s.large – The node type with a configuration of 12 GiB memory and 2 vCPUs.
        * kx.s.xlarge – The node type with a configuration of 27 GiB memory and 4 vCPUs.
        * kx.s.2xlarge – The node type with a configuration of 54 GiB memory and 8 vCPUs.
        * kx.s.4xlarge – The node type with a configuration of 108 GiB memory and 16 vCPUs.
        * kx.s.8xlarge – The node type with a configuration of 216 GiB memory and 32 vCPUs.
        * kx.s.16xlarge – The node type with a configuration of 432 GiB memory and 64 vCPUs.
        * kx.s.32xlarge – The node type with a configuration of 864 GiB memory and 128 vCPUs.
        """
        return pulumi.get(self, "node_type")


@pulumi.output_type
class KxClusterCode(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "s3Bucket":
            suggest = "s3_bucket"
        elif key == "s3Key":
            suggest = "s3_key"
        elif key == "s3ObjectVersion":
            suggest = "s3_object_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KxClusterCode. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KxClusterCode.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KxClusterCode.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 s3_bucket: str,
                 s3_key: str,
                 s3_object_version: Optional[str] = None):
        """
        :param str s3_bucket: Unique name for the S3 bucket.
        :param str s3_key: Full S3 path (excluding bucket) to the .zip file that contains the code to be loaded onto the cluster when it’s started.
        :param str s3_object_version: Version of an S3 Object.
        """
        pulumi.set(__self__, "s3_bucket", s3_bucket)
        pulumi.set(__self__, "s3_key", s3_key)
        if s3_object_version is not None:
            pulumi.set(__self__, "s3_object_version", s3_object_version)

    @property
    @pulumi.getter(name="s3Bucket")
    def s3_bucket(self) -> str:
        """
        Unique name for the S3 bucket.
        """
        return pulumi.get(self, "s3_bucket")

    @property
    @pulumi.getter(name="s3Key")
    def s3_key(self) -> str:
        """
        Full S3 path (excluding bucket) to the .zip file that contains the code to be loaded onto the cluster when it’s started.
        """
        return pulumi.get(self, "s3_key")

    @property
    @pulumi.getter(name="s3ObjectVersion")
    def s3_object_version(self) -> Optional[str]:
        """
        Version of an S3 Object.
        """
        return pulumi.get(self, "s3_object_version")


@pulumi.output_type
class KxClusterDatabase(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "databaseName":
            suggest = "database_name"
        elif key == "cacheConfigurations":
            suggest = "cache_configurations"
        elif key == "changesetId":
            suggest = "changeset_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KxClusterDatabase. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KxClusterDatabase.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KxClusterDatabase.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 database_name: str,
                 cache_configurations: Optional[Sequence['outputs.KxClusterDatabaseCacheConfiguration']] = None,
                 changeset_id: Optional[str] = None):
        """
        :param str database_name: Name of the KX database.
        :param Sequence['KxClusterDatabaseCacheConfigurationArgs'] cache_configurations: Configuration details for the disk cache to increase performance reading from a KX database mounted to the cluster. See cache_configurations.
        :param str changeset_id: A unique identifier of the changeset that is associated with the cluster.
        """
        pulumi.set(__self__, "database_name", database_name)
        if cache_configurations is not None:
            pulumi.set(__self__, "cache_configurations", cache_configurations)
        if changeset_id is not None:
            pulumi.set(__self__, "changeset_id", changeset_id)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> str:
        """
        Name of the KX database.
        """
        return pulumi.get(self, "database_name")

    @property
    @pulumi.getter(name="cacheConfigurations")
    def cache_configurations(self) -> Optional[Sequence['outputs.KxClusterDatabaseCacheConfiguration']]:
        """
        Configuration details for the disk cache to increase performance reading from a KX database mounted to the cluster. See cache_configurations.
        """
        return pulumi.get(self, "cache_configurations")

    @property
    @pulumi.getter(name="changesetId")
    def changeset_id(self) -> Optional[str]:
        """
        A unique identifier of the changeset that is associated with the cluster.
        """
        return pulumi.get(self, "changeset_id")


@pulumi.output_type
class KxClusterDatabaseCacheConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cacheType":
            suggest = "cache_type"
        elif key == "dbPaths":
            suggest = "db_paths"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KxClusterDatabaseCacheConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KxClusterDatabaseCacheConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KxClusterDatabaseCacheConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cache_type: str,
                 db_paths: Optional[Sequence[str]] = None):
        """
        :param str cache_type: Type of disk cache.
        :param Sequence[str] db_paths: Paths within the database to cache.
        """
        pulumi.set(__self__, "cache_type", cache_type)
        if db_paths is not None:
            pulumi.set(__self__, "db_paths", db_paths)

    @property
    @pulumi.getter(name="cacheType")
    def cache_type(self) -> str:
        """
        Type of disk cache.
        """
        return pulumi.get(self, "cache_type")

    @property
    @pulumi.getter(name="dbPaths")
    def db_paths(self) -> Optional[Sequence[str]]:
        """
        Paths within the database to cache.
        """
        return pulumi.get(self, "db_paths")


@pulumi.output_type
class KxClusterSavedownStorageConfiguration(dict):
    def __init__(__self__, *,
                 size: int,
                 type: str):
        """
        :param int size: Size of temporary storage in gigabytes. Must be between 10 and 16000.
        :param str type: Type of writeable storage space for temporarily storing your savedown data. The valid values are:
               * SDS01 - This type represents 3000 IOPS and io2 ebs volume type.
        """
        pulumi.set(__self__, "size", size)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def size(self) -> int:
        """
        Size of temporary storage in gigabytes. Must be between 10 and 16000.
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of writeable storage space for temporarily storing your savedown data. The valid values are:
        * SDS01 - This type represents 3000 IOPS and io2 ebs volume type.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class KxClusterVpcConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipAddressType":
            suggest = "ip_address_type"
        elif key == "securityGroupIds":
            suggest = "security_group_ids"
        elif key == "subnetIds":
            suggest = "subnet_ids"
        elif key == "vpcId":
            suggest = "vpc_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KxClusterVpcConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KxClusterVpcConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KxClusterVpcConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip_address_type: str,
                 security_group_ids: Sequence[str],
                 subnet_ids: Sequence[str],
                 vpc_id: str):
        """
        :param str ip_address_type: IP address type for cluster network configuration parameters. The following type is available: IP_V4 - IP address version 4.
        :param Sequence[str] security_group_ids: Unique identifier of the VPC security group applied to the VPC endpoint ENI for the cluster.
               * `subnet_ids `- (Required) Identifier of the subnet that the Privatelink VPC endpoint uses to connect to the cluster.
        :param str vpc_id: Identifier of the VPC endpoint
        """
        pulumi.set(__self__, "ip_address_type", ip_address_type)
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="ipAddressType")
    def ip_address_type(self) -> str:
        """
        IP address type for cluster network configuration parameters. The following type is available: IP_V4 - IP address version 4.
        """
        return pulumi.get(self, "ip_address_type")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Sequence[str]:
        """
        Unique identifier of the VPC security group applied to the VPC endpoint ENI for the cluster.
        * `subnet_ids `- (Required) Identifier of the subnet that the Privatelink VPC endpoint uses to connect to the cluster.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        Identifier of the VPC endpoint
        """
        return pulumi.get(self, "vpc_id")


@pulumi.output_type
class KxEnvironmentCustomDnsConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "customDnsServerIp":
            suggest = "custom_dns_server_ip"
        elif key == "customDnsServerName":
            suggest = "custom_dns_server_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KxEnvironmentCustomDnsConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KxEnvironmentCustomDnsConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KxEnvironmentCustomDnsConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 custom_dns_server_ip: str,
                 custom_dns_server_name: str):
        """
        :param str custom_dns_server_ip: IP address of the DNS server.
        :param str custom_dns_server_name: Name of the DNS server.
        """
        pulumi.set(__self__, "custom_dns_server_ip", custom_dns_server_ip)
        pulumi.set(__self__, "custom_dns_server_name", custom_dns_server_name)

    @property
    @pulumi.getter(name="customDnsServerIp")
    def custom_dns_server_ip(self) -> str:
        """
        IP address of the DNS server.
        """
        return pulumi.get(self, "custom_dns_server_ip")

    @property
    @pulumi.getter(name="customDnsServerName")
    def custom_dns_server_name(self) -> str:
        """
        Name of the DNS server.
        """
        return pulumi.get(self, "custom_dns_server_name")


@pulumi.output_type
class KxEnvironmentTransitGatewayConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "routableCidrSpace":
            suggest = "routable_cidr_space"
        elif key == "transitGatewayId":
            suggest = "transit_gateway_id"
        elif key == "attachmentNetworkAclConfigurations":
            suggest = "attachment_network_acl_configurations"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KxEnvironmentTransitGatewayConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KxEnvironmentTransitGatewayConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KxEnvironmentTransitGatewayConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 routable_cidr_space: str,
                 transit_gateway_id: str,
                 attachment_network_acl_configurations: Optional[Sequence['outputs.KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfiguration']] = None):
        """
        :param str routable_cidr_space: Routing CIDR on behalf of KX environment. It could be any “/26 range in the 100.64.0.0 CIDR space. After providing, it will be added to the customer’s transit gateway routing table so that the traffics could be routed to KX network.
        :param str transit_gateway_id: Identifier of the transit gateway created by the customer to connect outbound traffics from KX network to your internal network.
        :param Sequence['KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationArgs'] attachment_network_acl_configurations: Rules that define how you manage outbound traffic from kdb network to your internal network. Defined below.
        """
        pulumi.set(__self__, "routable_cidr_space", routable_cidr_space)
        pulumi.set(__self__, "transit_gateway_id", transit_gateway_id)
        if attachment_network_acl_configurations is not None:
            pulumi.set(__self__, "attachment_network_acl_configurations", attachment_network_acl_configurations)

    @property
    @pulumi.getter(name="routableCidrSpace")
    def routable_cidr_space(self) -> str:
        """
        Routing CIDR on behalf of KX environment. It could be any “/26 range in the 100.64.0.0 CIDR space. After providing, it will be added to the customer’s transit gateway routing table so that the traffics could be routed to KX network.
        """
        return pulumi.get(self, "routable_cidr_space")

    @property
    @pulumi.getter(name="transitGatewayId")
    def transit_gateway_id(self) -> str:
        """
        Identifier of the transit gateway created by the customer to connect outbound traffics from KX network to your internal network.
        """
        return pulumi.get(self, "transit_gateway_id")

    @property
    @pulumi.getter(name="attachmentNetworkAclConfigurations")
    def attachment_network_acl_configurations(self) -> Optional[Sequence['outputs.KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfiguration']]:
        """
        Rules that define how you manage outbound traffic from kdb network to your internal network. Defined below.
        """
        return pulumi.get(self, "attachment_network_acl_configurations")


@pulumi.output_type
class KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cidrBlock":
            suggest = "cidr_block"
        elif key == "ruleAction":
            suggest = "rule_action"
        elif key == "ruleNumber":
            suggest = "rule_number"
        elif key == "icmpTypeCode":
            suggest = "icmp_type_code"
        elif key == "portRange":
            suggest = "port_range"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cidr_block: str,
                 protocol: str,
                 rule_action: str,
                 rule_number: int,
                 icmp_type_code: Optional['outputs.KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationIcmpTypeCode'] = None,
                 port_range: Optional['outputs.KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationPortRange'] = None):
        """
        :param str cidr_block: The IPv4 network range to allow or deny, in CIDR notation. The specified CIDR block is modified to its canonical form. For example, `100.68.0.18/18` will be converted to `100.68.0.0/18`.
        :param str protocol: Protocol number. A value of `1` means all the protocols.
        :param str rule_action: Indicates whether to `allow` or `deny` the traffic that matches the rule.
        :param int rule_number: Rule number for the entry. All the network ACL entries are processed in ascending order by rule number.
        :param 'KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationIcmpTypeCodeArgs' icmp_type_code: Defines the ICMP protocol that consists of the ICMP type and code. Defined below.
        :param 'KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationPortRangeArgs' port_range: Range of ports the rule applies to. Defined below.
        """
        pulumi.set(__self__, "cidr_block", cidr_block)
        pulumi.set(__self__, "protocol", protocol)
        pulumi.set(__self__, "rule_action", rule_action)
        pulumi.set(__self__, "rule_number", rule_number)
        if icmp_type_code is not None:
            pulumi.set(__self__, "icmp_type_code", icmp_type_code)
        if port_range is not None:
            pulumi.set(__self__, "port_range", port_range)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> str:
        """
        The IPv4 network range to allow or deny, in CIDR notation. The specified CIDR block is modified to its canonical form. For example, `100.68.0.18/18` will be converted to `100.68.0.0/18`.
        """
        return pulumi.get(self, "cidr_block")

    @property
    @pulumi.getter
    def protocol(self) -> str:
        """
        Protocol number. A value of `1` means all the protocols.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="ruleAction")
    def rule_action(self) -> str:
        """
        Indicates whether to `allow` or `deny` the traffic that matches the rule.
        """
        return pulumi.get(self, "rule_action")

    @property
    @pulumi.getter(name="ruleNumber")
    def rule_number(self) -> int:
        """
        Rule number for the entry. All the network ACL entries are processed in ascending order by rule number.
        """
        return pulumi.get(self, "rule_number")

    @property
    @pulumi.getter(name="icmpTypeCode")
    def icmp_type_code(self) -> Optional['outputs.KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationIcmpTypeCode']:
        """
        Defines the ICMP protocol that consists of the ICMP type and code. Defined below.
        """
        return pulumi.get(self, "icmp_type_code")

    @property
    @pulumi.getter(name="portRange")
    def port_range(self) -> Optional['outputs.KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationPortRange']:
        """
        Range of ports the rule applies to. Defined below.
        """
        return pulumi.get(self, "port_range")


@pulumi.output_type
class KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationIcmpTypeCode(dict):
    def __init__(__self__, *,
                 code: int,
                 type: int):
        """
        :param int code: ICMP code. A value of `-1` means all codes for the specified ICMP type.
        :param int type: ICMP type. A value of `-1` means all types.
        """
        pulumi.set(__self__, "code", code)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def code(self) -> int:
        """
        ICMP code. A value of `-1` means all codes for the specified ICMP type.
        """
        return pulumi.get(self, "code")

    @property
    @pulumi.getter
    def type(self) -> int:
        """
        ICMP type. A value of `-1` means all types.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationPortRange(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "from":
            suggest = "from_"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationPortRange. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationPortRange.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KxEnvironmentTransitGatewayConfigurationAttachmentNetworkAclConfigurationPortRange.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 from_: int,
                 to: int):
        """
        :param int from_: First port in the range.
        :param int to: Last port in the range.
        """
        pulumi.set(__self__, "from_", from_)
        pulumi.set(__self__, "to", to)

    @property
    @pulumi.getter(name="from")
    def from_(self) -> int:
        """
        First port in the range.
        """
        return pulumi.get(self, "from_")

    @property
    @pulumi.getter
    def to(self) -> int:
        """
        Last port in the range.
        """
        return pulumi.get(self, "to")


