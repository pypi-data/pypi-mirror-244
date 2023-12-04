'''
# newrelic-observability-alertsnrqlcondition

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NewRelic::Observability::AlertsNrqlCondition` v1.0.1.

## Description

CRUD operations for New Relic Alerts Nrql Condition via the NerdGraph API

## References

* [Source](https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertsnrqlcondition.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NewRelic::Observability::AlertsNrqlCondition \
  --publisher-id 759f81f13de188bad7cafc8a2d50910f7d5e2bcc \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/759f81f13de188bad7cafc8a2d50910f7d5e2bcc/NewRelic-Observability-AlertsNrqlCondition \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NewRelic::Observability::AlertsNrqlCondition`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnewrelic-observability-alertsnrqlcondition+v1.0.1).
* Issues related to `NewRelic::Observability::AlertsNrqlCondition` should be reported to the [publisher](https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertsnrqlcondition.git).

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


class CfnAlertsNrqlCondition(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/newrelic-observability-alertsnrqlcondition.CfnAlertsNrqlCondition",
):
    '''A CloudFormation ``NewRelic::Observability::AlertsNrqlCondition``.

    :cloudformationResource: NewRelic::Observability::AlertsNrqlCondition
    :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertsnrqlcondition.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        condition: builtins.str,
        condition_type: "ConditionType",
        policy_id: builtins.str,
        list_query_filter: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        variables: typing.Any = None,
    ) -> None:
        '''Create a new ``NewRelic::Observability::AlertsNrqlCondition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param condition: 
        :param condition_type: 
        :param policy_id: 
        :param list_query_filter: 
        :param tags: 
        :param variables: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc3dfcb6f46b4dcf63d6996378afc2da93eb05f21e183d6bef653ded8933b41)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAlertsNrqlConditionProps(
            condition=condition,
            condition_type=condition_type,
            policy_id=policy_id,
            list_query_filter=list_query_filter,
            tags=tags,
            variables=variables,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrEntityGuid")
    def attr_entity_guid(self) -> builtins.str:
        '''Attribute ``NewRelic::Observability::AlertsNrqlCondition.EntityGuid``.

        :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertsnrqlcondition.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEntityGuid"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``NewRelic::Observability::AlertsNrqlCondition.Id``.

        :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertsnrqlcondition.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnAlertsNrqlConditionProps":
        '''Resource props.'''
        return typing.cast("CfnAlertsNrqlConditionProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-observability-alertsnrqlcondition.CfnAlertsNrqlConditionProps",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "condition_type": "conditionType",
        "policy_id": "policyId",
        "list_query_filter": "listQueryFilter",
        "tags": "tags",
        "variables": "variables",
    },
)
class CfnAlertsNrqlConditionProps:
    def __init__(
        self,
        *,
        condition: builtins.str,
        condition_type: "ConditionType",
        policy_id: builtins.str,
        list_query_filter: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        variables: typing.Any = None,
    ) -> None:
        '''CRUD operations for New Relic Alerts Nrql Condition via the NerdGraph API.

        :param condition: 
        :param condition_type: 
        :param policy_id: 
        :param list_query_filter: 
        :param tags: 
        :param variables: 

        :schema: CfnAlertsNrqlConditionProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900e3f3b72a9db43c52e49253ed814154abc8ce4287e87546aa9d8ea60069c4d)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument condition_type", value=condition_type, expected_type=type_hints["condition_type"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument list_query_filter", value=list_query_filter, expected_type=type_hints["list_query_filter"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition": condition,
            "condition_type": condition_type,
            "policy_id": policy_id,
        }
        if list_query_filter is not None:
            self._values["list_query_filter"] = list_query_filter
        if tags is not None:
            self._values["tags"] = tags
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def condition(self) -> builtins.str:
        '''
        :schema: CfnAlertsNrqlConditionProps#Condition
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition_type(self) -> "ConditionType":
        '''
        :schema: CfnAlertsNrqlConditionProps#ConditionType
        '''
        result = self._values.get("condition_type")
        assert result is not None, "Required property 'condition_type' is missing"
        return typing.cast("ConditionType", result)

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''
        :schema: CfnAlertsNrqlConditionProps#PolicyId
        '''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def list_query_filter(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnAlertsNrqlConditionProps#ListQueryFilter
        '''
        result = self._values.get("list_query_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''
        :schema: CfnAlertsNrqlConditionProps#Tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def variables(self) -> typing.Any:
        '''
        :schema: CfnAlertsNrqlConditionProps#Variables
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAlertsNrqlConditionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/newrelic-observability-alertsnrqlcondition.ConditionType"
)
class ConditionType(enum.Enum):
    '''
    :schema: ConditionType
    '''

    BASELINE = "BASELINE"
    '''Baseline.'''
    STATIC = "STATIC"
    '''Static.'''


__all__ = [
    "CfnAlertsNrqlCondition",
    "CfnAlertsNrqlConditionProps",
    "ConditionType",
]

publication.publish()

def _typecheckingstub__abc3dfcb6f46b4dcf63d6996378afc2da93eb05f21e183d6bef653ded8933b41(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    condition: builtins.str,
    condition_type: ConditionType,
    policy_id: builtins.str,
    list_query_filter: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900e3f3b72a9db43c52e49253ed814154abc8ce4287e87546aa9d8ea60069c4d(
    *,
    condition: builtins.str,
    condition_type: ConditionType,
    policy_id: builtins.str,
    list_query_filter: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
