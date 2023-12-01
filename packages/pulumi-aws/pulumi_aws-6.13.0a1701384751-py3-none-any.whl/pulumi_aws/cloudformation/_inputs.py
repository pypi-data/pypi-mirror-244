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
    'CloudFormationTypeLoggingConfigArgs',
    'StackSetAutoDeploymentArgs',
    'StackSetInstanceDeploymentTargetsArgs',
    'StackSetInstanceOperationPreferencesArgs',
    'StackSetInstanceStackInstanceSummaryArgs',
    'StackSetManagedExecutionArgs',
    'StackSetOperationPreferencesArgs',
]

@pulumi.input_type
class CloudFormationTypeLoggingConfigArgs:
    def __init__(__self__, *,
                 log_group_name: pulumi.Input[str],
                 log_role_arn: pulumi.Input[str]):
        """
        :param pulumi.Input[str] log_group_name: Name of the CloudWatch Log Group where CloudFormation sends error logging information when invoking the type's handlers.
        :param pulumi.Input[str] log_role_arn: Amazon Resource Name (ARN) of the IAM Role CloudFormation assumes when sending error logging information to CloudWatch Logs.
        """
        pulumi.set(__self__, "log_group_name", log_group_name)
        pulumi.set(__self__, "log_role_arn", log_role_arn)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> pulumi.Input[str]:
        """
        Name of the CloudWatch Log Group where CloudFormation sends error logging information when invoking the type's handlers.
        """
        return pulumi.get(self, "log_group_name")

    @log_group_name.setter
    def log_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_group_name", value)

    @property
    @pulumi.getter(name="logRoleArn")
    def log_role_arn(self) -> pulumi.Input[str]:
        """
        Amazon Resource Name (ARN) of the IAM Role CloudFormation assumes when sending error logging information to CloudWatch Logs.
        """
        return pulumi.get(self, "log_role_arn")

    @log_role_arn.setter
    def log_role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_role_arn", value)


