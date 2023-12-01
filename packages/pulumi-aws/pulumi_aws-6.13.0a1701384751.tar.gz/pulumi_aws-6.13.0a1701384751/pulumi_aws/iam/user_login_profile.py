# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['UserLoginProfileArgs', 'UserLoginProfile']

@pulumi.input_type
class UserLoginProfileArgs:
    def __init__(__self__, *,
                 user: pulumi.Input[str],
                 password_length: Optional[pulumi.Input[int]] = None,
                 password_reset_required: Optional[pulumi.Input[bool]] = None,
                 pgp_key: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a UserLoginProfile resource.
        :param pulumi.Input[str] user: The IAM user's name.
        :param pulumi.Input[int] password_length: The length of the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument. Default value is `20`.
        :param pulumi.Input[bool] password_reset_required: Whether the user should be forced to reset the generated password on resource creation. Only applies on resource creation.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:username`. Only applies on resource creation. Drift detection is not possible with this argument.
        """
        pulumi.set(__self__, "user", user)
        if password_length is not None:
            pulumi.set(__self__, "password_length", password_length)
        if password_reset_required is not None:
            pulumi.set(__self__, "password_reset_required", password_reset_required)
        if pgp_key is not None:
            pulumi.set(__self__, "pgp_key", pgp_key)

    @property
    @pulumi.getter
    def user(self) -> pulumi.Input[str]:
        """
        The IAM user's name.
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: pulumi.Input[str]):
        pulumi.set(self, "user", value)

    @property
    @pulumi.getter(name="passwordLength")
    def password_length(self) -> Optional[pulumi.Input[int]]:
        """
        The length of the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument. Default value is `20`.
        """
        return pulumi.get(self, "password_length")

    @password_length.setter
    def password_length(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "password_length", value)

    @property
    @pulumi.getter(name="passwordResetRequired")
    def password_reset_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the user should be forced to reset the generated password on resource creation. Only applies on resource creation.
        """
        return pulumi.get(self, "password_reset_required")

    @password_reset_required.setter
    def password_reset_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "password_reset_required", value)

    @property
    @pulumi.getter(name="pgpKey")
    def pgp_key(self) -> Optional[pulumi.Input[str]]:
        """
        Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:username`. Only applies on resource creation. Drift detection is not possible with this argument.
        """
        return pulumi.get(self, "pgp_key")

    @pgp_key.setter
    def pgp_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pgp_key", value)


@pulumi.input_type
class _UserLoginProfileState:
    def __init__(__self__, *,
                 encrypted_password: Optional[pulumi.Input[str]] = None,
                 key_fingerprint: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 password_length: Optional[pulumi.Input[int]] = None,
                 password_reset_required: Optional[pulumi.Input[bool]] = None,
                 pgp_key: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering UserLoginProfile resources.
        :param pulumi.Input[str] encrypted_password: The encrypted password, base64 encoded. Only available if password was handled on resource creation, not import.
        :param pulumi.Input[str] key_fingerprint: The fingerprint of the PGP key used to encrypt the password. Only available if password was handled on this provider resource creation, not import.
        :param pulumi.Input[str] password: The plain text password, only available when `pgp_key` is not provided.
        :param pulumi.Input[int] password_length: The length of the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument. Default value is `20`.
        :param pulumi.Input[bool] password_reset_required: Whether the user should be forced to reset the generated password on resource creation. Only applies on resource creation.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:username`. Only applies on resource creation. Drift detection is not possible with this argument.
        :param pulumi.Input[str] user: The IAM user's name.
        """
        if encrypted_password is not None:
            pulumi.set(__self__, "encrypted_password", encrypted_password)
        if key_fingerprint is not None:
            pulumi.set(__self__, "key_fingerprint", key_fingerprint)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if password_length is not None:
            pulumi.set(__self__, "password_length", password_length)
        if password_reset_required is not None:
            pulumi.set(__self__, "password_reset_required", password_reset_required)
        if pgp_key is not None:
            pulumi.set(__self__, "pgp_key", pgp_key)
        if user is not None:
            pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter(name="encryptedPassword")
    def encrypted_password(self) -> Optional[pulumi.Input[str]]:
        """
        The encrypted password, base64 encoded. Only available if password was handled on resource creation, not import.
        """
        return pulumi.get(self, "encrypted_password")

    @encrypted_password.setter
    def encrypted_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encrypted_password", value)

    @property
    @pulumi.getter(name="keyFingerprint")
    def key_fingerprint(self) -> Optional[pulumi.Input[str]]:
        """
        The fingerprint of the PGP key used to encrypt the password. Only available if password was handled on this provider resource creation, not import.
        """
        return pulumi.get(self, "key_fingerprint")

    @key_fingerprint.setter
    def key_fingerprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_fingerprint", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The plain text password, only available when `pgp_key` is not provided.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="passwordLength")
    def password_length(self) -> Optional[pulumi.Input[int]]:
        """
        The length of the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument. Default value is `20`.
        """
        return pulumi.get(self, "password_length")

    @password_length.setter
    def password_length(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "password_length", value)

    @property
    @pulumi.getter(name="passwordResetRequired")
    def password_reset_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the user should be forced to reset the generated password on resource creation. Only applies on resource creation.
        """
        return pulumi.get(self, "password_reset_required")

    @password_reset_required.setter
    def password_reset_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "password_reset_required", value)

    @property
    @pulumi.getter(name="pgpKey")
    def pgp_key(self) -> Optional[pulumi.Input[str]]:
        """
        Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:username`. Only applies on resource creation. Drift detection is not possible with this argument.
        """
        return pulumi.get(self, "pgp_key")

    @pgp_key.setter
    def pgp_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pgp_key", value)

    @property
    @pulumi.getter
    def user(self) -> Optional[pulumi.Input[str]]:
        """
        The IAM user's name.
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user", value)


class UserLoginProfile(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 password_length: Optional[pulumi.Input[int]] = None,
                 password_reset_required: Optional[pulumi.Input[bool]] = None,
                 pgp_key: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an IAM User Login Profile with limited support for password creation during this provider resource creation. Uses PGP to encrypt the password for safe transport to the user. PGP keys can be obtained from Keybase.

        > To reset an IAM User login password via this provider, you can use delete and recreate this resource or change any of the arguments.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_user = aws.iam.User("exampleUser",
            path="/",
            force_destroy=True)
        example_user_login_profile = aws.iam.UserLoginProfile("exampleUserLoginProfile",
            user=example_user.name,
            pgp_key="keybase:some_person_that_exists")
        pulumi.export("password", example_user_login_profile.encrypted_password)
        ```

        ## Import

        Using `pulumi import`, import IAM User Login Profiles without password information via the IAM User name. For example:

        ```sh
         $ pulumi import aws:iam/userLoginProfile:UserLoginProfile example myusername
        ```
         Since Pulumi has no method to read the PGP or password information during import, use the resource options `ignore_changes` argument to ignore them (unless you want to recreate a password). For example:

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] password_length: The length of the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument. Default value is `20`.
        :param pulumi.Input[bool] password_reset_required: Whether the user should be forced to reset the generated password on resource creation. Only applies on resource creation.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:username`. Only applies on resource creation. Drift detection is not possible with this argument.
        :param pulumi.Input[str] user: The IAM user's name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserLoginProfileArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an IAM User Login Profile with limited support for password creation during this provider resource creation. Uses PGP to encrypt the password for safe transport to the user. PGP keys can be obtained from Keybase.

        > To reset an IAM User login password via this provider, you can use delete and recreate this resource or change any of the arguments.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_user = aws.iam.User("exampleUser",
            path="/",
            force_destroy=True)
        example_user_login_profile = aws.iam.UserLoginProfile("exampleUserLoginProfile",
            user=example_user.name,
            pgp_key="keybase:some_person_that_exists")
        pulumi.export("password", example_user_login_profile.encrypted_password)
        ```

        ## Import

        Using `pulumi import`, import IAM User Login Profiles without password information via the IAM User name. For example:

        ```sh
         $ pulumi import aws:iam/userLoginProfile:UserLoginProfile example myusername
        ```
         Since Pulumi has no method to read the PGP or password information during import, use the resource options `ignore_changes` argument to ignore them (unless you want to recreate a password). For example:

        :param str resource_name: The name of the resource.
        :param UserLoginProfileArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserLoginProfileArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 password_length: Optional[pulumi.Input[int]] = None,
                 password_reset_required: Optional[pulumi.Input[bool]] = None,
                 pgp_key: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserLoginProfileArgs.__new__(UserLoginProfileArgs)

            __props__.__dict__["password_length"] = password_length
            __props__.__dict__["password_reset_required"] = password_reset_required
            __props__.__dict__["pgp_key"] = pgp_key
            if user is None and not opts.urn:
                raise TypeError("Missing required property 'user'")
            __props__.__dict__["user"] = user
            __props__.__dict__["encrypted_password"] = None
            __props__.__dict__["key_fingerprint"] = None
            __props__.__dict__["password"] = None
        super(UserLoginProfile, __self__).__init__(
            'aws:iam/userLoginProfile:UserLoginProfile',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            encrypted_password: Optional[pulumi.Input[str]] = None,
            key_fingerprint: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            password_length: Optional[pulumi.Input[int]] = None,
            password_reset_required: Optional[pulumi.Input[bool]] = None,
            pgp_key: Optional[pulumi.Input[str]] = None,
            user: Optional[pulumi.Input[str]] = None) -> 'UserLoginProfile':
        """
        Get an existing UserLoginProfile resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] encrypted_password: The encrypted password, base64 encoded. Only available if password was handled on resource creation, not import.
        :param pulumi.Input[str] key_fingerprint: The fingerprint of the PGP key used to encrypt the password. Only available if password was handled on this provider resource creation, not import.
        :param pulumi.Input[str] password: The plain text password, only available when `pgp_key` is not provided.
        :param pulumi.Input[int] password_length: The length of the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument. Default value is `20`.
        :param pulumi.Input[bool] password_reset_required: Whether the user should be forced to reset the generated password on resource creation. Only applies on resource creation.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:username`. Only applies on resource creation. Drift detection is not possible with this argument.
        :param pulumi.Input[str] user: The IAM user's name.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserLoginProfileState.__new__(_UserLoginProfileState)

        __props__.__dict__["encrypted_password"] = encrypted_password
        __props__.__dict__["key_fingerprint"] = key_fingerprint
        __props__.__dict__["password"] = password
        __props__.__dict__["password_length"] = password_length
        __props__.__dict__["password_reset_required"] = password_reset_required
        __props__.__dict__["pgp_key"] = pgp_key
        __props__.__dict__["user"] = user
        return UserLoginProfile(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="encryptedPassword")
    def encrypted_password(self) -> pulumi.Output[str]:
        """
        The encrypted password, base64 encoded. Only available if password was handled on resource creation, not import.
        """
        return pulumi.get(self, "encrypted_password")

    @property
    @pulumi.getter(name="keyFingerprint")
    def key_fingerprint(self) -> pulumi.Output[str]:
        """
        The fingerprint of the PGP key used to encrypt the password. Only available if password was handled on this provider resource creation, not import.
        """
        return pulumi.get(self, "key_fingerprint")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[str]:
        """
        The plain text password, only available when `pgp_key` is not provided.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="passwordLength")
    def password_length(self) -> pulumi.Output[Optional[int]]:
        """
        The length of the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument. Default value is `20`.
        """
        return pulumi.get(self, "password_length")

    @property
    @pulumi.getter(name="passwordResetRequired")
    def password_reset_required(self) -> pulumi.Output[bool]:
        """
        Whether the user should be forced to reset the generated password on resource creation. Only applies on resource creation.
        """
        return pulumi.get(self, "password_reset_required")

    @property
    @pulumi.getter(name="pgpKey")
    def pgp_key(self) -> pulumi.Output[Optional[str]]:
        """
        Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:username`. Only applies on resource creation. Drift detection is not possible with this argument.
        """
        return pulumi.get(self, "pgp_key")

    @property
    @pulumi.getter
    def user(self) -> pulumi.Output[str]:
        """
        The IAM user's name.
        """
        return pulumi.get(self, "user")

