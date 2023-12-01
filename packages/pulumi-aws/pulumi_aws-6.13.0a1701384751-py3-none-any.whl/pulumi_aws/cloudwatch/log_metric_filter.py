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

__all__ = ['LogMetricFilterArgs', 'LogMetricFilter']

@pulumi.input_type
class LogMetricFilterArgs:
    def __init__(__self__, *,
                 log_group_name: pulumi.Input[str],
                 metric_transformation: pulumi.Input['LogMetricFilterMetricTransformationArgs'],
                 pattern: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a LogMetricFilter resource.
        :param pulumi.Input[str] log_group_name: The name of the log group to associate the metric filter with.
        :param pulumi.Input['LogMetricFilterMetricTransformationArgs'] metric_transformation: A block defining collection of information needed to define how metric data gets emitted. See below.
        :param pulumi.Input[str] pattern: A valid [CloudWatch Logs filter pattern](https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/FilterAndPatternSyntax.html)
               for extracting metric data out of ingested log events.
        :param pulumi.Input[str] name: A name for the metric filter.
        """
        pulumi.set(__self__, "log_group_name", log_group_name)
        pulumi.set(__self__, "metric_transformation", metric_transformation)
        pulumi.set(__self__, "pattern", pattern)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> pulumi.Input[str]:
        """
        The name of the log group to associate the metric filter with.
        """
        return pulumi.get(self, "log_group_name")

    @log_group_name.setter
    def log_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_group_name", value)

    @property
    @pulumi.getter(name="metricTransformation")
    def metric_transformation(self) -> pulumi.Input['LogMetricFilterMetricTransformationArgs']:
        """
        A block defining collection of information needed to define how metric data gets emitted. See below.
        """
        return pulumi.get(self, "metric_transformation")

    @metric_transformation.setter
    def metric_transformation(self, value: pulumi.Input['LogMetricFilterMetricTransformationArgs']):
        pulumi.set(self, "metric_transformation", value)

    @property
    @pulumi.getter
    def pattern(self) -> pulumi.Input[str]:
        """
        A valid [CloudWatch Logs filter pattern](https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/FilterAndPatternSyntax.html)
        for extracting metric data out of ingested log events.
        """
        return pulumi.get(self, "pattern")

    @pattern.setter
    def pattern(self, value: pulumi.Input[str]):
        pulumi.set(self, "pattern", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the metric filter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _LogMetricFilterState:
    def __init__(__self__, *,
                 log_group_name: Optional[pulumi.Input[str]] = None,
                 metric_transformation: Optional[pulumi.Input['LogMetricFilterMetricTransformationArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pattern: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LogMetricFilter resources.
        :param pulumi.Input[str] log_group_name: The name of the log group to associate the metric filter with.
        :param pulumi.Input['LogMetricFilterMetricTransformationArgs'] metric_transformation: A block defining collection of information needed to define how metric data gets emitted. See below.
        :param pulumi.Input[str] name: A name for the metric filter.
        :param pulumi.Input[str] pattern: A valid [CloudWatch Logs filter pattern](https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/FilterAndPatternSyntax.html)
               for extracting metric data out of ingested log events.
        """
        if log_group_name is not None:
            pulumi.set(__self__, "log_group_name", log_group_name)
        if metric_transformation is not None:
            pulumi.set(__self__, "metric_transformation", metric_transformation)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if pattern is not None:
            pulumi.set(__self__, "pattern", pattern)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the log group to associate the metric filter with.
        """
        return pulumi.get(self, "log_group_name")

    @log_group_name.setter
    def log_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_group_name", value)

    @property
    @pulumi.getter(name="metricTransformation")
    def metric_transformation(self) -> Optional[pulumi.Input['LogMetricFilterMetricTransformationArgs']]:
        """
        A block defining collection of information needed to define how metric data gets emitted. See below.
        """
        return pulumi.get(self, "metric_transformation")

    @metric_transformation.setter
    def metric_transformation(self, value: Optional[pulumi.Input['LogMetricFilterMetricTransformationArgs']]):
        pulumi.set(self, "metric_transformation", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the metric filter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def pattern(self) -> Optional[pulumi.Input[str]]:
        """
        A valid [CloudWatch Logs filter pattern](https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/FilterAndPatternSyntax.html)
        for extracting metric data out of ingested log events.
        """
        return pulumi.get(self, "pattern")

    @pattern.setter
    def pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pattern", value)


class LogMetricFilter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 log_group_name: Optional[pulumi.Input[str]] = None,
                 metric_transformation: Optional[pulumi.Input[pulumi.InputType['LogMetricFilterMetricTransformationArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pattern: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a CloudWatch Log Metric Filter resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        dada = aws.cloudwatch.LogGroup("dada")
        yada = aws.cloudwatch.LogMetricFilter("yada",
            pattern="",
            log_group_name=dada.name,
            metric_transformation=aws.cloudwatch.LogMetricFilterMetricTransformationArgs(
                name="EventCount",
                namespace="YourNamespace",
                value="1",
            ))
        ```

        ## Import

        Using `pulumi import`, import CloudWatch Log Metric Filter using the `log_group_name:name`. For example:

        ```sh
         $ pulumi import aws:cloudwatch/logMetricFilter:LogMetricFilter test /aws/lambda/function:test
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] log_group_name: The name of the log group to associate the metric filter with.
        :param pulumi.Input[pulumi.InputType['LogMetricFilterMetricTransformationArgs']] metric_transformation: A block defining collection of information needed to define how metric data gets emitted. See below.
        :param pulumi.Input[str] name: A name for the metric filter.
        :param pulumi.Input[str] pattern: A valid [CloudWatch Logs filter pattern](https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/FilterAndPatternSyntax.html)
               for extracting metric data out of ingested log events.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LogMetricFilterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a CloudWatch Log Metric Filter resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        dada = aws.cloudwatch.LogGroup("dada")
        yada = aws.cloudwatch.LogMetricFilter("yada",
            pattern="",
            log_group_name=dada.name,
            metric_transformation=aws.cloudwatch.LogMetricFilterMetricTransformationArgs(
                name="EventCount",
                namespace="YourNamespace",
                value="1",
            ))
        ```

        ## Import

        Using `pulumi import`, import CloudWatch Log Metric Filter using the `log_group_name:name`. For example:

        ```sh
         $ pulumi import aws:cloudwatch/logMetricFilter:LogMetricFilter test /aws/lambda/function:test
        ```

        :param str resource_name: The name of the resource.
        :param LogMetricFilterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LogMetricFilterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 log_group_name: Optional[pulumi.Input[str]] = None,
                 metric_transformation: Optional[pulumi.Input[pulumi.InputType['LogMetricFilterMetricTransformationArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pattern: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LogMetricFilterArgs.__new__(LogMetricFilterArgs)

            if log_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'log_group_name'")
            __props__.__dict__["log_group_name"] = log_group_name
            if metric_transformation is None and not opts.urn:
                raise TypeError("Missing required property 'metric_transformation'")
            __props__.__dict__["metric_transformation"] = metric_transformation
            __props__.__dict__["name"] = name
            if pattern is None and not opts.urn:
                raise TypeError("Missing required property 'pattern'")
            __props__.__dict__["pattern"] = pattern
        super(LogMetricFilter, __self__).__init__(
            'aws:cloudwatch/logMetricFilter:LogMetricFilter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            log_group_name: Optional[pulumi.Input[str]] = None,
            metric_transformation: Optional[pulumi.Input[pulumi.InputType['LogMetricFilterMetricTransformationArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            pattern: Optional[pulumi.Input[str]] = None) -> 'LogMetricFilter':
        """
        Get an existing LogMetricFilter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] log_group_name: The name of the log group to associate the metric filter with.
        :param pulumi.Input[pulumi.InputType['LogMetricFilterMetricTransformationArgs']] metric_transformation: A block defining collection of information needed to define how metric data gets emitted. See below.
        :param pulumi.Input[str] name: A name for the metric filter.
        :param pulumi.Input[str] pattern: A valid [CloudWatch Logs filter pattern](https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/FilterAndPatternSyntax.html)
               for extracting metric data out of ingested log events.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LogMetricFilterState.__new__(_LogMetricFilterState)

        __props__.__dict__["log_group_name"] = log_group_name
        __props__.__dict__["metric_transformation"] = metric_transformation
        __props__.__dict__["name"] = name
        __props__.__dict__["pattern"] = pattern
        return LogMetricFilter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> pulumi.Output[str]:
        """
        The name of the log group to associate the metric filter with.
        """
        return pulumi.get(self, "log_group_name")

    @property
    @pulumi.getter(name="metricTransformation")
    def metric_transformation(self) -> pulumi.Output['outputs.LogMetricFilterMetricTransformation']:
        """
        A block defining collection of information needed to define how metric data gets emitted. See below.
        """
        return pulumi.get(self, "metric_transformation")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A name for the metric filter.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def pattern(self) -> pulumi.Output[str]:
        """
        A valid [CloudWatch Logs filter pattern](https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/FilterAndPatternSyntax.html)
        for extracting metric data out of ingested log events.
        """
        return pulumi.get(self, "pattern")

