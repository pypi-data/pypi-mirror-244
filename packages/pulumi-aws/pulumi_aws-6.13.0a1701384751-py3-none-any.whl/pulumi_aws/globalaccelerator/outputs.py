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
    'AcceleratorAttributes',
    'AcceleratorIpSet',
    'CustomRoutingAcceleratorAttributes',
    'CustomRoutingAcceleratorIpSet',
    'CustomRoutingEndpointGroupDestinationConfiguration',
    'CustomRoutingEndpointGroupEndpointConfiguration',
    'CustomRoutingListenerPortRange',
    'EndpointGroupEndpointConfiguration',
    'EndpointGroupPortOverride',
    'ListenerPortRange',
    'GetAcceleratorAttributeResult',
    'GetAcceleratorIpSetResult',
    'GetCustomRoutingAcceleratorAttributeResult',
    'GetCustomRoutingAcceleratorIpSetResult',
]

@pulumi.output_type
class AcceleratorAttributes(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "flowLogsEnabled":
            suggest = "flow_logs_enabled"
        elif key == "flowLogsS3Bucket":
            suggest = "flow_logs_s3_bucket"
        elif key == "flowLogsS3Prefix":
            suggest = "flow_logs_s3_prefix"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AcceleratorAttributes. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AcceleratorAttributes.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AcceleratorAttributes.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 flow_logs_enabled: Optional[bool] = None,
                 flow_logs_s3_bucket: Optional[str] = None,
                 flow_logs_s3_prefix: Optional[str] = None):
        """
        :param bool flow_logs_enabled: Indicates whether flow logs are enabled. Defaults to `false`. Valid values: `true`, `false`.
        :param str flow_logs_s3_bucket: The name of the Amazon S3 bucket for the flow logs. Required if `flow_logs_enabled` is `true`.
        :param str flow_logs_s3_prefix: The prefix for the location in the Amazon S3 bucket for the flow logs. Required if `flow_logs_enabled` is `true`.
        """
        if flow_logs_enabled is not None:
            pulumi.set(__self__, "flow_logs_enabled", flow_logs_enabled)
        if flow_logs_s3_bucket is not None:
            pulumi.set(__self__, "flow_logs_s3_bucket", flow_logs_s3_bucket)
        if flow_logs_s3_prefix is not None:
            pulumi.set(__self__, "flow_logs_s3_prefix", flow_logs_s3_prefix)

    @property
    @pulumi.getter(name="flowLogsEnabled")
    def flow_logs_enabled(self) -> Optional[bool]:
        """
        Indicates whether flow logs are enabled. Defaults to `false`. Valid values: `true`, `false`.
        """
        return pulumi.get(self, "flow_logs_enabled")

    @property
    @pulumi.getter(name="flowLogsS3Bucket")
    def flow_logs_s3_bucket(self) -> Optional[str]:
        """
        The name of the Amazon S3 bucket for the flow logs. Required if `flow_logs_enabled` is `true`.
        """
        return pulumi.get(self, "flow_logs_s3_bucket")

    @property
    @pulumi.getter(name="flowLogsS3Prefix")
    def flow_logs_s3_prefix(self) -> Optional[str]:
        """
        The prefix for the location in the Amazon S3 bucket for the flow logs. Required if `flow_logs_enabled` is `true`.
        """
        return pulumi.get(self, "flow_logs_s3_prefix")


@pulumi.output_type
class AcceleratorIpSet(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipAddresses":
            suggest = "ip_addresses"
        elif key == "ipFamily":
            suggest = "ip_family"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AcceleratorIpSet. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AcceleratorIpSet.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AcceleratorIpSet.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip_addresses: Optional[Sequence[str]] = None,
                 ip_family: Optional[str] = None):
        """
        :param Sequence[str] ip_addresses: The IP addresses to use for BYOIP accelerators. If not specified, the service assigns IP addresses. Valid values: 1 or 2 IPv4 addresses.
        :param str ip_family: The type of IP addresses included in this IP set.
        """
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)
        if ip_family is not None:
            pulumi.set(__self__, "ip_family", ip_family)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[Sequence[str]]:
        """
        The IP addresses to use for BYOIP accelerators. If not specified, the service assigns IP addresses. Valid values: 1 or 2 IPv4 addresses.
        """
        return pulumi.get(self, "ip_addresses")

    @property
    @pulumi.getter(name="ipFamily")
    def ip_family(self) -> Optional[str]:
        """
        The type of IP addresses included in this IP set.
        """
        return pulumi.get(self, "ip_family")


