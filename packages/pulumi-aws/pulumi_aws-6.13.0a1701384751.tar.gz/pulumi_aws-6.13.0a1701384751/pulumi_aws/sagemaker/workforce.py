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

__all__ = ['WorkforceArgs', 'Workforce']

@pulumi.input_type
class WorkforceArgs:
    def __init__(__self__, *,
                 workforce_name: pulumi.Input[str],
                 cognito_config: Optional[pulumi.Input['WorkforceCognitoConfigArgs']] = None,
                 oidc_config: Optional[pulumi.Input['WorkforceOidcConfigArgs']] = None,
                 source_ip_config: Optional[pulumi.Input['WorkforceSourceIpConfigArgs']] = None,
                 workforce_vpc_config: Optional[pulumi.Input['WorkforceWorkforceVpcConfigArgs']] = None):
        """
        The set of arguments for constructing a Workforce resource.
        :param pulumi.Input[str] workforce_name: The name of the Workforce (must be unique).
        :param pulumi.Input['WorkforceCognitoConfigArgs'] cognito_config: Use this parameter to configure an Amazon Cognito private workforce. A single Cognito workforce is created using and corresponds to a single Amazon Cognito user pool. Conflicts with `oidc_config`. see Cognito Config details below.
        :param pulumi.Input['WorkforceOidcConfigArgs'] oidc_config: Use this parameter to configure a private workforce using your own OIDC Identity Provider. Conflicts with `cognito_config`. see OIDC Config details below.
        :param pulumi.Input['WorkforceSourceIpConfigArgs'] source_ip_config: A list of IP address ranges Used to create an allow list of IP addresses for a private workforce. By default, a workforce isn't restricted to specific IP addresses. see Source Ip Config details below.
        :param pulumi.Input['WorkforceWorkforceVpcConfigArgs'] workforce_vpc_config: configure a workforce using VPC. see Workforce VPC Config details below.
        """
        pulumi.set(__self__, "workforce_name", workforce_name)
        if cognito_config is not None:
            pulumi.set(__self__, "cognito_config", cognito_config)
        if oidc_config is not None:
            pulumi.set(__self__, "oidc_config", oidc_config)
        if source_ip_config is not None:
            pulumi.set(__self__, "source_ip_config", source_ip_config)
        if workforce_vpc_config is not None:
            pulumi.set(__self__, "workforce_vpc_config", workforce_vpc_config)

    @property
    @pulumi.getter(name="workforceName")
    def workforce_name(self) -> pulumi.Input[str]:
        """
        The name of the Workforce (must be unique).
        """
        return pulumi.get(self, "workforce_name")

    @workforce_name.setter
    def workforce_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workforce_name", value)

    @property
    @pulumi.getter(name="cognitoConfig")
    def cognito_config(self) -> Optional[pulumi.Input['WorkforceCognitoConfigArgs']]:
        """
        Use this parameter to configure an Amazon Cognito private workforce. A single Cognito workforce is created using and corresponds to a single Amazon Cognito user pool. Conflicts with `oidc_config`. see Cognito Config details below.
        """
        return pulumi.get(self, "cognito_config")

    @cognito_config.setter
    def cognito_config(self, value: Optional[pulumi.Input['WorkforceCognitoConfigArgs']]):
        pulumi.set(self, "cognito_config", value)

    @property
    @pulumi.getter(name="oidcConfig")
    def oidc_config(self) -> Optional[pulumi.Input['WorkforceOidcConfigArgs']]:
        """
        Use this parameter to configure a private workforce using your own OIDC Identity Provider. Conflicts with `cognito_config`. see OIDC Config details below.
        """
        return pulumi.get(self, "oidc_config")

    @oidc_config.setter
    def oidc_config(self, value: Optional[pulumi.Input['WorkforceOidcConfigArgs']]):
        pulumi.set(self, "oidc_config", value)

    @property
    @pulumi.getter(name="sourceIpConfig")
    def source_ip_config(self) -> Optional[pulumi.Input['WorkforceSourceIpConfigArgs']]:
        """
        A list of IP address ranges Used to create an allow list of IP addresses for a private workforce. By default, a workforce isn't restricted to specific IP addresses. see Source Ip Config details below.
        """
        return pulumi.get(self, "source_ip_config")

    @source_ip_config.setter
    def source_ip_config(self, value: Optional[pulumi.Input['WorkforceSourceIpConfigArgs']]):
        pulumi.set(self, "source_ip_config", value)

    @property
    @pulumi.getter(name="workforceVpcConfig")
    def workforce_vpc_config(self) -> Optional[pulumi.Input['WorkforceWorkforceVpcConfigArgs']]:
        """
        configure a workforce using VPC. see Workforce VPC Config details below.
        """
        return pulumi.get(self, "workforce_vpc_config")

    @workforce_vpc_config.setter
    def workforce_vpc_config(self, value: Optional[pulumi.Input['WorkforceWorkforceVpcConfigArgs']]):
        pulumi.set(self, "workforce_vpc_config", value)


