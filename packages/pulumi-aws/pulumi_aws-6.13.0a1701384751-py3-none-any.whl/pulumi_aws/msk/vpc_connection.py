# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['VpcConnectionArgs', 'VpcConnection']

@pulumi.input_type
class VpcConnectionArgs:
    def __init__(__self__, *,
                 authentication: pulumi.Input[str],
                 client_subnets: pulumi.Input[Sequence[pulumi.Input[str]]],
                 security_groups: pulumi.Input[Sequence[pulumi.Input[str]]],
                 target_cluster_arn: pulumi.Input[str],
                 vpc_id: pulumi.Input[str],
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a VpcConnection resource.
        :param pulumi.Input[str] authentication: The authentication type for the client VPC connection. Specify one of these auth type strings: SASL_IAM, SASL_SCRAM, or TLS.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] client_subnets: The list of subnets in the client VPC to connect to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_groups: The security groups to attach to the ENIs for the broker nodes.
        :param pulumi.Input[str] target_cluster_arn: The Amazon Resource Name (ARN) of the cluster.
        :param pulumi.Input[str] vpc_id: The VPC ID of the remote client.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "authentication", authentication)
        pulumi.set(__self__, "client_subnets", client_subnets)
        pulumi.set(__self__, "security_groups", security_groups)
        pulumi.set(__self__, "target_cluster_arn", target_cluster_arn)
        pulumi.set(__self__, "vpc_id", vpc_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def authentication(self) -> pulumi.Input[str]:
        """
        The authentication type for the client VPC connection. Specify one of these auth type strings: SASL_IAM, SASL_SCRAM, or TLS.
        """
        return pulumi.get(self, "authentication")

    @authentication.setter
    def authentication(self, value: pulumi.Input[str]):
        pulumi.set(self, "authentication", value)

    @property
    @pulumi.getter(name="clientSubnets")
    def client_subnets(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The list of subnets in the client VPC to connect to.
        """
        return pulumi.get(self, "client_subnets")

    @client_subnets.setter
    def client_subnets(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "client_subnets", value)

    @property
    @pulumi.getter(name="securityGroups")
    def security_groups(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The security groups to attach to the ENIs for the broker nodes.
        """
        return pulumi.get(self, "security_groups")

    @security_groups.setter
    def security_groups(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "security_groups", value)

    @property
    @pulumi.getter(name="targetClusterArn")
    def target_cluster_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the cluster.
        """
        return pulumi.get(self, "target_cluster_arn")

    @target_cluster_arn.setter
    def target_cluster_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_cluster_arn", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The VPC ID of the remote client.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _VpcConnectionState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 authentication: Optional[pulumi.Input[str]] = None,
                 client_subnets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 security_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_cluster_arn: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering VpcConnection resources.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the VPC connection.
        :param pulumi.Input[str] authentication: The authentication type for the client VPC connection. Specify one of these auth type strings: SASL_IAM, SASL_SCRAM, or TLS.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] client_subnets: The list of subnets in the client VPC to connect to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_groups: The security groups to attach to the ENIs for the broker nodes.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] target_cluster_arn: The Amazon Resource Name (ARN) of the cluster.
        :param pulumi.Input[str] vpc_id: The VPC ID of the remote client.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if authentication is not None:
            pulumi.set(__self__, "authentication", authentication)
        if client_subnets is not None:
            pulumi.set(__self__, "client_subnets", client_subnets)
        if security_groups is not None:
            pulumi.set(__self__, "security_groups", security_groups)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if target_cluster_arn is not None:
            pulumi.set(__self__, "target_cluster_arn", target_cluster_arn)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the VPC connection.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def authentication(self) -> Optional[pulumi.Input[str]]:
        """
        The authentication type for the client VPC connection. Specify one of these auth type strings: SASL_IAM, SASL_SCRAM, or TLS.
        """
        return pulumi.get(self, "authentication")

    @authentication.setter
    def authentication(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authentication", value)

    @property
    @pulumi.getter(name="clientSubnets")
    def client_subnets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of subnets in the client VPC to connect to.
        """
        return pulumi.get(self, "client_subnets")

    @client_subnets.setter
    def client_subnets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "client_subnets", value)

    @property
    @pulumi.getter(name="securityGroups")
    def security_groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The security groups to attach to the ENIs for the broker nodes.
        """
        return pulumi.get(self, "security_groups")

    @security_groups.setter
    def security_groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "security_groups", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter(name="targetClusterArn")
    def target_cluster_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the cluster.
        """
        return pulumi.get(self, "target_cluster_arn")

    @target_cluster_arn.setter
    def target_cluster_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_cluster_arn", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The VPC ID of the remote client.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


class VpcConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication: Optional[pulumi.Input[str]] = None,
                 client_subnets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 security_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_cluster_arn: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS Managed Streaming for Kafka VPC Connection.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.msk.VpcConnection("test",
            authentication="SASL_IAM",
            target_cluster_arn="aws_msk_cluster.arn",
            vpc_id=aws_vpc["test"]["id"],
            client_subnets=[__item["id"] for __item in aws_subnet["test"]],
            security_groups=[aws_security_group["test"]["id"]])
        ```

        ## Import

        Using `pulumi import`, import MSK configurations using the configuration ARN. For example:

        ```sh
         $ pulumi import aws:msk/vpcConnection:VpcConnection example arn:aws:kafka:eu-west-2:123456789012:vpc-connection/123456789012/example/38173259-79cd-4ee8-87f3-682ea6023f48-2
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication: The authentication type for the client VPC connection. Specify one of these auth type strings: SASL_IAM, SASL_SCRAM, or TLS.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] client_subnets: The list of subnets in the client VPC to connect to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_groups: The security groups to attach to the ENIs for the broker nodes.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] target_cluster_arn: The Amazon Resource Name (ARN) of the cluster.
        :param pulumi.Input[str] vpc_id: The VPC ID of the remote client.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VpcConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS Managed Streaming for Kafka VPC Connection.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.msk.VpcConnection("test",
            authentication="SASL_IAM",
            target_cluster_arn="aws_msk_cluster.arn",
            vpc_id=aws_vpc["test"]["id"],
            client_subnets=[__item["id"] for __item in aws_subnet["test"]],
            security_groups=[aws_security_group["test"]["id"]])
        ```

        ## Import

        Using `pulumi import`, import MSK configurations using the configuration ARN. For example:

        ```sh
         $ pulumi import aws:msk/vpcConnection:VpcConnection example arn:aws:kafka:eu-west-2:123456789012:vpc-connection/123456789012/example/38173259-79cd-4ee8-87f3-682ea6023f48-2
        ```

        :param str resource_name: The name of the resource.
        :param VpcConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VpcConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication: Optional[pulumi.Input[str]] = None,
                 client_subnets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 security_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_cluster_arn: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VpcConnectionArgs.__new__(VpcConnectionArgs)

            if authentication is None and not opts.urn:
                raise TypeError("Missing required property 'authentication'")
            __props__.__dict__["authentication"] = authentication
            if client_subnets is None and not opts.urn:
                raise TypeError("Missing required property 'client_subnets'")
            __props__.__dict__["client_subnets"] = client_subnets
            if security_groups is None and not opts.urn:
                raise TypeError("Missing required property 'security_groups'")
            __props__.__dict__["security_groups"] = security_groups
            __props__.__dict__["tags"] = tags
            if target_cluster_arn is None and not opts.urn:
                raise TypeError("Missing required property 'target_cluster_arn'")
            __props__.__dict__["target_cluster_arn"] = target_cluster_arn
            if vpc_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_id'")
            __props__.__dict__["vpc_id"] = vpc_id
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["tagsAll"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(VpcConnection, __self__).__init__(
            'aws:msk/vpcConnection:VpcConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            authentication: Optional[pulumi.Input[str]] = None,
            client_subnets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            security_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            target_cluster_arn: Optional[pulumi.Input[str]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None) -> 'VpcConnection':
        """
        Get an existing VpcConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the VPC connection.
        :param pulumi.Input[str] authentication: The authentication type for the client VPC connection. Specify one of these auth type strings: SASL_IAM, SASL_SCRAM, or TLS.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] client_subnets: The list of subnets in the client VPC to connect to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_groups: The security groups to attach to the ENIs for the broker nodes.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] target_cluster_arn: The Amazon Resource Name (ARN) of the cluster.
        :param pulumi.Input[str] vpc_id: The VPC ID of the remote client.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VpcConnectionState.__new__(_VpcConnectionState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["authentication"] = authentication
        __props__.__dict__["client_subnets"] = client_subnets
        __props__.__dict__["security_groups"] = security_groups
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["target_cluster_arn"] = target_cluster_arn
        __props__.__dict__["vpc_id"] = vpc_id
        return VpcConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the VPC connection.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def authentication(self) -> pulumi.Output[str]:
        """
        The authentication type for the client VPC connection. Specify one of these auth type strings: SASL_IAM, SASL_SCRAM, or TLS.
        """
        return pulumi.get(self, "authentication")

    @property
    @pulumi.getter(name="clientSubnets")
    def client_subnets(self) -> pulumi.Output[Sequence[str]]:
        """
        The list of subnets in the client VPC to connect to.
        """
        return pulumi.get(self, "client_subnets")

    @property
    @pulumi.getter(name="securityGroups")
    def security_groups(self) -> pulumi.Output[Sequence[str]]:
        """
        The security groups to attach to the ENIs for the broker nodes.
        """
        return pulumi.get(self, "security_groups")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter(name="targetClusterArn")
    def target_cluster_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the cluster.
        """
        return pulumi.get(self, "target_cluster_arn")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The VPC ID of the remote client.
        """
        return pulumi.get(self, "vpc_id")