@pulumi.output_type
class CustomRoutingAcceleratorAttributes(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "flowLogsEnabled":
            suggest = "flow_logs_enabled"
        elif key == "flowLogsS3Bucket":
            suggest = "flow_logs_s3_bucket"
        elif key == "flowLogsS3Prefix":
            suggest = "flow_logs_s3_prefix"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomRoutingAcceleratorAttributes. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomRoutingAcceleratorAttributes.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CustomRoutingAcceleratorAttributes.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 flow_logs_enabled: Optional[bool] = None,
                 flow_logs_s3_bucket: Optional[str] = None,
                 flow_logs_s3_prefix: Optional[str] = None):
        """
        :param bool flow_logs_enabled: Indicates whether flow logs are enabled. Defaults to `false`. Valid values: `true`, `false`.
        :param str flow_logs_s3_bucket: The name of the Amazon S3 bucket for the flow logs. Required if `flow_logs_enabled` is `true`.
        :param str flow_logs_s3_prefix: The prefix for the location in the Amazon S3 bucket for the flow logs. Required if `flow_logs_enabled` is `true`.
        """
        if flow_logs_enabled is not None:
            pulumi.set(__self__, "flow_logs_enabled", flow_logs_enabled)
        if flow_logs_s3_bucket is not None:
            pulumi.set(__self__, "flow_logs_s3_bucket", flow_logs_s3_bucket)
        if flow_logs_s3_prefix is not None:
            pulumi.set(__self__, "flow_logs_s3_prefix", flow_logs_s3_prefix)

    @property
    @pulumi.getter(name="flowLogsEnabled")
    def flow_logs_enabled(self) -> Optional[bool]:
        """
        Indicates whether flow logs are enabled. Defaults to `false`. Valid values: `true`, `false`.
        """
        return pulumi.get(self, "flow_logs_enabled")

    @property
    @pulumi.getter(name="flowLogsS3Bucket")
    def flow_logs_s3_bucket(self) -> Optional[str]:
        """
        The name of the Amazon S3 bucket for the flow logs. Required if `flow_logs_enabled` is `true`.
        """
        return pulumi.get(self, "flow_logs_s3_bucket")

    @property
    @pulumi.getter(name="flowLogsS3Prefix")
    def flow_logs_s3_prefix(self) -> Optional[str]:
        """
        The prefix for the location in the Amazon S3 bucket for the flow logs. Required if `flow_logs_enabled` is `true`.
        """
        return pulumi.get(self, "flow_logs_s3_prefix")


@pulumi.output_type
class CustomRoutingAcceleratorIpSet(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipAddresses":
            suggest = "ip_addresses"
        elif key == "ipFamily":
            suggest = "ip_family"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomRoutingAcceleratorIpSet. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomRoutingAcceleratorIpSet.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CustomRoutingAcceleratorIpSet.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip_addresses: Optional[Sequence[str]] = None,
                 ip_family: Optional[str] = None):
        """
        :param Sequence[str] ip_addresses: The IP addresses to use for BYOIP accelerators. If not specified, the service assigns IP addresses. Valid values: 1 or 2 IPv4 addresses.
        :param str ip_family: The type of IP addresses included in this IP set.
        """
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)
        if ip_family is not None:
            pulumi.set(__self__, "ip_family", ip_family)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[Sequence[str]]:
        """
        The IP addresses to use for BYOIP accelerators. If not specified, the service assigns IP addresses. Valid values: 1 or 2 IPv4 addresses.
        """
        return pulumi.get(self, "ip_addresses")

    @property
    @pulumi.getter(name="ipFamily")
    def ip_family(self) -> Optional[str]:
        """
        The type of IP addresses included in this IP set.
        """
        return pulumi.get(self, "ip_family")


