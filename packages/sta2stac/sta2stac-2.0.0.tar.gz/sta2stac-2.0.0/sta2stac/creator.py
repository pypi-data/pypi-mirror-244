# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0

import sys
from datetime import datetime

import pystac
from shapely import geometry

from .analysers.existence_validator import ExistenceValidator
from .analysers.processing import Processing
from .assets import Assets
from .extensions.datacube import Datacube
from .extensions.extra_metadata import ExtraMetadata
from .logger import Logger


class Creator:
    """
    A class to create the STAC-Catalog, STAC-Collection, and STAC-Item.
    Args:
        logger_properties (dict): A dictionary of logger properties.
    """

    def __init__(self, logger_properties: dict):
        self.logger_properties = logger_properties

    def STACCatalog(
        self,
        sta_link: str,
        stac_id: str,
        stac_title: str,
        stac_description: str,
        stac_dir: str,
        default_catalog_name: str = "catalog.json",
        stac_existance_catalog: bool = False,
    ):
        """
        Create the STAC-Catalog.
        """
        catalog: dict = dict()
        if stac_description is None:
            stac_description = "This is a STAC catalog created by STA2STAC."

        # In the following if condition we are going to create a new STAC catalog or use the existed one.
        if stac_existance_catalog is True:
            if stac_dir is None:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties[
                    "logger_msg"
                ] = "You have turned on the `stac_existance`, so please provide the directory of the existed STAC catalog"
                Logger(self.logger_properties)
                return
            else:
                if (
                    ExistenceValidator(
                        stac_dir, default_catalog_name, self.logger_properties
                    ).existance
                    is True
                ):
                    self.logger_properties["logger_level"] = "INFO"
                    self.logger_properties[
                        "logger_msg"
                    ] = "The STAC catalog already exists in the directory. So, it will be used"
                    Logger(self.logger_properties)
                    id_catalog = pystac.Catalog.from_file(
                        stac_dir + "/" + default_catalog_name
                    ).id
                    catalog[id_catalog] = pystac.Catalog.from_file(
                        stac_dir + "/" + default_catalog_name
                    )
                else:
                    self.logger_properties["logger_level"] = "INFO"
                    self.logger_properties[
                        "logger_msg"
                    ] = "The STAC catalog does not exist in the directory. So, a new one will be created"
                    Logger(self.logger_properties)
                    id_catalog = stac_id + " Catalog"
                    catalog[id_catalog] = pystac.Catalog(
                        id=stac_id,
                        title=stac_title,
                        description="["
                        + stac_description
                        + "]("
                        + str(sta_link)
                        + ")",
                    )
        else:
            self.logger_properties["logger_level"] = "INFO"
            self.logger_properties[
                "logger_msg"
            ] = "It creates a new catalog in the directory"
            Logger(self.logger_properties)
            id_catalog = stac_id + "-catalog"
            catalog[id_catalog] = pystac.Catalog(
                id=stac_id,
                title=stac_title,
                description="["
                + stac_description
                + "]("
                + str(sta_link)
                + ")",
            )
        return catalog[id_catalog]

    def STACCollection(
        self,
        stac_id: str,
        stac_title: str,
        stac_description: str,
        harvesting_vars: dict,
        stac_existance_collection: bool,
        extra_metadata: dict = dict(),
        asset_properties: dict = dict(),
    ):
        """
        Create the STAC-Collection.
        """
        collection: pystac.Collection = pystac.Collection(
            id="stac_id",
            extent=pystac.Extent(
                spatial=pystac.SpatialExtent(bboxes=[0.0, 0.0]),
                temporal=pystac.TemporalExtent(
                    intervals=[[datetime.utcnow(), datetime.utcnow()]]
                ),
            ),
            description="stac_description",
        )
        existed_items_id_list = []
        if stac_existance_collection is True:
            existed_collections_id_list = []
            existed_collections_id_list = [
                existence_collection.id
                for existence_collection in list(
                    harvesting_vars["catalog"].get_collections()
                )
            ]
            if (
                collection is not None
                and stac_id in existed_collections_id_list
            ):
                collection = harvesting_vars["catalog"].get_child(stac_id)
                existed_items_id_list = [
                    existed_item.id
                    for existed_item in list(collection.get_items())
                ]
            else:
                # Defining a None Spatial and Temporal extent for the collection
                if stac_description is None:
                    stac_description = (
                        "This is a STAC collection created by STA2STAC."
                    )
                collection = pystac.Collection(
                    id=stac_id,
                    title=stac_title,
                    extent=pystac.Extent(
                        spatial=pystac.SpatialExtent(bboxes=[0.0, 0.0]),
                        temporal=pystac.TemporalExtent(
                            intervals=[[datetime.utcnow(), datetime.utcnow()]]
                        ),
                    ),
                    description=stac_description,
                )
        else:
            # When the STAC collection does not exist in the catalog
            # Instead of None value for Spatial and Temporal extent, we define a default value
            # as a list of [0.0, 0.0] for Spatial extent and [[datetime.utcnow(), datetime.utcnow()]] for Temporal extent
            collection = pystac.Collection(
                id=stac_id,
                title=stac_title,
                extent=pystac.Extent(
                    spatial=pystac.SpatialExtent(bboxes=[0.0, 0.0]),
                    temporal=pystac.TemporalExtent(
                        intervals=[[datetime.utcnow(), datetime.utcnow()]]
                    ),
                ),
                description=stac_description,
            )
        if asset_properties is not None and asset_properties != {}:
            if asset_properties.get("collection") is not None:
                Assets(logger_properties=self.logger_properties).collection(
                    collection=collection, asset_properties=asset_properties
                )
            else:
                self.logger_properties["logger_level"] = "INFO"
                self.logger_properties[
                    "logger_msg"
                ] = "The `collection` is not activated. So, it does not add any asset to the STAC collection."
                Logger(self.logger_properties)
        if extra_metadata is not None:
            if extra_metadata.get("extra_metadata"):
                ExtraMetadata(
                    logger_properties=self.logger_properties
                ).collection(
                    collection=collection, extra_metadata=extra_metadata
                )
            else:
                self.logger_properties["logger_level"] = "INFO"
                self.logger_properties[
                    "logger_msg"
                ] = "The `extra_metadata` is not activated. So, it does not add any extra metadata to the STAC collection."
                Logger(self.logger_properties)
        harvesting_vars["catalog"].add_child(collection)
        return existed_items_id_list, collection

    def STACItem(
        self,
        harvesting_vars: dict,
        extra_metadata: dict = dict(),
        datacube_extension: bool = False,
        asset_properties: dict = dict(),
    ) -> None:
        """
        Create the STAC-Item.
        """
        harvesting_vars["item_geometry"] = Processing(
            logger_properties=self.logger_properties
        ).geometry(
            harvesting_vars["item_bbox"], harvesting_vars["item_geometry"]
        )

        if (
            harvesting_vars["item_datetime"] is not None
            and harvesting_vars["item_bbox"] is not None
            and harvesting_vars["item_geometry"] is not None
        ):
            item = pystac.Item(
                id=harvesting_vars["item_id"],
                # geometry=geometry.mapping(harvesting_vars["item_footprint"]),
                geometry=geometry.mapping(harvesting_vars["item_footprint"]),
                bbox=harvesting_vars["item_bbox"],
                datetime=harvesting_vars["item_datetime"][1],
                properties={},
            )

            # TODO: Add the assets
            if asset_properties is not None and asset_properties != {}:
                if asset_properties.get("item") is not None:
                    Assets(logger_properties=self.logger_properties).item(
                        item=item,
                        asset_properties=asset_properties,
                        harvesting_vars=harvesting_vars,
                    )
                else:
                    self.logger_properties["logger_level"] = "INFO"
                    self.logger_properties[
                        "logger_msg"
                    ] = "The `item` is not activated. So, it does not add any asset to the STAC item."
                    Logger(self.logger_properties)

            # TODO: Add extensions
            if extra_metadata is not None:
                if extra_metadata.get("extra_metadata"):
                    ExtraMetadata(
                        logger_properties=self.logger_properties
                    ).item(
                        item=item,
                        extra_metadata=extra_metadata,
                        harvesting_vars=harvesting_vars,
                    )
                else:
                    self.logger_properties["logger_level"] = "INFO"
                    self.logger_properties[
                        "logger_msg"
                    ] = "The `extra_metadata` is not activated. So, it does not add any extra metadata to the STAC item."
                    Logger(self.logger_properties)

            if datacube_extension:
                Datacube(logger_properties=self.logger_properties).item(
                    item=item, harvesting_vars=harvesting_vars
                )

            harvesting_vars["collection"].add_item(item)

    def SaveCatalog(self, catalog: pystac.Catalog, stac_dir: str):
        """
        Save the STAC-Catalog.
        """

        try:
            catalog.normalize_hrefs(stac_dir)
            catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
        except Exception:
            import traceback

            print(traceback.format_exc())
            ex_type, ex_value, ex_traceback = sys.exc_info()
            if ex_type is not None and ex_value is not None:
                self.logger_properties["logger_level"] = "ERROR"
                self.logger_properties["logger_msg"] = (
                    "The primary cause of this error is the absence of temporal and bounding box information in the Collection. The STAC-Catalog can therefore not be generated. You can examine the arguments entered or use the `spatial_information` or `temporal_information` arguments for this purpose. %s : %s"
                    % (
                        ex_type.__name__,
                        ex_value,
                    )
                )
                Logger(self.logger_properties)
