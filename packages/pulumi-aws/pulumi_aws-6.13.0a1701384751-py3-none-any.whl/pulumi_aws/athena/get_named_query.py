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
    'GetNamedQueryResult',
    'AwaitableGetNamedQueryResult',
    'get_named_query',
    'get_named_query_output',
]

@pulumi.output_type
class GetNamedQueryResult:
    """
    A collection of values returned by getNamedQuery.
    """
    def __init__(__self__, database=None, description=None, id=None, name=None, querystring=None, workgroup=None):
        if database and not isinstance(database, str):
            raise TypeError("Expected argument 'database' to be a str")
        pulumi.set(__self__, "database", database)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if querystring and not isinstance(querystring, str):
            raise TypeError("Expected argument 'querystring' to be a str")
        pulumi.set(__self__, "querystring", querystring)
        if workgroup and not isinstance(workgroup, str):
            raise TypeError("Expected argument 'workgroup' to be a str")
        pulumi.set(__self__, "workgroup", workgroup)

    @property
    @pulumi.getter
    def database(self) -> str:
        """
        Database to which the query belongs.
        """
        return pulumi.get(self, "database")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Brief explanation of the query.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def querystring(self) -> str:
        return pulumi.get(self, "querystring")

    @property
    @pulumi.getter
    def workgroup(self) -> Optional[str]:
        return pulumi.get(self, "workgroup")


class AwaitableGetNamedQueryResult(GetNamedQueryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNamedQueryResult(
            database=self.database,
            description=self.description,
            id=self.id,
            name=self.name,
            querystring=self.querystring,
            workgroup=self.workgroup)


def get_named_query(name: Optional[str] = None,
                    workgroup: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNamedQueryResult:
    """
    Provides an Athena Named Query data source.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.athena.get_named_query(name="athenaQueryName")
    ```


    :param str name: The plain language name for the query. Maximum length of 128.
    :param str workgroup: The workgroup to which the query belongs. Defaults to `primary`.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['workgroup'] = workgroup
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:athena/getNamedQuery:getNamedQuery', __args__, opts=opts, typ=GetNamedQueryResult).value

    return AwaitableGetNamedQueryResult(
        database=pulumi.get(__ret__, 'database'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        querystring=pulumi.get(__ret__, 'querystring'),
        workgroup=pulumi.get(__ret__, 'workgroup'))


@_utilities.lift_output_func(get_named_query)
def get_named_query_output(name: Optional[pulumi.Input[str]] = None,
                           workgroup: Optional[pulumi.Input[Optional[str]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNamedQueryResult]:
    """
    Provides an Athena Named Query data source.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.athena.get_named_query(name="athenaQueryName")
    ```


    :param str name: The plain language name for the query. Maximum length of 128.
    :param str workgroup: The workgroup to which the query belongs. Defaults to `primary`.
    """
    ...