@pulumi.output_type
class CustomRoutingEndpointGroupDestinationConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "fromPort":
            suggest = "from_port"
        elif key == "toPort":
            suggest = "to_port"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomRoutingEndpointGroupDestinationConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomRoutingEndpointGroupDestinationConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CustomRoutingEndpointGroupDestinationConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 from_port: int,
                 protocols: Sequence[str],
                 to_port: int):
        """
        :param int from_port: The first port, inclusive, in the range of ports for the endpoint group that is associated with a custom routing accelerator.
        :param Sequence[str] protocols: The protocol for the endpoint group that is associated with a custom routing accelerator. The protocol can be either `"TCP"` or `"UDP"`.
        :param int to_port: The last port, inclusive, in the range of ports for the endpoint group that is associated with a custom routing accelerator.
        """
        pulumi.set(__self__, "from_port", from_port)
        pulumi.set(__self__, "protocols", protocols)
        pulumi.set(__self__, "to_port", to_port)

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> int:
        """
        The first port, inclusive, in the range of ports for the endpoint group that is associated with a custom routing accelerator.
        """
        return pulumi.get(self, "from_port")

    @property
    @pulumi.getter
    def protocols(self) -> Sequence[str]:
        """
        The protocol for the endpoint group that is associated with a custom routing accelerator. The protocol can be either `"TCP"` or `"UDP"`.
        """
        return pulumi.get(self, "protocols")

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> int:
        """
        The last port, inclusive, in the range of ports for the endpoint group that is associated with a custom routing accelerator.
        """
        return pulumi.get(self, "to_port")


@pulumi.output_type
class CustomRoutingEndpointGroupEndpointConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "endpointId":
            suggest = "endpoint_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomRoutingEndpointGroupEndpointConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomRoutingEndpointGroupEndpointConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CustomRoutingEndpointGroupEndpointConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 endpoint_id: Optional[str] = None):
        """
        :param str endpoint_id: An ID for the endpoint. For custom routing accelerators, this is the virtual private cloud (VPC) subnet ID.
        """
        if endpoint_id is not None:
            pulumi.set(__self__, "endpoint_id", endpoint_id)

    @property
    @pulumi.getter(name="endpointId")
    def endpoint_id(self) -> Optional[str]:
        """
        An ID for the endpoint. For custom routing accelerators, this is the virtual private cloud (VPC) subnet ID.
        """
        return pulumi.get(self, "endpoint_id")


@pulumi.output_type
class CustomRoutingListenerPortRange(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "fromPort":
            suggest = "from_port"
        elif key == "toPort":
            suggest = "to_port"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomRoutingListenerPortRange. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomRoutingListenerPortRange.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CustomRoutingListenerPortRange.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 from_port: Optional[int] = None,
                 to_port: Optional[int] = None):
        """
        :param int from_port: The first port in the range of ports, inclusive.
        :param int to_port: The last port in the range of ports, inclusive.
        """
        if from_port is not None:
            pulumi.set(__self__, "from_port", from_port)
        if to_port is not None:
            pulumi.set(__self__, "to_port", to_port)

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> Optional[int]:
        """
        The first port in the range of ports, inclusive.
        """
        return pulumi.get(self, "from_port")

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> Optional[int]:
        """
        The last port in the range of ports, inclusive.
        """
        return pulumi.get(self, "to_port")


