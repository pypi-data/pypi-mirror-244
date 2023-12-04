'''
# okta-group-group

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Okta::Group::Group` v1.9.0.

## Description

Manages an Okta Group

## References

* [Documentation](https://github.com/aws-ia/cloudformation-okta-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-okta-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Okta::Group::Group \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Okta-Group-Group \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Okta::Group::Group`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fokta-group-group+v1.9.0).
* Issues related to `Okta::Group::Group` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-okta-resource-providers).

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


class CfnGroup(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/okta-group-group.CfnGroup",
):
    '''A CloudFormation ``Okta::Group::Group``.

    :cloudformationResource: Okta::Group::Group
    :link: https://github.com/aws-ia/cloudformation-okta-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        profile: typing.Union["Profile", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Create a new ``Okta::Group::Group``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param profile: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf250407f4a679abe65b9ed3f1eb4a4fd6ddc302850f14fbea31b3b898809806)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupProps(profile=profile)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``Okta::Group::Group.Id``.

        :link: https://github.com/aws-ia/cloudformation-okta-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnGroupProps":
        '''Resource props.'''
        return typing.cast("CfnGroupProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/okta-group-group.CfnGroupProps",
    jsii_struct_bases=[],
    name_mapping={"profile": "profile"},
)
class CfnGroupProps:
    def __init__(
        self,
        *,
        profile: typing.Union["Profile", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Manages an Okta Group.

        :param profile: 

        :schema: CfnGroupProps
        '''
        if isinstance(profile, dict):
            profile = Profile(**profile)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08bf26ddbde04ec3aecc6e8a09bf92cd44adfed994c8fb8775ee186a748eab8e)
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "profile": profile,
        }

    @builtins.property
    def profile(self) -> "Profile":
        '''
        :schema: CfnGroupProps#Profile
        '''
        result = self._values.get("profile")
        assert result is not None, "Required property 'profile' is missing"
        return typing.cast("Profile", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/okta-group-group.Profile",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description"},
)
class Profile:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the Group.
        :param description: Description of the Group.

        :schema: Profile
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c8f986be1aa11e2d8d430aa4ee177cbc52263d7c5d451b8f3c989268c1b80a7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the Group.

        :schema: Profile#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the Group.

        :schema: Profile#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Profile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnGroup",
    "CfnGroupProps",
    "Profile",
]

publication.publish()

def _typecheckingstub__cf250407f4a679abe65b9ed3f1eb4a4fd6ddc302850f14fbea31b3b898809806(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    profile: typing.Union[Profile, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bf26ddbde04ec3aecc6e8a09bf92cd44adfed994c8fb8775ee186a748eab8e(
    *,
    profile: typing.Union[Profile, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8f986be1aa11e2d8d430aa4ee177cbc52263d7c5d451b8f3c989268c1b80a7(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
