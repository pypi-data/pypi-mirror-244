# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['OrganizationConfigurationArgs', 'OrganizationConfiguration']

@pulumi.input_type
class OrganizationConfigurationArgs:
    def __init__(__self__, *,
                 auto_enable: pulumi.Input[bool],
                 auto_enable_standards: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a OrganizationConfiguration resource.
        :param pulumi.Input[bool] auto_enable: Whether to automatically enable Security Hub for new accounts in the organization.
        :param pulumi.Input[str] auto_enable_standards: Whether to automatically enable Security Hub default standards for new member accounts in the organization. By default, this parameter is equal to `DEFAULT`, and new member accounts are automatically enabled with default Security Hub standards. To opt out of enabling default standards for new member accounts, set this parameter equal to `NONE`.
        """
        pulumi.set(__self__, "auto_enable", auto_enable)
        if auto_enable_standards is not None:
            pulumi.set(__self__, "auto_enable_standards", auto_enable_standards)

    @property
    @pulumi.getter(name="autoEnable")
    def auto_enable(self) -> pulumi.Input[bool]:
        """
        Whether to automatically enable Security Hub for new accounts in the organization.
        """
        return pulumi.get(self, "auto_enable")

    @auto_enable.setter
    def auto_enable(self, value: pulumi.Input[bool]):
        pulumi.set(self, "auto_enable", value)

    @property
    @pulumi.getter(name="autoEnableStandards")
    def auto_enable_standards(self) -> Optional[pulumi.Input[str]]:
        """
        Whether to automatically enable Security Hub default standards for new member accounts in the organization. By default, this parameter is equal to `DEFAULT`, and new member accounts are automatically enabled with default Security Hub standards. To opt out of enabling default standards for new member accounts, set this parameter equal to `NONE`.
        """
        return pulumi.get(self, "auto_enable_standards")

    @auto_enable_standards.setter
    def auto_enable_standards(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auto_enable_standards", value)


@pulumi.input_type
class _OrganizationConfigurationState:
    def __init__(__self__, *,
                 auto_enable: Optional[pulumi.Input[bool]] = None,
                 auto_enable_standards: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering OrganizationConfiguration resources.
        :param pulumi.Input[bool] auto_enable: Whether to automatically enable Security Hub for new accounts in the organization.
        :param pulumi.Input[str] auto_enable_standards: Whether to automatically enable Security Hub default standards for new member accounts in the organization. By default, this parameter is equal to `DEFAULT`, and new member accounts are automatically enabled with default Security Hub standards. To opt out of enabling default standards for new member accounts, set this parameter equal to `NONE`.
        """
        if auto_enable is not None:
            pulumi.set(__self__, "auto_enable", auto_enable)
        if auto_enable_standards is not None:
            pulumi.set(__self__, "auto_enable_standards", auto_enable_standards)

    @property
    @pulumi.getter(name="autoEnable")
    def auto_enable(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to automatically enable Security Hub for new accounts in the organization.
        """
        return pulumi.get(self, "auto_enable")

    @auto_enable.setter
    def auto_enable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_enable", value)

    @property
    @pulumi.getter(name="autoEnableStandards")
    def auto_enable_standards(self) -> Optional[pulumi.Input[str]]:
        """
        Whether to automatically enable Security Hub default standards for new member accounts in the organization. By default, this parameter is equal to `DEFAULT`, and new member accounts are automatically enabled with default Security Hub standards. To opt out of enabling default standards for new member accounts, set this parameter equal to `NONE`.
        """
        return pulumi.get(self, "auto_enable_standards")

    @auto_enable_standards.setter
    def auto_enable_standards(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auto_enable_standards", value)


class OrganizationConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_enable: Optional[pulumi.Input[bool]] = None,
                 auto_enable_standards: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages the Security Hub Organization Configuration.

        > **NOTE:** This resource requires an `securityhub.OrganizationAdminAccount` to be configured (not necessarily with Pulumi). More information about managing Security Hub in an organization can be found in the [Managing administrator and member accounts](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-accounts.html) documentation

        > **NOTE:** This is an advanced AWS resource. Pulumi will automatically assume management of the Security Hub Organization Configuration without import and perform no actions on removal from the Pulumi program.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_organization = aws.organizations.Organization("exampleOrganization",
            aws_service_access_principals=["securityhub.amazonaws.com"],
            feature_set="ALL")
        example_organization_admin_account = aws.securityhub.OrganizationAdminAccount("exampleOrganizationAdminAccount", admin_account_id="123456789012",
        opts=pulumi.ResourceOptions(depends_on=[example_organization]))
        example_organization_configuration = aws.securityhub.OrganizationConfiguration("exampleOrganizationConfiguration", auto_enable=True)
        ```

        ## Import

        Using `pulumi import`, import an existing Security Hub enabled account using the AWS account ID. For example:

        ```sh
         $ pulumi import aws:securityhub/organizationConfiguration:OrganizationConfiguration example 123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_enable: Whether to automatically enable Security Hub for new accounts in the organization.
        :param pulumi.Input[str] auto_enable_standards: Whether to automatically enable Security Hub default standards for new member accounts in the organization. By default, this parameter is equal to `DEFAULT`, and new member accounts are automatically enabled with default Security Hub standards. To opt out of enabling default standards for new member accounts, set this parameter equal to `NONE`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OrganizationConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages the Security Hub Organization Configuration.

        > **NOTE:** This resource requires an `securityhub.OrganizationAdminAccount` to be configured (not necessarily with Pulumi). More information about managing Security Hub in an organization can be found in the [Managing administrator and member accounts](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-accounts.html) documentation

        > **NOTE:** This is an advanced AWS resource. Pulumi will automatically assume management of the Security Hub Organization Configuration without import and perform no actions on removal from the Pulumi program.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_organization = aws.organizations.Organization("exampleOrganization",
            aws_service_access_principals=["securityhub.amazonaws.com"],
            feature_set="ALL")
        example_organization_admin_account = aws.securityhub.OrganizationAdminAccount("exampleOrganizationAdminAccount", admin_account_id="123456789012",
        opts=pulumi.ResourceOptions(depends_on=[example_organization]))
        example_organization_configuration = aws.securityhub.OrganizationConfiguration("exampleOrganizationConfiguration", auto_enable=True)
        ```

        ## Import

        Using `pulumi import`, import an existing Security Hub enabled account using the AWS account ID. For example:

        ```sh
         $ pulumi import aws:securityhub/organizationConfiguration:OrganizationConfiguration example 123456789012
        ```

        :param str resource_name: The name of the resource.
        :param OrganizationConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OrganizationConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_enable: Optional[pulumi.Input[bool]] = None,
                 auto_enable_standards: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OrganizationConfigurationArgs.__new__(OrganizationConfigurationArgs)

            if auto_enable is None and not opts.urn:
                raise TypeError("Missing required property 'auto_enable'")
            __props__.__dict__["auto_enable"] = auto_enable
            __props__.__dict__["auto_enable_standards"] = auto_enable_standards
        super(OrganizationConfiguration, __self__).__init__(
            'aws:securityhub/organizationConfiguration:OrganizationConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            auto_enable: Optional[pulumi.Input[bool]] = None,
            auto_enable_standards: Optional[pulumi.Input[str]] = None) -> 'OrganizationConfiguration':
        """
        Get an existing OrganizationConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_enable: Whether to automatically enable Security Hub for new accounts in the organization.
        :param pulumi.Input[str] auto_enable_standards: Whether to automatically enable Security Hub default standards for new member accounts in the organization. By default, this parameter is equal to `DEFAULT`, and new member accounts are automatically enabled with default Security Hub standards. To opt out of enabling default standards for new member accounts, set this parameter equal to `NONE`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OrganizationConfigurationState.__new__(_OrganizationConfigurationState)

        __props__.__dict__["auto_enable"] = auto_enable
        __props__.__dict__["auto_enable_standards"] = auto_enable_standards
        return OrganizationConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoEnable")
    def auto_enable(self) -> pulumi.Output[bool]:
        """
        Whether to automatically enable Security Hub for new accounts in the organization.
        """
        return pulumi.get(self, "auto_enable")

    @property
    @pulumi.getter(name="autoEnableStandards")
    def auto_enable_standards(self) -> pulumi.Output[str]:
        """
        Whether to automatically enable Security Hub default standards for new member accounts in the organization. By default, this parameter is equal to `DEFAULT`, and new member accounts are automatically enabled with default Security Hub standards. To opt out of enabling default standards for new member accounts, set this parameter equal to `NONE`.
        """
        return pulumi.get(self, "auto_enable_standards")