@pulumi.output_type
class EndpointGroupEndpointConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientIpPreservationEnabled":
            suggest = "client_ip_preservation_enabled"
        elif key == "endpointId":
            suggest = "endpoint_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointGroupEndpointConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointGroupEndpointConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointGroupEndpointConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_ip_preservation_enabled: Optional[bool] = None,
                 endpoint_id: Optional[str] = None,
                 weight: Optional[int] = None):
        """
        :param bool client_ip_preservation_enabled: Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. See the [AWS documentation](https://docs.aws.amazon.com/global-accelerator/latest/dg/preserve-client-ip-address.html) for more details. The default value is `false`.
               **Note:** When client IP address preservation is enabled, the Global Accelerator service creates an EC2 Security Group in the VPC named `GlobalAccelerator` that must be deleted (potentially outside of the provider) before the VPC will successfully delete. If this EC2 Security Group is not deleted, the provider will retry the VPC deletion for a few minutes before reporting a `DependencyViolation` error. This cannot be resolved by re-running the provider.
        :param str endpoint_id: An ID for the endpoint. If the endpoint is a Network Load Balancer or Application Load Balancer, this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address, this is the Elastic IP address allocation ID.
        :param int weight: The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify.
        """
        if client_ip_preservation_enabled is not None:
            pulumi.set(__self__, "client_ip_preservation_enabled", client_ip_preservation_enabled)
        if endpoint_id is not None:
            pulumi.set(__self__, "endpoint_id", endpoint_id)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter(name="clientIpPreservationEnabled")
    def client_ip_preservation_enabled(self) -> Optional[bool]:
        """
        Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. See the [AWS documentation](https://docs.aws.amazon.com/global-accelerator/latest/dg/preserve-client-ip-address.html) for more details. The default value is `false`.
        **Note:** When client IP address preservation is enabled, the Global Accelerator service creates an EC2 Security Group in the VPC named `GlobalAccelerator` that must be deleted (potentially outside of the provider) before the VPC will successfully delete. If this EC2 Security Group is not deleted, the provider will retry the VPC deletion for a few minutes before reporting a `DependencyViolation` error. This cannot be resolved by re-running the provider.
        """
        return pulumi.get(self, "client_ip_preservation_enabled")

    @property
    @pulumi.getter(name="endpointId")
    def endpoint_id(self) -> Optional[str]:
        """
        An ID for the endpoint. If the endpoint is a Network Load Balancer or Application Load Balancer, this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address, this is the Elastic IP address allocation ID.
        """
        return pulumi.get(self, "endpoint_id")

    @property
    @pulumi.getter
    def weight(self) -> Optional[int]:
        """
        The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify.
        """
        return pulumi.get(self, "weight")


@pulumi.output_type
class EndpointGroupPortOverride(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "endpointPort":
            suggest = "endpoint_port"
        elif key == "listenerPort":
            suggest = "listener_port"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointGroupPortOverride. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointGroupPortOverride.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointGroupPortOverride.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 endpoint_port: int,
                 listener_port: int):
        """
        :param int endpoint_port: The endpoint port that you want a listener port to be mapped to. This is the port on the endpoint, such as the Application Load Balancer or Amazon EC2 instance.
        :param int listener_port: The listener port that you want to map to a specific endpoint port. This is the port that user traffic arrives to the Global Accelerator on.
        """
        pulumi.set(__self__, "endpoint_port", endpoint_port)
        pulumi.set(__self__, "listener_port", listener_port)

    @property
    @pulumi.getter(name="endpointPort")
    def endpoint_port(self) -> int:
        """
        The endpoint port that you want a listener port to be mapped to. This is the port on the endpoint, such as the Application Load Balancer or Amazon EC2 instance.
        """
        return pulumi.get(self, "endpoint_port")

    @property
    @pulumi.getter(name="listenerPort")
    def listener_port(self) -> int:
        """
        The listener port that you want to map to a specific endpoint port. This is the port that user traffic arrives to the Global Accelerator on.
        """
        return pulumi.get(self, "listener_port")


