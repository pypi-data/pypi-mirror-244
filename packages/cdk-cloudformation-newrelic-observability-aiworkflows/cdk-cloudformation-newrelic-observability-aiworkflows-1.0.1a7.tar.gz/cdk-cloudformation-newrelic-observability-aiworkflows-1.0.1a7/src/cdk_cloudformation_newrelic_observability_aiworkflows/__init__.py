'''
# newrelic-observability-aiworkflows

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NewRelic::Observability::AIWorkflows` v1.0.1.

## Description

CRUD operations for New Relic Applied Intelligence Workflows via the NerdGraph API

## References

* [Source](https://github.com/newrelic/newrelic-cloudformation-resource-providers-aiworkflows.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NewRelic::Observability::AIWorkflows \
  --publisher-id 759f81f13de188bad7cafc8a2d50910f7d5e2bcc \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/759f81f13de188bad7cafc8a2d50910f7d5e2bcc/NewRelic-Observability-AIWorkflows \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NewRelic::Observability::AIWorkflows`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnewrelic-observability-aiworkflows+v1.0.1).
* Issues related to `NewRelic::Observability::AIWorkflows` should be reported to the [publisher](https://github.com/newrelic/newrelic-cloudformation-resource-providers-aiworkflows.git).

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


class CfnAiWorkflows(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/newrelic-observability-aiworkflows.CfnAiWorkflows",
):
    '''A CloudFormation ``NewRelic::Observability::AIWorkflows``.

    :cloudformationResource: NewRelic::Observability::AIWorkflows
    :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-aiworkflows.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        list_query_filter: typing.Optional[builtins.str] = None,
        variables: typing.Any = None,
        workflow_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``NewRelic::Observability::AIWorkflows``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param list_query_filter: 
        :param variables: 
        :param workflow_data: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79a25654e07d302d46c1f5cf073c157e5f941cc33321b3d473f77b93ac3dde0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAiWorkflowsProps(
            list_query_filter=list_query_filter,
            variables=variables,
            workflow_data=workflow_data,
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
        '''Attribute ``NewRelic::Observability::AIWorkflows.Id``.

        :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-aiworkflows.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnAiWorkflowsProps":
        '''Resource props.'''
        return typing.cast("CfnAiWorkflowsProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-observability-aiworkflows.CfnAiWorkflowsProps",
    jsii_struct_bases=[],
    name_mapping={
        "list_query_filter": "listQueryFilter",
        "variables": "variables",
        "workflow_data": "workflowData",
    },
)
class CfnAiWorkflowsProps:
    def __init__(
        self,
        *,
        list_query_filter: typing.Optional[builtins.str] = None,
        variables: typing.Any = None,
        workflow_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''CRUD operations for New Relic Applied Intelligence Workflows via the NerdGraph API.

        :param list_query_filter: 
        :param variables: 
        :param workflow_data: 

        :schema: CfnAiWorkflowsProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5516ddaf4ae439587b1574222a34f55191e48bc9429ffca400e4b164d7bd7077)
            check_type(argname="argument list_query_filter", value=list_query_filter, expected_type=type_hints["list_query_filter"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            check_type(argname="argument workflow_data", value=workflow_data, expected_type=type_hints["workflow_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if list_query_filter is not None:
            self._values["list_query_filter"] = list_query_filter
        if variables is not None:
            self._values["variables"] = variables
        if workflow_data is not None:
            self._values["workflow_data"] = workflow_data

    @builtins.property
    def list_query_filter(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnAiWorkflowsProps#ListQueryFilter
        '''
        result = self._values.get("list_query_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variables(self) -> typing.Any:
        '''
        :schema: CfnAiWorkflowsProps#Variables
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Any, result)

    @builtins.property
    def workflow_data(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnAiWorkflowsProps#WorkflowData
        '''
        result = self._values.get("workflow_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAiWorkflowsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAiWorkflows",
    "CfnAiWorkflowsProps",
]

publication.publish()

def _typecheckingstub__f79a25654e07d302d46c1f5cf073c157e5f941cc33321b3d473f77b93ac3dde0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    list_query_filter: typing.Optional[builtins.str] = None,
    variables: typing.Any = None,
    workflow_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5516ddaf4ae439587b1574222a34f55191e48bc9429ffca400e4b164d7bd7077(
    *,
    list_query_filter: typing.Optional[builtins.str] = None,
    variables: typing.Any = None,
    workflow_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
