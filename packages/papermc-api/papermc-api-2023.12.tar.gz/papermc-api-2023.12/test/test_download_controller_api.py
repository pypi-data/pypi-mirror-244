# coding: utf-8

"""
    PaperMC API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from papermc_api.api.download_controller_api import DownloadControllerApi


class TestDownloadControllerApi(unittest.TestCase):
    """DownloadControllerApi unit test stubs"""

    def setUp(self) -> None:
        self.api = DownloadControllerApi()

    def tearDown(self) -> None:
        pass

    def test_download(self) -> None:
        """Test case for download

        Downloads the given file from a build's data.
        """
        pass


if __name__ == '__main__':
    unittest.main()