@pulumi.output_type
class ListenerPortRange(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "fromPort":
            suggest = "from_port"
        elif key == "toPort":
            suggest = "to_port"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ListenerPortRange. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ListenerPortRange.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ListenerPortRange.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 from_port: Optional[int] = None,
                 to_port: Optional[int] = None):
        """
        :param int from_port: The first port in the range of ports, inclusive.
        :param int to_port: The last port in the range of ports, inclusive.
        """
        if from_port is not None:
            pulumi.set(__self__, "from_port", from_port)
        if to_port is not None:
            pulumi.set(__self__, "to_port", to_port)

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> Optional[int]:
        """
        The first port in the range of ports, inclusive.
        """
        return pulumi.get(self, "from_port")

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> Optional[int]:
        """
        The last port in the range of ports, inclusive.
        """
        return pulumi.get(self, "to_port")


@pulumi.output_type
class GetAcceleratorAttributeResult(dict):
    def __init__(__self__, *,
                 flow_logs_enabled: bool,
                 flow_logs_s3_bucket: str,
                 flow_logs_s3_prefix: str):
        pulumi.set(__self__, "flow_logs_enabled", flow_logs_enabled)
        pulumi.set(__self__, "flow_logs_s3_bucket", flow_logs_s3_bucket)
        pulumi.set(__self__, "flow_logs_s3_prefix", flow_logs_s3_prefix)

    @property
    @pulumi.getter(name="flowLogsEnabled")
    def flow_logs_enabled(self) -> bool:
        return pulumi.get(self, "flow_logs_enabled")

    @property
    @pulumi.getter(name="flowLogsS3Bucket")
    def flow_logs_s3_bucket(self) -> str:
        return pulumi.get(self, "flow_logs_s3_bucket")

    @property
    @pulumi.getter(name="flowLogsS3Prefix")
    def flow_logs_s3_prefix(self) -> str:
        return pulumi.get(self, "flow_logs_s3_prefix")


@pulumi.output_type
class GetAcceleratorIpSetResult(dict):
    def __init__(__self__, *,
                 ip_addresses: Sequence[str],
                 ip_family: str):
        pulumi.set(__self__, "ip_addresses", ip_addresses)
        pulumi.set(__self__, "ip_family", ip_family)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Sequence[str]:
        return pulumi.get(self, "ip_addresses")

    @property
    @pulumi.getter(name="ipFamily")
    def ip_family(self) -> str:
        return pulumi.get(self, "ip_family")


@pulumi.output_type
class GetCustomRoutingAcceleratorAttributeResult(dict):
    def __init__(__self__, *,
                 flow_logs_enabled: bool,
                 flow_logs_s3_bucket: str,
                 flow_logs_s3_prefix: str):
        pulumi.set(__self__, "flow_logs_enabled", flow_logs_enabled)
        pulumi.set(__self__, "flow_logs_s3_bucket", flow_logs_s3_bucket)
        pulumi.set(__self__, "flow_logs_s3_prefix", flow_logs_s3_prefix)

    @property
    @pulumi.getter(name="flowLogsEnabled")
    def flow_logs_enabled(self) -> bool:
        return pulumi.get(self, "flow_logs_enabled")

    @property
    @pulumi.getter(name="flowLogsS3Bucket")
    def flow_logs_s3_bucket(self) -> str:
        return pulumi.get(self, "flow_logs_s3_bucket")

    @property
    @pulumi.getter(name="flowLogsS3Prefix")
    def flow_logs_s3_prefix(self) -> str:
        return pulumi.get(self, "flow_logs_s3_prefix")


@pulumi.output_type
class GetCustomRoutingAcceleratorIpSetResult(dict):
    def __init__(__self__, *,
                 ip_addresses: Sequence[str],
                 ip_family: str):
        pulumi.set(__self__, "ip_addresses", ip_addresses)
        pulumi.set(__self__, "ip_family", ip_family)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Sequence[str]:
        return pulumi.get(self, "ip_addresses")

    @property
    @pulumi.getter(name="ipFamily")
    def ip_family(self) -> str:
        return pulumi.get(self, "ip_family")


