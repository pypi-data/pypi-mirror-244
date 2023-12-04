'''
# okta-group-groupapplicationassociation

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Okta::Group::GroupApplicationAssociation` v1.4.0.

## Description

Manage Groups assigned to an Application

## References

* [Documentation](https://github.com/aws-ia/cloudformation-okta-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-okta-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Okta::Group::GroupApplicationAssociation \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Okta-Group-GroupApplicationAssociation \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Okta::Group::GroupApplicationAssociation`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fokta-group-groupapplicationassociation+v1.4.0).
* Issues related to `Okta::Group::GroupApplicationAssociation` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-okta-resource-providers).

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


class CfnGroupApplicationAssociation(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/okta-group-groupapplicationassociation.CfnGroupApplicationAssociation",
):
    '''A CloudFormation ``Okta::Group::GroupApplicationAssociation``.

    :cloudformationResource: Okta::Group::GroupApplicationAssociation
    :link: https://github.com/aws-ia/cloudformation-okta-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        group_id: builtins.str,
    ) -> None:
        '''Create a new ``Okta::Group::GroupApplicationAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: id of an app.
        :param group_id: unique key of a valid Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce517d80bcb9c88d4882ae5b500dde554107bdce0069c157f538d1af78daf19c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupApplicationAssociationProps(
            application_id=application_id, group_id=group_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnGroupApplicationAssociationProps":
        '''Resource props.'''
        return typing.cast("CfnGroupApplicationAssociationProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/okta-group-groupapplicationassociation.CfnGroupApplicationAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"application_id": "applicationId", "group_id": "groupId"},
)
class CfnGroupApplicationAssociationProps:
    def __init__(self, *, application_id: builtins.str, group_id: builtins.str) -> None:
        '''Manage Groups assigned to an Application.

        :param application_id: id of an app.
        :param group_id: unique key of a valid Group.

        :schema: CfnGroupApplicationAssociationProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1add5c52b9c97593deb4a8801892ec6e393a4faebd55af0d2eafd540b5e7d5c1)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "group_id": group_id,
        }

    @builtins.property
    def application_id(self) -> builtins.str:
        '''id of an app.

        :schema: CfnGroupApplicationAssociationProps#ApplicationId
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_id(self) -> builtins.str:
        '''unique key of a valid Group.

        :schema: CfnGroupApplicationAssociationProps#GroupId
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupApplicationAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnGroupApplicationAssociation",
    "CfnGroupApplicationAssociationProps",
]

publication.publish()

def _typecheckingstub__ce517d80bcb9c88d4882ae5b500dde554107bdce0069c157f538d1af78daf19c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1add5c52b9c97593deb4a8801892ec6e393a4faebd55af0d2eafd540b5e7d5c1(
    *,
    application_id: builtins.str,
    group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
