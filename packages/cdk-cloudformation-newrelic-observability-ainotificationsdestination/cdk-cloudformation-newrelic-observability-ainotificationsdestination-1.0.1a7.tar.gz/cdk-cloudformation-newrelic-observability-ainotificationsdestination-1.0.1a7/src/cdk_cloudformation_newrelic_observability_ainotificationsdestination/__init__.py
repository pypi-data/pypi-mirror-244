'''
# newrelic-observability-ainotificationsdestination

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NewRelic::Observability::AINotificationsDestination` v1.0.1.

## Description

CRUD operations for New Relic AI Notifications Destination via the NerdGraph API

## References

* [Source](https://github.com/newrelic/newrelic-cloudformation-resource-providers-ainotificationsdestination.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NewRelic::Observability::AINotificationsDestination \
  --publisher-id 759f81f13de188bad7cafc8a2d50910f7d5e2bcc \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/759f81f13de188bad7cafc8a2d50910f7d5e2bcc/NewRelic-Observability-AINotificationsDestination \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NewRelic::Observability::AINotificationsDestination`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnewrelic-observability-ainotificationsdestination+v1.0.1).
* Issues related to `NewRelic::Observability::AINotificationsDestination` should be reported to the [publisher](https://github.com/newrelic/newrelic-cloudformation-resource-providers-ainotificationsdestination.git).

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


class CfnAiNotificationsDestination(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/newrelic-observability-ainotificationsdestination.CfnAiNotificationsDestination",
):
    '''A CloudFormation ``NewRelic::Observability::AINotificationsDestination``.

    :cloudformationResource: NewRelic::Observability::AINotificationsDestination
    :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-ainotificationsdestination.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        destination: builtins.str,
        list_query_filter: typing.Optional[builtins.str] = None,
        variables: typing.Any = None,
    ) -> None:
        '''Create a new ``NewRelic::Observability::AINotificationsDestination``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination: 
        :param list_query_filter: 
        :param variables: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42cc871467f5dbbb7a8ddea74df764c3a6fe9e918ee94aa51836d8d5369cd0e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAiNotificationsDestinationProps(
            destination=destination,
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
        '''Attribute ``NewRelic::Observability::AINotificationsDestination.Id``.

        :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-ainotificationsdestination.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnAiNotificationsDestinationProps":
        '''Resource props.'''
        return typing.cast("CfnAiNotificationsDestinationProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-observability-ainotificationsdestination.CfnAiNotificationsDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "list_query_filter": "listQueryFilter",
        "variables": "variables",
    },
)
class CfnAiNotificationsDestinationProps:
    def __init__(
        self,
        *,
        destination: builtins.str,
        list_query_filter: typing.Optional[builtins.str] = None,
        variables: typing.Any = None,
    ) -> None:
        '''CRUD operations for New Relic AI Notifications Destination via the NerdGraph API.

        :param destination: 
        :param list_query_filter: 
        :param variables: 

        :schema: CfnAiNotificationsDestinationProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2552e73071ad3c09e73c168bfb6f7e7531ae75685c01de33cc4973cf557769e1)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument list_query_filter", value=list_query_filter, expected_type=type_hints["list_query_filter"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }
        if list_query_filter is not None:
            self._values["list_query_filter"] = list_query_filter
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def destination(self) -> builtins.str:
        '''
        :schema: CfnAiNotificationsDestinationProps#Destination
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def list_query_filter(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnAiNotificationsDestinationProps#ListQueryFilter
        '''
        result = self._values.get("list_query_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variables(self) -> typing.Any:
        '''
        :schema: CfnAiNotificationsDestinationProps#Variables
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAiNotificationsDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAiNotificationsDestination",
    "CfnAiNotificationsDestinationProps",
]

publication.publish()

def _typecheckingstub__42cc871467f5dbbb7a8ddea74df764c3a6fe9e918ee94aa51836d8d5369cd0e7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    destination: builtins.str,
    list_query_filter: typing.Optional[builtins.str] = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2552e73071ad3c09e73c168bfb6f7e7531ae75685c01de33cc4973cf557769e1(
    *,
    destination: builtins.str,
    list_query_filter: typing.Optional[builtins.str] = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
