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
    'GetRealtimeLogConfigResult',
    'AwaitableGetRealtimeLogConfigResult',
    'get_realtime_log_config',
    'get_realtime_log_config_output',
]

@pulumi.output_type
class GetRealtimeLogConfigResult:
    """
    A collection of values returned by getRealtimeLogConfig.
    """
    def __init__(__self__, arn=None, endpoints=None, fields=None, id=None, name=None, sampling_rate=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if endpoints and not isinstance(endpoints, list):
            raise TypeError("Expected argument 'endpoints' to be a list")
        pulumi.set(__self__, "endpoints", endpoints)
        if fields and not isinstance(fields, list):
            raise TypeError("Expected argument 'fields' to be a list")
        pulumi.set(__self__, "fields", fields)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if sampling_rate and not isinstance(sampling_rate, int):
            raise TypeError("Expected argument 'sampling_rate' to be a int")
        pulumi.set(__self__, "sampling_rate", sampling_rate)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN (Amazon Resource Name) of the CloudFront real-time log configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def endpoints(self) -> Sequence['outputs.GetRealtimeLogConfigEndpointResult']:
        """
        (Required) Amazon Kinesis data streams where real-time log data is sent.
        """
        return pulumi.get(self, "endpoints")

    @property
    @pulumi.getter
    def fields(self) -> Sequence[str]:
        """
        (Required) Fields that are included in each real-time log record. See the [AWS documentation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/real-time-logs.html#understand-real-time-log-config-fields) for supported values.
        """
        return pulumi.get(self, "fields")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="samplingRate")
    def sampling_rate(self) -> int:
        """
        (Required) Sampling rate for this real-time log configuration. The sampling rate determines the percentage of viewer requests that are represented in the real-time log data. An integer between `1` and `100`, inclusive.
        """
        return pulumi.get(self, "sampling_rate")


class AwaitableGetRealtimeLogConfigResult(GetRealtimeLogConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRealtimeLogConfigResult(
            arn=self.arn,
            endpoints=self.endpoints,
            fields=self.fields,
            id=self.id,
            name=self.name,
            sampling_rate=self.sampling_rate)


def get_realtime_log_config(name: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRealtimeLogConfigResult:
    """
    Provides a CloudFront real-time log configuration resource.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.cloudfront.get_realtime_log_config(name="example")
    ```


    :param str name: Unique name to identify this real-time log configuration.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:cloudfront/getRealtimeLogConfig:getRealtimeLogConfig', __args__, opts=opts, typ=GetRealtimeLogConfigResult).value

    return AwaitableGetRealtimeLogConfigResult(
        arn=pulumi.get(__ret__, 'arn'),
        endpoints=pulumi.get(__ret__, 'endpoints'),
        fields=pulumi.get(__ret__, 'fields'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        sampling_rate=pulumi.get(__ret__, 'sampling_rate'))


@_utilities.lift_output_func(get_realtime_log_config)
def get_realtime_log_config_output(name: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRealtimeLogConfigResult]:
    """
    Provides a CloudFront real-time log configuration resource.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.cloudfront.get_realtime_log_config(name="example")
    ```


    :param str name: Unique name to identify this real-time log configuration.
    """
    ...
