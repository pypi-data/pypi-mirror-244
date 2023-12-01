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
    'AccountVdmAttributesDashboardAttributesArgs',
    'AccountVdmAttributesGuardianAttributesArgs',
    'ConfigurationSetDeliveryOptionsArgs',
    'ConfigurationSetEventDestinationEventDestinationArgs',
    'ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationArgs',
    'ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationArgs',
    'ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationArgs',
    'ConfigurationSetEventDestinationEventDestinationPinpointDestinationArgs',
    'ConfigurationSetEventDestinationEventDestinationSnsDestinationArgs',
    'ConfigurationSetReputationOptionsArgs',
    'ConfigurationSetSendingOptionsArgs',
    'ConfigurationSetSuppressionOptionsArgs',
    'ConfigurationSetTrackingOptionsArgs',
    'ConfigurationSetVdmOptionsArgs',
    'ConfigurationSetVdmOptionsDashboardOptionsArgs',
    'ConfigurationSetVdmOptionsGuardianOptionsArgs',
    'ContactListTopicArgs',
    'EmailIdentityDkimSigningAttributesArgs',
]

@pulumi.input_type
class AccountVdmAttributesDashboardAttributesArgs:
    def __init__(__self__, *,
                 engagement_metrics: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] engagement_metrics: Specifies the status of your VDM engagement metrics collection. Valid values: `ENABLED`, `DISABLED`.
        """
        if engagement_metrics is not None:
            pulumi.set(__self__, "engagement_metrics", engagement_metrics)

    @property
    @pulumi.getter(name="engagementMetrics")
    def engagement_metrics(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the status of your VDM engagement metrics collection. Valid values: `ENABLED`, `DISABLED`.
        """
        return pulumi.get(self, "engagement_metrics")

    @engagement_metrics.setter
    def engagement_metrics(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "engagement_metrics", value)


@pulumi.input_type
class AccountVdmAttributesGuardianAttributesArgs:
    def __init__(__self__, *,
                 optimized_shared_delivery: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] optimized_shared_delivery: Specifies the status of your VDM optimized shared delivery. Valid values: `ENABLED`, `DISABLED`.
        """
        if optimized_shared_delivery is not None:
            pulumi.set(__self__, "optimized_shared_delivery", optimized_shared_delivery)

    @property
    @pulumi.getter(name="optimizedSharedDelivery")
    def optimized_shared_delivery(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the status of your VDM optimized shared delivery. Valid values: `ENABLED`, `DISABLED`.
        """
        return pulumi.get(self, "optimized_shared_delivery")

    @optimized_shared_delivery.setter
    def optimized_shared_delivery(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "optimized_shared_delivery", value)


