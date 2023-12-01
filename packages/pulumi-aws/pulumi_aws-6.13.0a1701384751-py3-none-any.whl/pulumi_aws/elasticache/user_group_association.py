# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['UserGroupAssociationArgs', 'UserGroupAssociation']

@pulumi.input_type
class UserGroupAssociationArgs:
    def __init__(__self__, *,
                 user_group_id: pulumi.Input[str],
                 user_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a UserGroupAssociation resource.
        :param pulumi.Input[str] user_group_id: ID of the user group.
        :param pulumi.Input[str] user_id: ID of the user to associated with the user group.
        """
        pulumi.set(__self__, "user_group_id", user_group_id)
        pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter(name="userGroupId")
    def user_group_id(self) -> pulumi.Input[str]:
        """
        ID of the user group.
        """
        return pulumi.get(self, "user_group_id")

    @user_group_id.setter
    def user_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_group_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Input[str]:
        """
        ID of the user to associated with the user group.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_id", value)


@pulumi.input_type
class _UserGroupAssociationState:
    def __init__(__self__, *,
                 user_group_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering UserGroupAssociation resources.
        :param pulumi.Input[str] user_group_id: ID of the user group.
        :param pulumi.Input[str] user_id: ID of the user to associated with the user group.
        """
        if user_group_id is not None:
            pulumi.set(__self__, "user_group_id", user_group_id)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter(name="userGroupId")
    def user_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the user group.
        """
        return pulumi.get(self, "user_group_id")

    @user_group_id.setter
    def user_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_group_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the user to associated with the user group.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_id", value)


class UserGroupAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 user_group_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Associate an existing ElastiCache user and an existing user group.

        > **NOTE:** The provider will detect changes in the `elasticache.UserGroup` since `elasticache.UserGroupAssociation` changes the user IDs associated with the user group. You can ignore these changes with the `ignore_changes` option as shown in the example.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        default = aws.elasticache.User("default",
            user_id="defaultUserID",
            user_name="default",
            access_string="on ~app::* -@all +@read +@hash +@bitmap +@geo -setbit -bitfield -hset -hsetnx -hmset -hincrby -hincrbyfloat -hdel -bitop -geoadd -georadius -georadiusbymember",
            engine="REDIS",
            passwords=["password123456789"])
        example_user_group = aws.elasticache.UserGroup("exampleUserGroup",
            engine="REDIS",
            user_group_id="userGroupId",
            user_ids=[default.user_id])
        example_user = aws.elasticache.User("exampleUser",
            user_id="exampleUserID",
            user_name="exampleuser",
            access_string="on ~app::* -@all +@read +@hash +@bitmap +@geo -setbit -bitfield -hset -hsetnx -hmset -hincrby -hincrbyfloat -hdel -bitop -geoadd -georadius -georadiusbymember",
            engine="REDIS",
            passwords=["password123456789"])
        example_user_group_association = aws.elasticache.UserGroupAssociation("exampleUserGroupAssociation",
            user_group_id=example_user_group.user_group_id,
            user_id=example_user.user_id)
        ```

        ## Import

        Using `pulumi import`, import ElastiCache user group associations using the `user_group_id` and `user_id`. For example:

        ```sh
         $ pulumi import aws:elasticache/userGroupAssociation:UserGroupAssociation example userGoupId1,userId
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] user_group_id: ID of the user group.
        :param pulumi.Input[str] user_id: ID of the user to associated with the user group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserGroupAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Associate an existing ElastiCache user and an existing user group.

        > **NOTE:** The provider will detect changes in the `elasticache.UserGroup` since `elasticache.UserGroupAssociation` changes the user IDs associated with the user group. You can ignore these changes with the `ignore_changes` option as shown in the example.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        default = aws.elasticache.User("default",
            user_id="defaultUserID",
            user_name="default",
            access_string="on ~app::* -@all +@read +@hash +@bitmap +@geo -setbit -bitfield -hset -hsetnx -hmset -hincrby -hincrbyfloat -hdel -bitop -geoadd -georadius -georadiusbymember",
            engine="REDIS",
            passwords=["password123456789"])
        example_user_group = aws.elasticache.UserGroup("exampleUserGroup",
            engine="REDIS",
            user_group_id="userGroupId",
            user_ids=[default.user_id])
        example_user = aws.elasticache.User("exampleUser",
            user_id="exampleUserID",
            user_name="exampleuser",
            access_string="on ~app::* -@all +@read +@hash +@bitmap +@geo -setbit -bitfield -hset -hsetnx -hmset -hincrby -hincrbyfloat -hdel -bitop -geoadd -georadius -georadiusbymember",
            engine="REDIS",
            passwords=["password123456789"])
        example_user_group_association = aws.elasticache.UserGroupAssociation("exampleUserGroupAssociation",
            user_group_id=example_user_group.user_group_id,
            user_id=example_user.user_id)
        ```

        ## Import

        Using `pulumi import`, import ElastiCache user group associations using the `user_group_id` and `user_id`. For example:

        ```sh
         $ pulumi import aws:elasticache/userGroupAssociation:UserGroupAssociation example userGoupId1,userId
        ```

        :param str resource_name: The name of the resource.
        :param UserGroupAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserGroupAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 user_group_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserGroupAssociationArgs.__new__(UserGroupAssociationArgs)

            if user_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_group_id'")
            __props__.__dict__["user_group_id"] = user_group_id
            if user_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_id'")
            __props__.__dict__["user_id"] = user_id
        super(UserGroupAssociation, __self__).__init__(
            'aws:elasticache/userGroupAssociation:UserGroupAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            user_group_id: Optional[pulumi.Input[str]] = None,
            user_id: Optional[pulumi.Input[str]] = None) -> 'UserGroupAssociation':
        """
        Get an existing UserGroupAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] user_group_id: ID of the user group.
        :param pulumi.Input[str] user_id: ID of the user to associated with the user group.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserGroupAssociationState.__new__(_UserGroupAssociationState)

        __props__.__dict__["user_group_id"] = user_group_id
        __props__.__dict__["user_id"] = user_id
        return UserGroupAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="userGroupId")
    def user_group_id(self) -> pulumi.Output[str]:
        """
        ID of the user group.
        """
        return pulumi.get(self, "user_group_id")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[str]:
        """
        ID of the user to associated with the user group.
        """
        return pulumi.get(self, "user_id")

