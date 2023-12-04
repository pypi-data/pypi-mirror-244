# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0

from ..logger import Logger
from .properties_verifier import Verifier
from .utils import Utils


class ItemInfoHandler:
    """
    This class is responsible for managing the STAC item's
    metadata. It retrieves the STAC item's automatically
    generated ID, title, and description. This class can also
    sed to override the STAC item's automatically generated ID, Title, and Description with those specified by the user.

    Args:
        logger_properties (dict): A dictionary containing the logger properties.
    """

    logger_properties: dict
    """
    A dictionary containing the logger properties. By default it sets to None.
    You can look at keys in :class:`~tds2stac.logger.Logger` class.
    """

    def __init__(self, logger_properties: dict = dict()):
        self.logger_properties = logger_properties

    def get_entity_tuples_info(
        self,
        sta_link: str,
        sta_version: str,
        entity: str,
        filter: str = "",
        requests_properties: dict = dict(),
    ):
        """
        Get the STAC item's automatically generated ID, title, and description.

        Args:
            sta_link (str): The SensorThings API link.
            sta_version (str): The SensorThings API version.
            entity (str): The SensorThings API entity.
            filter (str): The SensorThings API filter.
            requests_properties (dict): A dictionary containing the requests properties.
        """

        harvesting_vars: dict = dict()
        list_of_entity_tuples: list = []
        entity_url = f"{sta_link}/{sta_version}/{entity}?$count=true"
        if requests_properties is not None or requests_properties == dict():
            verifier = Verifier()
            requests_properties = verifier.requests_properties(
                requests_properties
            )
        validator_value = Utils(self.logger_properties).validate_sta_link(
            link=sta_link,
            version=sta_version,
            filter=filter,
            requests_properties=requests_properties,
        )
        if validator_value is False:
            return
        else:
            entity_json = Utils(
                logger_properties=self.logger_properties
            ).open_sta_entity_links(
                link=entity_url, requests_properties=requests_properties
            )
        if entity_json is not None:
            if entity_json["@iot.count"] == 0:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties[
                    "logger_msg"
                ] = f"Entity {entity} is empty."
                Logger(self.logger_properties)
                return None
            elif entity_json["@iot.count"] > 0:
                sta_link_version = f"{sta_link}/{sta_version}"
                entity_count_number = Utils(
                    self.logger_properties
                ).get_number_of_entities(
                    link=sta_link_version,
                    entity=entity,
                    filter=filter,
                    requests_properties=requests_properties,
                )
                list_of_entities_id = Utils(
                    self.logger_properties
                ).get_list_of_entities_id(
                    link=sta_link_version,
                    entity=entity,
                    filter=filter,
                    requests_properties=requests_properties,
                )
                if entity_count_number == len(list_of_entities_id):
                    for entity_index, entity_number in enumerate(
                        list_of_entities_id
                    ):
                        entity_url_by_number = (
                            f"{sta_link_version}/{entity}({entity_number})"
                        )
                        entity_json_by_number = Utils(
                            logger_properties=self.logger_properties
                        ).open_sta_entity_links(
                            entity_url_by_number,
                            requests_properties,
                        )
                        harvesting_vars["entity_id"] = Utils(
                            logger_properties=self.logger_properties
                        ).sanitize_name(str(entity_json_by_number["name"]))
                        harvesting_vars[
                            "entity_title"
                        ] = entity_json_by_number["name"]
                        if entity_json_by_number.get("description") is None:
                            harvesting_vars[
                                "entity_description"
                            ] = "This is a STAC item created by STA2STAC."
                        else:
                            harvesting_vars[
                                "entity_description"
                            ] = entity_json_by_number["description"]
                        list_of_entity_tuples.append(
                            (
                                harvesting_vars["entity_id"],
                                harvesting_vars["entity_title"],
                                harvesting_vars["entity_description"],
                            )
                        )
                else:
                    self.logger_properties["logger_level"] = "WARNING"
                    self.logger_properties[
                        "logger_msg"
                    ] = f"Entity {entity} is not complete. Check the number of entities in the given STA."
                    Logger(self.logger_properties)
                    return None
                return list_of_entity_tuples

    def get_thing_info(self, thing_json: dict):
        """
        A function to get the automatically generated ID,
        title, and description of a specific Thing.
        """
        harvesting_vars = dict()
        harvesting_vars["item_id"] = Utils(
            logger_properties=self.logger_properties
        ).sanitize_name(str(thing_json["name"]))
        harvesting_vars["item_title"] = thing_json["name"]
        if (
            thing_json.get("description") is None
            and thing_json.get("properties", {}).get("description") is None
        ):
            harvesting_vars[
                "item_description"
            ] = "This is a STAC item created by STA2STAC."
        elif (
            thing_json.get("description") is not None
            and thing_json.get("properties", {}).get("description") is None
        ):
            harvesting_vars["item_description"] = thing_json["description"]
        elif (
            thing_json.get("description") is None
            and thing_json.get("properties", {}).get("description") is not None
        ):
            harvesting_vars["item_description"] = thing_json["properties"][
                "description"
            ]
        return (
            harvesting_vars["item_id"],
            harvesting_vars["item_title"],
            harvesting_vars["item_description"],
        )

    def replace_item_info(self, thing_json: dict, item_tuples: list = list()):
        """
        A function to replace the automatically generated ID,
        title, and description of a specific Thing with those
        specified by the user.
        """
        harvesting_vars = dict()
        (
            harvesting_vars["item_id"],
            harvesting_vars["item_title"],
            harvesting_vars["item_description"],
        ) = self.get_thing_info(thing_json=thing_json)
        if (
            harvesting_vars.get("item_id") is not None
            and harvesting_vars.get("item_title") is not None
            and harvesting_vars.get("item_description") is not None
        ):
            if item_tuples is not None:
                for item_tuple in item_tuples:
                    if item_tuple[0] == harvesting_vars["item_id"]:
                        harvesting_vars["item_id"] = item_tuple[1]
                        harvesting_vars["item_title"] = item_tuple[2]
                        harvesting_vars["item_description"] = item_tuple[3]
            else:
                self.logger_properties["logger_level"] = "INFO"
                self.logger_properties[
                    "logger_msg"
                ] = "Automatic ID, Title, and Description will be considered for the current Item."
                Logger(self.logger_properties)
        else:
            self.logger_properties["logger_level"] = "WARNING"
            self.logger_properties[
                "logger_msg"
            ] = "No Item ID, Title, and Description found."
            Logger(self.logger_properties)

        return (
            harvesting_vars["item_id"],
            harvesting_vars["item_title"],
            harvesting_vars["item_description"],
        )
