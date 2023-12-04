'''
# newrelic-observability-alertspolicy

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NewRelic::Observability::AlertsPolicy` v1.0.1.

## Description

CRUD operations for New Relic Alerts Policies via the NerdGraph API

## References

* [Source](https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertspolicy.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NewRelic::Observability::AlertsPolicy \
  --publisher-id 759f81f13de188bad7cafc8a2d50910f7d5e2bcc \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/759f81f13de188bad7cafc8a2d50910f7d5e2bcc/NewRelic-Observability-AlertsPolicy \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NewRelic::Observability::AlertsPolicy`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnewrelic-observability-alertspolicy+v1.0.1).
* Issues related to `NewRelic::Observability::AlertsPolicy` should be reported to the [publisher](https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertspolicy.git).

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


class CfnAlertsPolicy(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/newrelic-observability-alertspolicy.CfnAlertsPolicy",
):
    '''A CloudFormation ``NewRelic::Observability::AlertsPolicy``.

    :cloudformationResource: NewRelic::Observability::AlertsPolicy
    :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertspolicy.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        incident_preference: "IncidentPreferenceEnum",
        name: builtins.str,
        list_query_filter: typing.Optional[builtins.str] = None,
        variables: typing.Any = None,
    ) -> None:
        '''Create a new ``NewRelic::Observability::AlertsPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param incident_preference: 
        :param name: 
        :param list_query_filter: 
        :param variables: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6d0f72aea7f4b9d45a028575b7ca44ab7471806391facb42bd8683f1b43a01)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAlertsPolicyProps(
            incident_preference=incident_preference,
            name=name,
            list_query_filter=list_query_filter,
            variables=variables,
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
        '''Attribute ``NewRelic::Observability::AlertsPolicy.Id``.

        :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-alertspolicy.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnAlertsPolicyProps":
        '''Resource props.'''
        return typing.cast("CfnAlertsPolicyProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-observability-alertspolicy.CfnAlertsPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "incident_preference": "incidentPreference",
        "name": "name",
        "list_query_filter": "listQueryFilter",
        "variables": "variables",
    },
)
class CfnAlertsPolicyProps:
    def __init__(
        self,
        *,
        incident_preference: "IncidentPreferenceEnum",
        name: builtins.str,
        list_query_filter: typing.Optional[builtins.str] = None,
        variables: typing.Any = None,
    ) -> None:
        '''CRUD operations for New Relic Alerts Policies via the NerdGraph API.

        :param incident_preference: 
        :param name: 
        :param list_query_filter: 
        :param variables: 

        :schema: CfnAlertsPolicyProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0b159f438661ca3745dc0b2caeed96f4b0aef5e21a7f3c56623857e492499c)
            check_type(argname="argument incident_preference", value=incident_preference, expected_type=type_hints["incident_preference"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument list_query_filter", value=list_query_filter, expected_type=type_hints["list_query_filter"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "incident_preference": incident_preference,
            "name": name,
        }
        if list_query_filter is not None:
            self._values["list_query_filter"] = list_query_filter
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def incident_preference(self) -> "IncidentPreferenceEnum":
        '''
        :schema: CfnAlertsPolicyProps#IncidentPreference
        '''
        result = self._values.get("incident_preference")
        assert result is not None, "Required property 'incident_preference' is missing"
        return typing.cast("IncidentPreferenceEnum", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :schema: CfnAlertsPolicyProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def list_query_filter(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnAlertsPolicyProps#ListQueryFilter
        '''
        result = self._values.get("list_query_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variables(self) -> typing.Any:
        '''
        :schema: CfnAlertsPolicyProps#Variables
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAlertsPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/newrelic-observability-alertspolicy.IncidentPreferenceEnum"
)
class IncidentPreferenceEnum(enum.Enum):
    '''
    :schema: incidentPreferenceEnum
    '''

    PER_CONDITION = "PER_CONDITION"
    '''PER_CONDITION.'''
    PER_CONDITION_AND_TARGET = "PER_CONDITION_AND_TARGET"
    '''PER_CONDITION_AND_TARGET.'''
    PER_POLICY = "PER_POLICY"
    '''PER_POLICY.'''


__all__ = [
    "CfnAlertsPolicy",
    "CfnAlertsPolicyProps",
    "IncidentPreferenceEnum",
]

publication.publish()

def _typecheckingstub__ea6d0f72aea7f4b9d45a028575b7ca44ab7471806391facb42bd8683f1b43a01(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    incident_preference: IncidentPreferenceEnum,
    name: builtins.str,
    list_query_filter: typing.Optional[builtins.str] = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0b159f438661ca3745dc0b2caeed96f4b0aef5e21a7f3c56623857e492499c(
    *,
    incident_preference: IncidentPreferenceEnum,
    name: builtins.str,
    list_query_filter: typing.Optional[builtins.str] = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