@pulumi.input_type
class _WorkforceState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 cognito_config: Optional[pulumi.Input['WorkforceCognitoConfigArgs']] = None,
                 oidc_config: Optional[pulumi.Input['WorkforceOidcConfigArgs']] = None,
                 source_ip_config: Optional[pulumi.Input['WorkforceSourceIpConfigArgs']] = None,
                 subdomain: Optional[pulumi.Input[str]] = None,
                 workforce_name: Optional[pulumi.Input[str]] = None,
                 workforce_vpc_config: Optional[pulumi.Input['WorkforceWorkforceVpcConfigArgs']] = None):
        """
        Input properties used for looking up and filtering Workforce resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this Workforce.
        :param pulumi.Input['WorkforceCognitoConfigArgs'] cognito_config: Use this parameter to configure an Amazon Cognito private workforce. A single Cognito workforce is created using and corresponds to a single Amazon Cognito user pool. Conflicts with `oidc_config`. see Cognito Config details below.
        :param pulumi.Input['WorkforceOidcConfigArgs'] oidc_config: Use this parameter to configure a private workforce using your own OIDC Identity Provider. Conflicts with `cognito_config`. see OIDC Config details below.
        :param pulumi.Input['WorkforceSourceIpConfigArgs'] source_ip_config: A list of IP address ranges Used to create an allow list of IP addresses for a private workforce. By default, a workforce isn't restricted to specific IP addresses. see Source Ip Config details below.
        :param pulumi.Input[str] subdomain: The subdomain for your OIDC Identity Provider.
               * `workforce_vpc_config.0.vpc_endpoint_id` - The IDs for the VPC service endpoints of your VPC workforce.
        :param pulumi.Input[str] workforce_name: The name of the Workforce (must be unique).
        :param pulumi.Input['WorkforceWorkforceVpcConfigArgs'] workforce_vpc_config: configure a workforce using VPC. see Workforce VPC Config details below.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if cognito_config is not None:
            pulumi.set(__self__, "cognito_config", cognito_config)
        if oidc_config is not None:
            pulumi.set(__self__, "oidc_config", oidc_config)
        if source_ip_config is not None:
            pulumi.set(__self__, "source_ip_config", source_ip_config)
        if subdomain is not None:
            pulumi.set(__self__, "subdomain", subdomain)
        if workforce_name is not None:
            pulumi.set(__self__, "workforce_name", workforce_name)
        if workforce_vpc_config is not None:
            pulumi.set(__self__, "workforce_vpc_config", workforce_vpc_config)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) assigned by AWS to this Workforce.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="cognitoConfig")
    def cognito_config(self) -> Optional[pulumi.Input['WorkforceCognitoConfigArgs']]:
        """
        Use this parameter to configure an Amazon Cognito private workforce. A single Cognito workforce is created using and corresponds to a single Amazon Cognito user pool. Conflicts with `oidc_config`. see Cognito Config details below.
        """
        return pulumi.get(self, "cognito_config")

    @cognito_config.setter
    def cognito_config(self, value: Optional[pulumi.Input['WorkforceCognitoConfigArgs']]):
        pulumi.set(self, "cognito_config", value)

    @property
    @pulumi.getter(name="oidcConfig")
    def oidc_config(self) -> Optional[pulumi.Input['WorkforceOidcConfigArgs']]:
        """
        Use this parameter to configure a private workforce using your own OIDC Identity Provider. Conflicts with `cognito_config`. see OIDC Config details below.
        """
        return pulumi.get(self, "oidc_config")

    @oidc_config.setter
    def oidc_config(self, value: Optional[pulumi.Input['WorkforceOidcConfigArgs']]):
        pulumi.set(self, "oidc_config", value)

    @property
    @pulumi.getter(name="sourceIpConfig")
    def source_ip_config(self) -> Optional[pulumi.Input['WorkforceSourceIpConfigArgs']]:
        """
        A list of IP address ranges Used to create an allow list of IP addresses for a private workforce. By default, a workforce isn't restricted to specific IP addresses. see Source Ip Config details below.
        """
        return pulumi.get(self, "source_ip_config")

    @source_ip_config.setter
    def source_ip_config(self, value: Optional[pulumi.Input['WorkforceSourceIpConfigArgs']]):
        pulumi.set(self, "source_ip_config", value)

    @property
    @pulumi.getter
    def subdomain(self) -> Optional[pulumi.Input[str]]:
        """
        The subdomain for your OIDC Identity Provider.
        * `workforce_vpc_config.0.vpc_endpoint_id` - The IDs for the VPC service endpoints of your VPC workforce.
        """
        return pulumi.get(self, "subdomain")

    @subdomain.setter
    def subdomain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subdomain", value)

    @property
    @pulumi.getter(name="workforceName")
    def workforce_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Workforce (must be unique).
        """
        return pulumi.get(self, "workforce_name")

    @workforce_name.setter
    def workforce_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workforce_name", value)

    @property
    @pulumi.getter(name="workforceVpcConfig")
    def workforce_vpc_config(self) -> Optional[pulumi.Input['WorkforceWorkforceVpcConfigArgs']]:
        """
        configure a workforce using VPC. see Workforce VPC Config details below.
        """
        return pulumi.get(self, "workforce_vpc_config")

    @workforce_vpc_config.setter
    def workforce_vpc_config(self, value: Optional[pulumi.Input['WorkforceWorkforceVpcConfigArgs']]):
        pulumi.set(self, "workforce_vpc_config", value)


