import logging
from typing import Dict

import requests
import semver

import copernicus_marine_client
from copernicus_marine_client.core_functions.utils import (
    construct_query_params_for_marine_data_store_monitoring,
)

logger = logging.getLogger("copernicus_marine_root_logger")


class VersionVerifier:
    function_marine_data_store_service_mapping: dict[str, list[str]] = {
        "describe": ["mds", "mds/serverlessArco/meta"],
        "get": ["mds", "mds/serverlessNative", "mds/serverlessArco/meta"],
        "subset": ["mds", "mds/serverlessArco", "mds/serverlessArco/meta"],
    }

    @staticmethod
    def check_version_describe():
        VersionVerifier._check_version("describe")

    @staticmethod
    def check_version_get():
        VersionVerifier._check_version("get")

    @staticmethod
    def check_version_subset():
        VersionVerifier._check_version("subset")

    @staticmethod
    def _check_version(function_name: str):
        marine_data_store_versions = (
            VersionVerifier._get_client_required_versions()
        )
        client_version = copernicus_marine_client.__version__
        for (
            service
        ) in VersionVerifier.function_marine_data_store_service_mapping[
            function_name
        ]:
            required_version = marine_data_store_versions[service]
            if not semver.match(client_version, required_version):
                logger.debug(
                    f"Client version {client_version} is not compatible with "
                    f"{service}. Service needs version {required_version}."
                )
                logger.error(
                    f"Client version {client_version} is not compatible with current "
                    "backend service. Please update to the latest client version."
                )

    @staticmethod
    def _get_client_required_versions() -> Dict:
        mds_versions: dict[str, dict[str, str]] = requests.get(
            "https://stac.marine.copernicus.eu/mdsVersions.json",
            params=construct_query_params_for_marine_data_store_monitoring(),
        ).json()["clientVersions"]
        return mds_versions
