# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['UserPolicyArgs', 'UserPolicy']

@pulumi.input_type
class UserPolicyArgs:
    def __init__(__self__, *,
                 policy: pulumi.Input[str],
                 user: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a UserPolicy resource.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string.
        :param pulumi.Input[str] user: IAM user to which to attach this policy.
        :param pulumi.Input[str] name: The name of the policy. If omitted, the provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        pulumi.set(__self__, "policy", policy)
        pulumi.set(__self__, "user", user)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if name_prefix is not None:
            pulumi.set(__self__, "name_prefix", name_prefix)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Input[str]:
        """
        The policy document. This is a JSON formatted string.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter
    def user(self) -> pulumi.Input[str]:
        """
        IAM user to which to attach this policy.
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: pulumi.Input[str]):
        pulumi.set(self, "user", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the policy. If omitted, the provider will assign a random, unique name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="namePrefix")
    def name_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, "name_prefix")

    @name_prefix.setter
    def name_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name_prefix", value)


@pulumi.input_type
class _UserPolicyState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering UserPolicy resources.
        :param pulumi.Input[str] name: The name of the policy. If omitted, the provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string.
        :param pulumi.Input[str] user: IAM user to which to attach this policy.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if name_prefix is not None:
            pulumi.set(__self__, "name_prefix", name_prefix)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if user is not None:
            pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the policy. If omitted, the provider will assign a random, unique name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="namePrefix")
    def name_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, "name_prefix")

    @name_prefix.setter
    def name_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name_prefix", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        The policy document. This is a JSON formatted string.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter
    def user(self) -> Optional[pulumi.Input[str]]:
        """
        IAM user to which to attach this policy.
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user", value)


class UserPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an IAM policy attached to a user.

        ## Example Usage

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        lb_user = aws.iam.User("lbUser", path="/system/")
        lb_ro = aws.iam.UserPolicy("lbRo",
            user=lb_user.name,
            policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": ["ec2:Describe*"],
                    "Effect": "Allow",
                    "Resource": "*",
                }],
            }))
        lb_access_key = aws.iam.AccessKey("lbAccessKey", user=lb_user.name)
        ```

        ## Import

        Using `pulumi import`, import IAM User Policies using the `user_name:user_policy_name`. For example:

        ```sh
         $ pulumi import aws:iam/userPolicy:UserPolicy mypolicy user_of_mypolicy_name:mypolicy_name
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the policy. If omitted, the provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string.
        :param pulumi.Input[str] user: IAM user to which to attach this policy.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an IAM policy attached to a user.

        ## Example Usage

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        lb_user = aws.iam.User("lbUser", path="/system/")
        lb_ro = aws.iam.UserPolicy("lbRo",
            user=lb_user.name,
            policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": ["ec2:Describe*"],
                    "Effect": "Allow",
                    "Resource": "*",
                }],
            }))
        lb_access_key = aws.iam.AccessKey("lbAccessKey", user=lb_user.name)
        ```

        ## Import

        Using `pulumi import`, import IAM User Policies using the `user_name:user_policy_name`. For example:

        ```sh
         $ pulumi import aws:iam/userPolicy:UserPolicy mypolicy user_of_mypolicy_name:mypolicy_name
        ```

        :param str resource_name: The name of the resource.
        :param UserPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserPolicyArgs.__new__(UserPolicyArgs)

            __props__.__dict__["name"] = name
            __props__.__dict__["name_prefix"] = name_prefix
            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__["policy"] = policy
            if user is None and not opts.urn:
                raise TypeError("Missing required property 'user'")
            __props__.__dict__["user"] = user
        super(UserPolicy, __self__).__init__(
            'aws:iam/userPolicy:UserPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            name_prefix: Optional[pulumi.Input[str]] = None,
            policy: Optional[pulumi.Input[str]] = None,
            user: Optional[pulumi.Input[str]] = None) -> 'UserPolicy':
        """
        Get an existing UserPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the policy. If omitted, the provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string.
        :param pulumi.Input[str] user: IAM user to which to attach this policy.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserPolicyState.__new__(_UserPolicyState)

        __props__.__dict__["name"] = name
        __props__.__dict__["name_prefix"] = name_prefix
        __props__.__dict__["policy"] = policy
        __props__.__dict__["user"] = user
        return UserPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the policy. If omitted, the provider will assign a random, unique name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namePrefix")
    def name_prefix(self) -> pulumi.Output[str]:
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, "name_prefix")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        The policy document. This is a JSON formatted string.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter
    def user(self) -> pulumi.Output[str]:
        """
        IAM user to which to attach this policy.
        """
        return pulumi.get(self, "user")

