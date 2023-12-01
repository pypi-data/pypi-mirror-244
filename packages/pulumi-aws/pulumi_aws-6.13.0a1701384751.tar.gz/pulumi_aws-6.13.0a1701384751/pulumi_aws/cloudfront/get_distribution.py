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
    'GetDistributionResult',
    'AwaitableGetDistributionResult',
    'get_distribution',
    'get_distribution_output',
]

@pulumi.output_type
class GetDistributionResult:
    """
    A collection of values returned by getDistribution.
    """
    def __init__(__self__, aliases=None, arn=None, domain_name=None, enabled=None, etag=None, hosted_zone_id=None, id=None, in_progress_validation_batches=None, last_modified_time=None, status=None, tags=None, web_acl_id=None):
        if aliases and not isinstance(aliases, list):
            raise TypeError("Expected argument 'aliases' to be a list")
        pulumi.set(__self__, "aliases", aliases)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if domain_name and not isinstance(domain_name, str):
            raise TypeError("Expected argument 'domain_name' to be a str")
        pulumi.set(__self__, "domain_name", domain_name)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if hosted_zone_id and not isinstance(hosted_zone_id, str):
            raise TypeError("Expected argument 'hosted_zone_id' to be a str")
        pulumi.set(__self__, "hosted_zone_id", hosted_zone_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if in_progress_validation_batches and not isinstance(in_progress_validation_batches, int):
            raise TypeError("Expected argument 'in_progress_validation_batches' to be a int")
        pulumi.set(__self__, "in_progress_validation_batches", in_progress_validation_batches)
        if last_modified_time and not isinstance(last_modified_time, str):
            raise TypeError("Expected argument 'last_modified_time' to be a str")
        pulumi.set(__self__, "last_modified_time", last_modified_time)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if web_acl_id and not isinstance(web_acl_id, str):
            raise TypeError("Expected argument 'web_acl_id' to be a str")
        pulumi.set(__self__, "web_acl_id", web_acl_id)

    @property
    @pulumi.getter
    def aliases(self) -> Sequence[str]:
        """
        List that contains information about CNAMEs (alternate domain names), if any, for this distribution.
        """
        return pulumi.get(self, "aliases")

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN (Amazon Resource Name) for the distribution. For example: arn:aws:cloudfront::123456789012:distribution/EDFDVBD632BHDS5, where 123456789012 is your AWS account ID.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> str:
        """
        Domain name corresponding to the distribution. For
        example: `d604721fxaaqy9.cloudfront.net`.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        Current version of the distribution's information. For example:
        `E2QWRUHAPOMQZL`.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        """
        CloudFront Route 53 zone ID that can be used to
        route an [Alias Resource Record Set][7] to. This attribute is simply an
        alias for the zone ID `Z2FDTNDATAQYW2`.
        """
        return pulumi.get(self, "hosted_zone_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Identifier for the distribution. For example: `EDFDVBD632BHDS5`.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="inProgressValidationBatches")
    def in_progress_validation_batches(self) -> int:
        """
        The number of invalidation batches
        currently in progress.
        """
        return pulumi.get(self, "in_progress_validation_batches")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> str:
        """
        Date and time the distribution was last modified.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Current status of the distribution. `Deployed` if the
        distribution's information is fully propagated throughout the Amazon
        CloudFront system.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="webAclId")
    def web_acl_id(self) -> str:
        """
        AWS WAF web ACL associated with this distribution.
        """
        return pulumi.get(self, "web_acl_id")


class AwaitableGetDistributionResult(GetDistributionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDistributionResult(
            aliases=self.aliases,
            arn=self.arn,
            domain_name=self.domain_name,
            enabled=self.enabled,
            etag=self.etag,
            hosted_zone_id=self.hosted_zone_id,
            id=self.id,
            in_progress_validation_batches=self.in_progress_validation_batches,
            last_modified_time=self.last_modified_time,
            status=self.status,
            tags=self.tags,
            web_acl_id=self.web_acl_id)


def get_distribution(id: Optional[str] = None,
                     tags: Optional[Mapping[str, str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDistributionResult:
    """
    Use this data source to retrieve information about a CloudFront distribution.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.cloudfront.get_distribution(id="EDFDVBD632BHDS5")
    ```


    :param str id: Identifier for the distribution. For example: `EDFDVBD632BHDS5`.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:cloudfront/getDistribution:getDistribution', __args__, opts=opts, typ=GetDistributionResult).value

    return AwaitableGetDistributionResult(
        aliases=pulumi.get(__ret__, 'aliases'),
        arn=pulumi.get(__ret__, 'arn'),
        domain_name=pulumi.get(__ret__, 'domain_name'),
        enabled=pulumi.get(__ret__, 'enabled'),
        etag=pulumi.get(__ret__, 'etag'),
        hosted_zone_id=pulumi.get(__ret__, 'hosted_zone_id'),
        id=pulumi.get(__ret__, 'id'),
        in_progress_validation_batches=pulumi.get(__ret__, 'in_progress_validation_batches'),
        last_modified_time=pulumi.get(__ret__, 'last_modified_time'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'),
        web_acl_id=pulumi.get(__ret__, 'web_acl_id'))


@_utilities.lift_output_func(get_distribution)
def get_distribution_output(id: Optional[pulumi.Input[str]] = None,
                            tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDistributionResult]:
    """
    Use this data source to retrieve information about a CloudFront distribution.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.cloudfront.get_distribution(id="EDFDVBD632BHDS5")
    ```


    :param str id: Identifier for the distribution. For example: `EDFDVBD632BHDS5`.
    """
    ...
