# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['InvitationAccepterArgs', 'InvitationAccepter']

@pulumi.input_type
class InvitationAccepterArgs:
    def __init__(__self__, *,
                 administrator_account_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a InvitationAccepter resource.
        :param pulumi.Input[str] administrator_account_id: The AWS account ID for the account that sent the invitation.
        """
        pulumi.set(__self__, "administrator_account_id", administrator_account_id)

    @property
    @pulumi.getter(name="administratorAccountId")
    def administrator_account_id(self) -> pulumi.Input[str]:
        """
        The AWS account ID for the account that sent the invitation.
        """
        return pulumi.get(self, "administrator_account_id")

    @administrator_account_id.setter
    def administrator_account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "administrator_account_id", value)


@pulumi.input_type
class _InvitationAccepterState:
    def __init__(__self__, *,
                 administrator_account_id: Optional[pulumi.Input[str]] = None,
                 invitation_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering InvitationAccepter resources.
        :param pulumi.Input[str] administrator_account_id: The AWS account ID for the account that sent the invitation.
        :param pulumi.Input[str] invitation_id: The unique identifier for the invitation.
        """
        if administrator_account_id is not None:
            pulumi.set(__self__, "administrator_account_id", administrator_account_id)
        if invitation_id is not None:
            pulumi.set(__self__, "invitation_id", invitation_id)

    @property
    @pulumi.getter(name="administratorAccountId")
    def administrator_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS account ID for the account that sent the invitation.
        """
        return pulumi.get(self, "administrator_account_id")

    @administrator_account_id.setter
    def administrator_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "administrator_account_id", value)

    @property
    @pulumi.getter(name="invitationId")
    def invitation_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique identifier for the invitation.
        """
        return pulumi.get(self, "invitation_id")

    @invitation_id.setter
    def invitation_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "invitation_id", value)


class InvitationAccepter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 administrator_account_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage an [Amazon Macie Invitation Accepter](https://docs.aws.amazon.com/macie/latest/APIReference/invitations-accept.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        primary_account = aws.macie2.Account("primaryAccount", opts=pulumi.ResourceOptions(provider="awsalternate"))
        member_account = aws.macie2.Account("memberAccount")
        primary_member = aws.macie2.Member("primaryMember",
            account_id="ACCOUNT ID",
            email="EMAIL",
            invite=True,
            invitation_message="Message of the invite",
            opts=pulumi.ResourceOptions(provider="awsalternate",
                depends_on=[primary_account]))
        member_invitation_accepter = aws.macie2.InvitationAccepter("memberInvitationAccepter", administrator_account_id="ADMINISTRATOR ACCOUNT ID",
        opts=pulumi.ResourceOptions(depends_on=[primary_member]))
        ```

        ## Import

        Using `pulumi import`, import `aws_macie2_invitation_accepter` using the admin account ID. For example:

        ```sh
         $ pulumi import aws:macie2/invitationAccepter:InvitationAccepter example 123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] administrator_account_id: The AWS account ID for the account that sent the invitation.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InvitationAccepterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage an [Amazon Macie Invitation Accepter](https://docs.aws.amazon.com/macie/latest/APIReference/invitations-accept.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        primary_account = aws.macie2.Account("primaryAccount", opts=pulumi.ResourceOptions(provider="awsalternate"))
        member_account = aws.macie2.Account("memberAccount")
        primary_member = aws.macie2.Member("primaryMember",
            account_id="ACCOUNT ID",
            email="EMAIL",
            invite=True,
            invitation_message="Message of the invite",
            opts=pulumi.ResourceOptions(provider="awsalternate",
                depends_on=[primary_account]))
        member_invitation_accepter = aws.macie2.InvitationAccepter("memberInvitationAccepter", administrator_account_id="ADMINISTRATOR ACCOUNT ID",
        opts=pulumi.ResourceOptions(depends_on=[primary_member]))
        ```

        ## Import

        Using `pulumi import`, import `aws_macie2_invitation_accepter` using the admin account ID. For example:

        ```sh
         $ pulumi import aws:macie2/invitationAccepter:InvitationAccepter example 123456789012
        ```

        :param str resource_name: The name of the resource.
        :param InvitationAccepterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InvitationAccepterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 administrator_account_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InvitationAccepterArgs.__new__(InvitationAccepterArgs)

            if administrator_account_id is None and not opts.urn:
                raise TypeError("Missing required property 'administrator_account_id'")
            __props__.__dict__["administrator_account_id"] = administrator_account_id
            __props__.__dict__["invitation_id"] = None
        super(InvitationAccepter, __self__).__init__(
            'aws:macie2/invitationAccepter:InvitationAccepter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            administrator_account_id: Optional[pulumi.Input[str]] = None,
            invitation_id: Optional[pulumi.Input[str]] = None) -> 'InvitationAccepter':
        """
        Get an existing InvitationAccepter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] administrator_account_id: The AWS account ID for the account that sent the invitation.
        :param pulumi.Input[str] invitation_id: The unique identifier for the invitation.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InvitationAccepterState.__new__(_InvitationAccepterState)

        __props__.__dict__["administrator_account_id"] = administrator_account_id
        __props__.__dict__["invitation_id"] = invitation_id
        return InvitationAccepter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="administratorAccountId")
    def administrator_account_id(self) -> pulumi.Output[str]:
        """
        The AWS account ID for the account that sent the invitation.
        """
        return pulumi.get(self, "administrator_account_id")

    @property
    @pulumi.getter(name="invitationId")
    def invitation_id(self) -> pulumi.Output[str]:
        """
        The unique identifier for the invitation.
        """
        return pulumi.get(self, "invitation_id")