@pulumi.input_type
class StackSetAutoDeploymentArgs:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 retain_stacks_on_account_removal: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[bool] enabled: Whether or not auto-deployment is enabled.
        :param pulumi.Input[bool] retain_stacks_on_account_removal: Whether or not to retain stacks when the account is removed.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if retain_stacks_on_account_removal is not None:
            pulumi.set(__self__, "retain_stacks_on_account_removal", retain_stacks_on_account_removal)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not auto-deployment is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="retainStacksOnAccountRemoval")
    def retain_stacks_on_account_removal(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not to retain stacks when the account is removed.
        """
        return pulumi.get(self, "retain_stacks_on_account_removal")

    @retain_stacks_on_account_removal.setter
    def retain_stacks_on_account_removal(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "retain_stacks_on_account_removal", value)


@pulumi.input_type
class StackSetInstanceDeploymentTargetsArgs:
    def __init__(__self__, *,
                 organizational_unit_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] organizational_unit_ids: The organization root ID or organizational unit (OU) IDs to which StackSets deploys.
        """
        if organizational_unit_ids is not None:
            pulumi.set(__self__, "organizational_unit_ids", organizational_unit_ids)

    @property
    @pulumi.getter(name="organizationalUnitIds")
    def organizational_unit_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The organization root ID or organizational unit (OU) IDs to which StackSets deploys.
        """
        return pulumi.get(self, "organizational_unit_ids")

    @organizational_unit_ids.setter
    def organizational_unit_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "organizational_unit_ids", value)


@pulumi.input_type
class StackSetInstanceOperationPreferencesArgs:
    def __init__(__self__, *,
                 failure_tolerance_count: Optional[pulumi.Input[int]] = None,
                 failure_tolerance_percentage: Optional[pulumi.Input[int]] = None,
                 max_concurrent_count: Optional[pulumi.Input[int]] = None,
                 max_concurrent_percentage: Optional[pulumi.Input[int]] = None,
                 region_concurrency_type: Optional[pulumi.Input[str]] = None,
                 region_orders: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[int] failure_tolerance_count: The number of accounts, per Region, for which this operation can fail before AWS CloudFormation stops the operation in that Region.
        :param pulumi.Input[int] failure_tolerance_percentage: The percentage of accounts, per Region, for which this stack operation can fail before AWS CloudFormation stops the operation in that Region.
        :param pulumi.Input[int] max_concurrent_count: The maximum number of accounts in which to perform this operation at one time.
        :param pulumi.Input[int] max_concurrent_percentage: The maximum percentage of accounts in which to perform this operation at one time.
        :param pulumi.Input[str] region_concurrency_type: The concurrency type of deploying StackSets operations in Regions, could be in parallel or one Region at a time. Valid values are `SEQUENTIAL` and `PARALLEL`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] region_orders: The order of the Regions in where you want to perform the stack operation.
        """
        if failure_tolerance_count is not None:
            pulumi.set(__self__, "failure_tolerance_count", failure_tolerance_count)
        if failure_tolerance_percentage is not None:
            pulumi.set(__self__, "failure_tolerance_percentage", failure_tolerance_percentage)
        if max_concurrent_count is not None:
            pulumi.set(__self__, "max_concurrent_count", max_concurrent_count)
        if max_concurrent_percentage is not None:
            pulumi.set(__self__, "max_concurrent_percentage", max_concurrent_percentage)
        if region_concurrency_type is not None:
            pulumi.set(__self__, "region_concurrency_type", region_concurrency_type)
        if region_orders is not None:
            pulumi.set(__self__, "region_orders", region_orders)

    @property
    @pulumi.getter(name="failureToleranceCount")
    def failure_tolerance_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of accounts, per Region, for which this operation can fail before AWS CloudFormation stops the operation in that Region.
        """
        return pulumi.get(self, "failure_tolerance_count")

    @failure_tolerance_count.setter
    def failure_tolerance_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "failure_tolerance_count", value)

    @property
    @pulumi.getter(name="failureTolerancePercentage")
    def failure_tolerance_percentage(self) -> Optional[pulumi.Input[int]]:
        """
        The percentage of accounts, per Region, for which this stack operation can fail before AWS CloudFormation stops the operation in that Region.
        """
        return pulumi.get(self, "failure_tolerance_percentage")

    @failure_tolerance_percentage.setter
    def failure_tolerance_percentage(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "failure_tolerance_percentage", value)

    @property
    @pulumi.getter(name="maxConcurrentCount")
    def max_concurrent_count(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum number of accounts in which to perform this operation at one time.
        """
        return pulumi.get(self, "max_concurrent_count")

    @max_concurrent_count.setter
    def max_concurrent_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_concurrent_count", value)

    @property
    @pulumi.getter(name="maxConcurrentPercentage")
    def max_concurrent_percentage(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum percentage of accounts in which to perform this operation at one time.
        """
        return pulumi.get(self, "max_concurrent_percentage")

    @max_concurrent_percentage.setter
    def max_concurrent_percentage(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_concurrent_percentage", value)

    @property
    @pulumi.getter(name="regionConcurrencyType")
    def region_concurrency_type(self) -> Optional[pulumi.Input[str]]:
        """
        The concurrency type of deploying StackSets operations in Regions, could be in parallel or one Region at a time. Valid values are `SEQUENTIAL` and `PARALLEL`.
        """
        return pulumi.get(self, "region_concurrency_type")

    @region_concurrency_type.setter
    def region_concurrency_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region_concurrency_type", value)

    @property
    @pulumi.getter(name="regionOrders")
    def region_orders(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The order of the Regions in where you want to perform the stack operation.
        """
        return pulumi.get(self, "region_orders")

    @region_orders.setter
    def region_orders(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "region_orders", value)


@pulumi.input_type
class StackSetInstanceStackInstanceSummaryArgs:
    def __init__(__self__, *,
                 account_id: Optional[pulumi.Input[str]] = None,
                 organizational_unit_id: Optional[pulumi.Input[str]] = None,
                 stack_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] account_id: Target AWS Account ID to create a Stack based on the StackSet. Defaults to current account.
        :param pulumi.Input[str] organizational_unit_id: Organizational unit ID in which the stack is deployed.
        :param pulumi.Input[str] stack_id: Stack identifier.
        """
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if organizational_unit_id is not None:
            pulumi.set(__self__, "organizational_unit_id", organizational_unit_id)
        if stack_id is not None:
            pulumi.set(__self__, "stack_id", stack_id)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        Target AWS Account ID to create a Stack based on the StackSet. Defaults to current account.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="organizationalUnitId")
    def organizational_unit_id(self) -> Optional[pulumi.Input[str]]:
        """
        Organizational unit ID in which the stack is deployed.
        """
        return pulumi.get(self, "organizational_unit_id")

    @organizational_unit_id.setter
    def organizational_unit_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organizational_unit_id", value)

    @property
    @pulumi.getter(name="stackId")
    def stack_id(self) -> Optional[pulumi.Input[str]]:
        """
        Stack identifier.
        """
        return pulumi.get(self, "stack_id")

    @stack_id.setter
    def stack_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stack_id", value)


@pulumi.input_type
class StackSetManagedExecutionArgs:
    def __init__(__self__, *,
                 active: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[bool] active: When set to true, StackSets performs non-conflicting operations concurrently and queues conflicting operations. After conflicting operations finish, StackSets starts queued operations in request order. Default is false.
        """
        if active is not None:
            pulumi.set(__self__, "active", active)

    @property
    @pulumi.getter
    def active(self) -> Optional[pulumi.Input[bool]]:
        """
        When set to true, StackSets performs non-conflicting operations concurrently and queues conflicting operations. After conflicting operations finish, StackSets starts queued operations in request order. Default is false.
        """
        return pulumi.get(self, "active")

    @active.setter
    def active(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "active", value)


@pulumi.input_type
class StackSetOperationPreferencesArgs:
    def __init__(__self__, *,
                 failure_tolerance_count: Optional[pulumi.Input[int]] = None,
                 failure_tolerance_percentage: Optional[pulumi.Input[int]] = None,
                 max_concurrent_count: Optional[pulumi.Input[int]] = None,
                 max_concurrent_percentage: Optional[pulumi.Input[int]] = None,
                 region_concurrency_type: Optional[pulumi.Input[str]] = None,
                 region_orders: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[int] failure_tolerance_count: The number of accounts, per Region, for which this operation can fail before AWS CloudFormation stops the operation in that Region.
        :param pulumi.Input[int] failure_tolerance_percentage: The percentage of accounts, per Region, for which this stack operation can fail before AWS CloudFormation stops the operation in that Region.
        :param pulumi.Input[int] max_concurrent_count: The maximum number of accounts in which to perform this operation at one time.
        :param pulumi.Input[int] max_concurrent_percentage: The maximum percentage of accounts in which to perform this operation at one time.
        :param pulumi.Input[str] region_concurrency_type: The concurrency type of deploying StackSets operations in Regions, could be in parallel or one Region at a time.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] region_orders: The order of the Regions in where you want to perform the stack operation.
        """
        if failure_tolerance_count is not None:
            pulumi.set(__self__, "failure_tolerance_count", failure_tolerance_count)
        if failure_tolerance_percentage is not None:
            pulumi.set(__self__, "failure_tolerance_percentage", failure_tolerance_percentage)
        if max_concurrent_count is not None:
            pulumi.set(__self__, "max_concurrent_count", max_concurrent_count)
        if max_concurrent_percentage is not None:
            pulumi.set(__self__, "max_concurrent_percentage", max_concurrent_percentage)
        if region_concurrency_type is not None:
            pulumi.set(__self__, "region_concurrency_type", region_concurrency_type)
        if region_orders is not None:
            pulumi.set(__self__, "region_orders", region_orders)

    @property
    @pulumi.getter(name="failureToleranceCount")
    def failure_tolerance_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of accounts, per Region, for which this operation can fail before AWS CloudFormation stops the operation in that Region.
        """
        return pulumi.get(self, "failure_tolerance_count")

    @failure_tolerance_count.setter
    def failure_tolerance_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "failure_tolerance_count", value)

    @property
    @pulumi.getter(name="failureTolerancePercentage")
    def failure_tolerance_percentage(self) -> Optional[pulumi.Input[int]]:
        """
        The percentage of accounts, per Region, for which this stack operation can fail before AWS CloudFormation stops the operation in that Region.
        """
        return pulumi.get(self, "failure_tolerance_percentage")

    @failure_tolerance_percentage.setter
    def failure_tolerance_percentage(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "failure_tolerance_percentage", value)

    @property
    @pulumi.getter(name="maxConcurrentCount")
    def max_concurrent_count(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum number of accounts in which to perform this operation at one time.
        """
        return pulumi.get(self, "max_concurrent_count")

    @max_concurrent_count.setter
    def max_concurrent_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_concurrent_count", value)

    @property
    @pulumi.getter(name="maxConcurrentPercentage")
    def max_concurrent_percentage(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum percentage of accounts in which to perform this operation at one time.
        """
        return pulumi.get(self, "max_concurrent_percentage")

    @max_concurrent_percentage.setter
    def max_concurrent_percentage(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_concurrent_percentage", value)

    @property
    @pulumi.getter(name="regionConcurrencyType")
    def region_concurrency_type(self) -> Optional[pulumi.Input[str]]:
        """
        The concurrency type of deploying StackSets operations in Regions, could be in parallel or one Region at a time.
        """
        return pulumi.get(self, "region_concurrency_type")

    @region_concurrency_type.setter
    def region_concurrency_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region_concurrency_type", value)

    @property
    @pulumi.getter(name="regionOrders")
    def region_orders(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The order of the Regions in where you want to perform the stack operation.
        """
        return pulumi.get(self, "region_orders")

    @region_orders.setter
    def region_orders(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "region_orders", value)


