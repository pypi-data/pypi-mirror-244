# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
import pystac
from pystac.extensions.datacube import (
    DatacubeExtension,
    Dimension,
    DimensionType,
    Variable,
    VariableType,
)

from ..logger import Logger


class Datacube:
    """
    This is a class for adding datacube extension to the STAC item.
    Args:
        logger_properties (dict): A dictionary containing the logger properties.
    """

    logger_properties: dict
    """
    A dictionary containing the logger properties. By default it sets to None.
    """

    def __init__(self, logger_properties: dict = dict()):
        self.logger_properties = logger_properties

    def item(self, item: pystac.Item, harvesting_vars: dict = dict()):
        """
        Add datacube extension to the STAC item.
        Args:
            item (pystac.Item): A STAC item.
            harvesting_vars (dict): A dictionary containing the harvesting variables.
        """

        variables = (
            {}
        )  # variables dictionary for gathering the Variable objects
        dimensions: dict = (
            {}
        )  # dimensions dictionary for gathering the Dimension objects
        cube = DatacubeExtension.ext(item, add_if_missing=True)

        variable_dimensions = harvesting_vars["item_variable_dimensions"]
        if len(harvesting_vars["item_variable_names"]) != len(
            variable_dimensions
        ):
            # Another solution for this is to index each output element and find the None values to decide about them later
            self.logger_properties["logger_level"] = "ERROR"
            self.logger_properties[
                "logger_msg"
            ] = "The length of the variable list and the dimension list are not equal. Check your data in STA."
        else:
            for i, v in enumerate(harvesting_vars["item_variable_names"]):
                variable_dict = dict()
                # forth case is when description is not available or is less than then variable ids or dimensions. It's not required then can be ignored
                # Usually every varialbe in ncML has name and shape attrs that it can be used as variable id and dimension.
                variable_dict["dimensions"] = variable_dimensions[i]
                variable_dict["type"] = VariableType.DATA.value
                if (
                    harvesting_vars["item_variable_descriptions"] is not None
                    and len(harvesting_vars["item_variable_names"])
                    == len(harvesting_vars["item_variable_descriptions"])
                    and len(harvesting_vars["item_variable_descriptions"])
                    != harvesting_vars["item_variable_descriptions"].count(
                        None
                    )
                ):
                    if (
                        harvesting_vars["item_variable_descriptions"][i]
                        is not None
                    ):
                        variable_dict["description"] = harvesting_vars[
                            "item_variable_descriptions"
                        ][i]
                variable_dict["dimensions"] = variable_dimensions[i]
                if (
                    harvesting_vars["item_variable_units"] is not None
                    and len(harvesting_vars["item_variable_units"])
                    == len(variable_dimensions)
                    and len(harvesting_vars["item_variable_units"])
                    != harvesting_vars["item_variable_units"].count(None)
                ):
                    if harvesting_vars["item_variable_units"][i] is not None:
                        variable_dict["units"] = harvesting_vars[
                            "item_variable_units"
                        ][i]
                variables[
                    harvesting_vars["item_variable_names"][i]
                ] = Variable(variable_dict)

        # Temporal Dimension
        list_of_required_keys = [
            "item_datetime",
        ]
        if all(
            harvesting_vars.get(key) is not None
            for key in list_of_required_keys
        ):
            temporal_dict = dict()
            harvesting_vars["item_datetime_str"] = [
                datetime_elem.strftime("%Y-%m-%dT%H:%M:%SZ")
                for datetime_elem in harvesting_vars["item_datetime"]
            ]
            temporal_dict = {
                "type": DimensionType.TEMPORAL.value,
                "description": "time dimension",
                "extent": harvesting_vars["item_datetime_str"],
            }
            dimensions["time"] = Dimension(temporal_dict)
        else:
            self.logger_properties["logger_level"] = "ERROR"
            self.logger_properties[
                "logger_msg"
            ] = "Required attributes are not involved in the output dictionary. Check your TS data in STA. "
            Logger(self.logger_properties)

        cube.apply(dimensions=dimensions, variables=variables)
