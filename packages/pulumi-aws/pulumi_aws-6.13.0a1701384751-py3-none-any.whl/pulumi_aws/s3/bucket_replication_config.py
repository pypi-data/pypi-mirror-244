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

__all__ = ['BucketReplicationConfigArgs', 'BucketReplicationConfig']

@pulumi.input_type
class BucketReplicationConfigArgs:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 role: pulumi.Input[str],
                 rules: pulumi.Input[Sequence[pulumi.Input['BucketReplicationConfigRuleArgs']]],
                 token: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BucketReplicationConfig resource.
        :param pulumi.Input[str] bucket: Name of the source S3 bucket you want Amazon S3 to monitor.
        :param pulumi.Input[str] role: ARN of the IAM role for Amazon S3 to assume when replicating the objects.
        :param pulumi.Input[Sequence[pulumi.Input['BucketReplicationConfigRuleArgs']]] rules: List of configuration blocks describing the rules managing the replication. See below.
        :param pulumi.Input[str] token: Token to allow replication to be enabled on an Object Lock-enabled bucket. You must contact AWS support for the bucket's "Object Lock token".
               For more details, see [Using S3 Object Lock with replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html#object-lock-managing-replication).
        """
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "role", role)
        pulumi.set(__self__, "rules", rules)
        if token is not None:
            pulumi.set(__self__, "token", token)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        """
        Name of the source S3 bucket you want Amazon S3 to monitor.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter
    def role(self) -> pulumi.Input[str]:
        """
        ARN of the IAM role for Amazon S3 to assume when replicating the objects.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Input[Sequence[pulumi.Input['BucketReplicationConfigRuleArgs']]]:
        """
        List of configuration blocks describing the rules managing the replication. See below.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: pulumi.Input[Sequence[pulumi.Input['BucketReplicationConfigRuleArgs']]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter
    def token(self) -> Optional[pulumi.Input[str]]:
        """
        Token to allow replication to be enabled on an Object Lock-enabled bucket. You must contact AWS support for the bucket's "Object Lock token".
        For more details, see [Using S3 Object Lock with replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html#object-lock-managing-replication).
        """
        return pulumi.get(self, "token")

    @token.setter
    def token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token", value)


@pulumi.input_type
class _BucketReplicationConfigState:
    def __init__(__self__, *,
                 bucket: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input['BucketReplicationConfigRuleArgs']]]] = None,
                 token: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BucketReplicationConfig resources.
        :param pulumi.Input[str] bucket: Name of the source S3 bucket you want Amazon S3 to monitor.
        :param pulumi.Input[str] role: ARN of the IAM role for Amazon S3 to assume when replicating the objects.
        :param pulumi.Input[Sequence[pulumi.Input['BucketReplicationConfigRuleArgs']]] rules: List of configuration blocks describing the rules managing the replication. See below.
        :param pulumi.Input[str] token: Token to allow replication to be enabled on an Object Lock-enabled bucket. You must contact AWS support for the bucket's "Object Lock token".
               For more details, see [Using S3 Object Lock with replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html#object-lock-managing-replication).
        """
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if role is not None:
            pulumi.set(__self__, "role", role)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)
        if token is not None:
            pulumi.set(__self__, "token", token)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the source S3 bucket you want Amazon S3 to monitor.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the IAM role for Amazon S3 to assume when replicating the objects.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BucketReplicationConfigRuleArgs']]]]:
        """
        List of configuration blocks describing the rules managing the replication. See below.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BucketReplicationConfigRuleArgs']]]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter
    def token(self) -> Optional[pulumi.Input[str]]:
        """
        Token to allow replication to be enabled on an Object Lock-enabled bucket. You must contact AWS support for the bucket's "Object Lock token".
        For more details, see [Using S3 Object Lock with replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html#object-lock-managing-replication).
        """
        return pulumi.get(self, "token")

    @token.setter
    def token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token", value)


class BucketReplicationConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketReplicationConfigRuleArgs']]]]] = None,
                 token: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an independent configuration resource for S3 bucket [replication configuration](http://docs.aws.amazon.com/AmazonS3/latest/dev/crr.html).

        > **NOTE:** S3 Buckets only support a single replication configuration. Declaring multiple `s3.BucketReplicationConfig` resources to the same S3 Bucket will cause a perpetual difference in configuration.

        > This resource cannot be used with S3 directory buckets.

        ## Example Usage
        ### Using replication configuration

        ```python
        import pulumi
        import pulumi_aws as aws

        central = aws.Provider("central", region="eu-central-1")
        assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["s3.amazonaws.com"],
            )],
            actions=["sts:AssumeRole"],
        )])
        replication_role = aws.iam.Role("replicationRole", assume_role_policy=assume_role.json)
        destination_bucket_v2 = aws.s3.BucketV2("destinationBucketV2")
        source_bucket_v2 = aws.s3.BucketV2("sourceBucketV2", opts=pulumi.ResourceOptions(provider=aws["central"]))
        replication_policy_document = aws.iam.get_policy_document_output(statements=[
            aws.iam.GetPolicyDocumentStatementArgs(
                effect="Allow",
                actions=[
                    "s3:GetReplicationConfiguration",
                    "s3:ListBucket",
                ],
                resources=[source_bucket_v2.arn],
            ),
            aws.iam.GetPolicyDocumentStatementArgs(
                effect="Allow",
                actions=[
                    "s3:GetObjectVersionForReplication",
                    "s3:GetObjectVersionAcl",
                    "s3:GetObjectVersionTagging",
                ],
                resources=[source_bucket_v2.arn.apply(lambda arn: f"{arn}/*")],
            ),
            aws.iam.GetPolicyDocumentStatementArgs(
                effect="Allow",
                actions=[
                    "s3:ReplicateObject",
                    "s3:ReplicateDelete",
                    "s3:ReplicateTags",
                ],
                resources=[destination_bucket_v2.arn.apply(lambda arn: f"{arn}/*")],
            ),
        ])
        replication_policy = aws.iam.Policy("replicationPolicy", policy=replication_policy_document.json)
        replication_role_policy_attachment = aws.iam.RolePolicyAttachment("replicationRolePolicyAttachment",
            role=replication_role.name,
            policy_arn=replication_policy.arn)
        destination_bucket_versioning_v2 = aws.s3.BucketVersioningV2("destinationBucketVersioningV2",
            bucket=destination_bucket_v2.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ))
        source_bucket_acl = aws.s3.BucketAclV2("sourceBucketAcl",
            bucket=source_bucket_v2.id,
            acl="private",
            opts=pulumi.ResourceOptions(provider=aws["central"]))
        source_bucket_versioning_v2 = aws.s3.BucketVersioningV2("sourceBucketVersioningV2",
            bucket=source_bucket_v2.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ),
            opts=pulumi.ResourceOptions(provider=aws["central"]))
        replication_bucket_replication_config = aws.s3.BucketReplicationConfig("replicationBucketReplicationConfig",
            role=replication_role.arn,
            bucket=source_bucket_v2.id,
            rules=[aws.s3.BucketReplicationConfigRuleArgs(
                id="foobar",
                filter=aws.s3.BucketReplicationConfigRuleFilterArgs(
                    prefix="foo",
                ),
                status="Enabled",
                destination=aws.s3.BucketReplicationConfigRuleDestinationArgs(
                    bucket=destination_bucket_v2.arn,
                    storage_class="STANDARD",
                ),
            )],
            opts=pulumi.ResourceOptions(provider=aws["central"],
                depends_on=[source_bucket_versioning_v2]))
        ```
        ### Bi-Directional Replication

        ```python
        import pulumi
        import pulumi_aws as aws

        # ... other configuration ...
        east_bucket_v2 = aws.s3.BucketV2("eastBucketV2")
        east_bucket_versioning_v2 = aws.s3.BucketVersioningV2("eastBucketVersioningV2",
            bucket=east_bucket_v2.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ))
        west_bucket_v2 = aws.s3.BucketV2("westBucketV2", opts=pulumi.ResourceOptions(provider=aws["west"]))
        west_bucket_versioning_v2 = aws.s3.BucketVersioningV2("westBucketVersioningV2",
            bucket=west_bucket_v2.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ),
            opts=pulumi.ResourceOptions(provider=aws["west"]))
        east_to_west = aws.s3.BucketReplicationConfig("eastToWest",
            role=aws_iam_role["east_replication"]["arn"],
            bucket=east_bucket_v2.id,
            rules=[aws.s3.BucketReplicationConfigRuleArgs(
                id="foobar",
                filter=aws.s3.BucketReplicationConfigRuleFilterArgs(
                    prefix="foo",
                ),
                status="Enabled",
                destination=aws.s3.BucketReplicationConfigRuleDestinationArgs(
                    bucket=west_bucket_v2.arn,
                    storage_class="STANDARD",
                ),
            )],
            opts=pulumi.ResourceOptions(depends_on=[east_bucket_versioning_v2]))
        west_to_east = aws.s3.BucketReplicationConfig("westToEast",
            role=aws_iam_role["west_replication"]["arn"],
            bucket=west_bucket_v2.id,
            rules=[aws.s3.BucketReplicationConfigRuleArgs(
                id="foobar",
                filter=aws.s3.BucketReplicationConfigRuleFilterArgs(
                    prefix="foo",
                ),
                status="Enabled",
                destination=aws.s3.BucketReplicationConfigRuleDestinationArgs(
                    bucket=east_bucket_v2.arn,
                    storage_class="STANDARD",
                ),
            )],
            opts=pulumi.ResourceOptions(provider=aws["west"],
                depends_on=[west_bucket_versioning_v2]))
        ```

        ## Import

        Using `pulumi import`, import S3 bucket replication configuration using the `bucket`. For example:

        ```sh
         $ pulumi import aws:s3/bucketReplicationConfig:BucketReplicationConfig replication bucket-name
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Name of the source S3 bucket you want Amazon S3 to monitor.
        :param pulumi.Input[str] role: ARN of the IAM role for Amazon S3 to assume when replicating the objects.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketReplicationConfigRuleArgs']]]] rules: List of configuration blocks describing the rules managing the replication. See below.
        :param pulumi.Input[str] token: Token to allow replication to be enabled on an Object Lock-enabled bucket. You must contact AWS support for the bucket's "Object Lock token".
               For more details, see [Using S3 Object Lock with replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html#object-lock-managing-replication).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BucketReplicationConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an independent configuration resource for S3 bucket [replication configuration](http://docs.aws.amazon.com/AmazonS3/latest/dev/crr.html).

        > **NOTE:** S3 Buckets only support a single replication configuration. Declaring multiple `s3.BucketReplicationConfig` resources to the same S3 Bucket will cause a perpetual difference in configuration.

        > This resource cannot be used with S3 directory buckets.

        ## Example Usage
        ### Using replication configuration

        ```python
        import pulumi
        import pulumi_aws as aws

        central = aws.Provider("central", region="eu-central-1")
        assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["s3.amazonaws.com"],
            )],
            actions=["sts:AssumeRole"],
        )])
        replication_role = aws.iam.Role("replicationRole", assume_role_policy=assume_role.json)
        destination_bucket_v2 = aws.s3.BucketV2("destinationBucketV2")
        source_bucket_v2 = aws.s3.BucketV2("sourceBucketV2", opts=pulumi.ResourceOptions(provider=aws["central"]))
        replication_policy_document = aws.iam.get_policy_document_output(statements=[
            aws.iam.GetPolicyDocumentStatementArgs(
                effect="Allow",
                actions=[
                    "s3:GetReplicationConfiguration",
                    "s3:ListBucket",
                ],
                resources=[source_bucket_v2.arn],
            ),
            aws.iam.GetPolicyDocumentStatementArgs(
                effect="Allow",
                actions=[
                    "s3:GetObjectVersionForReplication",
                    "s3:GetObjectVersionAcl",
                    "s3:GetObjectVersionTagging",
                ],
                resources=[source_bucket_v2.arn.apply(lambda arn: f"{arn}/*")],
            ),
            aws.iam.GetPolicyDocumentStatementArgs(
                effect="Allow",
                actions=[
                    "s3:ReplicateObject",
                    "s3:ReplicateDelete",
                    "s3:ReplicateTags",
                ],
                resources=[destination_bucket_v2.arn.apply(lambda arn: f"{arn}/*")],
            ),
        ])
        replication_policy = aws.iam.Policy("replicationPolicy", policy=replication_policy_document.json)
        replication_role_policy_attachment = aws.iam.RolePolicyAttachment("replicationRolePolicyAttachment",
            role=replication_role.name,
            policy_arn=replication_policy.arn)
        destination_bucket_versioning_v2 = aws.s3.BucketVersioningV2("destinationBucketVersioningV2",
            bucket=destination_bucket_v2.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ))
        source_bucket_acl = aws.s3.BucketAclV2("sourceBucketAcl",
            bucket=source_bucket_v2.id,
            acl="private",
            opts=pulumi.ResourceOptions(provider=aws["central"]))
        source_bucket_versioning_v2 = aws.s3.BucketVersioningV2("sourceBucketVersioningV2",
            bucket=source_bucket_v2.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ),
            opts=pulumi.ResourceOptions(provider=aws["central"]))
        replication_bucket_replication_config = aws.s3.BucketReplicationConfig("replicationBucketReplicationConfig",
            role=replication_role.arn,
            bucket=source_bucket_v2.id,
            rules=[aws.s3.BucketReplicationConfigRuleArgs(
                id="foobar",
                filter=aws.s3.BucketReplicationConfigRuleFilterArgs(
                    prefix="foo",
                ),
                status="Enabled",
                destination=aws.s3.BucketReplicationConfigRuleDestinationArgs(
                    bucket=destination_bucket_v2.arn,
                    storage_class="STANDARD",
                ),
            )],
            opts=pulumi.ResourceOptions(provider=aws["central"],
                depends_on=[source_bucket_versioning_v2]))
        ```
        ### Bi-Directional Replication

        ```python
        import pulumi
        import pulumi_aws as aws

        # ... other configuration ...
        east_bucket_v2 = aws.s3.BucketV2("eastBucketV2")
        east_bucket_versioning_v2 = aws.s3.BucketVersioningV2("eastBucketVersioningV2",
            bucket=east_bucket_v2.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ))
        west_bucket_v2 = aws.s3.BucketV2("westBucketV2", opts=pulumi.ResourceOptions(provider=aws["west"]))
        west_bucket_versioning_v2 = aws.s3.BucketVersioningV2("westBucketVersioningV2",
            bucket=west_bucket_v2.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ),
            opts=pulumi.ResourceOptions(provider=aws["west"]))
        east_to_west = aws.s3.BucketReplicationConfig("eastToWest",
            role=aws_iam_role["east_replication"]["arn"],
            bucket=east_bucket_v2.id,
            rules=[aws.s3.BucketReplicationConfigRuleArgs(
                id="foobar",
                filter=aws.s3.BucketReplicationConfigRuleFilterArgs(
                    prefix="foo",
                ),
                status="Enabled",
                destination=aws.s3.BucketReplicationConfigRuleDestinationArgs(
                    bucket=west_bucket_v2.arn,
                    storage_class="STANDARD",
                ),
            )],
            opts=pulumi.ResourceOptions(depends_on=[east_bucket_versioning_v2]))
        west_to_east = aws.s3.BucketReplicationConfig("westToEast",
            role=aws_iam_role["west_replication"]["arn"],
            bucket=west_bucket_v2.id,
            rules=[aws.s3.BucketReplicationConfigRuleArgs(
                id="foobar",
                filter=aws.s3.BucketReplicationConfigRuleFilterArgs(
                    prefix="foo",
                ),
                status="Enabled",
                destination=aws.s3.BucketReplicationConfigRuleDestinationArgs(
                    bucket=east_bucket_v2.arn,
                    storage_class="STANDARD",
                ),
            )],
            opts=pulumi.ResourceOptions(provider=aws["west"],
                depends_on=[west_bucket_versioning_v2]))
        ```

        ## Import

        Using `pulumi import`, import S3 bucket replication configuration using the `bucket`. For example:

        ```sh
         $ pulumi import aws:s3/bucketReplicationConfig:BucketReplicationConfig replication bucket-name
        ```

        :param str resource_name: The name of the resource.
        :param BucketReplicationConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BucketReplicationConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketReplicationConfigRuleArgs']]]]] = None,
                 token: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BucketReplicationConfigArgs.__new__(BucketReplicationConfigArgs)

            if bucket is None and not opts.urn:
                raise TypeError("Missing required property 'bucket'")
            __props__.__dict__["bucket"] = bucket
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            if rules is None and not opts.urn:
                raise TypeError("Missing required property 'rules'")
            __props__.__dict__["rules"] = rules
            __props__.__dict__["token"] = None if token is None else pulumi.Output.secret(token)
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["token"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(BucketReplicationConfig, __self__).__init__(
            'aws:s3/bucketReplicationConfig:BucketReplicationConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bucket: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None,
            rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketReplicationConfigRuleArgs']]]]] = None,
            token: Optional[pulumi.Input[str]] = None) -> 'BucketReplicationConfig':
        """
        Get an existing BucketReplicationConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Name of the source S3 bucket you want Amazon S3 to monitor.
        :param pulumi.Input[str] role: ARN of the IAM role for Amazon S3 to assume when replicating the objects.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketReplicationConfigRuleArgs']]]] rules: List of configuration blocks describing the rules managing the replication. See below.
        :param pulumi.Input[str] token: Token to allow replication to be enabled on an Object Lock-enabled bucket. You must contact AWS support for the bucket's "Object Lock token".
               For more details, see [Using S3 Object Lock with replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html#object-lock-managing-replication).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BucketReplicationConfigState.__new__(_BucketReplicationConfigState)

        __props__.__dict__["bucket"] = bucket
        __props__.__dict__["role"] = role
        __props__.__dict__["rules"] = rules
        __props__.__dict__["token"] = token
        return BucketReplicationConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        """
        Name of the source S3 bucket you want Amazon S3 to monitor.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        ARN of the IAM role for Amazon S3 to assume when replicating the objects.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Output[Sequence['outputs.BucketReplicationConfigRule']]:
        """
        List of configuration blocks describing the rules managing the replication. See below.
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter
    def token(self) -> pulumi.Output[Optional[str]]:
        """
        Token to allow replication to be enabled on an Object Lock-enabled bucket. You must contact AWS support for the bucket's "Object Lock token".
        For more details, see [Using S3 Object Lock with replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html#object-lock-managing-replication).
        """
        return pulumi.get(self, "token")

