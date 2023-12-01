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
    'EventDataStoreAdvancedEventSelectorArgs',
    'EventDataStoreAdvancedEventSelectorFieldSelectorArgs',
    'TrailAdvancedEventSelectorArgs',
    'TrailAdvancedEventSelectorFieldSelectorArgs',
    'TrailEventSelectorArgs',
    'TrailEventSelectorDataResourceArgs',
    'TrailInsightSelectorArgs',
]

@pulumi.input_type
class EventDataStoreAdvancedEventSelectorArgs:
    def __init__(__self__, *,
                 field_selectors: Optional[pulumi.Input[Sequence[pulumi.Input['EventDataStoreAdvancedEventSelectorFieldSelectorArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['EventDataStoreAdvancedEventSelectorFieldSelectorArgs']]] field_selectors: Specifies the selector statements in an advanced event selector. Fields documented below.
        :param pulumi.Input[str] name: Specifies the name of the advanced event selector.
        """
        if field_selectors is not None:
            pulumi.set(__self__, "field_selectors", field_selectors)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="fieldSelectors")
    def field_selectors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EventDataStoreAdvancedEventSelectorFieldSelectorArgs']]]]:
        """
        Specifies the selector statements in an advanced event selector. Fields documented below.
        """
        return pulumi.get(self, "field_selectors")

    @field_selectors.setter
    def field_selectors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EventDataStoreAdvancedEventSelectorFieldSelectorArgs']]]]):
        pulumi.set(self, "field_selectors", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the advanced event selector.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class EventDataStoreAdvancedEventSelectorFieldSelectorArgs:
    def __init__(__self__, *,
                 ends_withs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 equals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 field: Optional[pulumi.Input[str]] = None,
                 not_ends_withs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 not_equals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 not_starts_withs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 starts_withs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ends_withs: A list of values that includes events that match the last few characters of the event record field specified as the value of `field`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] equals: A list of values that includes events that match the exact value of the event record field specified as the value of `field`. This is the only valid operator that you can use with the `readOnly`, `eventCategory`, and `resources.type` fields.
        :param pulumi.Input[str] field: Specifies a field in an event record on which to filter events to be logged. You can specify only the following values: `readOnly`, `eventSource`, `eventName`, `eventCategory`, `resources.type`, `resources.ARN`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_ends_withs: A list of values that excludes events that match the last few characters of the event record field specified as the value of `field`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_equals: A list of values that excludes events that match the exact value of the event record field specified as the value of `field`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_starts_withs: A list of values that excludes events that match the first few characters of the event record field specified as the value of `field`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] starts_withs: A list of values that includes events that match the first few characters of the event record field specified as the value of `field`.
        """
        if ends_withs is not None:
            pulumi.set(__self__, "ends_withs", ends_withs)
        if equals is not None:
            pulumi.set(__self__, "equals", equals)
        if field is not None:
            pulumi.set(__self__, "field", field)
        if not_ends_withs is not None:
            pulumi.set(__self__, "not_ends_withs", not_ends_withs)
        if not_equals is not None:
            pulumi.set(__self__, "not_equals", not_equals)
        if not_starts_withs is not None:
            pulumi.set(__self__, "not_starts_withs", not_starts_withs)
        if starts_withs is not None:
            pulumi.set(__self__, "starts_withs", starts_withs)

    @property
    @pulumi.getter(name="endsWiths")
    def ends_withs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that includes events that match the last few characters of the event record field specified as the value of `field`.
        """
        return pulumi.get(self, "ends_withs")

    @ends_withs.setter
    def ends_withs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ends_withs", value)

    @property
    @pulumi.getter
    def equals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that includes events that match the exact value of the event record field specified as the value of `field`. This is the only valid operator that you can use with the `readOnly`, `eventCategory`, and `resources.type` fields.
        """
        return pulumi.get(self, "equals")

    @equals.setter
    def equals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "equals", value)

    @property
    @pulumi.getter
    def field(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a field in an event record on which to filter events to be logged. You can specify only the following values: `readOnly`, `eventSource`, `eventName`, `eventCategory`, `resources.type`, `resources.ARN`.
        """
        return pulumi.get(self, "field")

    @field.setter
    def field(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "field", value)

    @property
    @pulumi.getter(name="notEndsWiths")
    def not_ends_withs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that excludes events that match the last few characters of the event record field specified as the value of `field`.
        """
        return pulumi.get(self, "not_ends_withs")

    @not_ends_withs.setter
    def not_ends_withs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_ends_withs", value)

    @property
    @pulumi.getter(name="notEquals")
    def not_equals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that excludes events that match the exact value of the event record field specified as the value of `field`.
        """
        return pulumi.get(self, "not_equals")

    @not_equals.setter
    def not_equals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_equals", value)

    @property
    @pulumi.getter(name="notStartsWiths")
    def not_starts_withs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that excludes events that match the first few characters of the event record field specified as the value of `field`.
        """
        return pulumi.get(self, "not_starts_withs")

    @not_starts_withs.setter
    def not_starts_withs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_starts_withs", value)

    @property
    @pulumi.getter(name="startsWiths")
    def starts_withs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that includes events that match the first few characters of the event record field specified as the value of `field`.
        """
        return pulumi.get(self, "starts_withs")

    @starts_withs.setter
    def starts_withs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "starts_withs", value)


@pulumi.input_type
class TrailAdvancedEventSelectorArgs:
    def __init__(__self__, *,
                 field_selectors: pulumi.Input[Sequence[pulumi.Input['TrailAdvancedEventSelectorFieldSelectorArgs']]],
                 name: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['TrailAdvancedEventSelectorFieldSelectorArgs']]] field_selectors: Specifies the selector statements in an advanced event selector. Fields documented below.
        :param pulumi.Input[str] name: Name of the trail.
        """
        pulumi.set(__self__, "field_selectors", field_selectors)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="fieldSelectors")
    def field_selectors(self) -> pulumi.Input[Sequence[pulumi.Input['TrailAdvancedEventSelectorFieldSelectorArgs']]]:
        """
        Specifies the selector statements in an advanced event selector. Fields documented below.
        """
        return pulumi.get(self, "field_selectors")

    @field_selectors.setter
    def field_selectors(self, value: pulumi.Input[Sequence[pulumi.Input['TrailAdvancedEventSelectorFieldSelectorArgs']]]):
        pulumi.set(self, "field_selectors", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the trail.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class TrailAdvancedEventSelectorFieldSelectorArgs:
    def __init__(__self__, *,
                 field: pulumi.Input[str],
                 ends_withs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 equals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 not_ends_withs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 not_equals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 not_starts_withs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 starts_withs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] field: Field in an event record on which to filter events to be logged. You can specify only the following values: `readOnly`, `eventSource`, `eventName`, `eventCategory`, `resources.type`, `resources.ARN`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ends_withs: A list of values that includes events that match the last few characters of the event record field specified as the value of `field`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] equals: A list of values that includes events that match the exact value of the event record field specified as the value of `field`. This is the only valid operator that you can use with the `readOnly`, `eventCategory`, and `resources.type` fields.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_ends_withs: A list of values that excludes events that match the last few characters of the event record field specified as the value of `field`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_equals: A list of values that excludes events that match the exact value of the event record field specified as the value of `field`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_starts_withs: A list of values that excludes events that match the first few characters of the event record field specified as the value of `field`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] starts_withs: A list of values that includes events that match the first few characters of the event record field specified as the value of `field`.
        """
        pulumi.set(__self__, "field", field)
        if ends_withs is not None:
            pulumi.set(__self__, "ends_withs", ends_withs)
        if equals is not None:
            pulumi.set(__self__, "equals", equals)
        if not_ends_withs is not None:
            pulumi.set(__self__, "not_ends_withs", not_ends_withs)
        if not_equals is not None:
            pulumi.set(__self__, "not_equals", not_equals)
        if not_starts_withs is not None:
            pulumi.set(__self__, "not_starts_withs", not_starts_withs)
        if starts_withs is not None:
            pulumi.set(__self__, "starts_withs", starts_withs)

    @property
    @pulumi.getter
    def field(self) -> pulumi.Input[str]:
        """
        Field in an event record on which to filter events to be logged. You can specify only the following values: `readOnly`, `eventSource`, `eventName`, `eventCategory`, `resources.type`, `resources.ARN`.
        """
        return pulumi.get(self, "field")

    @field.setter
    def field(self, value: pulumi.Input[str]):
        pulumi.set(self, "field", value)

    @property
    @pulumi.getter(name="endsWiths")
    def ends_withs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that includes events that match the last few characters of the event record field specified as the value of `field`.
        """
        return pulumi.get(self, "ends_withs")

    @ends_withs.setter
    def ends_withs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ends_withs", value)

    @property
    @pulumi.getter
    def equals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that includes events that match the exact value of the event record field specified as the value of `field`. This is the only valid operator that you can use with the `readOnly`, `eventCategory`, and `resources.type` fields.
        """
        return pulumi.get(self, "equals")

    @equals.setter
    def equals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "equals", value)

    @property
    @pulumi.getter(name="notEndsWiths")
    def not_ends_withs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that excludes events that match the last few characters of the event record field specified as the value of `field`.
        """
        return pulumi.get(self, "not_ends_withs")

    @not_ends_withs.setter
    def not_ends_withs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_ends_withs", value)

    @property
    @pulumi.getter(name="notEquals")
    def not_equals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that excludes events that match the exact value of the event record field specified as the value of `field`.
        """
        return pulumi.get(self, "not_equals")

    @not_equals.setter
    def not_equals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_equals", value)

    @property
    @pulumi.getter(name="notStartsWiths")
    def not_starts_withs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that excludes events that match the first few characters of the event record field specified as the value of `field`.
        """
        return pulumi.get(self, "not_starts_withs")

    @not_starts_withs.setter
    def not_starts_withs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_starts_withs", value)

    @property
    @pulumi.getter(name="startsWiths")
    def starts_withs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that includes events that match the first few characters of the event record field specified as the value of `field`.
        """
        return pulumi.get(self, "starts_withs")

    @starts_withs.setter
    def starts_withs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "starts_withs", value)


@pulumi.input_type
class TrailEventSelectorArgs:
    def __init__(__self__, *,
                 data_resources: Optional[pulumi.Input[Sequence[pulumi.Input['TrailEventSelectorDataResourceArgs']]]] = None,
                 exclude_management_event_sources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 include_management_events: Optional[pulumi.Input[bool]] = None,
                 read_write_type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['TrailEventSelectorDataResourceArgs']]] data_resources: Configuration block for data events. See details below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] exclude_management_event_sources: A set of event sources to exclude. Valid values include: `kms.amazonaws.com` and `rdsdata.amazonaws.com`. `include_management_events` must be set to`true` to allow this.
        :param pulumi.Input[bool] include_management_events: Whether to include management events for your trail. Defaults to `true`.
        :param pulumi.Input[str] read_write_type: Type of events to log. Valid values are `ReadOnly`, `WriteOnly`, `All`. Default value is `All`.
        """
        if data_resources is not None:
            pulumi.set(__self__, "data_resources", data_resources)
        if exclude_management_event_sources is not None:
            pulumi.set(__self__, "exclude_management_event_sources", exclude_management_event_sources)
        if include_management_events is not None:
            pulumi.set(__self__, "include_management_events", include_management_events)
        if read_write_type is not None:
            pulumi.set(__self__, "read_write_type", read_write_type)

    @property
    @pulumi.getter(name="dataResources")
    def data_resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TrailEventSelectorDataResourceArgs']]]]:
        """
        Configuration block for data events. See details below.
        """
        return pulumi.get(self, "data_resources")

    @data_resources.setter
    def data_resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TrailEventSelectorDataResourceArgs']]]]):
        pulumi.set(self, "data_resources", value)

    @property
    @pulumi.getter(name="excludeManagementEventSources")
    def exclude_management_event_sources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A set of event sources to exclude. Valid values include: `kms.amazonaws.com` and `rdsdata.amazonaws.com`. `include_management_events` must be set to`true` to allow this.
        """
        return pulumi.get(self, "exclude_management_event_sources")

    @exclude_management_event_sources.setter
    def exclude_management_event_sources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "exclude_management_event_sources", value)

    @property
    @pulumi.getter(name="includeManagementEvents")
    def include_management_events(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to include management events for your trail. Defaults to `true`.
        """
        return pulumi.get(self, "include_management_events")

    @include_management_events.setter
    def include_management_events(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_management_events", value)

    @property
    @pulumi.getter(name="readWriteType")
    def read_write_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of events to log. Valid values are `ReadOnly`, `WriteOnly`, `All`. Default value is `All`.
        """
        return pulumi.get(self, "read_write_type")

    @read_write_type.setter
    def read_write_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "read_write_type", value)


@pulumi.input_type
class TrailEventSelectorDataResourceArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 values: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        :param pulumi.Input[str] type: Resource type in which you want to log data events. You can specify only the following value: "AWS::S3::Object", "AWS::Lambda::Function" and "AWS::DynamoDB::Table".
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: List of ARN strings or partial ARN strings to specify selectors for data audit events over data resources. ARN list is specific to single-valued `type`. For example, `arn:aws:s3:::<bucket name>/` for all objects in a bucket, `arn:aws:s3:::<bucket name>/key` for specific objects, `arn:aws:lambda` for all lambda events within an account, `arn:aws:lambda:<region>:<account number>:function:<function name>` for a specific Lambda function, `arn:aws:dynamodb` for all DDB events for all tables within an account, or `arn:aws:dynamodb:<region>:<account number>:table/<table name>` for a specific DynamoDB table.
        """
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Resource type in which you want to log data events. You can specify only the following value: "AWS::S3::Object", "AWS::Lambda::Function" and "AWS::DynamoDB::Table".
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def values(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of ARN strings or partial ARN strings to specify selectors for data audit events over data resources. ARN list is specific to single-valued `type`. For example, `arn:aws:s3:::<bucket name>/` for all objects in a bucket, `arn:aws:s3:::<bucket name>/key` for specific objects, `arn:aws:lambda` for all lambda events within an account, `arn:aws:lambda:<region>:<account number>:function:<function name>` for a specific Lambda function, `arn:aws:dynamodb` for all DDB events for all tables within an account, or `arn:aws:dynamodb:<region>:<account number>:table/<table name>` for a specific DynamoDB table.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class TrailInsightSelectorArgs:
    def __init__(__self__, *,
                 insight_type: pulumi.Input[str]):
        """
        :param pulumi.Input[str] insight_type: Type of insights to log on a trail. Valid values are: `ApiCallRateInsight` and `ApiErrorRateInsight`.
        """
        pulumi.set(__self__, "insight_type", insight_type)

    @property
    @pulumi.getter(name="insightType")
    def insight_type(self) -> pulumi.Input[str]:
        """
        Type of insights to log on a trail. Valid values are: `ApiCallRateInsight` and `ApiErrorRateInsight`.
        """
        return pulumi.get(self, "insight_type")

    @insight_type.setter
    def insight_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "insight_type", value)