@pulumi.input_type
class ConfigurationSetDeliveryOptionsArgs:
    def __init__(__self__, *,
                 sending_pool_name: Optional[pulumi.Input[str]] = None,
                 tls_policy: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] sending_pool_name: The name of the dedicated IP pool to associate with the configuration set.
        :param pulumi.Input[str] tls_policy: Specifies whether messages that use the configuration set are required to use Transport Layer Security (TLS). Valid values: `REQUIRE`, `OPTIONAL`.
        """
        if sending_pool_name is not None:
            pulumi.set(__self__, "sending_pool_name", sending_pool_name)
        if tls_policy is not None:
            pulumi.set(__self__, "tls_policy", tls_policy)

    @property
    @pulumi.getter(name="sendingPoolName")
    def sending_pool_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the dedicated IP pool to associate with the configuration set.
        """
        return pulumi.get(self, "sending_pool_name")

    @sending_pool_name.setter
    def sending_pool_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sending_pool_name", value)

    @property
    @pulumi.getter(name="tlsPolicy")
    def tls_policy(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether messages that use the configuration set are required to use Transport Layer Security (TLS). Valid values: `REQUIRE`, `OPTIONAL`.
        """
        return pulumi.get(self, "tls_policy")

    @tls_policy.setter
    def tls_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tls_policy", value)


@pulumi.input_type
class ConfigurationSetEventDestinationEventDestinationArgs:
    def __init__(__self__, *,
                 matching_event_types: pulumi.Input[Sequence[pulumi.Input[str]]],
                 cloud_watch_destination: Optional[pulumi.Input['ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationArgs']] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 kinesis_firehose_destination: Optional[pulumi.Input['ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationArgs']] = None,
                 pinpoint_destination: Optional[pulumi.Input['ConfigurationSetEventDestinationEventDestinationPinpointDestinationArgs']] = None,
                 sns_destination: Optional[pulumi.Input['ConfigurationSetEventDestinationEventDestinationSnsDestinationArgs']] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] matching_event_types: An array that specifies which events the Amazon SES API v2 should send to the destinations. Valid values: `SEND`, `REJECT`, `BOUNCE`, `COMPLAINT`, `DELIVERY`, `OPEN`, `CLICK`, `RENDERING_FAILURE`, `DELIVERY_DELAY`, `SUBSCRIPTION`.
               
               The following arguments are optional:
        :param pulumi.Input['ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationArgs'] cloud_watch_destination: An object that defines an Amazon CloudWatch destination for email events. See cloud_watch_destination below
        :param pulumi.Input[bool] enabled: When the event destination is enabled, the specified event types are sent to the destinations. Default: `false`.
        :param pulumi.Input['ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationArgs'] kinesis_firehose_destination: An object that defines an Amazon Kinesis Data Firehose destination for email events. See kinesis_firehose_destination below.
        :param pulumi.Input['ConfigurationSetEventDestinationEventDestinationPinpointDestinationArgs'] pinpoint_destination: An object that defines an Amazon Pinpoint project destination for email events. See pinpoint_destination below.
        :param pulumi.Input['ConfigurationSetEventDestinationEventDestinationSnsDestinationArgs'] sns_destination: An object that defines an Amazon SNS destination for email events. See sns_destination below.
        """
        pulumi.set(__self__, "matching_event_types", matching_event_types)
        if cloud_watch_destination is not None:
            pulumi.set(__self__, "cloud_watch_destination", cloud_watch_destination)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if kinesis_firehose_destination is not None:
            pulumi.set(__self__, "kinesis_firehose_destination", kinesis_firehose_destination)
        if pinpoint_destination is not None:
            pulumi.set(__self__, "pinpoint_destination", pinpoint_destination)
        if sns_destination is not None:
            pulumi.set(__self__, "sns_destination", sns_destination)

    @property
    @pulumi.getter(name="matchingEventTypes")
    def matching_event_types(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        An array that specifies which events the Amazon SES API v2 should send to the destinations. Valid values: `SEND`, `REJECT`, `BOUNCE`, `COMPLAINT`, `DELIVERY`, `OPEN`, `CLICK`, `RENDERING_FAILURE`, `DELIVERY_DELAY`, `SUBSCRIPTION`.

        The following arguments are optional:
        """
        return pulumi.get(self, "matching_event_types")

    @matching_event_types.setter
    def matching_event_types(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "matching_event_types", value)

    @property
    @pulumi.getter(name="cloudWatchDestination")
    def cloud_watch_destination(self) -> Optional[pulumi.Input['ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationArgs']]:
        """
        An object that defines an Amazon CloudWatch destination for email events. See cloud_watch_destination below
        """
        return pulumi.get(self, "cloud_watch_destination")

    @cloud_watch_destination.setter
    def cloud_watch_destination(self, value: Optional[pulumi.Input['ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationArgs']]):
        pulumi.set(self, "cloud_watch_destination", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        When the event destination is enabled, the specified event types are sent to the destinations. Default: `false`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="kinesisFirehoseDestination")
    def kinesis_firehose_destination(self) -> Optional[pulumi.Input['ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationArgs']]:
        """
        An object that defines an Amazon Kinesis Data Firehose destination for email events. See kinesis_firehose_destination below.
        """
        return pulumi.get(self, "kinesis_firehose_destination")

    @kinesis_firehose_destination.setter
    def kinesis_firehose_destination(self, value: Optional[pulumi.Input['ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationArgs']]):
        pulumi.set(self, "kinesis_firehose_destination", value)

    @property
    @pulumi.getter(name="pinpointDestination")
    def pinpoint_destination(self) -> Optional[pulumi.Input['ConfigurationSetEventDestinationEventDestinationPinpointDestinationArgs']]:
        """
        An object that defines an Amazon Pinpoint project destination for email events. See pinpoint_destination below.
        """
        return pulumi.get(self, "pinpoint_destination")

    @pinpoint_destination.setter
    def pinpoint_destination(self, value: Optional[pulumi.Input['ConfigurationSetEventDestinationEventDestinationPinpointDestinationArgs']]):
        pulumi.set(self, "pinpoint_destination", value)

    @property
    @pulumi.getter(name="snsDestination")
    def sns_destination(self) -> Optional[pulumi.Input['ConfigurationSetEventDestinationEventDestinationSnsDestinationArgs']]:
        """
        An object that defines an Amazon SNS destination for email events. See sns_destination below.
        """
        return pulumi.get(self, "sns_destination")

    @sns_destination.setter
    def sns_destination(self, value: Optional[pulumi.Input['ConfigurationSetEventDestinationEventDestinationSnsDestinationArgs']]):
        pulumi.set(self, "sns_destination", value)


@pulumi.input_type
class ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationArgs:
    def __init__(__self__, *,
                 dimension_configurations: pulumi.Input[Sequence[pulumi.Input['ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationArgs']]]):
        """
        :param pulumi.Input[Sequence[pulumi.Input['ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationArgs']]] dimension_configurations: An array of objects that define the dimensions to use when you send email events to Amazon CloudWatch. See dimension_configuration below.
        """
        pulumi.set(__self__, "dimension_configurations", dimension_configurations)

    @property
    @pulumi.getter(name="dimensionConfigurations")
    def dimension_configurations(self) -> pulumi.Input[Sequence[pulumi.Input['ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationArgs']]]:
        """
        An array of objects that define the dimensions to use when you send email events to Amazon CloudWatch. See dimension_configuration below.
        """
        return pulumi.get(self, "dimension_configurations")

    @dimension_configurations.setter
    def dimension_configurations(self, value: pulumi.Input[Sequence[pulumi.Input['ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationArgs']]]):
        pulumi.set(self, "dimension_configurations", value)


@pulumi.input_type
class ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationArgs:
    def __init__(__self__, *,
                 default_dimension_value: pulumi.Input[str],
                 dimension_name: pulumi.Input[str],
                 dimension_value_source: pulumi.Input[str]):
        """
        :param pulumi.Input[str] default_dimension_value: The default value of the dimension that is published to Amazon CloudWatch if you don't provide the value of the dimension when you send an email.
        :param pulumi.Input[str] dimension_name: The name of an Amazon CloudWatch dimension associated with an email sending metric.
        :param pulumi.Input[str] dimension_value_source: The location where the Amazon SES API v2 finds the value of a dimension to publish to Amazon CloudWatch. Valid values: `MESSAGE_TAG`, `EMAIL_HEADER`, `LINK_TAG`.
        """
        pulumi.set(__self__, "default_dimension_value", default_dimension_value)
        pulumi.set(__self__, "dimension_name", dimension_name)
        pulumi.set(__self__, "dimension_value_source", dimension_value_source)

    @property
    @pulumi.getter(name="defaultDimensionValue")
    def default_dimension_value(self) -> pulumi.Input[str]:
        """
        The default value of the dimension that is published to Amazon CloudWatch if you don't provide the value of the dimension when you send an email.
        """
        return pulumi.get(self, "default_dimension_value")

    @default_dimension_value.setter
    def default_dimension_value(self, value: pulumi.Input[str]):
        pulumi.set(self, "default_dimension_value", value)

    @property
    @pulumi.getter(name="dimensionName")
    def dimension_name(self) -> pulumi.Input[str]:
        """
        The name of an Amazon CloudWatch dimension associated with an email sending metric.
        """
        return pulumi.get(self, "dimension_name")

    @dimension_name.setter
    def dimension_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "dimension_name", value)

    @property
    @pulumi.getter(name="dimensionValueSource")
    def dimension_value_source(self) -> pulumi.Input[str]:
        """
        The location where the Amazon SES API v2 finds the value of a dimension to publish to Amazon CloudWatch. Valid values: `MESSAGE_TAG`, `EMAIL_HEADER`, `LINK_TAG`.
        """
        return pulumi.get(self, "dimension_value_source")

    @dimension_value_source.setter
    def dimension_value_source(self, value: pulumi.Input[str]):
        pulumi.set(self, "dimension_value_source", value)


@pulumi.input_type
class ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationArgs:
    def __init__(__self__, *,
                 delivery_stream_arn: pulumi.Input[str],
                 iam_role_arn: pulumi.Input[str]):
        """
        :param pulumi.Input[str] delivery_stream_arn: The Amazon Resource Name (ARN) of the Amazon Kinesis Data Firehose stream that the Amazon SES API v2 sends email events to.
        :param pulumi.Input[str] iam_role_arn: The Amazon Resource Name (ARN) of the IAM role that the Amazon SES API v2 uses to send email events to the Amazon Kinesis Data Firehose stream.
        """
        pulumi.set(__self__, "delivery_stream_arn", delivery_stream_arn)
        pulumi.set(__self__, "iam_role_arn", iam_role_arn)

    @property
    @pulumi.getter(name="deliveryStreamArn")
    def delivery_stream_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the Amazon Kinesis Data Firehose stream that the Amazon SES API v2 sends email events to.
        """
        return pulumi.get(self, "delivery_stream_arn")

    @delivery_stream_arn.setter
    def delivery_stream_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "delivery_stream_arn", value)

    @property
    @pulumi.getter(name="iamRoleArn")
    def iam_role_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role that the Amazon SES API v2 uses to send email events to the Amazon Kinesis Data Firehose stream.
        """
        return pulumi.get(self, "iam_role_arn")

    @iam_role_arn.setter
    def iam_role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "iam_role_arn", value)


@pulumi.input_type
class ConfigurationSetEventDestinationEventDestinationPinpointDestinationArgs:
    def __init__(__self__, *,
                 application_arn: pulumi.Input[str]):
        pulumi.set(__self__, "application_arn", application_arn)

    @property
    @pulumi.getter(name="applicationArn")
    def application_arn(self) -> pulumi.Input[str]:
        return pulumi.get(self, "application_arn")

    @application_arn.setter
    def application_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "application_arn", value)


@pulumi.input_type
class ConfigurationSetEventDestinationEventDestinationSnsDestinationArgs:
    def __init__(__self__, *,
                 topic_arn: pulumi.Input[str]):
        """
        :param pulumi.Input[str] topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to publish email events to.
        """
        pulumi.set(__self__, "topic_arn", topic_arn)

    @property
    @pulumi.getter(name="topicArn")
    def topic_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the Amazon SNS topic to publish email events to.
        """
        return pulumi.get(self, "topic_arn")

    @topic_arn.setter
    def topic_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "topic_arn", value)


