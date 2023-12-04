# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0

import json
import sys

import requests

from ..logger import Logger


class Utils:
    """
    This is a utility class that contains some useful methods.
    For example, it can be used to open a JSON file, validate
    the STA link, get the number of entities, get the list of
    entities, and sanitize the name.

    Args:
        logger_properties (dict): A dictionary containing the logger properties.
    """

    logger_properties: dict
    """
    A dictionary containing the logger properties. By default it sets to None.
    """

    def __init__(self, logger_properties: dict = dict()):
        self.logger_properties = logger_properties

    def validate_sta_link(
        self,
        link: str,
        version: str,
        filter: str = "",
        requests_properties: dict = dict(),
    ):
        """
        Validate the SensorThings API link.
        """
        try:
            if filter != "" and filter is not None:
                response = requests.get(
                    link + "/" + version,
                    verify=requests_properties["verify"],
                    timeout=requests_properties["timeout"],
                    auth=requests_properties["auth"],
                )
            else:
                response = requests.get(
                    link + "/" + version,
                    verify=requests_properties["verify"],
                    timeout=requests_properties["timeout"],
                    auth=requests_properties["auth"],
                )
            if response.status_code == 200:
                self.logger_properties["logger_level"] = "INFO"
                self.logger_properties["logger_msg"] = "The STA link is valid!"
                Logger(self.logger_properties)
                return True
            else:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties[
                    "logger_msg"
                ] = "The STA link is not valid! Please check it. %s : %s" % (
                    response.status_code,
                    response.reason,
                )
                Logger(self.logger_properties)
                return False
        except Exception:
            ex_type, ex_value, ex_traceback = sys.exc_info()

            self.logger_properties["logger_level"] = "ERROR"
            if ex_type is not None and ex_value is not None:
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not connect to {link}/{version}. %s: %s" % (
                    ex_type.__name__,
                    ex_value,
                )
            else:
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not connect to {link}/{version}."
            Logger(self.logger_properties)
            return False

    def get_number_of_entities(
        self,
        link: str,
        entity: str,
        filter: str = "",
        requests_properties: dict = dict(),
    ) -> int:
        """
        Get the number of Things in the SensorThings API.
        """
        url = f"{link}/{entity}?$count=true"
        try:
            if filter != "" and filter is not None:
                response = requests.get(
                    url,
                    verify=requests_properties["verify"],
                    timeout=requests_properties["timeout"],
                    auth=requests_properties["auth"],
                )
            else:
                response = requests.get(
                    url,
                    verify=requests_properties["verify"],
                    timeout=requests_properties["timeout"],
                    auth=requests_properties["auth"],
                )

            if response.status_code == 200:
                return response.json()["@iot.count"]
            else:
                if response.json()["@iot.count"] != 0:
                    self.logger_properties["logger_level"] = "ERROR"
                    self.logger_properties[
                        "logger_msg"
                    ] = f"It could get the number of Things in {link} but with {response.status_code} HTTP reponse : {response.reason}"
                    Logger(self.logger_properties)
                    return response.json()["@iot.count"]
                else:
                    self.logger_properties["logger_level"] = "ERROR"
                    self.logger_properties[
                        "logger_msg"
                    ] = f"Could not get the number of Things in {link}. {response.status_code} : {response.reason}"
                    Logger(self.logger_properties)
                    return 0
        except Exception:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            self.logger_properties["logger_level"] = "ERROR"
            if ex_type is not None and ex_value is not None:
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not get the number of Things in {link}. %s: %s" % (
                    ex_type.__name__,
                    ex_value,
                )
            else:
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not get the number of Things in {link}."
            Logger(self.logger_properties)
            return 0

    def get_list_of_entities_id(
        self,
        link: str,
        entity: str,
        filter: str = "",
        requests_properties: dict = dict(),
    ) -> list:
        """
        Get the list of Things in the SensorThings API.
        """
        final_list = []
        for i in range(
            0,
            self.get_number_of_entities(
                link=link,
                entity=entity,
                filter=filter,
                requests_properties=requests_properties,
            ),
            100,
        ):
            url = f"{link}/{entity}?$count=true&$top=100&$skip={i}&$select=%40iot.id&$orderby=%40iot.id+asc"
            try:
                if filter != "" and filter is not None:
                    response = requests.get(
                        url,
                        verify=requests_properties["verify"],
                        timeout=requests_properties["timeout"],
                        auth=requests_properties["auth"],
                    )
                else:
                    response = requests.get(
                        url,
                        verify=requests_properties["verify"],
                        timeout=requests_properties["timeout"],
                        auth=requests_properties["auth"],
                    )
                if response.status_code == 200:
                    iot_ids = [
                        item["@iot.id"] for item in response.json()["value"]
                    ]
                    final_list.extend(iot_ids)
                else:
                    self.logger_properties["logger_level"] = "ERROR"
                    self.logger_properties[
                        "logger_msg"
                    ] = f"Could not get the list of Things in {url}. {response.status_code} : {response.reason}"
                    Logger(self.logger_properties)

            except Exception:
                ex_type, ex_value, ex_traceback = sys.exc_info()
                self.logger_properties["logger_level"] = "ERROR"
                if ex_type is not None and ex_value is not None:
                    self.logger_properties["logger_msg"] = (
                        f"Could not get the list of Things in {url}. %s: %s"
                        % (ex_type.__name__, ex_value)
                    )
                else:
                    self.logger_properties[
                        "logger_msg"
                    ] = f"Could not get the list of Things in {url}."
                Logger(self.logger_properties)

        return final_list

    def open_sta_entity_links(
        self, link: str, requests_properties: dict = dict()
    ) -> dict:
        """
        Open the SensorThings API entity.
        """

        try:
            response = requests.get(
                link,
                verify=requests_properties["verify"],
                timeout=requests_properties["timeout"],
                auth=requests_properties["auth"],
            )
            if response.status_code == 200:
                return response.json()
            else:
                self.logger_properties["logger_level"] = "ERROR"
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not open {link}. {response.status_code} : {response.reason}"
                Logger(self.logger_properties)
                return {}
        except Exception:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            self.logger_properties["logger_level"] = "ERROR"
            if ex_type is not None and ex_value is not None:
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not open {link}. %s: %s" % (
                    ex_type.__name__,
                    ex_value,
                )
            else:
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not open {link}."
            Logger(self.logger_properties)
            return {}

    def sanitize_name(self, string: str) -> str:
        """
        Making the STAC ID with hyphens.
        """
        return (
            string.replace(" ", "-")
            .replace("/", "-")
            .replace("\\", "-")
            .replace(":", "-")
            .replace("*", "-")
            .replace("?", "-")
            .replace('"', "-")
            .replace("<", "-")
            .replace(">", "-")
            .replace("|", "-")
        )

    def open_json_file(self, file_path: str) -> dict:
        """
        Open the JSON file.
        """
        try:
            loaded_json = json.load(open(file_path))
            return loaded_json

        except Exception:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            self.logger_properties["logger_level"] = "ERROR"
            if ex_type is not None and ex_value is not None:
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not open {file_path}. %s: %s" % (
                    ex_type.__name__,
                    ex_value,
                )
            else:
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not open {file_path}."
            Logger(self.logger_properties)
            return {}
