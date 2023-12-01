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
    'GetEmailIdentityResult',
    'AwaitableGetEmailIdentityResult',
    'get_email_identity',
    'get_email_identity_output',
]

@pulumi.output_type
class GetEmailIdentityResult:
    """
    A collection of values returned by getEmailIdentity.
    """
    def __init__(__self__, arn=None, email=None, id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if email and not isinstance(email, str):
            raise TypeError("Expected argument 'email' to be a str")
        pulumi.set(__self__, "email", email)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The ARN of the email identity.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def email(self) -> str:
        """
        Email identity.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetEmailIdentityResult(GetEmailIdentityResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEmailIdentityResult(
            arn=self.arn,
            email=self.email,
            id=self.id)


def get_email_identity(email: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEmailIdentityResult:
    """
    Retrieve the active SES email identity

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ses.get_email_identity(email="awesome@example.com")
    ```


    :param str email: Email identity.
    """
    __args__ = dict()
    __args__['email'] = email
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ses/getEmailIdentity:getEmailIdentity', __args__, opts=opts, typ=GetEmailIdentityResult).value

    return AwaitableGetEmailIdentityResult(
        arn=pulumi.get(__ret__, 'arn'),
        email=pulumi.get(__ret__, 'email'),
        id=pulumi.get(__ret__, 'id'))


@_utilities.lift_output_func(get_email_identity)
def get_email_identity_output(email: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEmailIdentityResult]:
    """
    Retrieve the active SES email identity

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ses.get_email_identity(email="awesome@example.com")
    ```


    :param str email: Email identity.
    """
    ...