@pulumi.input_type
class ConfigurationSetReputationOptionsArgs:
    def __init__(__self__, *,
                 last_fresh_start: Optional[pulumi.Input[str]] = None,
                 reputation_metrics_enabled: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] last_fresh_start: The date and time (in Unix time) when the reputation metrics were last given a fresh start. When your account is given a fresh start, your reputation metrics are calculated starting from the date of the fresh start.
        :param pulumi.Input[bool] reputation_metrics_enabled: If `true`, tracking of reputation metrics is enabled for the configuration set. If `false`, tracking of reputation metrics is disabled for the configuration set.
        """
        if last_fresh_start is not None:
            pulumi.set(__self__, "last_fresh_start", last_fresh_start)
        if reputation_metrics_enabled is not None:
            pulumi.set(__self__, "reputation_metrics_enabled", reputation_metrics_enabled)

    @property
    @pulumi.getter(name="lastFreshStart")
    def last_fresh_start(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time (in Unix time) when the reputation metrics were last given a fresh start. When your account is given a fresh start, your reputation metrics are calculated starting from the date of the fresh start.
        """
        return pulumi.get(self, "last_fresh_start")

    @last_fresh_start.setter
    def last_fresh_start(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_fresh_start", value)

    @property
    @pulumi.getter(name="reputationMetricsEnabled")
    def reputation_metrics_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If `true`, tracking of reputation metrics is enabled for the configuration set. If `false`, tracking of reputation metrics is disabled for the configuration set.
        """
        return pulumi.get(self, "reputation_metrics_enabled")

    @reputation_metrics_enabled.setter
    def reputation_metrics_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "reputation_metrics_enabled", value)


@pulumi.input_type
class ConfigurationSetSendingOptionsArgs:
    def __init__(__self__, *,
                 sending_enabled: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[bool] sending_enabled: If `true`, email sending is enabled for the configuration set. If `false`, email sending is disabled for the configuration set.
        """
        if sending_enabled is not None:
            pulumi.set(__self__, "sending_enabled", sending_enabled)

    @property
    @pulumi.getter(name="sendingEnabled")
    def sending_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If `true`, email sending is enabled for the configuration set. If `false`, email sending is disabled for the configuration set.
        """
        return pulumi.get(self, "sending_enabled")

    @sending_enabled.setter
    def sending_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sending_enabled", value)


@pulumi.input_type
class ConfigurationSetSuppressionOptionsArgs:
    def __init__(__self__, *,
                 suppressed_reasons: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] suppressed_reasons: A list that contains the reasons that email addresses are automatically added to the suppression list for your account. Valid values: `BOUNCE`, `COMPLAINT`.
        """
        if suppressed_reasons is not None:
            pulumi.set(__self__, "suppressed_reasons", suppressed_reasons)

    @property
    @pulumi.getter(name="suppressedReasons")
    def suppressed_reasons(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list that contains the reasons that email addresses are automatically added to the suppression list for your account. Valid values: `BOUNCE`, `COMPLAINT`.
        """
        return pulumi.get(self, "suppressed_reasons")

    @suppressed_reasons.setter
    def suppressed_reasons(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "suppressed_reasons", value)


@pulumi.input_type
class ConfigurationSetTrackingOptionsArgs:
    def __init__(__self__, *,
                 custom_redirect_domain: pulumi.Input[str]):
        """
        :param pulumi.Input[str] custom_redirect_domain: The domain to use for tracking open and click events.
        """
        pulumi.set(__self__, "custom_redirect_domain", custom_redirect_domain)

    @property
    @pulumi.getter(name="customRedirectDomain")
    def custom_redirect_domain(self) -> pulumi.Input[str]:
        """
        The domain to use for tracking open and click events.
        """
        return pulumi.get(self, "custom_redirect_domain")

    @custom_redirect_domain.setter
    def custom_redirect_domain(self, value: pulumi.Input[str]):
        pulumi.set(self, "custom_redirect_domain", value)


@pulumi.input_type
class ConfigurationSetVdmOptionsArgs:
    def __init__(__self__, *,
                 dashboard_options: Optional[pulumi.Input['ConfigurationSetVdmOptionsDashboardOptionsArgs']] = None,
                 guardian_options: Optional[pulumi.Input['ConfigurationSetVdmOptionsGuardianOptionsArgs']] = None):
        """
        :param pulumi.Input['ConfigurationSetVdmOptionsDashboardOptionsArgs'] dashboard_options: Specifies additional settings for your VDM configuration as applicable to the Dashboard.
        :param pulumi.Input['ConfigurationSetVdmOptionsGuardianOptionsArgs'] guardian_options: Specifies additional settings for your VDM configuration as applicable to the Guardian.
        """
        if dashboard_options is not None:
            pulumi.set(__self__, "dashboard_options", dashboard_options)
        if guardian_options is not None:
            pulumi.set(__self__, "guardian_options", guardian_options)

    @property
    @pulumi.getter(name="dashboardOptions")
    def dashboard_options(self) -> Optional[pulumi.Input['ConfigurationSetVdmOptionsDashboardOptionsArgs']]:
        """
        Specifies additional settings for your VDM configuration as applicable to the Dashboard.
        """
        return pulumi.get(self, "dashboard_options")

    @dashboard_options.setter
    def dashboard_options(self, value: Optional[pulumi.Input['ConfigurationSetVdmOptionsDashboardOptionsArgs']]):
        pulumi.set(self, "dashboard_options", value)

    @property
    @pulumi.getter(name="guardianOptions")
    def guardian_options(self) -> Optional[pulumi.Input['ConfigurationSetVdmOptionsGuardianOptionsArgs']]:
        """
        Specifies additional settings for your VDM configuration as applicable to the Guardian.
        """
        return pulumi.get(self, "guardian_options")

    @guardian_options.setter
    def guardian_options(self, value: Optional[pulumi.Input['ConfigurationSetVdmOptionsGuardianOptionsArgs']]):
        pulumi.set(self, "guardian_options", value)


@pulumi.input_type
class ConfigurationSetVdmOptionsDashboardOptionsArgs:
    def __init__(__self__, *,
                 engagement_metrics: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] engagement_metrics: Specifies the status of your VDM engagement metrics collection. Valid values: `ENABLED`, `DISABLED`.
        """
        if engagement_metrics is not None:
            pulumi.set(__self__, "engagement_metrics", engagement_metrics)

    @property
    @pulumi.getter(name="engagementMetrics")
    def engagement_metrics(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the status of your VDM engagement metrics collection. Valid values: `ENABLED`, `DISABLED`.
        """
        return pulumi.get(self, "engagement_metrics")

    @engagement_metrics.setter
    def engagement_metrics(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "engagement_metrics", value)


@pulumi.input_type
class ConfigurationSetVdmOptionsGuardianOptionsArgs:
    def __init__(__self__, *,
                 optimized_shared_delivery: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] optimized_shared_delivery: Specifies the status of your VDM optimized shared delivery. Valid values: `ENABLED`, `DISABLED`.
        """
        if optimized_shared_delivery is not None:
            pulumi.set(__self__, "optimized_shared_delivery", optimized_shared_delivery)

    @property
    @pulumi.getter(name="optimizedSharedDelivery")
    def optimized_shared_delivery(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the status of your VDM optimized shared delivery. Valid values: `ENABLED`, `DISABLED`.
        """
        return pulumi.get(self, "optimized_shared_delivery")

    @optimized_shared_delivery.setter
    def optimized_shared_delivery(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "optimized_shared_delivery", value)


@pulumi.input_type
class ContactListTopicArgs:
    def __init__(__self__, *,
                 default_subscription_status: pulumi.Input[str],
                 display_name: pulumi.Input[str],
                 topic_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] default_subscription_status: The default subscription status to be applied to a contact if the contact has not noted their preference for subscribing to a topic.
        :param pulumi.Input[str] display_name: The name of the topic the contact will see.
        :param pulumi.Input[str] topic_name: The name of the topic.
               
               The following arguments are optional:
        :param pulumi.Input[str] description: A description of what the topic is about, which the contact will see.
        """
        pulumi.set(__self__, "default_subscription_status", default_subscription_status)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "topic_name", topic_name)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="defaultSubscriptionStatus")
    def default_subscription_status(self) -> pulumi.Input[str]:
        """
        The default subscription status to be applied to a contact if the contact has not noted their preference for subscribing to a topic.
        """
        return pulumi.get(self, "default_subscription_status")

    @default_subscription_status.setter
    def default_subscription_status(self, value: pulumi.Input[str]):
        pulumi.set(self, "default_subscription_status", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        The name of the topic the contact will see.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="topicName")
    def topic_name(self) -> pulumi.Input[str]:
        """
        The name of the topic.

        The following arguments are optional:
        """
        return pulumi.get(self, "topic_name")

    @topic_name.setter
    def topic_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "topic_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of what the topic is about, which the contact will see.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class EmailIdentityDkimSigningAttributesArgs:
    def __init__(__self__, *,
                 current_signing_key_length: Optional[pulumi.Input[str]] = None,
                 domain_signing_private_key: Optional[pulumi.Input[str]] = None,
                 domain_signing_selector: Optional[pulumi.Input[str]] = None,
                 last_key_generation_timestamp: Optional[pulumi.Input[str]] = None,
                 next_signing_key_length: Optional[pulumi.Input[str]] = None,
                 signing_attributes_origin: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tokens: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] current_signing_key_length: [Easy DKIM] The key length of the DKIM key pair in use.
        :param pulumi.Input[str] domain_signing_private_key: [Bring Your Own DKIM] A private key that's used to generate a DKIM signature. The private key must use 1024 or 2048-bit RSA encryption, and must be encoded using base64 encoding.
               
               > **NOTE:** You have to delete the first and last lines ('-----BEGIN PRIVATE KEY-----' and '-----END PRIVATE KEY-----', respectively) of the generated private key. Additionally, you have to remove the line breaks in the generated private key. The resulting value is a string of characters with no spaces or line breaks.
        :param pulumi.Input[str] domain_signing_selector: [Bring Your Own DKIM] A string that's used to identify a public key in the DNS configuration for a domain.
        :param pulumi.Input[str] last_key_generation_timestamp: [Easy DKIM] The last time a key pair was generated for this identity.
        :param pulumi.Input[str] next_signing_key_length: [Easy DKIM] The key length of the future DKIM key pair to be generated. This can be changed at most once per day. Valid values: `RSA_1024_BIT`, `RSA_2048_BIT`.
        :param pulumi.Input[str] signing_attributes_origin: A string that indicates how DKIM was configured for the identity. `AWS_SES` indicates that DKIM was configured for the identity by using Easy DKIM. `EXTERNAL` indicates that DKIM was configured for the identity by using Bring Your Own DKIM (BYODKIM).
        :param pulumi.Input[str] status: Describes whether or not Amazon SES has successfully located the DKIM records in the DNS records for the domain. See the [AWS SES API v2 Reference](https://docs.aws.amazon.com/ses/latest/APIReference-V2/API_DkimAttributes.html#SES-Type-DkimAttributes-Status) for supported statuses.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tokens: If you used Easy DKIM to configure DKIM authentication for the domain, then this object contains a set of unique strings that you use to create a set of CNAME records that you add to the DNS configuration for your domain. When Amazon SES detects these records in the DNS configuration for your domain, the DKIM authentication process is complete. If you configured DKIM authentication for the domain by providing your own public-private key pair, then this object contains the selector for the public key.
        """
        if current_signing_key_length is not None:
            pulumi.set(__self__, "current_signing_key_length", current_signing_key_length)
        if domain_signing_private_key is not None:
            pulumi.set(__self__, "domain_signing_private_key", domain_signing_private_key)
        if domain_signing_selector is not None:
            pulumi.set(__self__, "domain_signing_selector", domain_signing_selector)
        if last_key_generation_timestamp is not None:
            pulumi.set(__self__, "last_key_generation_timestamp", last_key_generation_timestamp)
        if next_signing_key_length is not None:
            pulumi.set(__self__, "next_signing_key_length", next_signing_key_length)
        if signing_attributes_origin is not None:
            pulumi.set(__self__, "signing_attributes_origin", signing_attributes_origin)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if tokens is not None:
            pulumi.set(__self__, "tokens", tokens)

    @property
    @pulumi.getter(name="currentSigningKeyLength")
    def current_signing_key_length(self) -> Optional[pulumi.Input[str]]:
        """
        [Easy DKIM] The key length of the DKIM key pair in use.
        """
        return pulumi.get(self, "current_signing_key_length")

    @current_signing_key_length.setter
    def current_signing_key_length(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "current_signing_key_length", value)

    @property
    @pulumi.getter(name="domainSigningPrivateKey")
    def domain_signing_private_key(self) -> Optional[pulumi.Input[str]]:
        """
        [Bring Your Own DKIM] A private key that's used to generate a DKIM signature. The private key must use 1024 or 2048-bit RSA encryption, and must be encoded using base64 encoding.

        > **NOTE:** You have to delete the first and last lines ('-----BEGIN PRIVATE KEY-----' and '-----END PRIVATE KEY-----', respectively) of the generated private key. Additionally, you have to remove the line breaks in the generated private key. The resulting value is a string of characters with no spaces or line breaks.
        """
        return pulumi.get(self, "domain_signing_private_key")

    @domain_signing_private_key.setter
    def domain_signing_private_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_signing_private_key", value)

    @property
    @pulumi.getter(name="domainSigningSelector")
    def domain_signing_selector(self) -> Optional[pulumi.Input[str]]:
        """
        [Bring Your Own DKIM] A string that's used to identify a public key in the DNS configuration for a domain.
        """
        return pulumi.get(self, "domain_signing_selector")

    @domain_signing_selector.setter
    def domain_signing_selector(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_signing_selector", value)

    @property
    @pulumi.getter(name="lastKeyGenerationTimestamp")
    def last_key_generation_timestamp(self) -> Optional[pulumi.Input[str]]:
        """
        [Easy DKIM] The last time a key pair was generated for this identity.
        """
        return pulumi.get(self, "last_key_generation_timestamp")

    @last_key_generation_timestamp.setter
    def last_key_generation_timestamp(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_key_generation_timestamp", value)

    @property
    @pulumi.getter(name="nextSigningKeyLength")
    def next_signing_key_length(self) -> Optional[pulumi.Input[str]]:
        """
        [Easy DKIM] The key length of the future DKIM key pair to be generated. This can be changed at most once per day. Valid values: `RSA_1024_BIT`, `RSA_2048_BIT`.
        """
        return pulumi.get(self, "next_signing_key_length")

    @next_signing_key_length.setter
    def next_signing_key_length(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "next_signing_key_length", value)

    @property
    @pulumi.getter(name="signingAttributesOrigin")
    def signing_attributes_origin(self) -> Optional[pulumi.Input[str]]:
        """
        A string that indicates how DKIM was configured for the identity. `AWS_SES` indicates that DKIM was configured for the identity by using Easy DKIM. `EXTERNAL` indicates that DKIM was configured for the identity by using Bring Your Own DKIM (BYODKIM).
        """
        return pulumi.get(self, "signing_attributes_origin")

    @signing_attributes_origin.setter
    def signing_attributes_origin(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "signing_attributes_origin", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Describes whether or not Amazon SES has successfully located the DKIM records in the DNS records for the domain. See the [AWS SES API v2 Reference](https://docs.aws.amazon.com/ses/latest/APIReference-V2/API_DkimAttributes.html#SES-Type-DkimAttributes-Status) for supported statuses.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def tokens(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        If you used Easy DKIM to configure DKIM authentication for the domain, then this object contains a set of unique strings that you use to create a set of CNAME records that you add to the DNS configuration for your domain. When Amazon SES detects these records in the DNS configuration for your domain, the DKIM authentication process is complete. If you configured DKIM authentication for the domain by providing your own public-private key pair, then this object contains the selector for the public key.
        """
        return pulumi.get(self, "tokens")

    @tokens.setter
    def tokens(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tokens", value)


