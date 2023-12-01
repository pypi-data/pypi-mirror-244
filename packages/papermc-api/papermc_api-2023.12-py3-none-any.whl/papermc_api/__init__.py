# coding: utf-8

# flake8: noqa

"""
    PaperMC API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


__version__ = "2023.12"

# import apis into sdk package
from papermc_api.api.download_controller_api import DownloadControllerApi
from papermc_api.api.project_controller_api import ProjectControllerApi
from papermc_api.api.projects_controller_api import ProjectsControllerApi
from papermc_api.api.version_build_controller_api import VersionBuildControllerApi
from papermc_api.api.version_builds_controller_api import VersionBuildsControllerApi
from papermc_api.api.version_controller_api import VersionControllerApi
from papermc_api.api.version_family_builds_controller_api import VersionFamilyBuildsControllerApi
from papermc_api.api.version_family_controller_api import VersionFamilyControllerApi

# import ApiClient
from papermc_api.api_response import ApiResponse
from papermc_api.api_client import ApiClient
from papermc_api.configuration import Configuration
from papermc_api.exceptions import OpenApiException
from papermc_api.exceptions import ApiTypeError
from papermc_api.exceptions import ApiValueError
from papermc_api.exceptions import ApiKeyError
from papermc_api.exceptions import ApiAttributeError
from papermc_api.exceptions import ApiException

# import models into sdk package
from papermc_api.models.build_response import BuildResponse
from papermc_api.models.builds_response import BuildsResponse
from papermc_api.models.change import Change
from papermc_api.models.download import Download
from papermc_api.models.project_response import ProjectResponse
from papermc_api.models.projects_response import ProjectsResponse
from papermc_api.models.version_build import VersionBuild
from papermc_api.models.version_family_build import VersionFamilyBuild
from papermc_api.models.version_family_builds_response import VersionFamilyBuildsResponse
from papermc_api.models.version_family_response import VersionFamilyResponse
from papermc_api.models.version_response import VersionResponse