class Workforce(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cognito_config: Optional[pulumi.Input[pulumi.InputType['WorkforceCognitoConfigArgs']]] = None,
                 oidc_config: Optional[pulumi.Input[pulumi.InputType['WorkforceOidcConfigArgs']]] = None,
                 source_ip_config: Optional[pulumi.Input[pulumi.InputType['WorkforceSourceIpConfigArgs']]] = None,
                 workforce_name: Optional[pulumi.Input[str]] = None,
                 workforce_vpc_config: Optional[pulumi.Input[pulumi.InputType['WorkforceWorkforceVpcConfigArgs']]] = None,
                 __props__=None):
        """
        Provides a SageMaker Workforce resource.

        ## Example Usage
        ### Cognito Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_user_pool = aws.cognito.UserPool("exampleUserPool")
        example_user_pool_client = aws.cognito.UserPoolClient("exampleUserPoolClient",
            generate_secret=True,
            user_pool_id=example_user_pool.id)
        example_user_pool_domain = aws.cognito.UserPoolDomain("exampleUserPoolDomain",
            domain="example",
            user_pool_id=example_user_pool.id)
        example_workforce = aws.sagemaker.Workforce("exampleWorkforce",
            workforce_name="example",
            cognito_config=aws.sagemaker.WorkforceCognitoConfigArgs(
                client_id=example_user_pool_client.id,
                user_pool=example_user_pool_domain.user_pool_id,
            ))
        ```
        ### Oidc Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sagemaker.Workforce("example",
            oidc_config=aws.sagemaker.WorkforceOidcConfigArgs(
                authorization_endpoint="https://example.com",
                client_id="example",
                client_secret="example",
                issuer="https://example.com",
                jwks_uri="https://example.com",
                logout_endpoint="https://example.com",
                token_endpoint="https://example.com",
                user_info_endpoint="https://example.com",
            ),
            workforce_name="example")
        ```

        ## Import

        Using `pulumi import`, import SageMaker Workforces using the `workforce_name`. For example:

        ```sh
         $ pulumi import aws:sagemaker/workforce:Workforce example example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['WorkforceCognitoConfigArgs']] cognito_config: Use this parameter to configure an Amazon Cognito private workforce. A single Cognito workforce is created using and corresponds to a single Amazon Cognito user pool. Conflicts with `oidc_config`. see Cognito Config details below.
        :param pulumi.Input[pulumi.InputType['WorkforceOidcConfigArgs']] oidc_config: Use this parameter to configure a private workforce using your own OIDC Identity Provider. Conflicts with `cognito_config`. see OIDC Config details below.
        :param pulumi.Input[pulumi.InputType['WorkforceSourceIpConfigArgs']] source_ip_config: A list of IP address ranges Used to create an allow list of IP addresses for a private workforce. By default, a workforce isn't restricted to specific IP addresses. see Source Ip Config details below.
        :param pulumi.Input[str] workforce_name: The name of the Workforce (must be unique).
        :param pulumi.Input[pulumi.InputType['WorkforceWorkforceVpcConfigArgs']] workforce_vpc_config: configure a workforce using VPC. see Workforce VPC Config details below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WorkforceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a SageMaker Workforce resource.

        ## Example Usage
        ### Cognito Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_user_pool = aws.cognito.UserPool("exampleUserPool")
        example_user_pool_client = aws.cognito.UserPoolClient("exampleUserPoolClient",
            generate_secret=True,
            user_pool_id=example_user_pool.id)
        example_user_pool_domain = aws.cognito.UserPoolDomain("exampleUserPoolDomain",
            domain="example",
            user_pool_id=example_user_pool.id)
        example_workforce = aws.sagemaker.Workforce("exampleWorkforce",
            workforce_name="example",
            cognito_config=aws.sagemaker.WorkforceCognitoConfigArgs(
                client_id=example_user_pool_client.id,
                user_pool=example_user_pool_domain.user_pool_id,
            ))
        ```
        ### Oidc Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sagemaker.Workforce("example",
            oidc_config=aws.sagemaker.WorkforceOidcConfigArgs(
                authorization_endpoint="https://example.com",
                client_id="example",
                client_secret="example",
                issuer="https://example.com",
                jwks_uri="https://example.com",
                logout_endpoint="https://example.com",
                token_endpoint="https://example.com",
                user_info_endpoint="https://example.com",
            ),
            workforce_name="example")
        ```

        ## Import

        Using `pulumi import`, import SageMaker Workforces using the `workforce_name`. For example:

        ```sh
         $ pulumi import aws:sagemaker/workforce:Workforce example example
        ```

        :param str resource_name: The name of the resource.
        :param WorkforceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WorkforceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cognito_config: Optional[pulumi.Input[pulumi.InputType['WorkforceCognitoConfigArgs']]] = None,
                 oidc_config: Optional[pulumi.Input[pulumi.InputType['WorkforceOidcConfigArgs']]] = None,
                 source_ip_config: Optional[pulumi.Input[pulumi.InputType['WorkforceSourceIpConfigArgs']]] = None,
                 workforce_name: Optional[pulumi.Input[str]] = None,
                 workforce_vpc_config: Optional[pulumi.Input[pulumi.InputType['WorkforceWorkforceVpcConfigArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WorkforceArgs.__new__(WorkforceArgs)

            __props__.__dict__["cognito_config"] = cognito_config
            __props__.__dict__["oidc_config"] = oidc_config
            __props__.__dict__["source_ip_config"] = source_ip_config
            if workforce_name is None and not opts.urn:
                raise TypeError("Missing required property 'workforce_name'")
            __props__.__dict__["workforce_name"] = workforce_name
            __props__.__dict__["workforce_vpc_config"] = workforce_vpc_config
            __props__.__dict__["arn"] = None
            __props__.__dict__["subdomain"] = None
        super(Workforce, __self__).__init__(
            'aws:sagemaker/workforce:Workforce',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            cognito_config: Optional[pulumi.Input[pulumi.InputType['WorkforceCognitoConfigArgs']]] = None,
            oidc_config: Optional[pulumi.Input[pulumi.InputType['WorkforceOidcConfigArgs']]] = None,
            source_ip_config: Optional[pulumi.Input[pulumi.InputType['WorkforceSourceIpConfigArgs']]] = None,
            subdomain: Optional[pulumi.Input[str]] = None,
            workforce_name: Optional[pulumi.Input[str]] = None,
            workforce_vpc_config: Optional[pulumi.Input[pulumi.InputType['WorkforceWorkforceVpcConfigArgs']]] = None) -> 'Workforce':
        """
        Get an existing Workforce resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this Workforce.
        :param pulumi.Input[pulumi.InputType['WorkforceCognitoConfigArgs']] cognito_config: Use this parameter to configure an Amazon Cognito private workforce. A single Cognito workforce is created using and corresponds to a single Amazon Cognito user pool. Conflicts with `oidc_config`. see Cognito Config details below.
        :param pulumi.Input[pulumi.InputType['WorkforceOidcConfigArgs']] oidc_config: Use this parameter to configure a private workforce using your own OIDC Identity Provider. Conflicts with `cognito_config`. see OIDC Config details below.
        :param pulumi.Input[pulumi.InputType['WorkforceSourceIpConfigArgs']] source_ip_config: A list of IP address ranges Used to create an allow list of IP addresses for a private workforce. By default, a workforce isn't restricted to specific IP addresses. see Source Ip Config details below.
        :param pulumi.Input[str] subdomain: The subdomain for your OIDC Identity Provider.
               * `workforce_vpc_config.0.vpc_endpoint_id` - The IDs for the VPC service endpoints of your VPC workforce.
        :param pulumi.Input[str] workforce_name: The name of the Workforce (must be unique).
        :param pulumi.Input[pulumi.InputType['WorkforceWorkforceVpcConfigArgs']] workforce_vpc_config: configure a workforce using VPC. see Workforce VPC Config details below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _WorkforceState.__new__(_WorkforceState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["cognito_config"] = cognito_config
        __props__.__dict__["oidc_config"] = oidc_config
        __props__.__dict__["source_ip_config"] = source_ip_config
        __props__.__dict__["subdomain"] = subdomain
        __props__.__dict__["workforce_name"] = workforce_name
        __props__.__dict__["workforce_vpc_config"] = workforce_vpc_config
        return Workforce(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) assigned by AWS to this Workforce.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="cognitoConfig")
    def cognito_config(self) -> pulumi.Output[Optional['outputs.WorkforceCognitoConfig']]:
        """
        Use this parameter to configure an Amazon Cognito private workforce. A single Cognito workforce is created using and corresponds to a single Amazon Cognito user pool. Conflicts with `oidc_config`. see Cognito Config details below.
        """
        return pulumi.get(self, "cognito_config")

    @property
    @pulumi.getter(name="oidcConfig")
    def oidc_config(self) -> pulumi.Output[Optional['outputs.WorkforceOidcConfig']]:
        """
        Use this parameter to configure a private workforce using your own OIDC Identity Provider. Conflicts with `cognito_config`. see OIDC Config details below.
        """
        return pulumi.get(self, "oidc_config")

    @property
    @pulumi.getter(name="sourceIpConfig")
    def source_ip_config(self) -> pulumi.Output['outputs.WorkforceSourceIpConfig']:
        """
        A list of IP address ranges Used to create an allow list of IP addresses for a private workforce. By default, a workforce isn't restricted to specific IP addresses. see Source Ip Config details below.
        """
        return pulumi.get(self, "source_ip_config")

    @property
    @pulumi.getter
    def subdomain(self) -> pulumi.Output[str]:
        """
        The subdomain for your OIDC Identity Provider.
        * `workforce_vpc_config.0.vpc_endpoint_id` - The IDs for the VPC service endpoints of your VPC workforce.
        """
        return pulumi.get(self, "subdomain")

    @property
    @pulumi.getter(name="workforceName")
    def workforce_name(self) -> pulumi.Output[str]:
        """
        The name of the Workforce (must be unique).
        """
        return pulumi.get(self, "workforce_name")

    @property
    @pulumi.getter(name="workforceVpcConfig")
    def workforce_vpc_config(self) -> pulumi.Output[Optional['outputs.WorkforceWorkforceVpcConfig']]:
        """
        configure a workforce using VPC. see Workforce VPC Config details below.
        """
        return pulumi.get(self, "workforce_vpc_config")

