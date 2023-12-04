'''
# okta-policy-policy

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Okta::Policy::Policy` v1.4.0.

## Description

Manages an Okta Policy

## References

* [Documentation](https://github.com/aws-ia/cloudformation-okta-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-okta-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Okta::Policy::Policy \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Okta-Policy-Policy \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Okta::Policy::Policy`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fokta-policy-policy+v1.4.0).
* Issues related to `Okta::Policy::Policy` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-okta-resource-providers).

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


class CfnPolicy(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/okta-policy-policy.CfnPolicy",
):
    '''A CloudFormation ``Okta::Policy::Policy``.

    :cloudformationResource: Okta::Policy::Policy
    :link: https://github.com/aws-ia/cloudformation-okta-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: builtins.str,
        name: builtins.str,
        type: "CfnPolicyPropsType",
        conditions: typing.Any = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``Okta::Policy::Policy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: Description of the Policy.
        :param name: Name of the Policy.
        :param type: Specifies the type of Policy.
        :param conditions: 
        :param priority: Priority of the Policy.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b8d0f2fb0fd3f08c2215290a51a5f9e50c5bfc60b9ebbfdfffe76a459e849f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPolicyProps(
            description=description,
            name=name,
            type=type,
            conditions=conditions,
            priority=priority,
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
        '''Attribute ``Okta::Policy::Policy.Id``.

        :link: https://github.com/aws-ia/cloudformation-okta-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnPolicyProps":
        '''Resource props.'''
        return typing.cast("CfnPolicyProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/okta-policy-policy.CfnPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "type": "type",
        "conditions": "conditions",
        "priority": "priority",
    },
)
class CfnPolicyProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        name: builtins.str,
        type: "CfnPolicyPropsType",
        conditions: typing.Any = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Manages an Okta Policy.

        :param description: Description of the Policy.
        :param name: Name of the Policy.
        :param type: Specifies the type of Policy.
        :param conditions: 
        :param priority: Priority of the Policy.

        :schema: CfnPolicyProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b496efc3badbe0f4938b3f5bf4806f95e2b3aa7aafc70f9413ffbcf12e4fda4c)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "name": name,
            "type": type,
        }
        if conditions is not None:
            self._values["conditions"] = conditions
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def description(self) -> builtins.str:
        '''Description of the Policy.

        :schema: CfnPolicyProps#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the Policy.

        :schema: CfnPolicyProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "CfnPolicyPropsType":
        '''Specifies the type of Policy.

        :schema: CfnPolicyProps#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("CfnPolicyPropsType", result)

    @builtins.property
    def conditions(self) -> typing.Any:
        '''
        :schema: CfnPolicyProps#Conditions
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Any, result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Priority of the Policy.

        :schema: CfnPolicyProps#Priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/okta-policy-policy.CfnPolicyPropsType")
class CfnPolicyPropsType(enum.Enum):
    '''Specifies the type of Policy.

    :schema: CfnPolicyPropsType
    '''

    OKTA_SIGN_ON = "OKTA_SIGN_ON"
    '''OKTA_SIGN_ON.'''
    PASSWORD = "PASSWORD"
    '''PASSWORD.'''
    MFA_ENROLL = "MFA_ENROLL"
    '''MFA_ENROLL.'''
    OAUTH_AUTHORIZATION_POLICY = "OAUTH_AUTHORIZATION_POLICY"
    '''OAUTH_AUTHORIZATION_POLICY.'''
    IDP_DISCOVERY = "IDP_DISCOVERY"
    '''IDP_DISCOVERY.'''
    ACCESS_POLICY = "ACCESS_POLICY"
    '''ACCESS_POLICY.'''


__all__ = [
    "CfnPolicy",
    "CfnPolicyProps",
    "CfnPolicyPropsType",
]

publication.publish()

def _typecheckingstub__d1b8d0f2fb0fd3f08c2215290a51a5f9e50c5bfc60b9ebbfdfffe76a459e849f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: builtins.str,
    name: builtins.str,
    type: CfnPolicyPropsType,
    conditions: typing.Any = None,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b496efc3badbe0f4938b3f5bf4806f95e2b3aa7aafc70f9413ffbcf12e4fda4c(
    *,
    description: builtins.str,
    name: builtins.str,
    type: CfnPolicyPropsType,
    conditions: typing.Any = None,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
