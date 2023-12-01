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
    'GetQuicksightUserResult',
    'AwaitableGetQuicksightUserResult',
    'get_quicksight_user',
    'get_quicksight_user_output',
]

@pulumi.output_type
class GetQuicksightUserResult:
    """
    A collection of values returned by getQuicksightUser.
    """
    def __init__(__self__, active=None, arn=None, aws_account_id=None, email=None, id=None, identity_type=None, namespace=None, principal_id=None, user_name=None, user_role=None):
        if active and not isinstance(active, bool):
            raise TypeError("Expected argument 'active' to be a bool")
        pulumi.set(__self__, "active", active)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if aws_account_id and not isinstance(aws_account_id, str):
            raise TypeError("Expected argument 'aws_account_id' to be a str")
        pulumi.set(__self__, "aws_account_id", aws_account_id)
        if email and not isinstance(email, str):
            raise TypeError("Expected argument 'email' to be a str")
        pulumi.set(__self__, "email", email)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity_type and not isinstance(identity_type, str):
            raise TypeError("Expected argument 'identity_type' to be a str")
        pulumi.set(__self__, "identity_type", identity_type)
        if namespace and not isinstance(namespace, str):
            raise TypeError("Expected argument 'namespace' to be a str")
        pulumi.set(__self__, "namespace", namespace)
        if principal_id and not isinstance(principal_id, str):
            raise TypeError("Expected argument 'principal_id' to be a str")
        pulumi.set(__self__, "principal_id", principal_id)
        if user_name and not isinstance(user_name, str):
            raise TypeError("Expected argument 'user_name' to be a str")
        pulumi.set(__self__, "user_name", user_name)
        if user_role and not isinstance(user_role, str):
            raise TypeError("Expected argument 'user_role' to be a str")
        pulumi.set(__self__, "user_role", user_role)

    @property
    @pulumi.getter
    def active(self) -> bool:
        """
        The active status of user. When you create an Amazon QuickSight user that’s not an IAM user or an Active Directory user, that user is inactive until they sign in and provide a password.
        """
        return pulumi.get(self, "active")

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Amazon Resource Name (ARN) for the user.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> str:
        return pulumi.get(self, "aws_account_id")

    @property
    @pulumi.getter
    def email(self) -> str:
        """
        The user's email address.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="identityType")
    def identity_type(self) -> str:
        """
        The type of identity authentication used by the user.
        """
        return pulumi.get(self, "identity_type")

    @property
    @pulumi.getter
    def namespace(self) -> Optional[str]:
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal ID of the user.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> str:
        return pulumi.get(self, "user_name")

    @property
    @pulumi.getter(name="userRole")
    def user_role(self) -> str:
        """
        The Amazon QuickSight role for the user. The user role can be one of the following:.
        """
        return pulumi.get(self, "user_role")


class AwaitableGetQuicksightUserResult(GetQuicksightUserResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetQuicksightUserResult(
            active=self.active,
            arn=self.arn,
            aws_account_id=self.aws_account_id,
            email=self.email,
            id=self.id,
            identity_type=self.identity_type,
            namespace=self.namespace,
            principal_id=self.principal_id,
            user_name=self.user_name,
            user_role=self.user_role)


def get_quicksight_user(aws_account_id: Optional[str] = None,
                        namespace: Optional[str] = None,
                        user_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetQuicksightUserResult:
    """
    This data source can be used to fetch information about a specific
    QuickSight user. By using this data source, you can reference QuickSight user
    properties without having to hard code ARNs or unique IDs as input.

    ## Example Usage
    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.quicksight.get_quicksight_user(user_name="example")
    ```


    :param str aws_account_id: AWS account ID.
    :param str namespace: QuickSight namespace. Defaults to `default`.
    :param str user_name: The name of the user that you want to match.
           
           The following arguments are optional:
    """
    __args__ = dict()
    __args__['awsAccountId'] = aws_account_id
    __args__['namespace'] = namespace
    __args__['userName'] = user_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:quicksight/getQuicksightUser:getQuicksightUser', __args__, opts=opts, typ=GetQuicksightUserResult).value

    return AwaitableGetQuicksightUserResult(
        active=pulumi.get(__ret__, 'active'),
        arn=pulumi.get(__ret__, 'arn'),
        aws_account_id=pulumi.get(__ret__, 'aws_account_id'),
        email=pulumi.get(__ret__, 'email'),
        id=pulumi.get(__ret__, 'id'),
        identity_type=pulumi.get(__ret__, 'identity_type'),
        namespace=pulumi.get(__ret__, 'namespace'),
        principal_id=pulumi.get(__ret__, 'principal_id'),
        user_name=pulumi.get(__ret__, 'user_name'),
        user_role=pulumi.get(__ret__, 'user_role'))


@_utilities.lift_output_func(get_quicksight_user)
def get_quicksight_user_output(aws_account_id: Optional[pulumi.Input[Optional[str]]] = None,
                               namespace: Optional[pulumi.Input[Optional[str]]] = None,
                               user_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetQuicksightUserResult]:
    """
    This data source can be used to fetch information about a specific
    QuickSight user. By using this data source, you can reference QuickSight user
    properties without having to hard code ARNs or unique IDs as input.

    ## Example Usage
    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.quicksight.get_quicksight_user(user_name="example")
    ```


    :param str aws_account_id: AWS account ID.
    :param str namespace: QuickSight namespace. Defaults to `default`.
    :param str user_name: The name of the user that you want to match.
           
           The following arguments are optional:
    """
    ...
