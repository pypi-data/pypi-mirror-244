# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['ConfigurationSetArgs', 'ConfigurationSet']

@pulumi.input_type
class ConfigurationSetArgs:
    def __init__(__self__, *,
                 delivery_options: Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reputation_metrics_enabled: Optional[pulumi.Input[bool]] = None,
                 sending_enabled: Optional[pulumi.Input[bool]] = None,
                 tracking_options: Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']] = None):
        """
        The set of arguments for constructing a ConfigurationSet resource.
        :param pulumi.Input['ConfigurationSetDeliveryOptionsArgs'] delivery_options: Whether messages that use the configuration set are required to use TLS. See below.
        :param pulumi.Input[str] name: Name of the configuration set.
               
               The following argument is optional:
        :param pulumi.Input[bool] reputation_metrics_enabled: Whether or not Amazon SES publishes reputation metrics for the configuration set, such as bounce and complaint rates, to Amazon CloudWatch. The default value is `false`.
        :param pulumi.Input[bool] sending_enabled: Whether email sending is enabled or disabled for the configuration set. The default value is `true`.
        :param pulumi.Input['ConfigurationSetTrackingOptionsArgs'] tracking_options: Domain that is used to redirect email recipients to an Amazon SES-operated domain. See below. **NOTE:** This functionality is best effort.
        """
        if delivery_options is not None:
            pulumi.set(__self__, "delivery_options", delivery_options)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if reputation_metrics_enabled is not None:
            pulumi.set(__self__, "reputation_metrics_enabled", reputation_metrics_enabled)
        if sending_enabled is not None:
            pulumi.set(__self__, "sending_enabled", sending_enabled)
        if tracking_options is not None:
            pulumi.set(__self__, "tracking_options", tracking_options)

    @property
    @pulumi.getter(name="deliveryOptions")
    def delivery_options(self) -> Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']]:
        """
        Whether messages that use the configuration set are required to use TLS. See below.
        """
        return pulumi.get(self, "delivery_options")

    @delivery_options.setter
    def delivery_options(self, value: Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']]):
        pulumi.set(self, "delivery_options", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the configuration set.

        The following argument is optional:
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="reputationMetricsEnabled")
    def reputation_metrics_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not Amazon SES publishes reputation metrics for the configuration set, such as bounce and complaint rates, to Amazon CloudWatch. The default value is `false`.
        """
        return pulumi.get(self, "reputation_metrics_enabled")

    @reputation_metrics_enabled.setter
    def reputation_metrics_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "reputation_metrics_enabled", value)

    @property
    @pulumi.getter(name="sendingEnabled")
    def sending_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether email sending is enabled or disabled for the configuration set. The default value is `true`.
        """
        return pulumi.get(self, "sending_enabled")

    @sending_enabled.setter
    def sending_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sending_enabled", value)

    @property
    @pulumi.getter(name="trackingOptions")
    def tracking_options(self) -> Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']]:
        """
        Domain that is used to redirect email recipients to an Amazon SES-operated domain. See below. **NOTE:** This functionality is best effort.
        """
        return pulumi.get(self, "tracking_options")

    @tracking_options.setter
    def tracking_options(self, value: Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']]):
        pulumi.set(self, "tracking_options", value)


@pulumi.input_type
class _ConfigurationSetState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 delivery_options: Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']] = None,
                 last_fresh_start: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reputation_metrics_enabled: Optional[pulumi.Input[bool]] = None,
                 sending_enabled: Optional[pulumi.Input[bool]] = None,
                 tracking_options: Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']] = None):
        """
        Input properties used for looking up and filtering ConfigurationSet resources.
        :param pulumi.Input[str] arn: SES configuration set ARN.
        :param pulumi.Input['ConfigurationSetDeliveryOptionsArgs'] delivery_options: Whether messages that use the configuration set are required to use TLS. See below.
        :param pulumi.Input[str] last_fresh_start: Date and time at which the reputation metrics for the configuration set were last reset. Resetting these metrics is known as a fresh start.
        :param pulumi.Input[str] name: Name of the configuration set.
               
               The following argument is optional:
        :param pulumi.Input[bool] reputation_metrics_enabled: Whether or not Amazon SES publishes reputation metrics for the configuration set, such as bounce and complaint rates, to Amazon CloudWatch. The default value is `false`.
        :param pulumi.Input[bool] sending_enabled: Whether email sending is enabled or disabled for the configuration set. The default value is `true`.
        :param pulumi.Input['ConfigurationSetTrackingOptionsArgs'] tracking_options: Domain that is used to redirect email recipients to an Amazon SES-operated domain. See below. **NOTE:** This functionality is best effort.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if delivery_options is not None:
            pulumi.set(__self__, "delivery_options", delivery_options)
        if last_fresh_start is not None:
            pulumi.set(__self__, "last_fresh_start", last_fresh_start)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if reputation_metrics_enabled is not None:
            pulumi.set(__self__, "reputation_metrics_enabled", reputation_metrics_enabled)
        if sending_enabled is not None:
            pulumi.set(__self__, "sending_enabled", sending_enabled)
        if tracking_options is not None:
            pulumi.set(__self__, "tracking_options", tracking_options)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        SES configuration set ARN.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="deliveryOptions")
    def delivery_options(self) -> Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']]:
        """
        Whether messages that use the configuration set are required to use TLS. See below.
        """
        return pulumi.get(self, "delivery_options")

    @delivery_options.setter
    def delivery_options(self, value: Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']]):
        pulumi.set(self, "delivery_options", value)

    @property
    @pulumi.getter(name="lastFreshStart")
    def last_fresh_start(self) -> Optional[pulumi.Input[str]]:
        """
        Date and time at which the reputation metrics for the configuration set were last reset. Resetting these metrics is known as a fresh start.
        """
        return pulumi.get(self, "last_fresh_start")

    @last_fresh_start.setter
    def last_fresh_start(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_fresh_start", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the configuration set.

        The following argument is optional:
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="reputationMetricsEnabled")
    def reputation_metrics_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not Amazon SES publishes reputation metrics for the configuration set, such as bounce and complaint rates, to Amazon CloudWatch. The default value is `false`.
        """
        return pulumi.get(self, "reputation_metrics_enabled")

    @reputation_metrics_enabled.setter
    def reputation_metrics_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "reputation_metrics_enabled", value)

    @property
    @pulumi.getter(name="sendingEnabled")
    def sending_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether email sending is enabled or disabled for the configuration set. The default value is `true`.
        """
        return pulumi.get(self, "sending_enabled")

    @sending_enabled.setter
    def sending_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sending_enabled", value)

    @property
    @pulumi.getter(name="trackingOptions")
    def tracking_options(self) -> Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']]:
        """
        Domain that is used to redirect email recipients to an Amazon SES-operated domain. See below. **NOTE:** This functionality is best effort.
        """
        return pulumi.get(self, "tracking_options")

    @tracking_options.setter
    def tracking_options(self, value: Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']]):
        pulumi.set(self, "tracking_options", value)


class ConfigurationSet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 delivery_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetDeliveryOptionsArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reputation_metrics_enabled: Optional[pulumi.Input[bool]] = None,
                 sending_enabled: Optional[pulumi.Input[bool]] = None,
                 tracking_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetTrackingOptionsArgs']]] = None,
                 __props__=None):
        """
        Provides an SES configuration set resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.ses.ConfigurationSet("test")
        ```
        ### Require TLS Connections

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.ses.ConfigurationSet("test", delivery_options=aws.ses.ConfigurationSetDeliveryOptionsArgs(
            tls_policy="Require",
        ))
        ```

        ## Import

        Using `pulumi import`, import SES Configuration Sets using their `name`. For example:

        ```sh
         $ pulumi import aws:ses/configurationSet:ConfigurationSet test some-configuration-set-test
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetDeliveryOptionsArgs']] delivery_options: Whether messages that use the configuration set are required to use TLS. See below.
        :param pulumi.Input[str] name: Name of the configuration set.
               
               The following argument is optional:
        :param pulumi.Input[bool] reputation_metrics_enabled: Whether or not Amazon SES publishes reputation metrics for the configuration set, such as bounce and complaint rates, to Amazon CloudWatch. The default value is `false`.
        :param pulumi.Input[bool] sending_enabled: Whether email sending is enabled or disabled for the configuration set. The default value is `true`.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetTrackingOptionsArgs']] tracking_options: Domain that is used to redirect email recipients to an Amazon SES-operated domain. See below. **NOTE:** This functionality is best effort.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ConfigurationSetArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an SES configuration set resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.ses.ConfigurationSet("test")
        ```
        ### Require TLS Connections

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.ses.ConfigurationSet("test", delivery_options=aws.ses.ConfigurationSetDeliveryOptionsArgs(
            tls_policy="Require",
        ))
        ```

        ## Import

        Using `pulumi import`, import SES Configuration Sets using their `name`. For example:

        ```sh
         $ pulumi import aws:ses/configurationSet:ConfigurationSet test some-configuration-set-test
        ```

        :param str resource_name: The name of the resource.
        :param ConfigurationSetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConfigurationSetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 delivery_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetDeliveryOptionsArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reputation_metrics_enabled: Optional[pulumi.Input[bool]] = None,
                 sending_enabled: Optional[pulumi.Input[bool]] = None,
                 tracking_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetTrackingOptionsArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConfigurationSetArgs.__new__(ConfigurationSetArgs)

            __props__.__dict__["delivery_options"] = delivery_options
            __props__.__dict__["name"] = name
            __props__.__dict__["reputation_metrics_enabled"] = reputation_metrics_enabled
            __props__.__dict__["sending_enabled"] = sending_enabled
            __props__.__dict__["tracking_options"] = tracking_options
            __props__.__dict__["arn"] = None
            __props__.__dict__["last_fresh_start"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="aws:ses/confgurationSet:ConfgurationSet")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ConfigurationSet, __self__).__init__(
            'aws:ses/configurationSet:ConfigurationSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            delivery_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetDeliveryOptionsArgs']]] = None,
            last_fresh_start: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            reputation_metrics_enabled: Optional[pulumi.Input[bool]] = None,
            sending_enabled: Optional[pulumi.Input[bool]] = None,
            tracking_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetTrackingOptionsArgs']]] = None) -> 'ConfigurationSet':
        """
        Get an existing ConfigurationSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: SES configuration set ARN.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetDeliveryOptionsArgs']] delivery_options: Whether messages that use the configuration set are required to use TLS. See below.
        :param pulumi.Input[str] last_fresh_start: Date and time at which the reputation metrics for the configuration set were last reset. Resetting these metrics is known as a fresh start.
        :param pulumi.Input[str] name: Name of the configuration set.
               
               The following argument is optional:
        :param pulumi.Input[bool] reputation_metrics_enabled: Whether or not Amazon SES publishes reputation metrics for the configuration set, such as bounce and complaint rates, to Amazon CloudWatch. The default value is `false`.
        :param pulumi.Input[bool] sending_enabled: Whether email sending is enabled or disabled for the configuration set. The default value is `true`.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetTrackingOptionsArgs']] tracking_options: Domain that is used to redirect email recipients to an Amazon SES-operated domain. See below. **NOTE:** This functionality is best effort.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ConfigurationSetState.__new__(_ConfigurationSetState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["delivery_options"] = delivery_options
        __props__.__dict__["last_fresh_start"] = last_fresh_start
        __props__.__dict__["name"] = name
        __props__.__dict__["reputation_metrics_enabled"] = reputation_metrics_enabled
        __props__.__dict__["sending_enabled"] = sending_enabled
        __props__.__dict__["tracking_options"] = tracking_options
        return ConfigurationSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        SES configuration set ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="deliveryOptions")
    def delivery_options(self) -> pulumi.Output[Optional['outputs.ConfigurationSetDeliveryOptions']]:
        """
        Whether messages that use the configuration set are required to use TLS. See below.
        """
        return pulumi.get(self, "delivery_options")

    @property
    @pulumi.getter(name="lastFreshStart")
    def last_fresh_start(self) -> pulumi.Output[str]:
        """
        Date and time at which the reputation metrics for the configuration set were last reset. Resetting these metrics is known as a fresh start.
        """
        return pulumi.get(self, "last_fresh_start")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the configuration set.

        The following argument is optional:
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="reputationMetricsEnabled")
    def reputation_metrics_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether or not Amazon SES publishes reputation metrics for the configuration set, such as bounce and complaint rates, to Amazon CloudWatch. The default value is `false`.
        """
        return pulumi.get(self, "reputation_metrics_enabled")

    @property
    @pulumi.getter(name="sendingEnabled")
    def sending_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether email sending is enabled or disabled for the configuration set. The default value is `true`.
        """
        return pulumi.get(self, "sending_enabled")

    @property
    @pulumi.getter(name="trackingOptions")
    def tracking_options(self) -> pulumi.Output[Optional['outputs.ConfigurationSetTrackingOptions']]:
        """
        Domain that is used to redirect email recipients to an Amazon SES-operated domain. See below. **NOTE:** This functionality is best effort.
        """
        return pulumi.get(self, "tracking_options")

