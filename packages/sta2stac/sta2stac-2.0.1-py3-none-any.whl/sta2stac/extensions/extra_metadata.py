import pystac

from ..analysers.utils import Utils
from ..logger import Logger

# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
from ..statics import constants


class ExtraMetadata:
    """
    A class to add extra metadata to the STAC items and collections.
    Args:
        logger_properties (dict): A dictionary containing the logger properties.
    """

    def __init__(self, logger_properties: dict = dict()):
        self.logger_properties = logger_properties

    def item(
        self,
        item: pystac.Item,
        extra_metadata: dict = dict(),
        harvesting_vars: dict = dict(),
    ):
        """
        Add extra metadata to the STAC item.
        """
        if extra_metadata.get("extra_metadata_file") is not None:
            extra_metadata_json = Utils(
                logger_properties=self.logger_properties
            ).open_json_file(str(extra_metadata.get("extra_metadata_file")))
            if (
                extra_metadata_json != {}
                and extra_metadata_json.get("item") is not None
            ):
                for key, value in extra_metadata_json["item"].items():
                    if key == "properties":
                        item.properties = value
                    if key == "extra_fields":
                        item.extra_fields = value
                    elif key == "providers":
                        item.common_metadata.providers = value
                    elif key == "license":
                        item.common_metadata.license = value
                    elif key == "constellation":
                        item.common_metadata.constellation = value
                    elif key == "platform":
                        item.common_metadata.platform = value
                    elif key == "instruments":
                        item.common_metadata.instruments = value
                    elif key == "gsd":
                        item.common_metadata.gsd = value
                    elif key == "providers":
                        item.common_metadata.providers = value
                    elif key == "title":
                        item.common_metadata.title = value
                    elif key == "description":
                        item.common_metadata.description = value
                    elif key == "start_datetime":
                        item.common_metadata.start_datetime = harvesting_vars[
                            "item_datetime"
                        ][0]
                    elif key == "end_datetime":
                        item.common_metadata.end_datetime = harvesting_vars[
                            "item_datetime"
                        ][1]
                    elif key == "updated":
                        item.common_metadata.updated = harvesting_vars[
                            "item_datetime"
                        ][1]
                    elif key == "created":
                        item.common_metadata.created = harvesting_vars[
                            "item_datetime"
                        ][1]

            else:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties[
                    "logger_msg"
                ] = "The `extra_metadata_file` is empty. So, the default extra metadata won't be added to the STAC item."
                Logger(self.logger_properties)
        else:
            self.logger_properties["logger_level"] = "WARNING"
            self.logger_properties[
                "logger_msg"
            ] = "The `extra_metadata_file` is not provided. So, the default extra metadata will be added to the STAC item."
            Logger(self.logger_properties)
            extra_metadata[
                "extra_metadata_file"
            ] = constants.default_extra_metadata_file
            extra_metadata_json = Utils(
                logger_properties=self.logger_properties
            ).open_json_file(str(extra_metadata.get("extra_metadata_file")))
            if (
                extra_metadata_json != {}
                and extra_metadata_json.get("item") is not None
            ):
                for key, value in extra_metadata_json["item"].items():
                    if key == "extra_fields":
                        item.extra_fields = value
                    elif key == "providers":
                        item.common_metadata.providers = value
                    elif key == "license":
                        item.common_metadata.license = value
                    elif key == "constellation":
                        item.common_metadata.constellation = value
                    elif key == "platform":
                        item.common_metadata.platform = value
                    elif key == "instruments":
                        item.common_metadata.instruments = value
                    elif key == "gsd":
                        item.common_metadata.gsd = value
                    elif key == "providers":
                        item.common_metadata.providers = value
                    elif key == "title":
                        item.common_metadata.title = value
                    elif key == "description":
                        item.common_metadata.description = value
                    elif key == "start_datetime":
                        item.common_metadata.start_datetime = harvesting_vars[
                            "item_datetime"
                        ][0]
                    elif key == "end_datetime":
                        item.common_metadata.end_datetime = harvesting_vars[
                            "item_datetime"
                        ][1]
                    elif key == "updated":
                        item.common_metadata.updated = harvesting_vars[
                            "item_datetime"
                        ][1]
                    elif key == "created":
                        item.common_metadata.created = harvesting_vars[
                            "item_datetime"
                        ][1]
            else:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties[
                    "logger_msg"
                ] = "The default `extra_metadata_file` is empty. So, the default extra metadata won't be added to the STAC item."
                Logger(self.logger_properties)

    def collection(
        self, collection: pystac.Collection, extra_metadata: dict = dict()
    ):
        """
        Add extra metadata to the STAC collection.
        """
        if extra_metadata.get("extra_metadata_file") is not None:
            extra_metadata_json = Utils(
                logger_properties=self.logger_properties
            ).open_json_file(str(extra_metadata.get("extra_metadata_file")))
            if (
                extra_metadata_json != {}
                and extra_metadata_json.get("collection") is not None
            ):
                for key, value in extra_metadata_json["collection"].items():
                    if key == "extra_fields":
                        collection.extra_fields = value
                    elif key == "keywords":
                        collection.keywords = value
                    elif key == "providers":
                        collection.providers = value
                    elif key == "license":
                        collection.license = value
            else:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties[
                    "logger_msg"
                ] = "The `extra_metadata_file` is empty. So, the default extra metadata won't be added to the STAC collection."
                Logger(self.logger_properties)
        else:
            self.logger_properties["logger_level"] = "WARNING"
            self.logger_properties[
                "logger_msg"
            ] = "The `extra_metadata_file` is not provided. So, the default extra metadata will be added to the STAC collection."
            Logger(self.logger_properties)
            extra_metadata[
                "extra_metadata_file"
            ] = constants.default_extra_metadata_file
            extra_metadata_json = Utils(
                logger_properties=self.logger_properties
            ).open_json_file(str(extra_metadata.get("extra_metadata_file")))
            if (
                extra_metadata_json != {}
                and extra_metadata_json.get("collection") is not None
            ):
                for key, value in extra_metadata_json["collection"].items():
                    if key == "extra_fields":
                        collection.extra_fields = value
                    elif key == "keywords":
                        collection.keywords = value
                    elif key == "providers":
                        collection.providers = value
                    elif key == "license":
                        collection.license = value
            else:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties[
                    "logger_msg"
                ] = "The default `extra_metadata_file` is empty. So, the default extra metadata won't be added to the STAC collection."
                Logger(self.logger_properties)
