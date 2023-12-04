# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0


from ..statics import constants


class Verifier(object):  # type: ignore
    """
    A class to refine the properties and user input values.
    """

    def asset_properties(
        self,
        asset_properties: dict,
    ):
        if asset_properties == {}:
            asset_properties["collection"] = dict()
            asset_properties["item"] = dict()
            asset_properties["item"]["thing_json"] = True
            asset_properties["item"]["all_observations_geojson"] = True
            asset_properties["item"]["all_observations_csv"] = True
        return asset_properties

    def logger_properties(
        self,
        logger_properties: dict,
    ) -> dict:
        if logger_properties == {}:
            logger_properties["logger_handler"] = "NullHandler"
        return logger_properties

    def requests_properties(
        self,
        requests_properties: dict,
    ) -> dict:
        if requests_properties == {}:
            requests_properties["auth"] = None
            requests_properties["verify"] = False
            requests_properties["timeout"] = 10
        return requests_properties

    def extra_metadata(
        self,
        extra_metadata: dict,
    ) -> dict:
        if extra_metadata == {}:
            extra_metadata["extra_metadata"] = False
            extra_metadata[
                "extra_metadata_file"
            ] = constants.default_extra_metadata_file
        return extra_metadata

    def sta_version(
        self,
        sta_version: str,
    ) -> str:
        if sta_version == "":
            sta_version = "v1.1"
        if sta_version == "1.0":
            sta_version = "v1.0"
        elif sta_version == "1.1":
            sta_version = "v1.1"
        return sta_version
