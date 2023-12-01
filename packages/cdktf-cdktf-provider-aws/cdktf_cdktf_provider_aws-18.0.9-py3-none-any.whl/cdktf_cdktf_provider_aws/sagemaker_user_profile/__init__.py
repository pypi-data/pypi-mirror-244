'''
# `aws_sagemaker_user_profile`

Refer to the Terraform Registory for docs: [`aws_sagemaker_user_profile`](https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class SagemakerUserProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile aws_sagemaker_user_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        domain_id: builtins.str,
        user_profile_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        single_sign_on_user_identifier: typing.Optional[builtins.str] = None,
        single_sign_on_user_value: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile aws_sagemaker_user_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param domain_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#domain_id SagemakerUserProfile#domain_id}.
        :param user_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#user_profile_name SagemakerUserProfile#user_profile_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#id SagemakerUserProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param single_sign_on_user_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#single_sign_on_user_identifier SagemakerUserProfile#single_sign_on_user_identifier}.
        :param single_sign_on_user_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#single_sign_on_user_value SagemakerUserProfile#single_sign_on_user_value}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#tags SagemakerUserProfile#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#tags_all SagemakerUserProfile#tags_all}.
        :param user_settings: user_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#user_settings SagemakerUserProfile#user_settings}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94364b035a7681e7ff1e1e978f4c54626eea050d5ed2a082854aae0f430168b3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerUserProfileConfig(
            domain_id=domain_id,
            user_profile_name=user_profile_name,
            id=id,
            single_sign_on_user_identifier=single_sign_on_user_identifier,
            single_sign_on_user_value=single_sign_on_user_value,
            tags=tags,
            tags_all=tags_all,
            user_settings=user_settings,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a SagemakerUserProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SagemakerUserProfile to import.
        :param import_from_id: The id of the existing SagemakerUserProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SagemakerUserProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c59c1e36fa8f0580dd0c35e797ceb8b2783e0d49366f3afaa62808fcff37e6d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putUserSettings")
    def put_user_settings(
        self,
        *,
        execution_role: builtins.str,
        canvas_app_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsCanvasAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        jupyter_server_app_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsJupyterServerAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kernel_gateway_app_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsKernelGatewayAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        r_session_app_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsRSessionAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        r_studio_server_pro_app_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsRStudioServerProAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        sharing_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsSharingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        tensor_board_app_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsTensorBoardAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execution_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#execution_role SagemakerUserProfile#execution_role}.
        :param canvas_app_settings: canvas_app_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#canvas_app_settings SagemakerUserProfile#canvas_app_settings}
        :param jupyter_server_app_settings: jupyter_server_app_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#jupyter_server_app_settings SagemakerUserProfile#jupyter_server_app_settings}
        :param kernel_gateway_app_settings: kernel_gateway_app_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#kernel_gateway_app_settings SagemakerUserProfile#kernel_gateway_app_settings}
        :param r_session_app_settings: r_session_app_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#r_session_app_settings SagemakerUserProfile#r_session_app_settings}
        :param r_studio_server_pro_app_settings: r_studio_server_pro_app_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#r_studio_server_pro_app_settings SagemakerUserProfile#r_studio_server_pro_app_settings}
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#security_groups SagemakerUserProfile#security_groups}.
        :param sharing_settings: sharing_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sharing_settings SagemakerUserProfile#sharing_settings}
        :param tensor_board_app_settings: tensor_board_app_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#tensor_board_app_settings SagemakerUserProfile#tensor_board_app_settings}
        '''
        value = SagemakerUserProfileUserSettings(
            execution_role=execution_role,
            canvas_app_settings=canvas_app_settings,
            jupyter_server_app_settings=jupyter_server_app_settings,
            kernel_gateway_app_settings=kernel_gateway_app_settings,
            r_session_app_settings=r_session_app_settings,
            r_studio_server_pro_app_settings=r_studio_server_pro_app_settings,
            security_groups=security_groups,
            sharing_settings=sharing_settings,
            tensor_board_app_settings=tensor_board_app_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putUserSettings", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSingleSignOnUserIdentifier")
    def reset_single_sign_on_user_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleSignOnUserIdentifier", []))

    @jsii.member(jsii_name="resetSingleSignOnUserValue")
    def reset_single_sign_on_user_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleSignOnUserValue", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetUserSettings")
    def reset_user_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserSettings", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="homeEfsFileSystemUid")
    def home_efs_file_system_uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "homeEfsFileSystemUid"))

    @builtins.property
    @jsii.member(jsii_name="userSettings")
    def user_settings(self) -> "SagemakerUserProfileUserSettingsOutputReference":
        return typing.cast("SagemakerUserProfileUserSettingsOutputReference", jsii.get(self, "userSettings"))

    @builtins.property
    @jsii.member(jsii_name="domainIdInput")
    def domain_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="singleSignOnUserIdentifierInput")
    def single_sign_on_user_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "singleSignOnUserIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="singleSignOnUserValueInput")
    def single_sign_on_user_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "singleSignOnUserValueInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="userProfileNameInput")
    def user_profile_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userProfileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="userSettingsInput")
    def user_settings_input(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettings"]:
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettings"], jsii.get(self, "userSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @domain_id.setter
    def domain_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56faad451bf707c890b7ea60d99a0256d2c7c1994e664b67ff186544449ec4ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2258f1842205c3327e3e0519e820048176de11f935c701b620e5df3796c7146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="singleSignOnUserIdentifier")
    def single_sign_on_user_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "singleSignOnUserIdentifier"))

    @single_sign_on_user_identifier.setter
    def single_sign_on_user_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1cd32e5df9deb98b78b97c000d3b9ecfcd0cd53a8cdeeecdd69c31ddfbdbca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleSignOnUserIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="singleSignOnUserValue")
    def single_sign_on_user_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "singleSignOnUserValue"))

    @single_sign_on_user_value.setter
    def single_sign_on_user_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c5c8b544d8bd22c81eed872047804b11b2c00b978e66086e333643149079a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleSignOnUserValue", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d064da11325e97f3a64a9e15c89dbb22d24e7a498007bb940a94bdf13ea5d788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fafebc2a6c90906f0e60c4cee21a6c0fb4e40f9690449112d7d1d2aa09cf17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="userProfileName")
    def user_profile_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userProfileName"))

    @user_profile_name.setter
    def user_profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073696c04c11f488a4acc9662e6caaa2e5e0c7dfb40c08aabd96033ada4152a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userProfileName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "domain_id": "domainId",
        "user_profile_name": "userProfileName",
        "id": "id",
        "single_sign_on_user_identifier": "singleSignOnUserIdentifier",
        "single_sign_on_user_value": "singleSignOnUserValue",
        "tags": "tags",
        "tags_all": "tagsAll",
        "user_settings": "userSettings",
    },
)
class SagemakerUserProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        domain_id: builtins.str,
        user_profile_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        single_sign_on_user_identifier: typing.Optional[builtins.str] = None,
        single_sign_on_user_value: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param domain_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#domain_id SagemakerUserProfile#domain_id}.
        :param user_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#user_profile_name SagemakerUserProfile#user_profile_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#id SagemakerUserProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param single_sign_on_user_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#single_sign_on_user_identifier SagemakerUserProfile#single_sign_on_user_identifier}.
        :param single_sign_on_user_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#single_sign_on_user_value SagemakerUserProfile#single_sign_on_user_value}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#tags SagemakerUserProfile#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#tags_all SagemakerUserProfile#tags_all}.
        :param user_settings: user_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#user_settings SagemakerUserProfile#user_settings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(user_settings, dict):
            user_settings = SagemakerUserProfileUserSettings(**user_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c83051f8a67245071364ce9e0a39bf8664578a6178a27d3c94df4f7b8d626f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
            check_type(argname="argument user_profile_name", value=user_profile_name, expected_type=type_hints["user_profile_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument single_sign_on_user_identifier", value=single_sign_on_user_identifier, expected_type=type_hints["single_sign_on_user_identifier"])
            check_type(argname="argument single_sign_on_user_value", value=single_sign_on_user_value, expected_type=type_hints["single_sign_on_user_value"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument user_settings", value=user_settings, expected_type=type_hints["user_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_id": domain_id,
            "user_profile_name": user_profile_name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if id is not None:
            self._values["id"] = id
        if single_sign_on_user_identifier is not None:
            self._values["single_sign_on_user_identifier"] = single_sign_on_user_identifier
        if single_sign_on_user_value is not None:
            self._values["single_sign_on_user_value"] = single_sign_on_user_value
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if user_settings is not None:
            self._values["user_settings"] = user_settings

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def domain_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#domain_id SagemakerUserProfile#domain_id}.'''
        result = self._values.get("domain_id")
        assert result is not None, "Required property 'domain_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_profile_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#user_profile_name SagemakerUserProfile#user_profile_name}.'''
        result = self._values.get("user_profile_name")
        assert result is not None, "Required property 'user_profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#id SagemakerUserProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_sign_on_user_identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#single_sign_on_user_identifier SagemakerUserProfile#single_sign_on_user_identifier}.'''
        result = self._values.get("single_sign_on_user_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_sign_on_user_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#single_sign_on_user_value SagemakerUserProfile#single_sign_on_user_value}.'''
        result = self._values.get("single_sign_on_user_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#tags SagemakerUserProfile#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#tags_all SagemakerUserProfile#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def user_settings(self) -> typing.Optional["SagemakerUserProfileUserSettings"]:
        '''user_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#user_settings SagemakerUserProfile#user_settings}
        '''
        result = self._values.get("user_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettings",
    jsii_struct_bases=[],
    name_mapping={
        "execution_role": "executionRole",
        "canvas_app_settings": "canvasAppSettings",
        "jupyter_server_app_settings": "jupyterServerAppSettings",
        "kernel_gateway_app_settings": "kernelGatewayAppSettings",
        "r_session_app_settings": "rSessionAppSettings",
        "r_studio_server_pro_app_settings": "rStudioServerProAppSettings",
        "security_groups": "securityGroups",
        "sharing_settings": "sharingSettings",
        "tensor_board_app_settings": "tensorBoardAppSettings",
    },
)
class SagemakerUserProfileUserSettings:
    def __init__(
        self,
        *,
        execution_role: builtins.str,
        canvas_app_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsCanvasAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        jupyter_server_app_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsJupyterServerAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kernel_gateway_app_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsKernelGatewayAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        r_session_app_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsRSessionAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        r_studio_server_pro_app_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsRStudioServerProAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        sharing_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsSharingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        tensor_board_app_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsTensorBoardAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execution_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#execution_role SagemakerUserProfile#execution_role}.
        :param canvas_app_settings: canvas_app_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#canvas_app_settings SagemakerUserProfile#canvas_app_settings}
        :param jupyter_server_app_settings: jupyter_server_app_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#jupyter_server_app_settings SagemakerUserProfile#jupyter_server_app_settings}
        :param kernel_gateway_app_settings: kernel_gateway_app_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#kernel_gateway_app_settings SagemakerUserProfile#kernel_gateway_app_settings}
        :param r_session_app_settings: r_session_app_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#r_session_app_settings SagemakerUserProfile#r_session_app_settings}
        :param r_studio_server_pro_app_settings: r_studio_server_pro_app_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#r_studio_server_pro_app_settings SagemakerUserProfile#r_studio_server_pro_app_settings}
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#security_groups SagemakerUserProfile#security_groups}.
        :param sharing_settings: sharing_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sharing_settings SagemakerUserProfile#sharing_settings}
        :param tensor_board_app_settings: tensor_board_app_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#tensor_board_app_settings SagemakerUserProfile#tensor_board_app_settings}
        '''
        if isinstance(canvas_app_settings, dict):
            canvas_app_settings = SagemakerUserProfileUserSettingsCanvasAppSettings(**canvas_app_settings)
        if isinstance(jupyter_server_app_settings, dict):
            jupyter_server_app_settings = SagemakerUserProfileUserSettingsJupyterServerAppSettings(**jupyter_server_app_settings)
        if isinstance(kernel_gateway_app_settings, dict):
            kernel_gateway_app_settings = SagemakerUserProfileUserSettingsKernelGatewayAppSettings(**kernel_gateway_app_settings)
        if isinstance(r_session_app_settings, dict):
            r_session_app_settings = SagemakerUserProfileUserSettingsRSessionAppSettings(**r_session_app_settings)
        if isinstance(r_studio_server_pro_app_settings, dict):
            r_studio_server_pro_app_settings = SagemakerUserProfileUserSettingsRStudioServerProAppSettings(**r_studio_server_pro_app_settings)
        if isinstance(sharing_settings, dict):
            sharing_settings = SagemakerUserProfileUserSettingsSharingSettings(**sharing_settings)
        if isinstance(tensor_board_app_settings, dict):
            tensor_board_app_settings = SagemakerUserProfileUserSettingsTensorBoardAppSettings(**tensor_board_app_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d876be7b60ae620343f56346c172342ec3c15cd2e2779d7a87f74de85fb319f)
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument canvas_app_settings", value=canvas_app_settings, expected_type=type_hints["canvas_app_settings"])
            check_type(argname="argument jupyter_server_app_settings", value=jupyter_server_app_settings, expected_type=type_hints["jupyter_server_app_settings"])
            check_type(argname="argument kernel_gateway_app_settings", value=kernel_gateway_app_settings, expected_type=type_hints["kernel_gateway_app_settings"])
            check_type(argname="argument r_session_app_settings", value=r_session_app_settings, expected_type=type_hints["r_session_app_settings"])
            check_type(argname="argument r_studio_server_pro_app_settings", value=r_studio_server_pro_app_settings, expected_type=type_hints["r_studio_server_pro_app_settings"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument sharing_settings", value=sharing_settings, expected_type=type_hints["sharing_settings"])
            check_type(argname="argument tensor_board_app_settings", value=tensor_board_app_settings, expected_type=type_hints["tensor_board_app_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role": execution_role,
        }
        if canvas_app_settings is not None:
            self._values["canvas_app_settings"] = canvas_app_settings
        if jupyter_server_app_settings is not None:
            self._values["jupyter_server_app_settings"] = jupyter_server_app_settings
        if kernel_gateway_app_settings is not None:
            self._values["kernel_gateway_app_settings"] = kernel_gateway_app_settings
        if r_session_app_settings is not None:
            self._values["r_session_app_settings"] = r_session_app_settings
        if r_studio_server_pro_app_settings is not None:
            self._values["r_studio_server_pro_app_settings"] = r_studio_server_pro_app_settings
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if sharing_settings is not None:
            self._values["sharing_settings"] = sharing_settings
        if tensor_board_app_settings is not None:
            self._values["tensor_board_app_settings"] = tensor_board_app_settings

    @builtins.property
    def execution_role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#execution_role SagemakerUserProfile#execution_role}.'''
        result = self._values.get("execution_role")
        assert result is not None, "Required property 'execution_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def canvas_app_settings(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettings"]:
        '''canvas_app_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#canvas_app_settings SagemakerUserProfile#canvas_app_settings}
        '''
        result = self._values.get("canvas_app_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettings"], result)

    @builtins.property
    def jupyter_server_app_settings(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsJupyterServerAppSettings"]:
        '''jupyter_server_app_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#jupyter_server_app_settings SagemakerUserProfile#jupyter_server_app_settings}
        '''
        result = self._values.get("jupyter_server_app_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsJupyterServerAppSettings"], result)

    @builtins.property
    def kernel_gateway_app_settings(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsKernelGatewayAppSettings"]:
        '''kernel_gateway_app_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#kernel_gateway_app_settings SagemakerUserProfile#kernel_gateway_app_settings}
        '''
        result = self._values.get("kernel_gateway_app_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsKernelGatewayAppSettings"], result)

    @builtins.property
    def r_session_app_settings(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsRSessionAppSettings"]:
        '''r_session_app_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#r_session_app_settings SagemakerUserProfile#r_session_app_settings}
        '''
        result = self._values.get("r_session_app_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsRSessionAppSettings"], result)

    @builtins.property
    def r_studio_server_pro_app_settings(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsRStudioServerProAppSettings"]:
        '''r_studio_server_pro_app_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#r_studio_server_pro_app_settings SagemakerUserProfile#r_studio_server_pro_app_settings}
        '''
        result = self._values.get("r_studio_server_pro_app_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsRStudioServerProAppSettings"], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#security_groups SagemakerUserProfile#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sharing_settings(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsSharingSettings"]:
        '''sharing_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sharing_settings SagemakerUserProfile#sharing_settings}
        '''
        result = self._values.get("sharing_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsSharingSettings"], result)

    @builtins.property
    def tensor_board_app_settings(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsTensorBoardAppSettings"]:
        '''tensor_board_app_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#tensor_board_app_settings SagemakerUserProfile#tensor_board_app_settings}
        '''
        result = self._values.get("tensor_board_app_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsTensorBoardAppSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettings",
    jsii_struct_bases=[],
    name_mapping={
        "direct_deploy_settings": "directDeploySettings",
        "identity_provider_oauth_settings": "identityProviderOauthSettings",
        "kendra_settings": "kendraSettings",
        "model_register_settings": "modelRegisterSettings",
        "time_series_forecasting_settings": "timeSeriesForecastingSettings",
        "workspace_settings": "workspaceSettings",
    },
)
class SagemakerUserProfileUserSettingsCanvasAppSettings:
    def __init__(
        self,
        *,
        direct_deploy_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        identity_provider_oauth_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kendra_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        model_register_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        time_series_forecasting_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        workspace_settings: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param direct_deploy_settings: direct_deploy_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#direct_deploy_settings SagemakerUserProfile#direct_deploy_settings}
        :param identity_provider_oauth_settings: identity_provider_oauth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#identity_provider_oauth_settings SagemakerUserProfile#identity_provider_oauth_settings}
        :param kendra_settings: kendra_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#kendra_settings SagemakerUserProfile#kendra_settings}
        :param model_register_settings: model_register_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#model_register_settings SagemakerUserProfile#model_register_settings}
        :param time_series_forecasting_settings: time_series_forecasting_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#time_series_forecasting_settings SagemakerUserProfile#time_series_forecasting_settings}
        :param workspace_settings: workspace_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#workspace_settings SagemakerUserProfile#workspace_settings}
        '''
        if isinstance(direct_deploy_settings, dict):
            direct_deploy_settings = SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings(**direct_deploy_settings)
        if isinstance(kendra_settings, dict):
            kendra_settings = SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings(**kendra_settings)
        if isinstance(model_register_settings, dict):
            model_register_settings = SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings(**model_register_settings)
        if isinstance(time_series_forecasting_settings, dict):
            time_series_forecasting_settings = SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings(**time_series_forecasting_settings)
        if isinstance(workspace_settings, dict):
            workspace_settings = SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings(**workspace_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7452fb45342ec38d7a759913db76d0645787d5eb94555b6707624a9797d604b3)
            check_type(argname="argument direct_deploy_settings", value=direct_deploy_settings, expected_type=type_hints["direct_deploy_settings"])
            check_type(argname="argument identity_provider_oauth_settings", value=identity_provider_oauth_settings, expected_type=type_hints["identity_provider_oauth_settings"])
            check_type(argname="argument kendra_settings", value=kendra_settings, expected_type=type_hints["kendra_settings"])
            check_type(argname="argument model_register_settings", value=model_register_settings, expected_type=type_hints["model_register_settings"])
            check_type(argname="argument time_series_forecasting_settings", value=time_series_forecasting_settings, expected_type=type_hints["time_series_forecasting_settings"])
            check_type(argname="argument workspace_settings", value=workspace_settings, expected_type=type_hints["workspace_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if direct_deploy_settings is not None:
            self._values["direct_deploy_settings"] = direct_deploy_settings
        if identity_provider_oauth_settings is not None:
            self._values["identity_provider_oauth_settings"] = identity_provider_oauth_settings
        if kendra_settings is not None:
            self._values["kendra_settings"] = kendra_settings
        if model_register_settings is not None:
            self._values["model_register_settings"] = model_register_settings
        if time_series_forecasting_settings is not None:
            self._values["time_series_forecasting_settings"] = time_series_forecasting_settings
        if workspace_settings is not None:
            self._values["workspace_settings"] = workspace_settings

    @builtins.property
    def direct_deploy_settings(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings"]:
        '''direct_deploy_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#direct_deploy_settings SagemakerUserProfile#direct_deploy_settings}
        '''
        result = self._values.get("direct_deploy_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings"], result)

    @builtins.property
    def identity_provider_oauth_settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings"]]]:
        '''identity_provider_oauth_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#identity_provider_oauth_settings SagemakerUserProfile#identity_provider_oauth_settings}
        '''
        result = self._values.get("identity_provider_oauth_settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings"]]], result)

    @builtins.property
    def kendra_settings(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings"]:
        '''kendra_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#kendra_settings SagemakerUserProfile#kendra_settings}
        '''
        result = self._values.get("kendra_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings"], result)

    @builtins.property
    def model_register_settings(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings"]:
        '''model_register_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#model_register_settings SagemakerUserProfile#model_register_settings}
        '''
        result = self._values.get("model_register_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings"], result)

    @builtins.property
    def time_series_forecasting_settings(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings"]:
        '''time_series_forecasting_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#time_series_forecasting_settings SagemakerUserProfile#time_series_forecasting_settings}
        '''
        result = self._values.get("time_series_forecasting_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings"], result)

    @builtins.property
    def workspace_settings(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings"]:
        '''workspace_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#workspace_settings SagemakerUserProfile#workspace_settings}
        '''
        result = self._values.get("workspace_settings")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsCanvasAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings:
    def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__529a1d38ab987ca1549aed27a902da1b855b01a06a9a7cc0c808f06dee274fbe)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8258db90684418a5a84b6de02e7f1a61c6f3b84b41781ba8781cf86c8da6a9b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab841f7de5b0f182fe22ec840754f07df5d191fd7d49072fdf11794dcb3f75c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f1c998c824c08939de379b24c1a4f7d4ffbdd1518445a628a00b270048af88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings",
    jsii_struct_bases=[],
    name_mapping={
        "secret_arn": "secretArn",
        "data_source_name": "dataSourceName",
        "status": "status",
    },
)
class SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings:
    def __init__(
        self,
        *,
        secret_arn: builtins.str,
        data_source_name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#secret_arn SagemakerUserProfile#secret_arn}.
        :param data_source_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#data_source_name SagemakerUserProfile#data_source_name}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf419f2a0aadf60e0ac4a38802926addeab6bcb3d69c4f9ddb7b04b445eb70df)
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_arn": secret_arn,
        }
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def secret_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#secret_arn SagemakerUserProfile#secret_arn}.'''
        result = self._values.get("secret_arn")
        assert result is not None, "Required property 'secret_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#data_source_name SagemakerUserProfile#data_source_name}.'''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettingsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e016dc1f0664ae154ecdf59e4e8d12d4a01e9342ab3aed3d682c4cbfea3381e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7dc4861a94bc2f45ec06053964b340c17ef52f201519652831453a9815b150)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c4502abeee145a6400c82b4c35d22f4d11b6417df0d70ee8a75d74472cc1fba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85fac916306192af5a9a610cf12a89f96e3a679fb4c16671d8f0d3ecf3c034b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c3c9cf7e2a8a7315ef264ee76e36101f967255b79f1a09c9217d17eb641b860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f33045b0782f1870b8b47235cfdcf6f6c142ba6b5a371f8674dcb1547c7cac1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae810955e8b040a570a674f4dca0f16a584dd411eabadbebf073a840e7370cc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDataSourceName")
    def reset_data_source_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSourceName", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="dataSourceNameInput")
    def data_source_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretArnInput")
    def secret_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretArnInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @data_source_name.setter
    def data_source_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809d4fc7911ee884cf27d20787f9b88b12023eafab1061e1cd7c35dbf6785116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceName", value)

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @secret_arn.setter
    def secret_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8278c226f218015a9d88d9008294d834f149623990a1bf09192990ab5591372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretArn", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da286f0534691dc018505501895ad6dc374cd5624f6dbd8106f8026c4f5c96c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58d4f5ce610753d44d729830a088fccf62e74d589ce1deff87b7bdedb426a701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings:
    def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec7e2cad6b0c861b21d801687cbe5960e8d7ec3f25044a0506abbf27efea4ed8)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4364bd6fbde66bceb191a11aee73d85eb690dc6178d64880174f19257fc64df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ea3008ae6cefa9ae6d4d4925d7ade897c2cdba712065cade41563647b3c0d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f70a4aff23d28e6c45efad27dba0ac2b00c56791dacecd52f1399516d23b82b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings",
    jsii_struct_bases=[],
    name_mapping={
        "cross_account_model_register_role_arn": "crossAccountModelRegisterRoleArn",
        "status": "status",
    },
)
class SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings:
    def __init__(
        self,
        *,
        cross_account_model_register_role_arn: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cross_account_model_register_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#cross_account_model_register_role_arn SagemakerUserProfile#cross_account_model_register_role_arn}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e9f9f428c608583d7fb691d3413acd5d35a3668eb3849e7471960ea60e4beb)
            check_type(argname="argument cross_account_model_register_role_arn", value=cross_account_model_register_role_arn, expected_type=type_hints["cross_account_model_register_role_arn"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cross_account_model_register_role_arn is not None:
            self._values["cross_account_model_register_role_arn"] = cross_account_model_register_role_arn
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def cross_account_model_register_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#cross_account_model_register_role_arn SagemakerUserProfile#cross_account_model_register_role_arn}.'''
        result = self._values.get("cross_account_model_register_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee6323a88191ce07913492e3954cbd6c01db4ac40434213eed3d981e65a8aa2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCrossAccountModelRegisterRoleArn")
    def reset_cross_account_model_register_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossAccountModelRegisterRoleArn", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="crossAccountModelRegisterRoleArnInput")
    def cross_account_model_register_role_arn_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossAccountModelRegisterRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="crossAccountModelRegisterRoleArn")
    def cross_account_model_register_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossAccountModelRegisterRoleArn"))

    @cross_account_model_register_role_arn.setter
    def cross_account_model_register_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc0fd1bad48ae339ede9bd6b983f36b070a1c7d66521e46f83e4d56c3c1884a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossAccountModelRegisterRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58f0d69dcbc008fcecfc6fb2c60d17c084ad25c6ab4b55e147280fa6f628d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf38cc2523994f59cd888a46c443ab2811144d0df79c8bf1d1d6c62975cc4d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerUserProfileUserSettingsCanvasAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32caf25643a9da55b393d9467b53ae401338dbf066e793469f77d75dccaba072)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDirectDeploySettings")
    def put_direct_deploy_settings(
        self,
        *,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.
        '''
        value = SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings(
            status=status
        )

        return typing.cast(None, jsii.invoke(self, "putDirectDeploySettings", [value]))

    @jsii.member(jsii_name="putIdentityProviderOauthSettings")
    def put_identity_provider_oauth_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f401848e47c92ed500ad2529dd0c33983c1330c643ea99d93d53f9a97b3dadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIdentityProviderOauthSettings", [value]))

    @jsii.member(jsii_name="putKendraSettings")
    def put_kendra_settings(
        self,
        *,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.
        '''
        value = SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings(
            status=status
        )

        return typing.cast(None, jsii.invoke(self, "putKendraSettings", [value]))

    @jsii.member(jsii_name="putModelRegisterSettings")
    def put_model_register_settings(
        self,
        *,
        cross_account_model_register_role_arn: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cross_account_model_register_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#cross_account_model_register_role_arn SagemakerUserProfile#cross_account_model_register_role_arn}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.
        '''
        value = SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings(
            cross_account_model_register_role_arn=cross_account_model_register_role_arn,
            status=status,
        )

        return typing.cast(None, jsii.invoke(self, "putModelRegisterSettings", [value]))

    @jsii.member(jsii_name="putTimeSeriesForecastingSettings")
    def put_time_series_forecasting_settings(
        self,
        *,
        amazon_forecast_role_arn: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param amazon_forecast_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#amazon_forecast_role_arn SagemakerUserProfile#amazon_forecast_role_arn}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.
        '''
        value = SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings(
            amazon_forecast_role_arn=amazon_forecast_role_arn, status=status
        )

        return typing.cast(None, jsii.invoke(self, "putTimeSeriesForecastingSettings", [value]))

    @jsii.member(jsii_name="putWorkspaceSettings")
    def put_workspace_settings(
        self,
        *,
        s3_artifact_path: typing.Optional[builtins.str] = None,
        s3_kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_artifact_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#s3_artifact_path SagemakerUserProfile#s3_artifact_path}.
        :param s3_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#s3_kms_key_id SagemakerUserProfile#s3_kms_key_id}.
        '''
        value = SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings(
            s3_artifact_path=s3_artifact_path, s3_kms_key_id=s3_kms_key_id
        )

        return typing.cast(None, jsii.invoke(self, "putWorkspaceSettings", [value]))

    @jsii.member(jsii_name="resetDirectDeploySettings")
    def reset_direct_deploy_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectDeploySettings", []))

    @jsii.member(jsii_name="resetIdentityProviderOauthSettings")
    def reset_identity_provider_oauth_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderOauthSettings", []))

    @jsii.member(jsii_name="resetKendraSettings")
    def reset_kendra_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKendraSettings", []))

    @jsii.member(jsii_name="resetModelRegisterSettings")
    def reset_model_register_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelRegisterSettings", []))

    @jsii.member(jsii_name="resetTimeSeriesForecastingSettings")
    def reset_time_series_forecasting_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeSeriesForecastingSettings", []))

    @jsii.member(jsii_name="resetWorkspaceSettings")
    def reset_workspace_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceSettings", []))

    @builtins.property
    @jsii.member(jsii_name="directDeploySettings")
    def direct_deploy_settings(
        self,
    ) -> SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettingsOutputReference:
        return typing.cast(SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettingsOutputReference, jsii.get(self, "directDeploySettings"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderOauthSettings")
    def identity_provider_oauth_settings(
        self,
    ) -> SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettingsList:
        return typing.cast(SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettingsList, jsii.get(self, "identityProviderOauthSettings"))

    @builtins.property
    @jsii.member(jsii_name="kendraSettings")
    def kendra_settings(
        self,
    ) -> SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettingsOutputReference:
        return typing.cast(SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettingsOutputReference, jsii.get(self, "kendraSettings"))

    @builtins.property
    @jsii.member(jsii_name="modelRegisterSettings")
    def model_register_settings(
        self,
    ) -> SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettingsOutputReference:
        return typing.cast(SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettingsOutputReference, jsii.get(self, "modelRegisterSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeSeriesForecastingSettings")
    def time_series_forecasting_settings(
        self,
    ) -> "SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettingsOutputReference":
        return typing.cast("SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettingsOutputReference", jsii.get(self, "timeSeriesForecastingSettings"))

    @builtins.property
    @jsii.member(jsii_name="workspaceSettings")
    def workspace_settings(
        self,
    ) -> "SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettingsOutputReference":
        return typing.cast("SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettingsOutputReference", jsii.get(self, "workspaceSettings"))

    @builtins.property
    @jsii.member(jsii_name="directDeploySettingsInput")
    def direct_deploy_settings_input(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings], jsii.get(self, "directDeploySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderOauthSettingsInput")
    def identity_provider_oauth_settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings]]], jsii.get(self, "identityProviderOauthSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="kendraSettingsInput")
    def kendra_settings_input(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings], jsii.get(self, "kendraSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="modelRegisterSettingsInput")
    def model_register_settings_input(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings], jsii.get(self, "modelRegisterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeSeriesForecastingSettingsInput")
    def time_series_forecasting_settings_input(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings"]:
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings"], jsii.get(self, "timeSeriesForecastingSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceSettingsInput")
    def workspace_settings_input(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings"]:
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings"], jsii.get(self, "workspaceSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142acff5e04e446b46d1be45aa0a9d541304fbc6c464205266252bbda3652690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "amazon_forecast_role_arn": "amazonForecastRoleArn",
        "status": "status",
    },
)
class SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings:
    def __init__(
        self,
        *,
        amazon_forecast_role_arn: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param amazon_forecast_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#amazon_forecast_role_arn SagemakerUserProfile#amazon_forecast_role_arn}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d26f9860d63b266c957bb65edcb81099743eb007b36d2638a8d3b5719022e4f)
            check_type(argname="argument amazon_forecast_role_arn", value=amazon_forecast_role_arn, expected_type=type_hints["amazon_forecast_role_arn"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amazon_forecast_role_arn is not None:
            self._values["amazon_forecast_role_arn"] = amazon_forecast_role_arn
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def amazon_forecast_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#amazon_forecast_role_arn SagemakerUserProfile#amazon_forecast_role_arn}.'''
        result = self._values.get("amazon_forecast_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#status SagemakerUserProfile#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e16e644a151eecf4c2b699bfb64168962bd886e57f2bcea292ef85596c1e143)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAmazonForecastRoleArn")
    def reset_amazon_forecast_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmazonForecastRoleArn", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="amazonForecastRoleArnInput")
    def amazon_forecast_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "amazonForecastRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="amazonForecastRoleArn")
    def amazon_forecast_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "amazonForecastRoleArn"))

    @amazon_forecast_role_arn.setter
    def amazon_forecast_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce6e05c84ee781121509eb7d6dd76956171f3133b9bd02154051c835a1217733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "amazonForecastRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a69b9fa074c105a8f073d469834c789924a6609480d037cca06ffd84e45bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fdee85ec39618e879189772d33ff8b564ed4f7cd7c09564df30f7800feb9d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings",
    jsii_struct_bases=[],
    name_mapping={"s3_artifact_path": "s3ArtifactPath", "s3_kms_key_id": "s3KmsKeyId"},
)
class SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings:
    def __init__(
        self,
        *,
        s3_artifact_path: typing.Optional[builtins.str] = None,
        s3_kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_artifact_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#s3_artifact_path SagemakerUserProfile#s3_artifact_path}.
        :param s3_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#s3_kms_key_id SagemakerUserProfile#s3_kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59d2f666ef0d90ff1ae38cdd07987fcad93f4f63767d3c09e3a29ea98fb71cd)
            check_type(argname="argument s3_artifact_path", value=s3_artifact_path, expected_type=type_hints["s3_artifact_path"])
            check_type(argname="argument s3_kms_key_id", value=s3_kms_key_id, expected_type=type_hints["s3_kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_artifact_path is not None:
            self._values["s3_artifact_path"] = s3_artifact_path
        if s3_kms_key_id is not None:
            self._values["s3_kms_key_id"] = s3_kms_key_id

    @builtins.property
    def s3_artifact_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#s3_artifact_path SagemakerUserProfile#s3_artifact_path}.'''
        result = self._values.get("s3_artifact_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#s3_kms_key_id SagemakerUserProfile#s3_kms_key_id}.'''
        result = self._values.get("s3_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c96c8a39871c6dea6a2243e6b3456506b3f4c0ddcb61c9dbdb487bbbf6f99b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3ArtifactPath")
    def reset_s3_artifact_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3ArtifactPath", []))

    @jsii.member(jsii_name="resetS3KmsKeyId")
    def reset_s3_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3KmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="s3ArtifactPathInput")
    def s3_artifact_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3ArtifactPathInput"))

    @builtins.property
    @jsii.member(jsii_name="s3KmsKeyIdInput")
    def s3_kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3KmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="s3ArtifactPath")
    def s3_artifact_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3ArtifactPath"))

    @s3_artifact_path.setter
    def s3_artifact_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37975da0714fd32c1153d6b8e96c179a4a8892306caa326386a59f88144f81cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3ArtifactPath", value)

    @builtins.property
    @jsii.member(jsii_name="s3KmsKeyId")
    def s3_kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3KmsKeyId"))

    @s3_kms_key_id.setter
    def s3_kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776ad1aa67f1b9a41bee86aadbd89ca22a219c88768333a1148c9ebfcc5c5891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3KmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d155802e260addc32bfe6004909a22e3bcc72136534c98f004da569cbf584fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsJupyterServerAppSettings",
    jsii_struct_bases=[],
    name_mapping={
        "code_repository": "codeRepository",
        "default_resource_spec": "defaultResourceSpec",
        "lifecycle_config_arns": "lifecycleConfigArns",
    },
)
class SagemakerUserProfileUserSettingsJupyterServerAppSettings:
    def __init__(
        self,
        *,
        code_repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param code_repository: code_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#code_repository SagemakerUserProfile#code_repository}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#default_resource_spec SagemakerUserProfile#default_resource_spec}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arns SagemakerUserProfile#lifecycle_config_arns}.
        '''
        if isinstance(default_resource_spec, dict):
            default_resource_spec = SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec(**default_resource_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db048a8f3a9189bebbcb0d45ee4a8cf25d1c55d188aed6defc54cd35050a58dc)
            check_type(argname="argument code_repository", value=code_repository, expected_type=type_hints["code_repository"])
            check_type(argname="argument default_resource_spec", value=default_resource_spec, expected_type=type_hints["default_resource_spec"])
            check_type(argname="argument lifecycle_config_arns", value=lifecycle_config_arns, expected_type=type_hints["lifecycle_config_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code_repository is not None:
            self._values["code_repository"] = code_repository
        if default_resource_spec is not None:
            self._values["default_resource_spec"] = default_resource_spec
        if lifecycle_config_arns is not None:
            self._values["lifecycle_config_arns"] = lifecycle_config_arns

    @builtins.property
    def code_repository(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository"]]]:
        '''code_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#code_repository SagemakerUserProfile#code_repository}
        '''
        result = self._values.get("code_repository")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository"]]], result)

    @builtins.property
    def default_resource_spec(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec"]:
        '''default_resource_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#default_resource_spec SagemakerUserProfile#default_resource_spec}
        '''
        result = self._values.get("default_resource_spec")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec"], result)

    @builtins.property
    def lifecycle_config_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arns SagemakerUserProfile#lifecycle_config_arns}.'''
        result = self._values.get("lifecycle_config_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsJupyterServerAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository",
    jsii_struct_bases=[],
    name_mapping={"repository_url": "repositoryUrl"},
)
class SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository:
    def __init__(self, *, repository_url: builtins.str) -> None:
        '''
        :param repository_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#repository_url SagemakerUserProfile#repository_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c5a161ff7bad6fe50a5a0287f6d594201900ef163c4ccf3794010c761bf673)
            check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_url": repository_url,
        }

    @builtins.property
    def repository_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#repository_url SagemakerUserProfile#repository_url}.'''
        result = self._values.get("repository_url")
        assert result is not None, "Required property 'repository_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepositoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepositoryList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ec8bf24f862479e8de048505b664ac709def87c3f347cc278b9aff4f489d58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepositoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02dff582f73ebc045e842aa848a8a23fcfc059add8599b7b9f93418b6786b755)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepositoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d248080d95ef3eb0992c58f811870b8b16630cc560eb9abc0d5a483faec4fc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e67c1dc5d5ebe1ff0f8a8d33c7142f52571e6af096ece262e72acded82e226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cbc195f59dbaf44184ba22dff515ef8a00762a208d574102a2cc08246793bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1459b5a475fa62e999b0a9bfe1e76073f70f2cfc8e6fd02dacf856f30d4fd2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepositoryOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ce83295d8bbae54dbc36a5ac115dd3a496f2075c5b79cb73e43f5c7dc91116)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="repositoryUrlInput")
    def repository_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryUrl")
    def repository_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryUrl"))

    @repository_url.setter
    def repository_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9fc4daca1128b6f9c4aca7584106407e8f78c77456ed60936c62a3c9a451a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryUrl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a44f1902cbefae0612ab33af602f921525e2c2b4b903518a36352ace538d4296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "lifecycle_config_arn": "lifecycleConfigArn",
        "sagemaker_image_arn": "sagemakerImageArn",
        "sagemaker_image_version_arn": "sagemakerImageVersionArn",
    },
)
class SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#instance_type SagemakerUserProfile#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arn SagemakerUserProfile#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_arn SagemakerUserProfile#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_version_arn SagemakerUserProfile#sagemaker_image_version_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3438b428ed79e05c9f3d9294075f5792c273929ffd55f6d0daeec85ef5e3ead)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument lifecycle_config_arn", value=lifecycle_config_arn, expected_type=type_hints["lifecycle_config_arn"])
            check_type(argname="argument sagemaker_image_arn", value=sagemaker_image_arn, expected_type=type_hints["sagemaker_image_arn"])
            check_type(argname="argument sagemaker_image_version_arn", value=sagemaker_image_version_arn, expected_type=type_hints["sagemaker_image_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if lifecycle_config_arn is not None:
            self._values["lifecycle_config_arn"] = lifecycle_config_arn
        if sagemaker_image_arn is not None:
            self._values["sagemaker_image_arn"] = sagemaker_image_arn
        if sagemaker_image_version_arn is not None:
            self._values["sagemaker_image_version_arn"] = sagemaker_image_version_arn

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#instance_type SagemakerUserProfile#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arn SagemakerUserProfile#lifecycle_config_arn}.'''
        result = self._values.get("lifecycle_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_arn SagemakerUserProfile#sagemaker_image_arn}.'''
        result = self._values.get("sagemaker_image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_version_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_version_arn SagemakerUserProfile#sagemaker_image_version_arn}.'''
        result = self._values.get("sagemaker_image_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696ee5abddc21cd93a701d843ee22f07b03c5b1cd876a454aaccc7a17461b6d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLifecycleConfigArn")
    def reset_lifecycle_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArn", []))

    @jsii.member(jsii_name="resetSagemakerImageArn")
    def reset_sagemaker_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageArn", []))

    @jsii.member(jsii_name="resetSagemakerImageVersionArn")
    def reset_sagemaker_image_version_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageVersionArn", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnInput")
    def lifecycle_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArnInput")
    def sagemaker_image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArnInput")
    def sagemaker_image_version_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageVersionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78341bbb361c279e579d12655e355bb6d4b60b3c910c55da6f527dd5505a442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArn")
    def lifecycle_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigArn"))

    @lifecycle_config_arn.setter
    def lifecycle_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24aca68ec2279150c9ea49cfa15e3a285885da2f2b2cd8445d166d354bc3af90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArn")
    def sagemaker_image_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageArn"))

    @sagemaker_image_arn.setter
    def sagemaker_image_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd703f527b25f98af7032b89adac2d66ae69f3d1a01676cdb6d369a84aba4fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArn")
    def sagemaker_image_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageVersionArn"))

    @sagemaker_image_version_arn.setter
    def sagemaker_image_version_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1d1a15a8c16eda18181a733e09ce48218d0985d0b0374d757490bce38d9493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de7c3e4b8ec85e2844fb98d794deeb690ed503a485db066312dafbcc0715f280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerUserProfileUserSettingsJupyterServerAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsJupyterServerAppSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8879ec84a916cf6e71ca7fabdcb8db3d8063a6ea53bb2aa3bcdb5f2940682b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCodeRepository")
    def put_code_repository(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1cc428abdda3dd32a7f7b8d2d2f5fcb9a0658acfa67771426b05678585a2cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCodeRepository", [value]))

    @jsii.member(jsii_name="putDefaultResourceSpec")
    def put_default_resource_spec(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#instance_type SagemakerUserProfile#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arn SagemakerUserProfile#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_arn SagemakerUserProfile#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_version_arn SagemakerUserProfile#sagemaker_image_version_arn}.
        '''
        value = SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec(
            instance_type=instance_type,
            lifecycle_config_arn=lifecycle_config_arn,
            sagemaker_image_arn=sagemaker_image_arn,
            sagemaker_image_version_arn=sagemaker_image_version_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultResourceSpec", [value]))

    @jsii.member(jsii_name="resetCodeRepository")
    def reset_code_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeRepository", []))

    @jsii.member(jsii_name="resetDefaultResourceSpec")
    def reset_default_resource_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultResourceSpec", []))

    @jsii.member(jsii_name="resetLifecycleConfigArns")
    def reset_lifecycle_config_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArns", []))

    @builtins.property
    @jsii.member(jsii_name="codeRepository")
    def code_repository(
        self,
    ) -> SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepositoryList:
        return typing.cast(SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepositoryList, jsii.get(self, "codeRepository"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpec")
    def default_resource_spec(
        self,
    ) -> SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference:
        return typing.cast(SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference, jsii.get(self, "defaultResourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="codeRepositoryInput")
    def code_repository_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository]]], jsii.get(self, "codeRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpecInput")
    def default_resource_spec_input(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec], jsii.get(self, "defaultResourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnsInput")
    def lifecycle_config_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "lifecycleConfigArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArns")
    def lifecycle_config_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "lifecycleConfigArns"))

    @lifecycle_config_arns.setter
    def lifecycle_config_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7a2b8ec6e31dd1fe395dc9e67438a77d2fece62da9d5f41d4a54c20a5f22dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArns", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsJupyterServerAppSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsJupyterServerAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsJupyterServerAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14bf9af7f3c9991425f5be3c43ef1fd363e99c2c86fdf78deaebd9d8c313b1f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsKernelGatewayAppSettings",
    jsii_struct_bases=[],
    name_mapping={
        "custom_image": "customImage",
        "default_resource_spec": "defaultResourceSpec",
        "lifecycle_config_arns": "lifecycleConfigArns",
    },
)
class SagemakerUserProfileUserSettingsKernelGatewayAppSettings:
    def __init__(
        self,
        *,
        custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#custom_image SagemakerUserProfile#custom_image}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#default_resource_spec SagemakerUserProfile#default_resource_spec}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arns SagemakerUserProfile#lifecycle_config_arns}.
        '''
        if isinstance(default_resource_spec, dict):
            default_resource_spec = SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec(**default_resource_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d346788be069afbab298b2155eed082b16a7ec00a903e41d88612b01ddb56911)
            check_type(argname="argument custom_image", value=custom_image, expected_type=type_hints["custom_image"])
            check_type(argname="argument default_resource_spec", value=default_resource_spec, expected_type=type_hints["default_resource_spec"])
            check_type(argname="argument lifecycle_config_arns", value=lifecycle_config_arns, expected_type=type_hints["lifecycle_config_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_image is not None:
            self._values["custom_image"] = custom_image
        if default_resource_spec is not None:
            self._values["default_resource_spec"] = default_resource_spec
        if lifecycle_config_arns is not None:
            self._values["lifecycle_config_arns"] = lifecycle_config_arns

    @builtins.property
    def custom_image(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage"]]]:
        '''custom_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#custom_image SagemakerUserProfile#custom_image}
        '''
        result = self._values.get("custom_image")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage"]]], result)

    @builtins.property
    def default_resource_spec(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec"]:
        '''default_resource_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#default_resource_spec SagemakerUserProfile#default_resource_spec}
        '''
        result = self._values.get("default_resource_spec")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec"], result)

    @builtins.property
    def lifecycle_config_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arns SagemakerUserProfile#lifecycle_config_arns}.'''
        result = self._values.get("lifecycle_config_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsKernelGatewayAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage",
    jsii_struct_bases=[],
    name_mapping={
        "app_image_config_name": "appImageConfigName",
        "image_name": "imageName",
        "image_version_number": "imageVersionNumber",
    },
)
class SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage:
    def __init__(
        self,
        *,
        app_image_config_name: builtins.str,
        image_name: builtins.str,
        image_version_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param app_image_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#app_image_config_name SagemakerUserProfile#app_image_config_name}.
        :param image_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#image_name SagemakerUserProfile#image_name}.
        :param image_version_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#image_version_number SagemakerUserProfile#image_version_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__656858a678e7193fbc8df64771353adcb9254d60bd3e7885916ca84449a584b3)
            check_type(argname="argument app_image_config_name", value=app_image_config_name, expected_type=type_hints["app_image_config_name"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_version_number", value=image_version_number, expected_type=type_hints["image_version_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_image_config_name": app_image_config_name,
            "image_name": image_name,
        }
        if image_version_number is not None:
            self._values["image_version_number"] = image_version_number

    @builtins.property
    def app_image_config_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#app_image_config_name SagemakerUserProfile#app_image_config_name}.'''
        result = self._values.get("app_image_config_name")
        assert result is not None, "Required property 'app_image_config_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#image_name SagemakerUserProfile#image_name}.'''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_version_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#image_version_number SagemakerUserProfile#image_version_number}.'''
        result = self._values.get("image_version_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImageList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4ccf627fafc6a473a83590771d8d4739b7b25d83f80838c81bcd6118bee415)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d6cbf1e5ccd920afb1e58627bf40632a10898eb5b80a9e72af3ab9183c9f5d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cab3eba8da8b95798aa60eae9c9b91b0c47a80c31b61320826973a9d135d769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3faa5bcc2086a3717da0e86a48d6f7b03a1b48b2478d0f4524bd8e10fdb35b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d20bae76ad7abc031f03482fc17251c0a3e4a9016f7fc57184cc2b54821edaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046578c5829f6220350b3e340f48773f5f3cd0a47092d87a789844c789d5aa17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImageOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b38ba2106c27faa97d366f07eaa6be4aadf513422ba61e22e7ded02e6c46e51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetImageVersionNumber")
    def reset_image_version_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersionNumber", []))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigNameInput")
    def app_image_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appImageConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersionNumberInput")
    def image_version_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageVersionNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigName")
    def app_image_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appImageConfigName"))

    @app_image_config_name.setter
    def app_image_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8fdc3288cfe9f50434faa71b18d189bcdf9dcf884361e1d63895361383bef9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appImageConfigName", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7a80926db30ea49905fcbaa8c60d5db2d0e7dab46a982db6247d8061f54dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageVersionNumber")
    def image_version_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageVersionNumber"))

    @image_version_number.setter
    def image_version_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecbbc54be8642eab4aa9a58cac705c4e434cd0917c19c152f460d28f785604da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersionNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c26870973a6eea454629daf66a126ac91ddf77c55d758ca5df3afb8397965bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "lifecycle_config_arn": "lifecycleConfigArn",
        "sagemaker_image_arn": "sagemakerImageArn",
        "sagemaker_image_version_arn": "sagemakerImageVersionArn",
    },
)
class SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#instance_type SagemakerUserProfile#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arn SagemakerUserProfile#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_arn SagemakerUserProfile#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_version_arn SagemakerUserProfile#sagemaker_image_version_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58596e21d298c43f57464f5f35c43627885ae62fff73bf1bb19757e8111158f0)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument lifecycle_config_arn", value=lifecycle_config_arn, expected_type=type_hints["lifecycle_config_arn"])
            check_type(argname="argument sagemaker_image_arn", value=sagemaker_image_arn, expected_type=type_hints["sagemaker_image_arn"])
            check_type(argname="argument sagemaker_image_version_arn", value=sagemaker_image_version_arn, expected_type=type_hints["sagemaker_image_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if lifecycle_config_arn is not None:
            self._values["lifecycle_config_arn"] = lifecycle_config_arn
        if sagemaker_image_arn is not None:
            self._values["sagemaker_image_arn"] = sagemaker_image_arn
        if sagemaker_image_version_arn is not None:
            self._values["sagemaker_image_version_arn"] = sagemaker_image_version_arn

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#instance_type SagemakerUserProfile#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arn SagemakerUserProfile#lifecycle_config_arn}.'''
        result = self._values.get("lifecycle_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_arn SagemakerUserProfile#sagemaker_image_arn}.'''
        result = self._values.get("sagemaker_image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_version_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_version_arn SagemakerUserProfile#sagemaker_image_version_arn}.'''
        result = self._values.get("sagemaker_image_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd59c2896eee144ccf2505eaa04bd48b37ac915c32fc20679364682393bf55b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLifecycleConfigArn")
    def reset_lifecycle_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArn", []))

    @jsii.member(jsii_name="resetSagemakerImageArn")
    def reset_sagemaker_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageArn", []))

    @jsii.member(jsii_name="resetSagemakerImageVersionArn")
    def reset_sagemaker_image_version_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageVersionArn", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnInput")
    def lifecycle_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArnInput")
    def sagemaker_image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArnInput")
    def sagemaker_image_version_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageVersionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac2870df50f95d2b38f90010c07b950b1c12eecd14ec42b622329a5a4e194be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArn")
    def lifecycle_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigArn"))

    @lifecycle_config_arn.setter
    def lifecycle_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134cf70572ec9741a12c5afe7697a2e774b8b8c3df17826342c396f3309e2c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArn")
    def sagemaker_image_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageArn"))

    @sagemaker_image_arn.setter
    def sagemaker_image_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f455d6aa38f8f2fb29f138bef6dfbf10ebb638f9ffe44b17b5870d8c33e177dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArn")
    def sagemaker_image_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageVersionArn"))

    @sagemaker_image_version_arn.setter
    def sagemaker_image_version_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c955b68b989f74df241815507692915f949450db63daa854778cb6a4652f2be6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__705dff396f9a7f66e7b62c2d2735ddf6454bc02e6e0ef125eae62e5eaea47b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerUserProfileUserSettingsKernelGatewayAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsKernelGatewayAppSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428f20d2d891ad1c7d7c16487ebed0c3c5d73687a4a00824fcf83e6fd467570e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomImage")
    def put_custom_image(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081e33c22fe7551cb4052fadca2a5e55c164a23579aa3b5a541477c38c65098c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomImage", [value]))

    @jsii.member(jsii_name="putDefaultResourceSpec")
    def put_default_resource_spec(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#instance_type SagemakerUserProfile#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arn SagemakerUserProfile#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_arn SagemakerUserProfile#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_version_arn SagemakerUserProfile#sagemaker_image_version_arn}.
        '''
        value = SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec(
            instance_type=instance_type,
            lifecycle_config_arn=lifecycle_config_arn,
            sagemaker_image_arn=sagemaker_image_arn,
            sagemaker_image_version_arn=sagemaker_image_version_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultResourceSpec", [value]))

    @jsii.member(jsii_name="resetCustomImage")
    def reset_custom_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomImage", []))

    @jsii.member(jsii_name="resetDefaultResourceSpec")
    def reset_default_resource_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultResourceSpec", []))

    @jsii.member(jsii_name="resetLifecycleConfigArns")
    def reset_lifecycle_config_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArns", []))

    @builtins.property
    @jsii.member(jsii_name="customImage")
    def custom_image(
        self,
    ) -> SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImageList:
        return typing.cast(SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImageList, jsii.get(self, "customImage"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpec")
    def default_resource_spec(
        self,
    ) -> SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference:
        return typing.cast(SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference, jsii.get(self, "defaultResourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="customImageInput")
    def custom_image_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage]]], jsii.get(self, "customImageInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpecInput")
    def default_resource_spec_input(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec], jsii.get(self, "defaultResourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnsInput")
    def lifecycle_config_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "lifecycleConfigArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArns")
    def lifecycle_config_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "lifecycleConfigArns"))

    @lifecycle_config_arns.setter
    def lifecycle_config_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783581cf280e45dd3c675002bab68483809ed3eb23a05edd9b6917e3f436f6a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArns", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsKernelGatewayAppSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsKernelGatewayAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsKernelGatewayAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3682d322f3ccc95304f1ebc121bdd9f16756b089d97455dcc0cdf80024ed084e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerUserProfileUserSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43bde5a1a592ed90c148352a0b606df4601524043ae6fbf279d2763cfc97e45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCanvasAppSettings")
    def put_canvas_app_settings(
        self,
        *,
        direct_deploy_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings, typing.Dict[builtins.str, typing.Any]]] = None,
        identity_provider_oauth_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
        kendra_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        model_register_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        time_series_forecasting_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        workspace_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param direct_deploy_settings: direct_deploy_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#direct_deploy_settings SagemakerUserProfile#direct_deploy_settings}
        :param identity_provider_oauth_settings: identity_provider_oauth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#identity_provider_oauth_settings SagemakerUserProfile#identity_provider_oauth_settings}
        :param kendra_settings: kendra_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#kendra_settings SagemakerUserProfile#kendra_settings}
        :param model_register_settings: model_register_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#model_register_settings SagemakerUserProfile#model_register_settings}
        :param time_series_forecasting_settings: time_series_forecasting_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#time_series_forecasting_settings SagemakerUserProfile#time_series_forecasting_settings}
        :param workspace_settings: workspace_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#workspace_settings SagemakerUserProfile#workspace_settings}
        '''
        value = SagemakerUserProfileUserSettingsCanvasAppSettings(
            direct_deploy_settings=direct_deploy_settings,
            identity_provider_oauth_settings=identity_provider_oauth_settings,
            kendra_settings=kendra_settings,
            model_register_settings=model_register_settings,
            time_series_forecasting_settings=time_series_forecasting_settings,
            workspace_settings=workspace_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putCanvasAppSettings", [value]))

    @jsii.member(jsii_name="putJupyterServerAppSettings")
    def put_jupyter_server_app_settings(
        self,
        *,
        code_repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param code_repository: code_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#code_repository SagemakerUserProfile#code_repository}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#default_resource_spec SagemakerUserProfile#default_resource_spec}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arns SagemakerUserProfile#lifecycle_config_arns}.
        '''
        value = SagemakerUserProfileUserSettingsJupyterServerAppSettings(
            code_repository=code_repository,
            default_resource_spec=default_resource_spec,
            lifecycle_config_arns=lifecycle_config_arns,
        )

        return typing.cast(None, jsii.invoke(self, "putJupyterServerAppSettings", [value]))

    @jsii.member(jsii_name="putKernelGatewayAppSettings")
    def put_kernel_gateway_app_settings(
        self,
        *,
        custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#custom_image SagemakerUserProfile#custom_image}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#default_resource_spec SagemakerUserProfile#default_resource_spec}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arns SagemakerUserProfile#lifecycle_config_arns}.
        '''
        value = SagemakerUserProfileUserSettingsKernelGatewayAppSettings(
            custom_image=custom_image,
            default_resource_spec=default_resource_spec,
            lifecycle_config_arns=lifecycle_config_arns,
        )

        return typing.cast(None, jsii.invoke(self, "putKernelGatewayAppSettings", [value]))

    @jsii.member(jsii_name="putRSessionAppSettings")
    def put_r_session_app_settings(
        self,
        *,
        custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#custom_image SagemakerUserProfile#custom_image}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#default_resource_spec SagemakerUserProfile#default_resource_spec}
        '''
        value = SagemakerUserProfileUserSettingsRSessionAppSettings(
            custom_image=custom_image, default_resource_spec=default_resource_spec
        )

        return typing.cast(None, jsii.invoke(self, "putRSessionAppSettings", [value]))

    @jsii.member(jsii_name="putRStudioServerProAppSettings")
    def put_r_studio_server_pro_app_settings(
        self,
        *,
        access_status: typing.Optional[builtins.str] = None,
        user_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#access_status SagemakerUserProfile#access_status}.
        :param user_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#user_group SagemakerUserProfile#user_group}.
        '''
        value = SagemakerUserProfileUserSettingsRStudioServerProAppSettings(
            access_status=access_status, user_group=user_group
        )

        return typing.cast(None, jsii.invoke(self, "putRStudioServerProAppSettings", [value]))

    @jsii.member(jsii_name="putSharingSettings")
    def put_sharing_settings(
        self,
        *,
        notebook_output_option: typing.Optional[builtins.str] = None,
        s3_kms_key_id: typing.Optional[builtins.str] = None,
        s3_output_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param notebook_output_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#notebook_output_option SagemakerUserProfile#notebook_output_option}.
        :param s3_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#s3_kms_key_id SagemakerUserProfile#s3_kms_key_id}.
        :param s3_output_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#s3_output_path SagemakerUserProfile#s3_output_path}.
        '''
        value = SagemakerUserProfileUserSettingsSharingSettings(
            notebook_output_option=notebook_output_option,
            s3_kms_key_id=s3_kms_key_id,
            s3_output_path=s3_output_path,
        )

        return typing.cast(None, jsii.invoke(self, "putSharingSettings", [value]))

    @jsii.member(jsii_name="putTensorBoardAppSettings")
    def put_tensor_board_app_settings(
        self,
        *,
        default_resource_spec: typing.Union["SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#default_resource_spec SagemakerUserProfile#default_resource_spec}
        '''
        value = SagemakerUserProfileUserSettingsTensorBoardAppSettings(
            default_resource_spec=default_resource_spec
        )

        return typing.cast(None, jsii.invoke(self, "putTensorBoardAppSettings", [value]))

    @jsii.member(jsii_name="resetCanvasAppSettings")
    def reset_canvas_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanvasAppSettings", []))

    @jsii.member(jsii_name="resetJupyterServerAppSettings")
    def reset_jupyter_server_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJupyterServerAppSettings", []))

    @jsii.member(jsii_name="resetKernelGatewayAppSettings")
    def reset_kernel_gateway_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKernelGatewayAppSettings", []))

    @jsii.member(jsii_name="resetRSessionAppSettings")
    def reset_r_session_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRSessionAppSettings", []))

    @jsii.member(jsii_name="resetRStudioServerProAppSettings")
    def reset_r_studio_server_pro_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRStudioServerProAppSettings", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetSharingSettings")
    def reset_sharing_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharingSettings", []))

    @jsii.member(jsii_name="resetTensorBoardAppSettings")
    def reset_tensor_board_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTensorBoardAppSettings", []))

    @builtins.property
    @jsii.member(jsii_name="canvasAppSettings")
    def canvas_app_settings(
        self,
    ) -> SagemakerUserProfileUserSettingsCanvasAppSettingsOutputReference:
        return typing.cast(SagemakerUserProfileUserSettingsCanvasAppSettingsOutputReference, jsii.get(self, "canvasAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="jupyterServerAppSettings")
    def jupyter_server_app_settings(
        self,
    ) -> SagemakerUserProfileUserSettingsJupyterServerAppSettingsOutputReference:
        return typing.cast(SagemakerUserProfileUserSettingsJupyterServerAppSettingsOutputReference, jsii.get(self, "jupyterServerAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="kernelGatewayAppSettings")
    def kernel_gateway_app_settings(
        self,
    ) -> SagemakerUserProfileUserSettingsKernelGatewayAppSettingsOutputReference:
        return typing.cast(SagemakerUserProfileUserSettingsKernelGatewayAppSettingsOutputReference, jsii.get(self, "kernelGatewayAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="rSessionAppSettings")
    def r_session_app_settings(
        self,
    ) -> "SagemakerUserProfileUserSettingsRSessionAppSettingsOutputReference":
        return typing.cast("SagemakerUserProfileUserSettingsRSessionAppSettingsOutputReference", jsii.get(self, "rSessionAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="rStudioServerProAppSettings")
    def r_studio_server_pro_app_settings(
        self,
    ) -> "SagemakerUserProfileUserSettingsRStudioServerProAppSettingsOutputReference":
        return typing.cast("SagemakerUserProfileUserSettingsRStudioServerProAppSettingsOutputReference", jsii.get(self, "rStudioServerProAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="sharingSettings")
    def sharing_settings(
        self,
    ) -> "SagemakerUserProfileUserSettingsSharingSettingsOutputReference":
        return typing.cast("SagemakerUserProfileUserSettingsSharingSettingsOutputReference", jsii.get(self, "sharingSettings"))

    @builtins.property
    @jsii.member(jsii_name="tensorBoardAppSettings")
    def tensor_board_app_settings(
        self,
    ) -> "SagemakerUserProfileUserSettingsTensorBoardAppSettingsOutputReference":
        return typing.cast("SagemakerUserProfileUserSettingsTensorBoardAppSettingsOutputReference", jsii.get(self, "tensorBoardAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="canvasAppSettingsInput")
    def canvas_app_settings_input(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettings], jsii.get(self, "canvasAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleInput")
    def execution_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="jupyterServerAppSettingsInput")
    def jupyter_server_app_settings_input(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsJupyterServerAppSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsJupyterServerAppSettings], jsii.get(self, "jupyterServerAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="kernelGatewayAppSettingsInput")
    def kernel_gateway_app_settings_input(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsKernelGatewayAppSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsKernelGatewayAppSettings], jsii.get(self, "kernelGatewayAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="rSessionAppSettingsInput")
    def r_session_app_settings_input(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsRSessionAppSettings"]:
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsRSessionAppSettings"], jsii.get(self, "rSessionAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="rStudioServerProAppSettingsInput")
    def r_studio_server_pro_app_settings_input(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsRStudioServerProAppSettings"]:
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsRStudioServerProAppSettings"], jsii.get(self, "rStudioServerProAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="sharingSettingsInput")
    def sharing_settings_input(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsSharingSettings"]:
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsSharingSettings"], jsii.get(self, "sharingSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="tensorBoardAppSettingsInput")
    def tensor_board_app_settings_input(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsTensorBoardAppSettings"]:
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsTensorBoardAppSettings"], jsii.get(self, "tensorBoardAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRole"))

    @execution_role.setter
    def execution_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455ac88bd73f0de55ce7e280ec61889e12cbc310195fa99591e8157f895e6b0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRole", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b7adeb4444a45916ed4c2ddcbe02add4fa593ca842f1a1202f828016edcc84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerUserProfileUserSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da7695c4441c85f09c2fb2170af083304ba86de8e93e0bf0b37a5e96f198b814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsRSessionAppSettings",
    jsii_struct_bases=[],
    name_mapping={
        "custom_image": "customImage",
        "default_resource_spec": "defaultResourceSpec",
    },
)
class SagemakerUserProfileUserSettingsRSessionAppSettings:
    def __init__(
        self,
        *,
        custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union["SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#custom_image SagemakerUserProfile#custom_image}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#default_resource_spec SagemakerUserProfile#default_resource_spec}
        '''
        if isinstance(default_resource_spec, dict):
            default_resource_spec = SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec(**default_resource_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4faa4239c756f19f06a1dba510819647ffbfaaad43cdb98b588df561af503b)
            check_type(argname="argument custom_image", value=custom_image, expected_type=type_hints["custom_image"])
            check_type(argname="argument default_resource_spec", value=default_resource_spec, expected_type=type_hints["default_resource_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_image is not None:
            self._values["custom_image"] = custom_image
        if default_resource_spec is not None:
            self._values["default_resource_spec"] = default_resource_spec

    @builtins.property
    def custom_image(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage"]]]:
        '''custom_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#custom_image SagemakerUserProfile#custom_image}
        '''
        result = self._values.get("custom_image")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage"]]], result)

    @builtins.property
    def default_resource_spec(
        self,
    ) -> typing.Optional["SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec"]:
        '''default_resource_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#default_resource_spec SagemakerUserProfile#default_resource_spec}
        '''
        result = self._values.get("default_resource_spec")
        return typing.cast(typing.Optional["SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsRSessionAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage",
    jsii_struct_bases=[],
    name_mapping={
        "app_image_config_name": "appImageConfigName",
        "image_name": "imageName",
        "image_version_number": "imageVersionNumber",
    },
)
class SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage:
    def __init__(
        self,
        *,
        app_image_config_name: builtins.str,
        image_name: builtins.str,
        image_version_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param app_image_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#app_image_config_name SagemakerUserProfile#app_image_config_name}.
        :param image_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#image_name SagemakerUserProfile#image_name}.
        :param image_version_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#image_version_number SagemakerUserProfile#image_version_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21a4c1c83487e979d27380b75f01c4d0e198bd43ac915464143662454e2e5b7c)
            check_type(argname="argument app_image_config_name", value=app_image_config_name, expected_type=type_hints["app_image_config_name"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_version_number", value=image_version_number, expected_type=type_hints["image_version_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_image_config_name": app_image_config_name,
            "image_name": image_name,
        }
        if image_version_number is not None:
            self._values["image_version_number"] = image_version_number

    @builtins.property
    def app_image_config_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#app_image_config_name SagemakerUserProfile#app_image_config_name}.'''
        result = self._values.get("app_image_config_name")
        assert result is not None, "Required property 'app_image_config_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#image_name SagemakerUserProfile#image_name}.'''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_version_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#image_version_number SagemakerUserProfile#image_version_number}.'''
        result = self._values.get("image_version_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImageList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e423b4fd31f6f108fa75595c3dd3be87f53dd3f7bfc97b8026da664531174624)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc345078e7217739b152c8e10d2ab3efa9bdafdb1138edf6a733a4ee09e72e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e0832e1d6660955869c26467f3aab9a38079082ffec3c0f5e373ea1580e4d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996d61a8a39ddcdb25a3c68857cfe73daf22c912d0eaaaf023f2f54a2c9e8326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd6e554f82d98426f94b542710c7e216bfd98799912122806177f9c510e74b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a374a9418bf2af5a3496d4b2ac0a91dd74c1dfaf4b5704b5ac26b66188071f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImageOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834537bbf711d221502a7733e741e8fe1cc5cdc30cb2b98d0827c83c8862995c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetImageVersionNumber")
    def reset_image_version_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersionNumber", []))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigNameInput")
    def app_image_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appImageConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersionNumberInput")
    def image_version_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageVersionNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigName")
    def app_image_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appImageConfigName"))

    @app_image_config_name.setter
    def app_image_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb66384d9b01ab44f809227c91e2e5067a98a7ab2d9fd1c2bb8019c04980f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appImageConfigName", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb7a1c377cdbbf0e4eb9b5d3db36c37481f235dcbeb2158013df8b6025986ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageVersionNumber")
    def image_version_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageVersionNumber"))

    @image_version_number.setter
    def image_version_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac45a480d8ea7e8ff86ba695aca87afe998e76d6f1a7d49ff9f566c6e4b98372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersionNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d7c10d0bf4b93f9aecd5df43002389febd774aefd672b3891dba09b991874ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "lifecycle_config_arn": "lifecycleConfigArn",
        "sagemaker_image_arn": "sagemakerImageArn",
        "sagemaker_image_version_arn": "sagemakerImageVersionArn",
    },
)
class SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#instance_type SagemakerUserProfile#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arn SagemakerUserProfile#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_arn SagemakerUserProfile#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_version_arn SagemakerUserProfile#sagemaker_image_version_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc93b5d53475692f637dbfb6371280a48f4aea6979f4f565fa2cd815940456bb)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument lifecycle_config_arn", value=lifecycle_config_arn, expected_type=type_hints["lifecycle_config_arn"])
            check_type(argname="argument sagemaker_image_arn", value=sagemaker_image_arn, expected_type=type_hints["sagemaker_image_arn"])
            check_type(argname="argument sagemaker_image_version_arn", value=sagemaker_image_version_arn, expected_type=type_hints["sagemaker_image_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if lifecycle_config_arn is not None:
            self._values["lifecycle_config_arn"] = lifecycle_config_arn
        if sagemaker_image_arn is not None:
            self._values["sagemaker_image_arn"] = sagemaker_image_arn
        if sagemaker_image_version_arn is not None:
            self._values["sagemaker_image_version_arn"] = sagemaker_image_version_arn

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#instance_type SagemakerUserProfile#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arn SagemakerUserProfile#lifecycle_config_arn}.'''
        result = self._values.get("lifecycle_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_arn SagemakerUserProfile#sagemaker_image_arn}.'''
        result = self._values.get("sagemaker_image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_version_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_version_arn SagemakerUserProfile#sagemaker_image_version_arn}.'''
        result = self._values.get("sagemaker_image_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpecOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8a285b6dafe551fe44ff44ad5080a627b4b1c21512abc8c54392b61876e20d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLifecycleConfigArn")
    def reset_lifecycle_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArn", []))

    @jsii.member(jsii_name="resetSagemakerImageArn")
    def reset_sagemaker_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageArn", []))

    @jsii.member(jsii_name="resetSagemakerImageVersionArn")
    def reset_sagemaker_image_version_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageVersionArn", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnInput")
    def lifecycle_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArnInput")
    def sagemaker_image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArnInput")
    def sagemaker_image_version_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageVersionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2537e30b8d8a276ddde2f151735641d4d52bf1b4c14ce146897edba5b43ab7ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArn")
    def lifecycle_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigArn"))

    @lifecycle_config_arn.setter
    def lifecycle_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9ec90b2251358711332595a49316a5c09f60ba2d5f55d968579689496f4ee20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArn")
    def sagemaker_image_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageArn"))

    @sagemaker_image_arn.setter
    def sagemaker_image_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__359fb4360f684b6f60cbc49ca4395d6b68e3e52fcd7e985dfa14afcb603b4a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArn")
    def sagemaker_image_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageVersionArn"))

    @sagemaker_image_version_arn.setter
    def sagemaker_image_version_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c166f2aeef4b5e1d2e333c493249713c5abb4b267db7077e4cf1816078b8365a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485746b07ddc8bfd50b64c1d1ec1fd80f400e2fadd64a9f0350c33b78b72b478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerUserProfileUserSettingsRSessionAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsRSessionAppSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14784ffa523406abf63a571e19bd87e2404469792ce4e3a875bb2baee6871c0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomImage")
    def put_custom_image(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08ffd807fa9edfa2ca3e3d54c0e7cdc645a421c2486677e9f34ff35577f4860f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomImage", [value]))

    @jsii.member(jsii_name="putDefaultResourceSpec")
    def put_default_resource_spec(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#instance_type SagemakerUserProfile#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arn SagemakerUserProfile#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_arn SagemakerUserProfile#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_version_arn SagemakerUserProfile#sagemaker_image_version_arn}.
        '''
        value = SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec(
            instance_type=instance_type,
            lifecycle_config_arn=lifecycle_config_arn,
            sagemaker_image_arn=sagemaker_image_arn,
            sagemaker_image_version_arn=sagemaker_image_version_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultResourceSpec", [value]))

    @jsii.member(jsii_name="resetCustomImage")
    def reset_custom_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomImage", []))

    @jsii.member(jsii_name="resetDefaultResourceSpec")
    def reset_default_resource_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultResourceSpec", []))

    @builtins.property
    @jsii.member(jsii_name="customImage")
    def custom_image(
        self,
    ) -> SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImageList:
        return typing.cast(SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImageList, jsii.get(self, "customImage"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpec")
    def default_resource_spec(
        self,
    ) -> SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpecOutputReference:
        return typing.cast(SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpecOutputReference, jsii.get(self, "defaultResourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="customImageInput")
    def custom_image_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage]]], jsii.get(self, "customImageInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpecInput")
    def default_resource_spec_input(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec], jsii.get(self, "defaultResourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsRSessionAppSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsRSessionAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsRSessionAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f21429fcf717441195b32f07eaba25ee476bb9986d1321a17be4fcc3469cc71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsRStudioServerProAppSettings",
    jsii_struct_bases=[],
    name_mapping={"access_status": "accessStatus", "user_group": "userGroup"},
)
class SagemakerUserProfileUserSettingsRStudioServerProAppSettings:
    def __init__(
        self,
        *,
        access_status: typing.Optional[builtins.str] = None,
        user_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#access_status SagemakerUserProfile#access_status}.
        :param user_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#user_group SagemakerUserProfile#user_group}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511fbd1bb69cfa14aad557f8808bb107b9f43314d62925fb75021494347d1482)
            check_type(argname="argument access_status", value=access_status, expected_type=type_hints["access_status"])
            check_type(argname="argument user_group", value=user_group, expected_type=type_hints["user_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_status is not None:
            self._values["access_status"] = access_status
        if user_group is not None:
            self._values["user_group"] = user_group

    @builtins.property
    def access_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#access_status SagemakerUserProfile#access_status}.'''
        result = self._values.get("access_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#user_group SagemakerUserProfile#user_group}.'''
        result = self._values.get("user_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsRStudioServerProAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsRStudioServerProAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsRStudioServerProAppSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f8af67339e32b9579fd68b2cc7593de9787bb97f68bd0516040074dd1e01c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessStatus")
    def reset_access_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessStatus", []))

    @jsii.member(jsii_name="resetUserGroup")
    def reset_user_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserGroup", []))

    @builtins.property
    @jsii.member(jsii_name="accessStatusInput")
    def access_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="userGroupInput")
    def user_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="accessStatus")
    def access_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessStatus"))

    @access_status.setter
    def access_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4f95b96e9fa001f7062ae3d7af4ac5925b6300eff75045864beb828e975f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessStatus", value)

    @builtins.property
    @jsii.member(jsii_name="userGroup")
    def user_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userGroup"))

    @user_group.setter
    def user_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c0fded862b3450124e40eb66a1dc6ff4f34a8e878ffcf9bb45b52a8c00d70f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userGroup", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsRStudioServerProAppSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsRStudioServerProAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsRStudioServerProAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d86707ec1a97e294a0fb564195ef82e1da15c13cb88fdf4f6bc31e37fa6849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsSharingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "notebook_output_option": "notebookOutputOption",
        "s3_kms_key_id": "s3KmsKeyId",
        "s3_output_path": "s3OutputPath",
    },
)
class SagemakerUserProfileUserSettingsSharingSettings:
    def __init__(
        self,
        *,
        notebook_output_option: typing.Optional[builtins.str] = None,
        s3_kms_key_id: typing.Optional[builtins.str] = None,
        s3_output_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param notebook_output_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#notebook_output_option SagemakerUserProfile#notebook_output_option}.
        :param s3_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#s3_kms_key_id SagemakerUserProfile#s3_kms_key_id}.
        :param s3_output_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#s3_output_path SagemakerUserProfile#s3_output_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270d965c9c3f9c3467fa3f02baf20ed3b0073e156eb0a5d62f32bdf45124b29a)
            check_type(argname="argument notebook_output_option", value=notebook_output_option, expected_type=type_hints["notebook_output_option"])
            check_type(argname="argument s3_kms_key_id", value=s3_kms_key_id, expected_type=type_hints["s3_kms_key_id"])
            check_type(argname="argument s3_output_path", value=s3_output_path, expected_type=type_hints["s3_output_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if notebook_output_option is not None:
            self._values["notebook_output_option"] = notebook_output_option
        if s3_kms_key_id is not None:
            self._values["s3_kms_key_id"] = s3_kms_key_id
        if s3_output_path is not None:
            self._values["s3_output_path"] = s3_output_path

    @builtins.property
    def notebook_output_option(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#notebook_output_option SagemakerUserProfile#notebook_output_option}.'''
        result = self._values.get("notebook_output_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#s3_kms_key_id SagemakerUserProfile#s3_kms_key_id}.'''
        result = self._values.get("s3_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_output_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#s3_output_path SagemakerUserProfile#s3_output_path}.'''
        result = self._values.get("s3_output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsSharingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsSharingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsSharingSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce83a2903af4f5e650d1396717e8ac4e3c73e7d93cc1209d1146f9dc4f094bc3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNotebookOutputOption")
    def reset_notebook_output_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotebookOutputOption", []))

    @jsii.member(jsii_name="resetS3KmsKeyId")
    def reset_s3_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3KmsKeyId", []))

    @jsii.member(jsii_name="resetS3OutputPath")
    def reset_s3_output_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3OutputPath", []))

    @builtins.property
    @jsii.member(jsii_name="notebookOutputOptionInput")
    def notebook_output_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notebookOutputOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="s3KmsKeyIdInput")
    def s3_kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3KmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="s3OutputPathInput")
    def s3_output_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3OutputPathInput"))

    @builtins.property
    @jsii.member(jsii_name="notebookOutputOption")
    def notebook_output_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notebookOutputOption"))

    @notebook_output_option.setter
    def notebook_output_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab57aedb4e0a0a391074cce2d69b1387fac12b394f0afdae02d98a77e4939057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebookOutputOption", value)

    @builtins.property
    @jsii.member(jsii_name="s3KmsKeyId")
    def s3_kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3KmsKeyId"))

    @s3_kms_key_id.setter
    def s3_kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6fda05c0bf98121d62bfc727e54e33d7477dba7c4f0972a1918138cf29cc159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3KmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="s3OutputPath")
    def s3_output_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3OutputPath"))

    @s3_output_path.setter
    def s3_output_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af67c2b0c967681ea3252efd41ca930a529ca31cfe54e3e3a0d96a711d3312d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3OutputPath", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsSharingSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsSharingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsSharingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9360963a9ba922f43b42d13ce3b855a8fcf01663192ae20efa46ca15feea0c30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsTensorBoardAppSettings",
    jsii_struct_bases=[],
    name_mapping={"default_resource_spec": "defaultResourceSpec"},
)
class SagemakerUserProfileUserSettingsTensorBoardAppSettings:
    def __init__(
        self,
        *,
        default_resource_spec: typing.Union["SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#default_resource_spec SagemakerUserProfile#default_resource_spec}
        '''
        if isinstance(default_resource_spec, dict):
            default_resource_spec = SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec(**default_resource_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841d6fe0afb9b888766eb94edd622771fe5400a897a374118efa05bd23ec3718)
            check_type(argname="argument default_resource_spec", value=default_resource_spec, expected_type=type_hints["default_resource_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_resource_spec": default_resource_spec,
        }

    @builtins.property
    def default_resource_spec(
        self,
    ) -> "SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec":
        '''default_resource_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#default_resource_spec SagemakerUserProfile#default_resource_spec}
        '''
        result = self._values.get("default_resource_spec")
        assert result is not None, "Required property 'default_resource_spec' is missing"
        return typing.cast("SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsTensorBoardAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "lifecycle_config_arn": "lifecycleConfigArn",
        "sagemaker_image_arn": "sagemakerImageArn",
        "sagemaker_image_version_arn": "sagemakerImageVersionArn",
    },
)
class SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#instance_type SagemakerUserProfile#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arn SagemakerUserProfile#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_arn SagemakerUserProfile#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_version_arn SagemakerUserProfile#sagemaker_image_version_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1447df3bb793b2b43abc3eeed88652392ae9dd7e0b0415cd632034e6e1aea0f1)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument lifecycle_config_arn", value=lifecycle_config_arn, expected_type=type_hints["lifecycle_config_arn"])
            check_type(argname="argument sagemaker_image_arn", value=sagemaker_image_arn, expected_type=type_hints["sagemaker_image_arn"])
            check_type(argname="argument sagemaker_image_version_arn", value=sagemaker_image_version_arn, expected_type=type_hints["sagemaker_image_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if lifecycle_config_arn is not None:
            self._values["lifecycle_config_arn"] = lifecycle_config_arn
        if sagemaker_image_arn is not None:
            self._values["sagemaker_image_arn"] = sagemaker_image_arn
        if sagemaker_image_version_arn is not None:
            self._values["sagemaker_image_version_arn"] = sagemaker_image_version_arn

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#instance_type SagemakerUserProfile#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arn SagemakerUserProfile#lifecycle_config_arn}.'''
        result = self._values.get("lifecycle_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_arn SagemakerUserProfile#sagemaker_image_arn}.'''
        result = self._values.get("sagemaker_image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_version_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_version_arn SagemakerUserProfile#sagemaker_image_version_arn}.'''
        result = self._values.get("sagemaker_image_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpecOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aecead6d8d13862ec8a5cb8061a5fa4a24a58c91d5ae78d0e2bd532330b609e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLifecycleConfigArn")
    def reset_lifecycle_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArn", []))

    @jsii.member(jsii_name="resetSagemakerImageArn")
    def reset_sagemaker_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageArn", []))

    @jsii.member(jsii_name="resetSagemakerImageVersionArn")
    def reset_sagemaker_image_version_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageVersionArn", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnInput")
    def lifecycle_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArnInput")
    def sagemaker_image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArnInput")
    def sagemaker_image_version_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageVersionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbd1574e0e4e15ba4a03488442c97903b1442cd426390d6514ed9f6ae7caead5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArn")
    def lifecycle_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigArn"))

    @lifecycle_config_arn.setter
    def lifecycle_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43d4c2f7bdceb4e7c45fdc6e5a8ef4158b08b622d65c3ae829f309bacbdf44b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArn")
    def sagemaker_image_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageArn"))

    @sagemaker_image_arn.setter
    def sagemaker_image_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ce79b81601f22283975e555be86d3bad8298dc994c0fd8a23f44b7cc6154e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArn")
    def sagemaker_image_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageVersionArn"))

    @sagemaker_image_version_arn.setter
    def sagemaker_image_version_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9663fef8c942acf3f16b96065778949f52ee9833c8cf13b8fa92fefce3721e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d5c20089f4579f7fc68cb919c6edf59b7dddec81659dc034106335a6a81a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerUserProfileUserSettingsTensorBoardAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerUserProfile.SagemakerUserProfileUserSettingsTensorBoardAppSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316ecdc041f582cc9076e950589d8afb530582495015e0b2d48301a1d2cd5613)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDefaultResourceSpec")
    def put_default_resource_spec(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#instance_type SagemakerUserProfile#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#lifecycle_config_arn SagemakerUserProfile#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_arn SagemakerUserProfile#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.29.0/docs/resources/sagemaker_user_profile#sagemaker_image_version_arn SagemakerUserProfile#sagemaker_image_version_arn}.
        '''
        value = SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec(
            instance_type=instance_type,
            lifecycle_config_arn=lifecycle_config_arn,
            sagemaker_image_arn=sagemaker_image_arn,
            sagemaker_image_version_arn=sagemaker_image_version_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultResourceSpec", [value]))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpec")
    def default_resource_spec(
        self,
    ) -> SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpecOutputReference:
        return typing.cast(SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpecOutputReference, jsii.get(self, "defaultResourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpecInput")
    def default_resource_spec_input(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec], jsii.get(self, "defaultResourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerUserProfileUserSettingsTensorBoardAppSettings]:
        return typing.cast(typing.Optional[SagemakerUserProfileUserSettingsTensorBoardAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerUserProfileUserSettingsTensorBoardAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1e1ffd8c17cf9a9138cfffd834fa3af301e25165fd3f77772edbdc9a49ef50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SagemakerUserProfile",
    "SagemakerUserProfileConfig",
    "SagemakerUserProfileUserSettings",
    "SagemakerUserProfileUserSettingsCanvasAppSettings",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettingsOutputReference",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettingsList",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettingsOutputReference",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettingsOutputReference",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettingsOutputReference",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsOutputReference",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettingsOutputReference",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings",
    "SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettingsOutputReference",
    "SagemakerUserProfileUserSettingsJupyterServerAppSettings",
    "SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository",
    "SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepositoryList",
    "SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepositoryOutputReference",
    "SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec",
    "SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference",
    "SagemakerUserProfileUserSettingsJupyterServerAppSettingsOutputReference",
    "SagemakerUserProfileUserSettingsKernelGatewayAppSettings",
    "SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage",
    "SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImageList",
    "SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImageOutputReference",
    "SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec",
    "SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference",
    "SagemakerUserProfileUserSettingsKernelGatewayAppSettingsOutputReference",
    "SagemakerUserProfileUserSettingsOutputReference",
    "SagemakerUserProfileUserSettingsRSessionAppSettings",
    "SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage",
    "SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImageList",
    "SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImageOutputReference",
    "SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec",
    "SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpecOutputReference",
    "SagemakerUserProfileUserSettingsRSessionAppSettingsOutputReference",
    "SagemakerUserProfileUserSettingsRStudioServerProAppSettings",
    "SagemakerUserProfileUserSettingsRStudioServerProAppSettingsOutputReference",
    "SagemakerUserProfileUserSettingsSharingSettings",
    "SagemakerUserProfileUserSettingsSharingSettingsOutputReference",
    "SagemakerUserProfileUserSettingsTensorBoardAppSettings",
    "SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec",
    "SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpecOutputReference",
    "SagemakerUserProfileUserSettingsTensorBoardAppSettingsOutputReference",
]

publication.publish()

def _typecheckingstub__94364b035a7681e7ff1e1e978f4c54626eea050d5ed2a082854aae0f430168b3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    domain_id: builtins.str,
    user_profile_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    single_sign_on_user_identifier: typing.Optional[builtins.str] = None,
    single_sign_on_user_value: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c59c1e36fa8f0580dd0c35e797ceb8b2783e0d49366f3afaa62808fcff37e6d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56faad451bf707c890b7ea60d99a0256d2c7c1994e664b67ff186544449ec4ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2258f1842205c3327e3e0519e820048176de11f935c701b620e5df3796c7146(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1cd32e5df9deb98b78b97c000d3b9ecfcd0cd53a8cdeeecdd69c31ddfbdbca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c5c8b544d8bd22c81eed872047804b11b2c00b978e66086e333643149079a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d064da11325e97f3a64a9e15c89dbb22d24e7a498007bb940a94bdf13ea5d788(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fafebc2a6c90906f0e60c4cee21a6c0fb4e40f9690449112d7d1d2aa09cf17(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073696c04c11f488a4acc9662e6caaa2e5e0c7dfb40c08aabd96033ada4152a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c83051f8a67245071364ce9e0a39bf8664578a6178a27d3c94df4f7b8d626f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain_id: builtins.str,
    user_profile_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    single_sign_on_user_identifier: typing.Optional[builtins.str] = None,
    single_sign_on_user_value: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d876be7b60ae620343f56346c172342ec3c15cd2e2779d7a87f74de85fb319f(
    *,
    execution_role: builtins.str,
    canvas_app_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    jupyter_server_app_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsJupyterServerAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    kernel_gateway_app_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsKernelGatewayAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    r_session_app_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsRSessionAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    r_studio_server_pro_app_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsRStudioServerProAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    sharing_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsSharingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    tensor_board_app_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsTensorBoardAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7452fb45342ec38d7a759913db76d0645787d5eb94555b6707624a9797d604b3(
    *,
    direct_deploy_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    identity_provider_oauth_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kendra_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    model_register_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    time_series_forecasting_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    workspace_settings: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529a1d38ab987ca1549aed27a902da1b855b01a06a9a7cc0c808f06dee274fbe(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8258db90684418a5a84b6de02e7f1a61c6f3b84b41781ba8781cf86c8da6a9b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab841f7de5b0f182fe22ec840754f07df5d191fd7d49072fdf11794dcb3f75c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f1c998c824c08939de379b24c1a4f7d4ffbdd1518445a628a00b270048af88(
    value: typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsDirectDeploySettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf419f2a0aadf60e0ac4a38802926addeab6bcb3d69c4f9ddb7b04b445eb70df(
    *,
    secret_arn: builtins.str,
    data_source_name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e016dc1f0664ae154ecdf59e4e8d12d4a01e9342ab3aed3d682c4cbfea3381e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7dc4861a94bc2f45ec06053964b340c17ef52f201519652831453a9815b150(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4502abeee145a6400c82b4c35d22f4d11b6417df0d70ee8a75d74472cc1fba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85fac916306192af5a9a610cf12a89f96e3a679fb4c16671d8f0d3ecf3c034b0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3c9cf7e2a8a7315ef264ee76e36101f967255b79f1a09c9217d17eb641b860(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f33045b0782f1870b8b47235cfdcf6f6c142ba6b5a371f8674dcb1547c7cac1a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae810955e8b040a570a674f4dca0f16a584dd411eabadbebf073a840e7370cc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809d4fc7911ee884cf27d20787f9b88b12023eafab1061e1cd7c35dbf6785116(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8278c226f218015a9d88d9008294d834f149623990a1bf09192990ab5591372(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da286f0534691dc018505501895ad6dc374cd5624f6dbd8106f8026c4f5c96c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d4f5ce610753d44d729830a088fccf62e74d589ce1deff87b7bdedb426a701(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7e2cad6b0c861b21d801687cbe5960e8d7ec3f25044a0506abbf27efea4ed8(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4364bd6fbde66bceb191a11aee73d85eb690dc6178d64880174f19257fc64df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ea3008ae6cefa9ae6d4d4925d7ade897c2cdba712065cade41563647b3c0d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f70a4aff23d28e6c45efad27dba0ac2b00c56791dacecd52f1399516d23b82b(
    value: typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsKendraSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e9f9f428c608583d7fb691d3413acd5d35a3668eb3849e7471960ea60e4beb(
    *,
    cross_account_model_register_role_arn: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee6323a88191ce07913492e3954cbd6c01db4ac40434213eed3d981e65a8aa2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc0fd1bad48ae339ede9bd6b983f36b070a1c7d66521e46f83e4d56c3c1884a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58f0d69dcbc008fcecfc6fb2c60d17c084ad25c6ab4b55e147280fa6f628d19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf38cc2523994f59cd888a46c443ab2811144d0df79c8bf1d1d6c62975cc4d3(
    value: typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsModelRegisterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32caf25643a9da55b393d9467b53ae401338dbf066e793469f77d75dccaba072(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f401848e47c92ed500ad2529dd0c33983c1330c643ea99d93d53f9a97b3dadb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsCanvasAppSettingsIdentityProviderOauthSettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142acff5e04e446b46d1be45aa0a9d541304fbc6c464205266252bbda3652690(
    value: typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d26f9860d63b266c957bb65edcb81099743eb007b36d2638a8d3b5719022e4f(
    *,
    amazon_forecast_role_arn: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e16e644a151eecf4c2b699bfb64168962bd886e57f2bcea292ef85596c1e143(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6e05c84ee781121509eb7d6dd76956171f3133b9bd02154051c835a1217733(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a69b9fa074c105a8f073d469834c789924a6609480d037cca06ffd84e45bd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdee85ec39618e879189772d33ff8b564ed4f7cd7c09564df30f7800feb9d41(
    value: typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59d2f666ef0d90ff1ae38cdd07987fcad93f4f63767d3c09e3a29ea98fb71cd(
    *,
    s3_artifact_path: typing.Optional[builtins.str] = None,
    s3_kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c96c8a39871c6dea6a2243e6b3456506b3f4c0ddcb61c9dbdb487bbbf6f99b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37975da0714fd32c1153d6b8e96c179a4a8892306caa326386a59f88144f81cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776ad1aa67f1b9a41bee86aadbd89ca22a219c88768333a1148c9ebfcc5c5891(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d155802e260addc32bfe6004909a22e3bcc72136534c98f004da569cbf584fe(
    value: typing.Optional[SagemakerUserProfileUserSettingsCanvasAppSettingsWorkspaceSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db048a8f3a9189bebbcb0d45ee4a8cf25d1c55d188aed6defc54cd35050a58dc(
    *,
    code_repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_resource_spec: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c5a161ff7bad6fe50a5a0287f6d594201900ef163c4ccf3794010c761bf673(
    *,
    repository_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ec8bf24f862479e8de048505b664ac709def87c3f347cc278b9aff4f489d58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02dff582f73ebc045e842aa848a8a23fcfc059add8599b7b9f93418b6786b755(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d248080d95ef3eb0992c58f811870b8b16630cc560eb9abc0d5a483faec4fc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e67c1dc5d5ebe1ff0f8a8d33c7142f52571e6af096ece262e72acded82e226(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cbc195f59dbaf44184ba22dff515ef8a00762a208d574102a2cc08246793bed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1459b5a475fa62e999b0a9bfe1e76073f70f2cfc8e6fd02dacf856f30d4fd2bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ce83295d8bbae54dbc36a5ac115dd3a496f2075c5b79cb73e43f5c7dc91116(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9fc4daca1128b6f9c4aca7584106407e8f78c77456ed60936c62a3c9a451a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44f1902cbefae0612ab33af602f921525e2c2b4b903518a36352ace538d4296(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3438b428ed79e05c9f3d9294075f5792c273929ffd55f6d0daeec85ef5e3ead(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    lifecycle_config_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696ee5abddc21cd93a701d843ee22f07b03c5b1cd876a454aaccc7a17461b6d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78341bbb361c279e579d12655e355bb6d4b60b3c910c55da6f527dd5505a442(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24aca68ec2279150c9ea49cfa15e3a285885da2f2b2cd8445d166d354bc3af90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd703f527b25f98af7032b89adac2d66ae69f3d1a01676cdb6d369a84aba4fb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1d1a15a8c16eda18181a733e09ce48218d0985d0b0374d757490bce38d9493(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7c3e4b8ec85e2844fb98d794deeb690ed503a485db066312dafbcc0715f280(
    value: typing.Optional[SagemakerUserProfileUserSettingsJupyterServerAppSettingsDefaultResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8879ec84a916cf6e71ca7fabdcb8db3d8063a6ea53bb2aa3bcdb5f2940682b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1cc428abdda3dd32a7f7b8d2d2f5fcb9a0658acfa67771426b05678585a2cd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7a2b8ec6e31dd1fe395dc9e67438a77d2fece62da9d5f41d4a54c20a5f22dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14bf9af7f3c9991425f5be3c43ef1fd363e99c2c86fdf78deaebd9d8c313b1f3(
    value: typing.Optional[SagemakerUserProfileUserSettingsJupyterServerAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d346788be069afbab298b2155eed082b16a7ec00a903e41d88612b01ddb56911(
    *,
    custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_resource_spec: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656858a678e7193fbc8df64771353adcb9254d60bd3e7885916ca84449a584b3(
    *,
    app_image_config_name: builtins.str,
    image_name: builtins.str,
    image_version_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4ccf627fafc6a473a83590771d8d4739b7b25d83f80838c81bcd6118bee415(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d6cbf1e5ccd920afb1e58627bf40632a10898eb5b80a9e72af3ab9183c9f5d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cab3eba8da8b95798aa60eae9c9b91b0c47a80c31b61320826973a9d135d769(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3faa5bcc2086a3717da0e86a48d6f7b03a1b48b2478d0f4524bd8e10fdb35b4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d20bae76ad7abc031f03482fc17251c0a3e4a9016f7fc57184cc2b54821edaa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046578c5829f6220350b3e340f48773f5f3cd0a47092d87a789844c789d5aa17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b38ba2106c27faa97d366f07eaa6be4aadf513422ba61e22e7ded02e6c46e51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fdc3288cfe9f50434faa71b18d189bcdf9dcf884361e1d63895361383bef9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7a80926db30ea49905fcbaa8c60d5db2d0e7dab46a982db6247d8061f54dac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbbc54be8642eab4aa9a58cac705c4e434cd0917c19c152f460d28f785604da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c26870973a6eea454629daf66a126ac91ddf77c55d758ca5df3afb8397965bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58596e21d298c43f57464f5f35c43627885ae62fff73bf1bb19757e8111158f0(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    lifecycle_config_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd59c2896eee144ccf2505eaa04bd48b37ac915c32fc20679364682393bf55b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac2870df50f95d2b38f90010c07b950b1c12eecd14ec42b622329a5a4e194be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134cf70572ec9741a12c5afe7697a2e774b8b8c3df17826342c396f3309e2c5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f455d6aa38f8f2fb29f138bef6dfbf10ebb638f9ffe44b17b5870d8c33e177dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c955b68b989f74df241815507692915f949450db63daa854778cb6a4652f2be6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705dff396f9a7f66e7b62c2d2735ddf6454bc02e6e0ef125eae62e5eaea47b58(
    value: typing.Optional[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsDefaultResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428f20d2d891ad1c7d7c16487ebed0c3c5d73687a4a00824fcf83e6fd467570e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081e33c22fe7551cb4052fadca2a5e55c164a23579aa3b5a541477c38c65098c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783581cf280e45dd3c675002bab68483809ed3eb23a05edd9b6917e3f436f6a4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3682d322f3ccc95304f1ebc121bdd9f16756b089d97455dcc0cdf80024ed084e(
    value: typing.Optional[SagemakerUserProfileUserSettingsKernelGatewayAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43bde5a1a592ed90c148352a0b606df4601524043ae6fbf279d2763cfc97e45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455ac88bd73f0de55ce7e280ec61889e12cbc310195fa99591e8157f895e6b0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b7adeb4444a45916ed4c2ddcbe02add4fa593ca842f1a1202f828016edcc84(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7695c4441c85f09c2fb2170af083304ba86de8e93e0bf0b37a5e96f198b814(
    value: typing.Optional[SagemakerUserProfileUserSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4faa4239c756f19f06a1dba510819647ffbfaaad43cdb98b588df561af503b(
    *,
    custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_resource_spec: typing.Optional[typing.Union[SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a4c1c83487e979d27380b75f01c4d0e198bd43ac915464143662454e2e5b7c(
    *,
    app_image_config_name: builtins.str,
    image_name: builtins.str,
    image_version_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e423b4fd31f6f108fa75595c3dd3be87f53dd3f7bfc97b8026da664531174624(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc345078e7217739b152c8e10d2ab3efa9bdafdb1138edf6a733a4ee09e72e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e0832e1d6660955869c26467f3aab9a38079082ffec3c0f5e373ea1580e4d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996d61a8a39ddcdb25a3c68857cfe73daf22c912d0eaaaf023f2f54a2c9e8326(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd6e554f82d98426f94b542710c7e216bfd98799912122806177f9c510e74b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a374a9418bf2af5a3496d4b2ac0a91dd74c1dfaf4b5704b5ac26b66188071f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834537bbf711d221502a7733e741e8fe1cc5cdc30cb2b98d0827c83c8862995c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb66384d9b01ab44f809227c91e2e5067a98a7ab2d9fd1c2bb8019c04980f62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb7a1c377cdbbf0e4eb9b5d3db36c37481f235dcbeb2158013df8b6025986ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac45a480d8ea7e8ff86ba695aca87afe998e76d6f1a7d49ff9f566c6e4b98372(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d7c10d0bf4b93f9aecd5df43002389febd774aefd672b3891dba09b991874ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc93b5d53475692f637dbfb6371280a48f4aea6979f4f565fa2cd815940456bb(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    lifecycle_config_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8a285b6dafe551fe44ff44ad5080a627b4b1c21512abc8c54392b61876e20d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2537e30b8d8a276ddde2f151735641d4d52bf1b4c14ce146897edba5b43ab7ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ec90b2251358711332595a49316a5c09f60ba2d5f55d968579689496f4ee20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359fb4360f684b6f60cbc49ca4395d6b68e3e52fcd7e985dfa14afcb603b4a62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c166f2aeef4b5e1d2e333c493249713c5abb4b267db7077e4cf1816078b8365a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485746b07ddc8bfd50b64c1d1ec1fd80f400e2fadd64a9f0350c33b78b72b478(
    value: typing.Optional[SagemakerUserProfileUserSettingsRSessionAppSettingsDefaultResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14784ffa523406abf63a571e19bd87e2404469792ce4e3a875bb2baee6871c0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ffd807fa9edfa2ca3e3d54c0e7cdc645a421c2486677e9f34ff35577f4860f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerUserProfileUserSettingsRSessionAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f21429fcf717441195b32f07eaba25ee476bb9986d1321a17be4fcc3469cc71(
    value: typing.Optional[SagemakerUserProfileUserSettingsRSessionAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511fbd1bb69cfa14aad557f8808bb107b9f43314d62925fb75021494347d1482(
    *,
    access_status: typing.Optional[builtins.str] = None,
    user_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f8af67339e32b9579fd68b2cc7593de9787bb97f68bd0516040074dd1e01c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4f95b96e9fa001f7062ae3d7af4ac5925b6300eff75045864beb828e975f5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c0fded862b3450124e40eb66a1dc6ff4f34a8e878ffcf9bb45b52a8c00d70f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d86707ec1a97e294a0fb564195ef82e1da15c13cb88fdf4f6bc31e37fa6849(
    value: typing.Optional[SagemakerUserProfileUserSettingsRStudioServerProAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270d965c9c3f9c3467fa3f02baf20ed3b0073e156eb0a5d62f32bdf45124b29a(
    *,
    notebook_output_option: typing.Optional[builtins.str] = None,
    s3_kms_key_id: typing.Optional[builtins.str] = None,
    s3_output_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce83a2903af4f5e650d1396717e8ac4e3c73e7d93cc1209d1146f9dc4f094bc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab57aedb4e0a0a391074cce2d69b1387fac12b394f0afdae02d98a77e4939057(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fda05c0bf98121d62bfc727e54e33d7477dba7c4f0972a1918138cf29cc159(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af67c2b0c967681ea3252efd41ca930a529ca31cfe54e3e3a0d96a711d3312d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9360963a9ba922f43b42d13ce3b855a8fcf01663192ae20efa46ca15feea0c30(
    value: typing.Optional[SagemakerUserProfileUserSettingsSharingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841d6fe0afb9b888766eb94edd622771fe5400a897a374118efa05bd23ec3718(
    *,
    default_resource_spec: typing.Union[SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1447df3bb793b2b43abc3eeed88652392ae9dd7e0b0415cd632034e6e1aea0f1(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    lifecycle_config_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecead6d8d13862ec8a5cb8061a5fa4a24a58c91d5ae78d0e2bd532330b609e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd1574e0e4e15ba4a03488442c97903b1442cd426390d6514ed9f6ae7caead5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43d4c2f7bdceb4e7c45fdc6e5a8ef4158b08b622d65c3ae829f309bacbdf44b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ce79b81601f22283975e555be86d3bad8298dc994c0fd8a23f44b7cc6154e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9663fef8c942acf3f16b96065778949f52ee9833c8cf13b8fa92fefce3721e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d5c20089f4579f7fc68cb919c6edf59b7dddec81659dc034106335a6a81a4c(
    value: typing.Optional[SagemakerUserProfileUserSettingsTensorBoardAppSettingsDefaultResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316ecdc041f582cc9076e950589d8afb530582495015e0b2d48301a1d2cd5613(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1e1ffd8c17cf9a9138cfffd834fa3af301e25165fd3f77772edbdc9a49ef50(
    value: typing.Optional[SagemakerUserProfileUserSettingsTensorBoardAppSettings],
) -> None:
    """Type checking stubs"""
    pass
