'''
# newrelic-observability-alertsmutingrule

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NewRelic::Observability::AlertsMutingRule` v1.0.1.

## Description

CRUD operations for New Relic Alerts Muting Rule via the NerdGraph API

## References

* [Source](https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertsmutingrule.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NewRelic::Observability::AlertsMutingRule \
  --publisher-id 759f81f13de188bad7cafc8a2d50910f7d5e2bcc \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/759f81f13de188bad7cafc8a2d50910f7d5e2bcc/NewRelic-Observability-AlertsMutingRule \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NewRelic::Observability::AlertsMutingRule`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnewrelic-observability-alertsmutingrule+v1.0.1).
* Issues related to `NewRelic::Observability::AlertsMutingRule` should be reported to the [publisher](https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertsmutingrule.git).

## License

Distributed under the Apache-2.0 License.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


class CfnAlertsMutingRule(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/newrelic-observability-alertsmutingrule.CfnAlertsMutingRule",
):
    '''A CloudFormation ``NewRelic::Observability::AlertsMutingRule``.

    :cloudformationResource: NewRelic::Observability::AlertsMutingRule
    :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertsmutingrule.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        rule: builtins.str,
        list_query_filter: typing.Optional[builtins.str] = None,
        variables: typing.Any = None,
    ) -> None:
        '''Create a new ``NewRelic::Observability::AlertsMutingRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rule: 
        :param list_query_filter: 
        :param variables: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5987e3d59de0904ba5f0c7fa84610cd416a73c15d5797ba89fb697bee942d83b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAlertsMutingRuleProps(
            rule=rule, list_query_filter=list_query_filter, variables=variables
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``NewRelic::Observability::AlertsMutingRule.Id``.

        :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertsmutingrule.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnAlertsMutingRuleProps":
        '''Resource props.'''
        return typing.cast("CfnAlertsMutingRuleProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-observability-alertsmutingrule.CfnAlertsMutingRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "rule": "rule",
        "list_query_filter": "listQueryFilter",
        "variables": "variables",
    },
)
class CfnAlertsMutingRuleProps:
    def __init__(
        self,
        *,
        rule: builtins.str,
        list_query_filter: typing.Optional[builtins.str] = None,
        variables: typing.Any = None,
    ) -> None:
        '''CRUD operations for New Relic Alerts Muting Rule via the NerdGraph API.

        :param rule: 
        :param list_query_filter: 
        :param variables: 

        :schema: CfnAlertsMutingRuleProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f9ee7c774d5df3cf9c061f47783404a6120768831da99bf4b6b70778d24183)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument list_query_filter", value=list_query_filter, expected_type=type_hints["list_query_filter"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule": rule,
        }
        if list_query_filter is not None:
            self._values["list_query_filter"] = list_query_filter
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def rule(self) -> builtins.str:
        '''
        :schema: CfnAlertsMutingRuleProps#Rule
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def list_query_filter(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnAlertsMutingRuleProps#ListQueryFilter
        '''
        result = self._values.get("list_query_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variables(self) -> typing.Any:
        '''
        :schema: CfnAlertsMutingRuleProps#Variables
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAlertsMutingRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAlertsMutingRule",
    "CfnAlertsMutingRuleProps",
]

publication.publish()

def _typecheckingstub__5987e3d59de0904ba5f0c7fa84610cd416a73c15d5797ba89fb697bee942d83b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    rule: builtins.str,
    list_query_filter: typing.Optional[builtins.str] = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f9ee7c774d5df3cf9c061f47783404a6120768831da99bf4b6b70778d24183(
    *,
    rule: builtins.str,
    list_query_filter: typing.Optional[builtins.str] = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
