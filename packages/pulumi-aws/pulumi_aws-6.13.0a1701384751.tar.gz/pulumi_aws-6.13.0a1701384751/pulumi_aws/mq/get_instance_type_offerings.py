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
    'GetInstanceTypeOfferingsResult',
    'AwaitableGetInstanceTypeOfferingsResult',
    'get_instance_type_offerings',
    'get_instance_type_offerings_output',
]

@pulumi.output_type
class GetInstanceTypeOfferingsResult:
    """
    A collection of values returned by getInstanceTypeOfferings.
    """
    def __init__(__self__, broker_instance_options=None, engine_type=None, host_instance_type=None, id=None, storage_type=None):
        if broker_instance_options and not isinstance(broker_instance_options, list):
            raise TypeError("Expected argument 'broker_instance_options' to be a list")
        pulumi.set(__self__, "broker_instance_options", broker_instance_options)
        if engine_type and not isinstance(engine_type, str):
            raise TypeError("Expected argument 'engine_type' to be a str")
        pulumi.set(__self__, "engine_type", engine_type)
        if host_instance_type and not isinstance(host_instance_type, str):
            raise TypeError("Expected argument 'host_instance_type' to be a str")
        pulumi.set(__self__, "host_instance_type", host_instance_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if storage_type and not isinstance(storage_type, str):
            raise TypeError("Expected argument 'storage_type' to be a str")
        pulumi.set(__self__, "storage_type", storage_type)

    @property
    @pulumi.getter(name="brokerInstanceOptions")
    def broker_instance_options(self) -> Sequence['outputs.GetInstanceTypeOfferingsBrokerInstanceOptionResult']:
        """
        Option for host instance type. See Broker Instance Options below.
        """
        return pulumi.get(self, "broker_instance_options")

    @property
    @pulumi.getter(name="engineType")
    def engine_type(self) -> Optional[str]:
        """
        Broker's engine type.
        """
        return pulumi.get(self, "engine_type")

    @property
    @pulumi.getter(name="hostInstanceType")
    def host_instance_type(self) -> Optional[str]:
        """
        Broker's instance type.
        """
        return pulumi.get(self, "host_instance_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="storageType")
    def storage_type(self) -> Optional[str]:
        """
        Broker's storage type.
        """
        return pulumi.get(self, "storage_type")


class AwaitableGetInstanceTypeOfferingsResult(GetInstanceTypeOfferingsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceTypeOfferingsResult(
            broker_instance_options=self.broker_instance_options,
            engine_type=self.engine_type,
            host_instance_type=self.host_instance_type,
            id=self.id,
            storage_type=self.storage_type)


def get_instance_type_offerings(engine_type: Optional[str] = None,
                                host_instance_type: Optional[str] = None,
                                storage_type: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstanceTypeOfferingsResult:
    """
    Provides information about a MQ Broker Instance Offerings.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    empty = aws.mq.get_instance_type_offerings()
    engine = aws.mq.get_instance_type_offerings(engine_type="ACTIVEMQ")
    storage = aws.mq.get_instance_type_offerings(storage_type="EBS")
    instance = aws.mq.get_instance_type_offerings(host_instance_type="mq.m5.large")
    all = aws.mq.get_instance_type_offerings(engine_type="ACTIVEMQ",
        host_instance_type="mq.m5.large",
        storage_type="EBS")
    ```


    :param str engine_type: Filter response by engine type.
    :param str host_instance_type: Filter response by host instance type.
    :param str storage_type: Filter response by storage type.
    """
    __args__ = dict()
    __args__['engineType'] = engine_type
    __args__['hostInstanceType'] = host_instance_type
    __args__['storageType'] = storage_type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:mq/getInstanceTypeOfferings:getInstanceTypeOfferings', __args__, opts=opts, typ=GetInstanceTypeOfferingsResult).value

    return AwaitableGetInstanceTypeOfferingsResult(
        broker_instance_options=pulumi.get(__ret__, 'broker_instance_options'),
        engine_type=pulumi.get(__ret__, 'engine_type'),
        host_instance_type=pulumi.get(__ret__, 'host_instance_type'),
        id=pulumi.get(__ret__, 'id'),
        storage_type=pulumi.get(__ret__, 'storage_type'))


@_utilities.lift_output_func(get_instance_type_offerings)
def get_instance_type_offerings_output(engine_type: Optional[pulumi.Input[Optional[str]]] = None,
                                       host_instance_type: Optional[pulumi.Input[Optional[str]]] = None,
                                       storage_type: Optional[pulumi.Input[Optional[str]]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstanceTypeOfferingsResult]:
    """
    Provides information about a MQ Broker Instance Offerings.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    empty = aws.mq.get_instance_type_offerings()
    engine = aws.mq.get_instance_type_offerings(engine_type="ACTIVEMQ")
    storage = aws.mq.get_instance_type_offerings(storage_type="EBS")
    instance = aws.mq.get_instance_type_offerings(host_instance_type="mq.m5.large")
    all = aws.mq.get_instance_type_offerings(engine_type="ACTIVEMQ",
        host_instance_type="mq.m5.large",
        storage_type="EBS")
    ```


    :param str engine_type: Filter response by engine type.
    :param str host_instance_type: Filter response by host instance type.
    :param str storage_type: Filter response by storage type.
    """
    ...
