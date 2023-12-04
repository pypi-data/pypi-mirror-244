'''
# okta-group-membership

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Okta::Group::Membership` v1.4.0.

## Description

Adds Okta users to groups

## References

* [Documentation](https://github.com/aws-ia/cloudformation-okta-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-okta-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Okta::Group::Membership \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Okta-Group-Membership \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Okta::Group::Membership`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fokta-group-membership+v1.4.0).
* Issues related to `Okta::Group::Membership` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-okta-resource-providers).

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


class CfnMembership(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/okta-group-membership.CfnMembership",
):
    '''A CloudFormation ``Okta::Group::Membership``.

    :cloudformationResource: Okta::Group::Membership
    :link: https://github.com/aws-ia/cloudformation-okta-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        group_id: builtins.str,
        user_id: builtins.str,
    ) -> None:
        '''Create a new ``Okta::Group::Membership``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param group_id: 
        :param user_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e3001e90590e6acef2ea4d2d11bd082fc6b1f14393d8b160d091fea4bf92b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMembershipProps(group_id=group_id, user_id=user_id)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnMembershipProps":
        '''Resource props.'''
        return typing.cast("CfnMembershipProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/okta-group-membership.CfnMembershipProps",
    jsii_struct_bases=[],
    name_mapping={"group_id": "groupId", "user_id": "userId"},
)
class CfnMembershipProps:
    def __init__(self, *, group_id: builtins.str, user_id: builtins.str) -> None:
        '''Adds Okta users to groups.

        :param group_id: 
        :param user_id: 

        :schema: CfnMembershipProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__371d51f4181e64144c489de67df1d66e1d92152976fa6dfdc359f6bc1ea4dde7)
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_id": group_id,
            "user_id": user_id,
        }

    @builtins.property
    def group_id(self) -> builtins.str:
        '''
        :schema: CfnMembershipProps#GroupId
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_id(self) -> builtins.str:
        '''
        :schema: CfnMembershipProps#UserId
        '''
        result = self._values.get("user_id")
        assert result is not None, "Required property 'user_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMembershipProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnMembership",
    "CfnMembershipProps",
]

publication.publish()

def _typecheckingstub__d4e3001e90590e6acef2ea4d2d11bd082fc6b1f14393d8b160d091fea4bf92b5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    group_id: builtins.str,
    user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371d51f4181e64144c489de67df1d66e1d92152976fa6dfdc359f6bc1ea4dde7(
    *,
    group_id: builtins.str,
    user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
