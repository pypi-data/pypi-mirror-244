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

__all__ = ['RegistryScanningConfigurationArgs', 'RegistryScanningConfiguration']

@pulumi.input_type
class RegistryScanningConfigurationArgs:
    def __init__(__self__, *,
                 scan_type: pulumi.Input[str],
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input['RegistryScanningConfigurationRuleArgs']]]] = None):
        """
        The set of arguments for constructing a RegistryScanningConfiguration resource.
        :param pulumi.Input[str] scan_type: the scanning type to set for the registry. Can be either `ENHANCED` or `BASIC`.
        :param pulumi.Input[Sequence[pulumi.Input['RegistryScanningConfigurationRuleArgs']]] rules: One or multiple blocks specifying scanning rules to determine which repository filters are used and at what frequency scanning will occur. See below for schema.
        """
        pulumi.set(__self__, "scan_type", scan_type)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)

    @property
    @pulumi.getter(name="scanType")
    def scan_type(self) -> pulumi.Input[str]:
        """
        the scanning type to set for the registry. Can be either `ENHANCED` or `BASIC`.
        """
        return pulumi.get(self, "scan_type")

    @scan_type.setter
    def scan_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "scan_type", value)

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RegistryScanningConfigurationRuleArgs']]]]:
        """
        One or multiple blocks specifying scanning rules to determine which repository filters are used and at what frequency scanning will occur. See below for schema.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RegistryScanningConfigurationRuleArgs']]]]):
        pulumi.set(self, "rules", value)


@pulumi.input_type
class _RegistryScanningConfigurationState:
    def __init__(__self__, *,
                 registry_id: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input['RegistryScanningConfigurationRuleArgs']]]] = None,
                 scan_type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RegistryScanningConfiguration resources.
        :param pulumi.Input[str] registry_id: The registry ID the scanning configuration applies to.
        :param pulumi.Input[Sequence[pulumi.Input['RegistryScanningConfigurationRuleArgs']]] rules: One or multiple blocks specifying scanning rules to determine which repository filters are used and at what frequency scanning will occur. See below for schema.
        :param pulumi.Input[str] scan_type: the scanning type to set for the registry. Can be either `ENHANCED` or `BASIC`.
        """
        if registry_id is not None:
            pulumi.set(__self__, "registry_id", registry_id)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)
        if scan_type is not None:
            pulumi.set(__self__, "scan_type", scan_type)

    @property
    @pulumi.getter(name="registryId")
    def registry_id(self) -> Optional[pulumi.Input[str]]:
        """
        The registry ID the scanning configuration applies to.
        """
        return pulumi.get(self, "registry_id")

    @registry_id.setter
    def registry_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "registry_id", value)

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RegistryScanningConfigurationRuleArgs']]]]:
        """
        One or multiple blocks specifying scanning rules to determine which repository filters are used and at what frequency scanning will occur. See below for schema.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RegistryScanningConfigurationRuleArgs']]]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter(name="scanType")
    def scan_type(self) -> Optional[pulumi.Input[str]]:
        """
        the scanning type to set for the registry. Can be either `ENHANCED` or `BASIC`.
        """
        return pulumi.get(self, "scan_type")

    @scan_type.setter
    def scan_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scan_type", value)


class RegistryScanningConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RegistryScanningConfigurationRuleArgs']]]]] = None,
                 scan_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an Elastic Container Registry Scanning Configuration. Can't be completely deleted, instead reverts to the default `BASIC` scanning configuration without rules.

        ## Example Usage
        ### Basic example

        ```python
        import pulumi
        import pulumi_aws as aws

        configuration = aws.ecr.RegistryScanningConfiguration("configuration",
            rules=[aws.ecr.RegistryScanningConfigurationRuleArgs(
                repository_filters=[aws.ecr.RegistryScanningConfigurationRuleRepositoryFilterArgs(
                    filter="example",
                    filter_type="WILDCARD",
                )],
                scan_frequency="CONTINUOUS_SCAN",
            )],
            scan_type="ENHANCED")
        ```
        ### Multiple rules

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.ecr.RegistryScanningConfiguration("test",
            rules=[
                aws.ecr.RegistryScanningConfigurationRuleArgs(
                    repository_filters=[aws.ecr.RegistryScanningConfigurationRuleRepositoryFilterArgs(
                        filter="*",
                        filter_type="WILDCARD",
                    )],
                    scan_frequency="SCAN_ON_PUSH",
                ),
                aws.ecr.RegistryScanningConfigurationRuleArgs(
                    repository_filters=[aws.ecr.RegistryScanningConfigurationRuleRepositoryFilterArgs(
                        filter="example",
                        filter_type="WILDCARD",
                    )],
                    scan_frequency="CONTINUOUS_SCAN",
                ),
            ],
            scan_type="ENHANCED")
        ```

        ## Import

        Using `pulumi import`, import ECR Scanning Configurations using the `registry_id`. For example:

        ```sh
         $ pulumi import aws:ecr/registryScanningConfiguration:RegistryScanningConfiguration example 012345678901
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RegistryScanningConfigurationRuleArgs']]]] rules: One or multiple blocks specifying scanning rules to determine which repository filters are used and at what frequency scanning will occur. See below for schema.
        :param pulumi.Input[str] scan_type: the scanning type to set for the registry. Can be either `ENHANCED` or `BASIC`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RegistryScanningConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Elastic Container Registry Scanning Configuration. Can't be completely deleted, instead reverts to the default `BASIC` scanning configuration without rules.

        ## Example Usage
        ### Basic example

        ```python
        import pulumi
        import pulumi_aws as aws

        configuration = aws.ecr.RegistryScanningConfiguration("configuration",
            rules=[aws.ecr.RegistryScanningConfigurationRuleArgs(
                repository_filters=[aws.ecr.RegistryScanningConfigurationRuleRepositoryFilterArgs(
                    filter="example",
                    filter_type="WILDCARD",
                )],
                scan_frequency="CONTINUOUS_SCAN",
            )],
            scan_type="ENHANCED")
        ```
        ### Multiple rules

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.ecr.RegistryScanningConfiguration("test",
            rules=[
                aws.ecr.RegistryScanningConfigurationRuleArgs(
                    repository_filters=[aws.ecr.RegistryScanningConfigurationRuleRepositoryFilterArgs(
                        filter="*",
                        filter_type="WILDCARD",
                    )],
                    scan_frequency="SCAN_ON_PUSH",
                ),
                aws.ecr.RegistryScanningConfigurationRuleArgs(
                    repository_filters=[aws.ecr.RegistryScanningConfigurationRuleRepositoryFilterArgs(
                        filter="example",
                        filter_type="WILDCARD",
                    )],
                    scan_frequency="CONTINUOUS_SCAN",
                ),
            ],
            scan_type="ENHANCED")
        ```

        ## Import

        Using `pulumi import`, import ECR Scanning Configurations using the `registry_id`. For example:

        ```sh
         $ pulumi import aws:ecr/registryScanningConfiguration:RegistryScanningConfiguration example 012345678901
        ```

        :param str resource_name: The name of the resource.
        :param RegistryScanningConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RegistryScanningConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RegistryScanningConfigurationRuleArgs']]]]] = None,
                 scan_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RegistryScanningConfigurationArgs.__new__(RegistryScanningConfigurationArgs)

            __props__.__dict__["rules"] = rules
            if scan_type is None and not opts.urn:
                raise TypeError("Missing required property 'scan_type'")
            __props__.__dict__["scan_type"] = scan_type
            __props__.__dict__["registry_id"] = None
        super(RegistryScanningConfiguration, __self__).__init__(
            'aws:ecr/registryScanningConfiguration:RegistryScanningConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            registry_id: Optional[pulumi.Input[str]] = None,
            rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RegistryScanningConfigurationRuleArgs']]]]] = None,
            scan_type: Optional[pulumi.Input[str]] = None) -> 'RegistryScanningConfiguration':
        """
        Get an existing RegistryScanningConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] registry_id: The registry ID the scanning configuration applies to.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RegistryScanningConfigurationRuleArgs']]]] rules: One or multiple blocks specifying scanning rules to determine which repository filters are used and at what frequency scanning will occur. See below for schema.
        :param pulumi.Input[str] scan_type: the scanning type to set for the registry. Can be either `ENHANCED` or `BASIC`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RegistryScanningConfigurationState.__new__(_RegistryScanningConfigurationState)

        __props__.__dict__["registry_id"] = registry_id
        __props__.__dict__["rules"] = rules
        __props__.__dict__["scan_type"] = scan_type
        return RegistryScanningConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="registryId")
    def registry_id(self) -> pulumi.Output[str]:
        """
        The registry ID the scanning configuration applies to.
        """
        return pulumi.get(self, "registry_id")

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Output[Optional[Sequence['outputs.RegistryScanningConfigurationRule']]]:
        """
        One or multiple blocks specifying scanning rules to determine which repository filters are used and at what frequency scanning will occur. See below for schema.
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter(name="scanType")
    def scan_type(self) -> pulumi.Output[str]:
        """
        the scanning type to set for the registry. Can be either `ENHANCED` or `BASIC`.
        """
        return pulumi.get(self, "scan_type")

