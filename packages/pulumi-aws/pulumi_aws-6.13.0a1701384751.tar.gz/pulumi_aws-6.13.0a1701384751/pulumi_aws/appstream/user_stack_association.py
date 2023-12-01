# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['UserStackAssociationArgs', 'UserStackAssociation']

@pulumi.input_type
class UserStackAssociationArgs:
    def __init__(__self__, *,
                 authentication_type: pulumi.Input[str],
                 stack_name: pulumi.Input[str],
                 user_name: pulumi.Input[str],
                 send_email_notification: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a UserStackAssociation resource.
        :param pulumi.Input[str] authentication_type: Authentication type for the user.
        :param pulumi.Input[str] stack_name: Name of the stack that is associated with the user.
        :param pulumi.Input[str] user_name: Email address of the user who is associated with the stack.
               
               The following arguments are optional:
        :param pulumi.Input[bool] send_email_notification: Whether a welcome email is sent to a user after the user is created in the user pool.
        """
        pulumi.set(__self__, "authentication_type", authentication_type)
        pulumi.set(__self__, "stack_name", stack_name)
        pulumi.set(__self__, "user_name", user_name)
        if send_email_notification is not None:
            pulumi.set(__self__, "send_email_notification", send_email_notification)

    @property
    @pulumi.getter(name="authenticationType")
    def authentication_type(self) -> pulumi.Input[str]:
        """
        Authentication type for the user.
        """
        return pulumi.get(self, "authentication_type")

    @authentication_type.setter
    def authentication_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "authentication_type", value)

    @property
    @pulumi.getter(name="stackName")
    def stack_name(self) -> pulumi.Input[str]:
        """
        Name of the stack that is associated with the user.
        """
        return pulumi.get(self, "stack_name")

    @stack_name.setter
    def stack_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "stack_name", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Input[str]:
        """
        Email address of the user who is associated with the stack.

        The following arguments are optional:
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_name", value)

    @property
    @pulumi.getter(name="sendEmailNotification")
    def send_email_notification(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether a welcome email is sent to a user after the user is created in the user pool.
        """
        return pulumi.get(self, "send_email_notification")

    @send_email_notification.setter
    def send_email_notification(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_email_notification", value)


@pulumi.input_type
class _UserStackAssociationState:
    def __init__(__self__, *,
                 authentication_type: Optional[pulumi.Input[str]] = None,
                 send_email_notification: Optional[pulumi.Input[bool]] = None,
                 stack_name: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering UserStackAssociation resources.
        :param pulumi.Input[str] authentication_type: Authentication type for the user.
        :param pulumi.Input[bool] send_email_notification: Whether a welcome email is sent to a user after the user is created in the user pool.
        :param pulumi.Input[str] stack_name: Name of the stack that is associated with the user.
        :param pulumi.Input[str] user_name: Email address of the user who is associated with the stack.
               
               The following arguments are optional:
        """
        if authentication_type is not None:
            pulumi.set(__self__, "authentication_type", authentication_type)
        if send_email_notification is not None:
            pulumi.set(__self__, "send_email_notification", send_email_notification)
        if stack_name is not None:
            pulumi.set(__self__, "stack_name", stack_name)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="authenticationType")
    def authentication_type(self) -> Optional[pulumi.Input[str]]:
        """
        Authentication type for the user.
        """
        return pulumi.get(self, "authentication_type")

    @authentication_type.setter
    def authentication_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authentication_type", value)

    @property
    @pulumi.getter(name="sendEmailNotification")
    def send_email_notification(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether a welcome email is sent to a user after the user is created in the user pool.
        """
        return pulumi.get(self, "send_email_notification")

    @send_email_notification.setter
    def send_email_notification(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_email_notification", value)

    @property
    @pulumi.getter(name="stackName")
    def stack_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the stack that is associated with the user.
        """
        return pulumi.get(self, "stack_name")

    @stack_name.setter
    def stack_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stack_name", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        Email address of the user who is associated with the stack.

        The following arguments are optional:
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)


class UserStackAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication_type: Optional[pulumi.Input[str]] = None,
                 send_email_notification: Optional[pulumi.Input[bool]] = None,
                 stack_name: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an AppStream User Stack association.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test_stack = aws.appstream.Stack("testStack")
        test_user = aws.appstream.User("testUser",
            authentication_type="USERPOOL",
            user_name="EMAIL")
        test_user_stack_association = aws.appstream.UserStackAssociation("testUserStackAssociation",
            authentication_type=test_user.authentication_type,
            stack_name=test_stack.name,
            user_name=test_user.user_name)
        ```

        ## Import

        Using `pulumi import`, import AppStream User Stack Association using the `user_name`, `authentication_type`, and `stack_name`, separated by a slash (`/`). For example:

        ```sh
         $ pulumi import aws:appstream/userStackAssociation:UserStackAssociation example userName/auhtenticationType/stackName
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication_type: Authentication type for the user.
        :param pulumi.Input[bool] send_email_notification: Whether a welcome email is sent to a user after the user is created in the user pool.
        :param pulumi.Input[str] stack_name: Name of the stack that is associated with the user.
        :param pulumi.Input[str] user_name: Email address of the user who is associated with the stack.
               
               The following arguments are optional:
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserStackAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an AppStream User Stack association.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test_stack = aws.appstream.Stack("testStack")
        test_user = aws.appstream.User("testUser",
            authentication_type="USERPOOL",
            user_name="EMAIL")
        test_user_stack_association = aws.appstream.UserStackAssociation("testUserStackAssociation",
            authentication_type=test_user.authentication_type,
            stack_name=test_stack.name,
            user_name=test_user.user_name)
        ```

        ## Import

        Using `pulumi import`, import AppStream User Stack Association using the `user_name`, `authentication_type`, and `stack_name`, separated by a slash (`/`). For example:

        ```sh
         $ pulumi import aws:appstream/userStackAssociation:UserStackAssociation example userName/auhtenticationType/stackName
        ```

        :param str resource_name: The name of the resource.
        :param UserStackAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserStackAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication_type: Optional[pulumi.Input[str]] = None,
                 send_email_notification: Optional[pulumi.Input[bool]] = None,
                 stack_name: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserStackAssociationArgs.__new__(UserStackAssociationArgs)

            if authentication_type is None and not opts.urn:
                raise TypeError("Missing required property 'authentication_type'")
            __props__.__dict__["authentication_type"] = authentication_type
            __props__.__dict__["send_email_notification"] = send_email_notification
            if stack_name is None and not opts.urn:
                raise TypeError("Missing required property 'stack_name'")
            __props__.__dict__["stack_name"] = stack_name
            if user_name is None and not opts.urn:
                raise TypeError("Missing required property 'user_name'")
            __props__.__dict__["user_name"] = user_name
        super(UserStackAssociation, __self__).__init__(
            'aws:appstream/userStackAssociation:UserStackAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            authentication_type: Optional[pulumi.Input[str]] = None,
            send_email_notification: Optional[pulumi.Input[bool]] = None,
            stack_name: Optional[pulumi.Input[str]] = None,
            user_name: Optional[pulumi.Input[str]] = None) -> 'UserStackAssociation':
        """
        Get an existing UserStackAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication_type: Authentication type for the user.
        :param pulumi.Input[bool] send_email_notification: Whether a welcome email is sent to a user after the user is created in the user pool.
        :param pulumi.Input[str] stack_name: Name of the stack that is associated with the user.
        :param pulumi.Input[str] user_name: Email address of the user who is associated with the stack.
               
               The following arguments are optional:
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserStackAssociationState.__new__(_UserStackAssociationState)

        __props__.__dict__["authentication_type"] = authentication_type
        __props__.__dict__["send_email_notification"] = send_email_notification
        __props__.__dict__["stack_name"] = stack_name
        __props__.__dict__["user_name"] = user_name
        return UserStackAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="authenticationType")
    def authentication_type(self) -> pulumi.Output[str]:
        """
        Authentication type for the user.
        """
        return pulumi.get(self, "authentication_type")

    @property
    @pulumi.getter(name="sendEmailNotification")
    def send_email_notification(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether a welcome email is sent to a user after the user is created in the user pool.
        """
        return pulumi.get(self, "send_email_notification")

    @property
    @pulumi.getter(name="stackName")
    def stack_name(self) -> pulumi.Output[str]:
        """
        Name of the stack that is associated with the user.
        """
        return pulumi.get(self, "stack_name")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Output[str]:
        """
        Email address of the user who is associated with the stack.

        The following arguments are optional:
        """
        return pulumi.get(self, "user_name")

