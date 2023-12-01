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
    'GetEncryptionByDefaultResult',
    'AwaitableGetEncryptionByDefaultResult',
    'get_encryption_by_default',
    'get_encryption_by_default_output',
]

@pulumi.output_type
class GetEncryptionByDefaultResult:
    """
    A collection of values returned by getEncryptionByDefault.
    """
    def __init__(__self__, enabled=None, id=None):
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Whether or not default EBS encryption is enabled. Returns as `true` or `false`.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetEncryptionByDefaultResult(GetEncryptionByDefaultResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEncryptionByDefaultResult(
            enabled=self.enabled,
            id=self.id)


def get_encryption_by_default(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEncryptionByDefaultResult:
    """
    Provides a way to check whether default EBS encryption is enabled for your AWS account in the current AWS region.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    current = aws.ebs.get_encryption_by_default()
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ebs/getEncryptionByDefault:getEncryptionByDefault', __args__, opts=opts, typ=GetEncryptionByDefaultResult).value

    return AwaitableGetEncryptionByDefaultResult(
        enabled=pulumi.get(__ret__, 'enabled'),
        id=pulumi.get(__ret__, 'id'))


@_utilities.lift_output_func(get_encryption_by_default)
def get_encryption_by_default_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEncryptionByDefaultResult]:
    """
    Provides a way to check whether default EBS encryption is enabled for your AWS account in the current AWS region.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    current = aws.ebs.get_encryption_by_default()
    ```
    """
    ...
