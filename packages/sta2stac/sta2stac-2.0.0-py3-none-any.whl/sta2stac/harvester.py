# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0


from shapely import geometry

from .analysers.item_info_retriever import ItemInfoHandler
from .analysers.processing import Processing
from .analysers.utils import Utils
from .logger import Logger


class Harvester:
    """
    A class to harvest the SensorThings API attributes.
    Args:
        logger_properties (dict): A dictionary containing the logger properties.
        harvesting_vars (dict): A dictionary containing the harvesting variables.
    """

    logger_properties: dict
    """
    A dictionary containing the logger properties.
    """
    harvesting_vars: dict
    """
    A dictionary containing the harvesting variables keys.
    """

    def __init__(self, logger_properties: dict, harvesting_vars: dict):
        self.logger_properties = logger_properties
        self.harvesting_vars = harvesting_vars

    def item(
        self,
        link: str,
        version: str,
        number_of_things: int,
        requests_properties: dict,
        item_tuples: list[tuple] = [],
        datacube_extension: bool = False,
        filter: str = "",
    ):
        """
        Harvest the Things in SensorThings API as STAC-Item.
        """

        if filter is not None and filter != "":
            thing_url = f"{link}/{version}/Things({number_of_things})"
            all_observations_geojson_url = f"{link}/{version}/Observations?$filter=Datastream/Thing/id%20eq%20%27{number_of_things}%27&$resultFormat=GeoJSON"
            all_observations_dataarray_url = f"{link}/{version}/Observations?$filter=Datastream/Thing/id%20eq%20%27{number_of_things}%27&$resultFormat=DataArray"
            all_observations_csv_url = f"{link}/{version}/Observations?$filter=Datastream/Thing/id%20eq%20%27{number_of_things}%27&$resultFormat=CSV"
            datastreams_url = f"{thing_url}/Datastreams?$count=true&$top=1000"
            locations_url = f"{thing_url}/Locations?$count=true&$top=1000"
        else:
            thing_url = f"{link}/{version}/Things({number_of_things})"
            all_observations_geojson_url = f"{link}/{version}/Observations?$filter=Datastream/Thing/id%20eq%20%27{number_of_things}%27&$resultFormat=GeoJSON"
            all_observations_dataarray_url = f"{link}/{version}/Observations?$filter=Datastream/Thing/id%20eq%20%27{number_of_things}%27&$resultFormat=DataArray"
            all_observations_csv_url = f"{link}/{version}/Observations?$filter=Datastream/Thing/id%20eq%20%27{number_of_things}%27&$resultFormat=CSV"
            datastreams_url = f"{thing_url}/Datastreams?$count=true&$top=1000"
            locations_url = f"{thing_url}/Locations?$count=true&$top=1000"

        self.harvesting_vars["item_thing_url_json"] = thing_url
        self.harvesting_vars[
            "item_all_observations_geojson_url"
        ] = all_observations_geojson_url
        self.harvesting_vars[
            "item_all_observations_dataarray_url"
        ] = all_observations_dataarray_url
        self.harvesting_vars[
            "item_all_observations_csv_url"
        ] = all_observations_csv_url

        thing_json = Utils(
            logger_properties=self.logger_properties
        ).open_sta_entity_links(
            link=thing_url, requests_properties=requests_properties
        )
        datastreams_json = Utils(
            logger_properties=self.logger_properties
        ).open_sta_entity_links(
            link=datastreams_url, requests_properties=requests_properties
        )
        locations_json = Utils(
            logger_properties=self.logger_properties
        ).open_sta_entity_links(
            link=locations_url, requests_properties=requests_properties
        )

        if thing_json is not None and thing_json != {}:
            # Harvesting the STAC-Item ID, Title and Description
            # TODO: make ID, Title, and Description in a another function based on comparison of `items_tuples`

            (
                self.harvesting_vars["item_id"],
                self.harvesting_vars["item_title"],
                self.harvesting_vars["item_description"],
            ) = ItemInfoHandler(
                logger_properties=self.logger_properties
            ).replace_item_info(
                thing_json=thing_json, item_tuples=item_tuples
            )

            # Harvesting the STAC-Item Spatial and Temporal extent
            if locations_json is not None and locations_json != {}:
                if locations_json["@iot.count"] == 0:
                    self.logger_properties["logger_level"] = "WARNING"
                    self.logger_properties[
                        "logger_msg"
                    ] = "The Thing does not have any Location. So, it will look for the location in `observedArea` attribute of `Datastream`, and if it couldn't find any coordinate there, the spatial extent of the item will be None."
                    Logger(self.logger_properties)
                elif locations_json["@iot.count"] == 1:
                    if (
                        locations_json.get("value", [])[0]
                        .get("location", {})
                        .get("type")
                        is not None
                    ):
                        self.harvesting_vars["item_geometry"] = locations_json[
                            "value"
                        ][0]["location"]["type"]
                    else:
                        self.logger_properties["logger_level"] = "WARNING"
                        self.logger_properties[
                            "logger_msg"
                        ] = "The Location of the Thing does not have any geometry type. So, it will look for the location in `observedArea` attribute of Datastream, and if it couldn't find any geometry there, the geometry of the item will be None."
                        Logger(self.logger_properties)
                    if (
                        locations_json.get("value", [])[0]
                        .get("location", {})
                        .get("coordinates")
                        is not None
                    ):
                        self.harvesting_vars["item_bbox"] = [
                            locations_json["value"][0]["location"][
                                "coordinates"
                            ]
                        ]
                    else:
                        self.logger_properties["logger_level"] = "WARNING"
                        self.logger_properties[
                            "logger_msg"
                        ] = "The Location of the Thing does not have any coordinates. So, it will look for the location in `observedArea` attribute of Datastream, and if it couldn't find any coordinate there, the spatial extent of the item will be None."
                        Logger(self.logger_properties)
                elif locations_json["@iot.count"] > 1:
                    geometry_list = []
                    bbox_list = []
                    locations_number = Utils(
                        self.logger_properties
                    ).get_number_of_entities(
                        link=thing_url,
                        entity="Locations",
                        filter=filter,
                        requests_properties=requests_properties,
                    )
                    list_of_locations_id = Utils(
                        self.logger_properties
                    ).get_list_of_entities_id(
                        link=thing_url,
                        entity="Locations",
                        filter=filter,
                        requests_properties=requests_properties,
                    )
                    if locations_number == len(list_of_locations_id):
                        for location_index, location_number in enumerate(
                            list_of_locations_id
                        ):
                            locations_url_by_number = (
                                f"{thing_url}/Locations({location_number})"
                            )
                            locations_json_by_number = Utils(
                                logger_properties=self.logger_properties
                            ).open_sta_entity_links(
                                locations_url_by_number,
                                requests_properties,
                            )
                            if (
                                locations_json_by_number.get(
                                    "location", {}
                                ).get("type")
                                is not None
                            ):
                                geometry_list.append(
                                    locations_json_by_number["location"][
                                        "type"
                                    ]
                                )
                            else:
                                self.logger_properties[
                                    "logger_level"
                                ] = "WARNING"
                                self.logger_properties[
                                    "logger_msg"
                                ] = "The Location of the Thing does not have any geometry type in the list of locations. So, it will look for the location in `observedArea` attribute of Datastream, and if it couldn't find any geometry there, the geometry of the item will be None."
                                Logger(self.logger_properties)
                            if (
                                locations_json_by_number.get(
                                    "location", {}
                                ).get("coordinates")
                                is not None
                            ):
                                bbox_list.append(
                                    locations_json_by_number["location"][
                                        "coordinates"
                                    ]
                                )
                            else:
                                self.logger_properties[
                                    "logger_level"
                                ] = "ERROR"
                                self.logger_properties[
                                    "logger_msg"
                                ] = "The Location of the Thing does not have any geometry type in the list of locations. So, it will look for the location in `observedArea` attribute of Datastream, and if it couldn't find any coordinate there, the spatial extent of the item will be None."
                                Logger(self.logger_properties)
                    else:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = "The number of Locations in the Thing is not equal to the number of Locations in the list of locations. So, it will look for the location in `observedArea` attribute of Datastream, and if it couldn't find any geometry there, the geometry of the item will be None."
                        Logger(self.logger_properties)
                    if self.harvesting_vars.get("item_geometry") is None:
                        self.harvesting_vars["item_geometry"] = geometry_list
                    if self.harvesting_vars.get("item_bbox") is None:
                        self.harvesting_vars["item_bbox"] = bbox_list

            if datastreams_json is not None and datastreams_json != {}:
                # Harvesting the STAC-Item Spatial and Temporal extent, Variable names, dimensions, description and units. Dimension names are lat, long and time.
                if datastreams_json["@iot.count"] == 0:
                    if self.harvesting_vars["item_bbox"] is None:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = "The Thing does not have any Datastream. So, there is no temporal and spatial extent for the item."
                        Logger(self.logger_properties)
                        return
                    else:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = "The Thing does not have any Datastream. So, there is no temporal extent for the item."
                        Logger(self.logger_properties)
                        return
                elif datastreams_json["@iot.count"] == 1:
                    if datastreams_json.get("observedArea") is not None:
                        if (
                            datastreams_json["observedArea"].get("type")
                            is not None
                            and self.harvesting_vars["item_geometry"] is None
                        ):
                            self.harvesting_vars[
                                "item_geometry"
                            ] = datastreams_json["observedArea"]["type"]
                        elif (
                            datastreams_json["observedArea"].get("type")
                            is None
                            and self.harvesting_vars["item_geometry"] is None
                        ):
                            self.logger_properties["logger_level"] = "WARNING"
                            self.logger_properties[
                                "logger_msg"
                            ] = "The Datastream does not have any geometry type. It tries to find out the geometry type automatically."
                            Logger(self.logger_properties)
                        if (
                            datastreams_json["observedArea"].get("coordinates")
                            is not None
                            and self.harvesting_vars["item_bbox"] is None
                        ):
                            self.harvesting_vars["item_bbox"] = [
                                datastreams_json["observedArea"]["coordinates"]
                            ]
                        elif (
                            datastreams_json["observedArea"].get("coordinates")
                            is None
                            and self.harvesting_vars["item_bbox"] is None
                        ):
                            self.logger_properties["logger_level"] = "ERROR"
                            self.logger_properties[
                                "logger_msg"
                            ] = "The Datastream does not have any coordinates. So, the spatial extent of the item will be None."
                            Logger(self.logger_properties)
                            return
                    else:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = "The Datastream does not have any observedArea. So, the spatial extent of the item will be None."
                        Logger(self.logger_properties)
                        return

                    if (
                        datastreams_json.get("name") is not None
                        and datacube_extension is True
                    ):
                        self.harvesting_vars["item_variable_names"] = [
                            datastreams_json["name"]
                        ]

                    if (
                        datastreams_json.get("description") is not None
                        and datacube_extension is True
                    ):
                        self.harvesting_vars["item_variable_descriptions"] = [
                            datastreams_json["description"]
                        ]

                    if (
                        datastreams_json.get("unitOfMeasurement") is not None
                        and datacube_extension is True
                    ):
                        self.harvesting_vars["item_variable_units"] = [
                            datastreams_json["unitOfMeasurement"]["name"]
                        ]

                    if (
                        datastreams_json.get("phenomenonTime") is not None
                        and datastreams_json.get("observedArea") is not None
                        and datacube_extension is True
                    ):
                        self.harvesting_vars["item_variable_dimensions"] = [
                            ["lat", "long", "time"]
                        ]
                        self.harvesting_vars["item_dimension_names"] = [
                            "lat",
                            "long",
                            "time",
                        ]
                    elif (
                        datastreams_json.get("phenomenonTime") is not None
                        and datastreams_json.get("observedArea") is None
                        and datacube_extension is True
                    ):
                        self.harvesting_vars["item_variable_dimensions"] = [
                            ["time"]
                        ]
                        self.harvesting_vars["item_dimension_names"] = ["time"]
                    elif (
                        datastreams_json.get("phenomenonTime") is None
                        and datastreams_json.get("observedArea") is not None
                        and datacube_extension is True
                    ):
                        self.harvesting_vars["item_variable_dimensions"] = [
                            ["lat", "long"]
                        ]
                        self.harvesting_vars["item_dimension_names"] = [
                            "lat",
                            "long",
                        ]
                    else:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = "The Datastream does not have any dimensions. So, it cannot attach datacube extension to the item."
                        Logger(self.logger_properties)
                        return

                    if datastreams_json.get("phenomenonTime") is not None:
                        self.harvesting_vars[
                            "item_datetime"
                        ] = datastreams_json["phenomenonTime"]
                    else:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = "The Datastream does not have any phenomenonTime. So, the temporal extent of the item will be None."
                        Logger(self.logger_properties)
                        return
                elif datastreams_json["@iot.count"] > 1:
                    geometry_list = []
                    bbox_list = []
                    datetime_list = []
                    variable_names_list = []
                    variable_descriptions_list = []
                    variable_units_list = []
                    variable_dimensions_list = []
                    dimension_names_list = []
                    datastreams_number = Utils(
                        self.logger_properties
                    ).get_number_of_entities(
                        link=thing_url,
                        entity="Datastreams",
                        filter=filter,
                        requests_properties=requests_properties,
                    )
                    list_of_datastreams_id = Utils(
                        self.logger_properties
                    ).get_list_of_entities_id(
                        link=thing_url,
                        entity="Datastreams",
                        filter=filter,
                        requests_properties=requests_properties,
                    )
                    if datastreams_number == len(list_of_datastreams_id):
                        for datastream_index, datastream_number in enumerate(
                            list_of_datastreams_id
                        ):
                            datastreams_url_by_number = (
                                f"{thing_url}/Datastreams({datastream_number})"
                            )
                            datastreams_json_by_number = Utils(
                                logger_properties=self.logger_properties
                            ).open_sta_entity_links(
                                link=datastreams_url_by_number,
                                requests_properties=requests_properties,
                            )
                            if (
                                datastreams_json_by_number.get("observedArea")
                                is not None
                            ):
                                if (
                                    datastreams_json_by_number.get(
                                        "observedArea", {}
                                    ).get("type")
                                    is not None
                                    and self.harvesting_vars.get(
                                        "item_geometry"
                                    )
                                    is None
                                ):
                                    geometry_list.append(
                                        datastreams_json_by_number[
                                            "observedArea"
                                        ]["type"]
                                    )
                                elif (
                                    datastreams_json_by_number.get(
                                        "observedArea", {}
                                    ).get("type")
                                    is None
                                    and self.harvesting_vars["item_geometry"]
                                    is None
                                ):
                                    self.logger_properties[
                                        "logger_level"
                                    ] = "WARNING"
                                    self.logger_properties[
                                        "logger_msg"
                                    ] = "The Datastream does not have any geometry type. It tries to find out the geometry type automatically."
                                    Logger(self.logger_properties)
                                if (
                                    datastreams_json_by_number.get(
                                        "observedArea", {}
                                    ).get("coordinates")
                                    is not None
                                    and self.harvesting_vars.get("item_bbox")
                                    is None
                                ):
                                    bbox_list.append(
                                        datastreams_json_by_number[
                                            "observedArea"
                                        ]["coordinates"]
                                    )
                                elif (
                                    datastreams_json_by_number.get(
                                        "observedArea", {}
                                    ).get("coordinates")
                                    is None
                                    and self.harvesting_vars.get("item_bbox")
                                    is None
                                ):
                                    self.logger_properties[
                                        "logger_level"
                                    ] = "WARNING"
                                    self.logger_properties[
                                        "logger_msg"
                                    ] = "The Datastream does not have any coordinates. So, the spatial extent of the item will be None."
                                    Logger(self.logger_properties)
                            else:
                                self.logger_properties[
                                    "logger_level"
                                ] = "WARNING"
                                self.logger_properties[
                                    "logger_msg"
                                ] = "The Datastream does not have any observedArea. So, the spatial extent of the item will be None."
                                Logger(self.logger_properties)

                            if (
                                datastreams_json_by_number.get("name")
                                is not None
                                and datacube_extension is True
                            ):
                                variable_names_list.append(
                                    datastreams_json_by_number["name"]
                                )
                            if (
                                datastreams_json_by_number.get("description")
                                is not None
                                and datacube_extension is True
                            ):
                                variable_descriptions_list.append(
                                    datastreams_json_by_number["description"]
                                )

                            if (
                                datastreams_json_by_number.get(
                                    "unitOfMeasurement"
                                )
                                is not None
                                and datacube_extension is True
                            ):
                                variable_units_list.append(
                                    datastreams_json_by_number[
                                        "unitOfMeasurement"
                                    ]["name"]
                                )
                            # TODO: We need to refactor this condition. Because in TS data we have one time dimension.
                            if (
                                datastreams_json_by_number.get(
                                    "phenomenonTime"
                                )
                                is not None
                                and datastreams_json_by_number.get(
                                    "observedArea"
                                )
                                is not None
                                and datacube_extension is True
                            ):
                                variable_dimensions_list.append(
                                    ["lat", "long", "time"]
                                )
                                dimension_names_list.append(
                                    ["lat", "long", "time"]
                                )
                            elif (
                                datastreams_json_by_number.get(
                                    "phenomenonTime"
                                )
                                is not None
                                and datastreams_json_by_number.get(
                                    "observedArea"
                                )
                                is None
                                and datacube_extension is True
                            ):
                                variable_dimensions_list.append(["time"])
                                dimension_names_list.append(["time"])
                            elif (
                                datastreams_json_by_number.get(
                                    "phenomenonTime"
                                )
                                is None
                                and datastreams_json_by_number.get(
                                    "observedArea"
                                )
                                is not None
                                and datacube_extension is True
                            ):
                                variable_dimensions_list.append(
                                    ["lat", "long"]
                                )
                                dimension_names_list.append(["lat", "long"])
                            elif (
                                datastreams_json_by_number.get(
                                    "phenomenonTime"
                                )
                                is None
                                and datastreams_json_by_number.get(
                                    "observedArea"
                                )
                                is None
                                and datacube_extension is True
                            ):
                                self.logger_properties[
                                    "logger_level"
                                ] = "WARNING"
                                self.logger_properties[
                                    "logger_msg"
                                ] = "The Datastream does not have any dimensions."
                                dimension_names_list.append(["time"])
                                variable_dimensions_list.append(["time"])
                                Logger(self.logger_properties)
                            if (
                                datastreams_json_by_number.get(
                                    "phenomenonTime"
                                )
                                is not None
                                and self.harvesting_vars.get("item_datetime")
                                is None
                            ):
                                datetime_list.append(
                                    datastreams_json_by_number[
                                        "phenomenonTime"
                                    ]
                                )
                            else:
                                datetime_list.append(None)
                                self.logger_properties[
                                    "logger_level"
                                ] = "WARNING"
                                self.logger_properties[
                                    "logger_msg"
                                ] = "The Datastream does not have any phenomenonTime. So, the temporal extent of the item will be None."
                                Logger(self.logger_properties)
                    else:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = "The number of Locations in the Thing is not equal to the number of Locations in the list of locations. So, it will look for the location in `observedArea` attribute of Datastream, and if it couldn't find any geometry there, the geometry of the item will be None."
                        Logger(self.logger_properties)
                        return

                    if self.harvesting_vars.get("item_geometry") is None:
                        self.harvesting_vars["item_geometry"] = geometry_list
                    if self.harvesting_vars.get("item_bbox") is None:
                        self.harvesting_vars["item_bbox"] = bbox_list
                    if self.harvesting_vars.get("item_datetime") is None:
                        self.harvesting_vars["item_datetime"] = datetime_list
                    if (
                        self.harvesting_vars.get("item_variable_names") is None
                        or self.harvesting_vars.get("item_variable_names")
                        == []
                    ):
                        self.harvesting_vars[
                            "item_variable_names"
                        ] = variable_names_list
                        for var in variable_names_list:
                            if filter is not None and filter != "":
                                self.harvesting_vars[
                                    "sta2stac_thing_variable_geojson_" + var
                                ] = f"{link}/{version}/Observations?$filter=Datastream/name%20eq%20%27{var}%27&$resultFormat=GeoJSON&{filter}"
                                self.harvesting_vars[
                                    "sta2stac_thing_variable_csv_" + var
                                ] = f"{link}/{version}/Observations?$filter=Datastream/name%20eq%20%27{var}%27&$resultFormat=CSV&{filter}"
                                self.harvesting_vars[
                                    "sta2stac_thing_variable_dataarray_" + var
                                ] = f"{link}/{version}/Observations?$filter=Datastream/name%20eq%20%27{var}%27&$resultFormat=DataArray&{filter}"
                            else:
                                self.harvesting_vars[
                                    "sta2stac_thing_variable_geojson_" + var
                                ] = f"{link}/{version}/Observations?$filter=Datastream/name%20eq%20%27{var}%27&$resultFormat=GeoJSON"
                                self.harvesting_vars[
                                    "sta2stac_thing_variable_csv_" + var
                                ] = f"{link}/{version}/Observations?$filter=Datastream/name%20eq%20%27{var}%27&$resultFormat=CSV"
                                self.harvesting_vars[
                                    "sta2stac_thing_variable_dataarray_" + var
                                ] = f"{link}/{version}/Observations?$filter=Datastream/name%20eq%20%27{var}%27&$resultFormat=DataArray"

                    if (
                        self.harvesting_vars.get("item_variable_descriptions")
                        is None
                        or self.harvesting_vars.get(
                            "item_variable_descriptions"
                        )
                        == []
                    ):
                        self.harvesting_vars[
                            "item_variable_descriptions"
                        ] = variable_descriptions_list
                    if (
                        self.harvesting_vars.get("item_variable_units") is None
                        or self.harvesting_vars.get("item_variable_units")
                        == []
                    ):
                        self.harvesting_vars[
                            "item_variable_units"
                        ] = variable_units_list
                    if (
                        self.harvesting_vars.get("item_variable_dimensions")
                        is None
                        or self.harvesting_vars.get("item_variable_dimensions")
                        == []
                    ):
                        self.harvesting_vars[
                            "item_variable_dimensions"
                        ] = variable_dimensions_list
                    if (
                        self.harvesting_vars.get("item_dimension_names")
                        is None
                        or self.harvesting_vars.get("item_dimension_names")
                        == []
                    ):
                        self.harvesting_vars[
                            "item_dimension_names"
                        ] = dimension_names_list

            self.harvesting_vars["item_footprint"] = Processing(
                self.logger_properties
            ).geometry(
                self.harvesting_vars["item_bbox"],
                self.harvesting_vars["item_geometry"],
            )
            if self.harvesting_vars.get("collection_footprint") is None:
                self.harvesting_vars[
                    "collection_footprint"
                ] = self.harvesting_vars["item_footprint"]
            Processing(logger_properties=self.logger_properties).item(
                self.harvesting_vars
            )
            self.harvesting_vars["collection_footprint"] = geometry.shape(
                self.harvesting_vars["item_footprint"]
            ).union(
                geometry.shape(self.harvesting_vars["collection_footprint"])
            )
            self.harvesting_vars["collection_bbox"] = list(
                self.harvesting_vars["collection_footprint"].bounds
            )
            if self.harvesting_vars.get("collection_datetime") is None:
                self.harvesting_vars["collection_datetime"] = []
            self.harvesting_vars["collection_datetime"].extend(
                self.harvesting_vars["item_datetime"]
            )
            # To arrange datetime and bbox

        return self.harvesting_vars
