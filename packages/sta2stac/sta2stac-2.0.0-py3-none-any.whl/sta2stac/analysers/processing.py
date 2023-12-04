import sys

# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
from datetime import datetime
from typing import Union

from shapely import geometry

from ..logger import Logger


class Processing:
    """
    A class to process the items attributes. For example, it
    can be used to convert the date-time to the ISO format,
    convert the bbox to the GeoJSON format, and process the
    items attributes to create the collection spatial and
    temporal extent.
    Args:
        logger_properties (dict): A dictionary containing the logger properties.
    """

    logger_properties: dict
    """
    A dictionary containing the logger properties.
    """

    def __init__(self, logger_properties: dict):
        self.logger_properties = logger_properties

    def datetime(self, date_time: str):
        """
        Convert the date-time to the ISO format.
        """
        try:
            datetime_begin = date_time.split("/")[0]
            datetime_end = date_time.split("/")[1]
            datetime_begin_formatted = datetime.strptime(
                datetime_begin, "%Y-%m-%dT%H:%M:%SZ"
            )
            datetime_end_formatted = datetime.strptime(
                datetime_end, "%Y-%m-%dT%H:%M:%SZ"
            )

            return [datetime_begin_formatted, datetime_end_formatted]
        except Exception as e:
            (
                exception_type,
                exception_value,
                exception_traceback,
            ) = sys.exc_info()
            if exception_type is not None and exception_value is not None:
                self.logger_properties["logger_level"] = "ERROR"
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not convert the date-time to the ISO format. {exception_type.__name__}: {exception_value}"
            else:
                self.logger_properties["logger_level"] = "ERROR"
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not convert the date-time to the ISO format. {e}"
            Logger(self.logger_properties)
            return None

    def geometry(self, bbox: list, geometry_type: str):
        """
        Convert the bbox to the GeoJSON format.
        """
        if geometry_type is not None and bbox is not None:
            if isinstance(geometry_type, str):
                if geometry_type == "Point":
                    try:
                        return geometry.Point(bbox[0][0], bbox[0][1])
                    except Exception as e:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = f"Could not convert the bbox to the GeoJSON format. {e}"
                        Logger(self.logger_properties)
                        return None
                elif geometry_type == "Polygon":
                    try:
                        return geometry.Polygon(bbox)
                    except Exception as e:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = f"Could not convert the bbox to the GeoJSON format. {e}"
                        Logger(self.logger_properties)
                        return None
                elif geometry_type == "LineString":
                    try:
                        return geometry.LineString(bbox)
                    except Exception as e:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = f"Could not convert the bbox to the GeoJSON format. {e}"
                        Logger(self.logger_properties)
                        return None
                elif geometry_type == "MultiPoint":
                    bbox = [[point[0], point[1]] for point in bbox]
                    try:
                        return geometry.MultiPoint(bbox)
                    except Exception as e:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = f"Could not convert the bbox to the GeoJSON format. {e}"
                        Logger(self.logger_properties)
                        return None
                elif geometry_type == "MultiPolygon":
                    try:
                        return geometry.MultiPolygon(bbox)
                    except Exception as e:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = f"Could not convert the bbox to the GeoJSON format. {e}"
                        Logger(self.logger_properties)
                        return None
                elif geometry_type == "MultiLineString":
                    try:
                        return geometry.MultiLineString(bbox)
                    except Exception as e:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = f"Could not convert the bbox to the GeoJSON format. {e}"
                        Logger(self.logger_properties)
                        return None
                else:
                    self.logger_properties["logger_level"] = "ERROR"
                    self.logger_properties[
                        "logger_msg"
                    ] = "Could not convert the bbox to the GeoJSON format. The geometry type is not valid."
                    Logger(self.logger_properties)
                    return None
            elif isinstance(geometry_type, list):
                if all(geometry == "Point" for geometry in geometry_type):
                    bbox = [[point[0], point[1]] for point in bbox]
                    try:
                        return geometry.MultiPoint(bbox)
                    except Exception as e:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = f"Could not convert the bbox to the GeoJSON format. {e}"
                        Logger(self.logger_properties)
                        return None
                elif all(geometry == "Polygon" for geometry in geometry_type):
                    try:
                        return geometry.MultiPolygon(bbox)
                    except Exception as e:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = f"Could not convert the bbox to the GeoJSON format. {e}"
                        Logger(self.logger_properties)
                        return None
                if all(geometry == "LineString" for geometry in geometry_type):
                    try:
                        return geometry.MultiLineString(bbox)
                    except Exception as e:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = f"Could not convert the bbox to the GeoJSON format. {e}"
                        Logger(self.logger_properties)
                        return None
                else:
                    self.logger_properties["logger_level"] = "ERROR"
                    self.logger_properties[
                        "logger_msg"
                    ] = "Could not convert the bbox to the GeoJSON format. The geometry type is not valid."
                    Logger(self.logger_properties)
                    return None
                try:
                    return geometry.MultiPolygon(self.bbox(bbox))
                except Exception as e:
                    self.logger_properties["logger_level"] = "ERROR"
                    self.logger_properties[
                        "logger_msg"
                    ] = f"Could not convert the bbox to the GeoJSON format. {e}"
                    Logger(self.logger_properties)
                    return None
            else:
                self.logger_properties["logger_level"] = "ERROR"
                self.logger_properties[
                    "logger_msg"
                ] = "This is not a format to convert the bbox to the GeoJSON format."
                Logger(self.logger_properties)
                return None
        elif geometry_type is None and bbox is not None:
            try:
                point = geometry.Point(bbox)
                return point
            except Exception:
                try:
                    polygon = geometry.Polygon(bbox)
                    return polygon
                except Exception:
                    try:
                        linestring = geometry.LineString(bbox)
                        return linestring
                    except Exception as e:
                        self.logger_properties["logger_level"] = "ERROR"
                        self.logger_properties[
                            "logger_msg"
                        ] = f"Could not convert the bbox to the GeoJSON format. {e}"
                        Logger(self.logger_properties)
                        return None

    def bbox(self, bbox: list, geometry: Union[str, list]):
        """
        Convert the bbox to the GeoJSON format.
        """

        if geometry is not None and bbox is not None:
            if isinstance(geometry, str):
                if geometry == "Point":
                    bbox = [[bbox[0][0], bbox[0][1]]]
                    return bbox
                else:
                    return bbox
            elif isinstance(geometry, list):
                if all(geometry == "Point" for geometry in geometry):
                    bbox = [[point[0], point[1]] for point in bbox]
                else:
                    return bbox
        elif geometry is None and bbox is not None:
            return bbox
        else:
            self.logger_properties["logger_level"] = "ERROR"
            self.logger_properties[
                "logger_msg"
            ] = "Could not convert the bbox to the GeoJSON format. The geometry type is not valid."
            Logger(self.logger_properties)
            return None

    def collection(self, date_times_list: list):
        """
        Process the items attributes to create the collection temporal extent.
        """

        date_times_list = sorted(date_times_list)
        return [date_times_list[0], date_times_list[-1]]

    def item(self, harvesting_vars: dict):
        """
        Process the items attributes to create the item temporal extent.
        """
        all_item_datetime = []
        if harvesting_vars.get("item_datetime") is not None:
            for item_datetime in harvesting_vars["item_datetime"]:
                if item_datetime is not None:
                    list_start_end_datetime = self.datetime(item_datetime)
                    if list_start_end_datetime is not None:
                        all_item_datetime.extend(list_start_end_datetime)

            all_item_datetime = sorted(all_item_datetime)
            harvesting_vars["item_datetime"] = [
                all_item_datetime[0],
                all_item_datetime[-1],
            ]
        if (
            harvesting_vars.get("item_bbox") is not None
            and harvesting_vars.get("item_geometry") is not None
        ):
            harvesting_vars["item_bbox"] = self.bbox(
                harvesting_vars["item_bbox"], harvesting_vars["item_geometry"]
            )
        return harvesting_vars
