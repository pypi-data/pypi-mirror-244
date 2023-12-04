# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0


# TODO:Assets for the current version are going to be Geojson file, CSV file, Jupyter Notebook, and an intractive map.
# If we add a plotted map as a thumbnail for each things for the last 100 time series, it would be better.

# TODO: To get the Variable names we can get the datastream that contains the variable name and the unit of measurement. Then we can get the sensor details related to each variable name.

# TODO: Spatial extend of each Thing is coing from `Location`.
# TODO: Both of spatial and temporal of each variable is including the `Datastream`
# TODO: If it couldn't get the spatial extend from `Location` it can get it from `Datastream`. But sometimes `Datastream` is not available.
# TODO: For getting the last 100 time series, we can get the `Observation` and then get the `result` and `phenomenonTime` from it:
# https://sensorthings.imk-ifu.kit.edu/v1.1/Datastreams(132)/Observations?$orderby=phenomenonTime+desc&$top=100
# TODO: Datetime_filter works based on the `phenomenonTime` of `Datastream`:
# TODO: Adding `skip` and `select` based on the name of Things
# TODO: Check the URL to not have version number in it
# TODO: check the version and if it is not correctly v1.1 or without v, add v or consider it as v1.1 and send a warning to the user
import os
from typing import Union

import pystac
import urllib3

from .analysers.processing import Processing
from .analysers.properties_verifier import Verifier
from .analysers.utils import Utils
from .creator import Creator
from .harvester import Harvester
from .logger import Logger

##################################################
# Disabling the warning of InsecureRequestWarning
# for web server that doesn't have SSL certificate
##################################################
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class STA2STAC:
    """
    This class is designed to harvest Time Series data from SensorthingsAPI (STA)
    and generate STAC-Metadata. In this algorithm, every STA project is treated
    as a STAC-Collection, and each Thing is considered a STAC-Item.

    Args:
        sta_link (str): The link of the STA project.
        sta_version (str, optional): The version of the STA project.
            Defaults to "v1.1".
        stac_dir (str, optional): The directory of the STAC project.
            Defaults to current directory.
        stac_id (str, optional): The ID of the STAC Catalog. Defaults
            to "STA2STAC". The default value is set to "STA2STAC". It
            is important to mention that this ID will also be regarded
            as the collection ID.
        stac_title (str, optional): The title of the STAC Catalog. The
            default value is set to "STA2STAC". It is important to mention
            that this title will also be regarded as a collection-title.
        stac_description (str, optional): The description of the STAC
            Catalog. The default value is set to "STA2STAC description".
            It is important to mention that this description will also
            be regarded as a collection-description.
        stac_existance_catalog (bool, optional): If the STAC Catalogue
            already exists in the specified directory and you do not
            wish to reharvest the dataset, it should be set to True.
            By default, the value is set to False.
        stac_existance_collection (bool, optional): If the STAC Collection
            already exists in the current STAC-Catalog and you want to
            avoid having to reharvest the dataset, it should be set
            to True. By default, the value is set to False.
        items_tuples (list[tuple], optional): A list of tuples that
            includes the auto-ID and user-defined-ID, -title, and
            -description of each Thing in a STA. To obtain additional
            information, please refer to the class `~sta2stac.STA2STAC.items_tuples`.
            By default, the value is set to None.
        filter (str, optional): A filter for retrieving the refined data
            from STA.To obtain additional information, please refer
            to the class:`~sta2stac.STA2STAC.filter`. The default
            value is None.
        default_catalog_name (str, optional): The name of the STAC Catalog.
            Defaults to "catalog.json".
        datacube_extension (bool, optional): To enable the datacube extension
            for the STAC-Collection, set its value to True. By default, the
            value is set to False.
        extra_metadata (dict, optional): A dictionary of extra metadata that
            you desire to include in the STAC-Collection and STAC-Items. To obtain
            additional information on this topic, please refere to the
            :class:`~sta2stac.STA2STAC.extra_metadata`. The default value is an empty
            dictionary.
        limited_number_of_things (int, optional): To restrict the quantity of Things in a STA,
            you can configure it to operate primarily for developmental objectives. By default,
            the value is set to None.
        asset_properties (dict, optional): A dictionary of assets that you desire to
            incorporate into the STAC-Collection and STAC-Items. To obtain additional
            information on this topic, please refere to the class:`~sta2stac.STA2STAC.asset_properties`.
            The default value is an empty dictionary.
        requests_properties (dict, optional): A dictionary that modify the requests to
            URLs. To obtain additional information on this topic, refer to
            the :class:`~sta2stac.STA2STAC.requests_properties`. The default value is
            an empty dictionary.
        logger_properties (dict, optional):A dictionary of attributes that control the logger.
            To obtain additional information on this topic, please see the documentation for the
            the :class:`~sta2stac.STA2STAC.requests_properties`. The default value is an empty
            dictionary.
    """

    sta_link: str
    """
    The link of the STA project. For example:

      `https://sensorthings.imk-ifu.kit.edu`
    """
    sta_version: str
    """
    This is the version of the STA project. The STA2STAC
    package currently provides support for two distinct
    versions: `v1.0` and `v1.1`. The format can be defined
    as either `v1.1` or `1.1`. It is important to mention
    that if the version is not accurately specified, it
    will be considered as `v1.1`.
    """
    stac_dir: str
    """
    The directory of the STAC project. By default it is the
    current directory.
    """
    stac_id: str
    """
    The ID of the STAC Catalog. It is important to mention that
    this ID will also be regarded as the collection ID.
    """
    stac_title: str
    """
    The title of the STAC Catalog. It is important to mention
    that this Title will also be regarded as the collection
    Title.
    """
    stac_description: str
    """
    The description of the STAC Catalog. It is important to mention
    that this Description will also be regarded as the collection
    Description.
    """
    stac_existance_catalog: bool
    """
    It should be set to True if the STAC Catalogue in the specified
    directory already exists and reharvesting the dataset is not
    desired.
    """
    stac_existance_collection: bool
    """
    It should be set to True if the STAC Collection in the current
    STAC-Catalog already exists and reharvesting the dataset is
    not desired.
    """
    items_tuples: Union[list[tuple], None]
    """
    A list of tuples that includes the auto-ID and user-defined-ID,
    -title, and -description of every Thing in a STA. To define
    `item_tuples`, you should first obtain auto-ID information.
    To achieve this, you can utilise the :class:`~sta2stac.STA2STAC.filter`
    function to obtain the automatically produced ID, title, and
    description. Afterwards, you can specify your own ID, Title,
    and Description using the following structure:

    .. code-block:: javascript
        [
            ("auto-ID1", "user-defined-ID1", "user-defined-Title1", "user-defined-Description1"),
            ("auto-ID2", "user-defined-ID2", "user-defined-Title2", "user-defined-Description2"),
            ("auto-ID3", "user-defined-ID3", "user-defined-Title3", "user-defined-Description3"),
        ]

    """
    filter: Union[str, None]
    """
    A filter is used to selectively filter the attributes in
    SensorThingAPI. It is strongly advised to avoid using `select`
    and `skip` filters in order to minimise conflicts when
    filtering the STA. To obtain additional information on
    filtering the STA, please visit the following website:

    https://fraunhoferiosb.github.io/FROST-Server/sensorthingsapi/requestingData/STA-Filtering.html
    """
    default_catalog_name: str
    """
    The name of the STAC Catalog. By default it is `catalog.json`.
    """
    datacube_extension: bool
    """
    If you want to add the datacube extension to the STAC-Collection, it should be set to True.
    """
    extra_metadata: dict
    """
    A dictionary of extra metadata that you want to add to the
    STAC-Collection and STAC-Items. It has two main keys,
    `extra_metadata` that is boolean and `extra_metadata_file`
    that is the address of `extra_metadata.json` JSON file. For
    getting more information about making the `extra_metadata.json`
    file, please refer to :ref:`extra_metadata`.
    By default, if 'extra_metadata' is set to True, the
    'extra_metadata.json' file is utilised for the 'extra_metadata_file'
    key, which is situated in the'sta2stac' main directory.
    """
    limited_number_of_things: Union[int, None]
    """
    If you want to limit the number of Things in a STA, you can
    set it it works more for development purposes.
    """
    asset_properties: dict
    """
    The assets' dictionary that is to be added to the STAC-Collection
    and STAC-Items. It includes the `item` and `collection` primary
    keys. Additionally, both the 'item' and 'collection' entities
    comprise the subsequent keys:

    .. code-block:: javascript
        {
            "item": {
                "thing_json": True,
                "all_observations_csv": True,
                "all_observations_geojson": True,
                "all_observations_dataarray": True,
                "item_observations_csv": True,
                "item_observations_geojson": True,
                "item_observations_dataarray": True,
                "jupyter_notebook": "Link of a Jupiter Notebook",
                "exploration": "Link of an interactive map"

            },
            "collection": {
                "thumbnail": "Link of a thumbnail",
                "jupyter_notebook": "Link of a Jupiter Notebook",
                "exploration": "Link of an interactive map"
            }
        }

    **item:**

        **thing_json (bool, optional)**:
            If this boolean value is True, the `Thing` JSON link is added to the STAC-Item as an asset.

        **all_observations_csv (bool, optional)**:
            If this boolean value is True, the `Observation` of each `Datastreams` of the current Thing is appended to the STAC-Item as a CSV link asset.

        **all_observations_geojson (bool, optional)**:
            If this boolean value is True, the `Observation` of each `Datastreams` of the current Thing is appended to the STAC-Item as a GeoJSON link asset.

        **all_observations_dataarray (bool, optional)**:
            If this boolean value is True, the `Observation` of each `Datastreams` of the current Thing is appended to the STAC-Item as a DataArray link asset.

        **item_observations_csv (bool, optional)**:
            If the boolean value is True, each `Datastream`'s `Observation` is separately added as a seperated CSV link asset to the STAC-Item.

        **item_observations_geojson (bool, optional)**:
            If the boolean value is True, each `Datastream`'s `Observation` is separately added as a seperated GeoJSON link asset to the STAC-Item.

        **item_observations_dataarray (bool, optional)**:
            If the boolean value is True, each `Datastream`'s `Observation` is separately added as a seperated DataArray link asset to the STAC-Item.

        **jupyter_notebook (str, optional)**:
            It is a string that contains the link of the Jupyter Notebook that is related to the current Thing.

        **exploration (str, optional)**:
            It is a string that contains the link of the interactive map that is related to the current Thing.

    **collection:**

        **thumbnail (str, optional)**:
            It is a string that contains the link of the thumbnail of the current collection.

        **jupyter_notebook (str, optional)**:
            It is a string that contains the link of the Jupyter Notebook that is related to the current collection.

        **exploration (str, optional)**:
            It is a string that contains the link of the interactive map that is related to the current collection.
    """
    requests_properties: dict
    """
    A dictionary of properties that adjust the requests to URLs. It contains the following keys:

        **verify (bool, optional)**:
            It is a boolean that if it is True, it verifies the SSL certificate. By default it is False.
        **timeout (int, optional)**:
            It is an integer that sets the timeout of the requests. By default it is 10 seconds.
        **auth (tuple, optional)**:
            It is a tuple that contains the username and password for the authentication. By default it is None.

    """
    logger_properties: dict
    """
    A dictionary of properties that adjust the logger. For getting more information about this refer to :class:`~sta2stac.logger.Logger`.
    """

    def __init__(
        self,
        sta_link: str,
        sta_version: str = "v1.1",
        stac_dir: str = os.getcwd(),
        stac_id: str = "STA2STAC",
        stac_title: str = "STA2STAC",
        stac_description: str = "STA2STAC description",
        stac_existance_catalog: bool = False,
        stac_existance_collection: bool = False,
        items_tuples: list[tuple] = [],
        filter: str = "",
        default_catalog_name: str = "catalog.json",
        datacube_extension: bool = False,
        extra_metadata: dict = dict(),
        limited_number_of_things: Union[int, None] = None,
        asset_properties: dict = dict(),
        requests_properties: dict = dict(),
        logger_properties: dict = dict(),
    ):
        verifier = Verifier()
        self.harvesting_vars = {}
        if asset_properties is not None and isinstance(asset_properties, dict):
            verifier.asset_properties(asset_properties)
        if requests_properties is not None and isinstance(
            requests_properties, dict
        ):
            verifier.requests_properties(requests_properties)

        if logger_properties is not None and isinstance(
            logger_properties, dict
        ):
            verifier.logger_properties(logger_properties)
        if logger_properties is not None and isinstance(
            logger_properties, dict
        ):
            self.logger_properties = logger_properties

        if extra_metadata is not None and isinstance(extra_metadata, dict):
            verifier.extra_metadata(extra_metadata)
        if sta_version is not None and isinstance(sta_version, str):
            sta_version = verifier.sta_version(sta_version)

        self.logger_properties["logger_level"] = "DEBUG"
        self.logger_properties["logger_msg"] = "Harvesting is started!"
        Logger(self.logger_properties)

        validator_value = Utils(self.logger_properties).validate_sta_link(
            link=sta_link,
            version=sta_version,
            filter=filter,
            requests_properties=requests_properties,
        )
        if not validator_value:
            return
        elif validator_value:
            self.harvesting_vars["catalog"] = Creator(
                self.logger_properties
            ).STACCatalog(
                sta_link=sta_link,
                stac_id=stac_id,
                stac_title=stac_title,
                stac_description=stac_description,
                stac_dir=stac_dir,
                default_catalog_name=default_catalog_name,
                stac_existance_catalog=stac_existance_catalog,
            )

            (
                self.harvesting_vars["existed_items_id_list"],
                self.harvesting_vars["collection"],
            ) = Creator(self.logger_properties).STACCollection(
                stac_id=stac_id,
                stac_title=stac_title,
                stac_description=stac_description,
                harvesting_vars=self.harvesting_vars,
                extra_metadata=extra_metadata,
                stac_existance_collection=stac_existance_collection,
                asset_properties=asset_properties,
            )

        things_number = Utils(self.logger_properties).get_number_of_entities(
            link=sta_link + "/" + sta_version,
            entity="Things",
            filter=filter,
            requests_properties=requests_properties,
        )
        list_of_things_id = Utils(
            self.logger_properties
        ).get_list_of_entities_id(
            link=sta_link + "/" + sta_version,
            entity="Things",
            filter=filter,
            requests_properties=requests_properties,
        )
        if things_number == 0:
            Creator(logger_properties=self.logger_properties).SaveCatalog(
                catalog=self.harvesting_vars["catalog"], stac_dir=stac_dir
            )
            self.logger_properties["logger_level"] = "INFO"
            self.logger_properties[
                "logger_msg"
            ] = "It saves an empty STAC-Collection. Harvesting and creating a STAC-Metadata with no STAC-Item is finished!"
            Logger(self.logger_properties)
            return
        elif things_number > 0 and things_number != len(list_of_things_id):
            self.logger_properties["logger_level"] = "INFO"
            self.logger_properties[
                "logger_msg"
            ] = f"Length of the list of Things ID and the total number of Things in STA are not equal. Number of Things in STA: {things_number}. Length of The list of Things ID in STA: {len(list_of_things_id)}. So it needs to be run it again!"
            Logger(self.logger_properties)
            list_of_things_id = Utils(
                self.logger_properties
            ).get_list_of_entities_id(
                link=sta_link + "/" + sta_version,
                entity="Things",
                filter=filter,
                requests_properties=requests_properties,
            )
        if things_number > 0 and things_number == len(list_of_things_id):
            self.logger_properties["logger_level"] = "INFO"
            self.logger_properties[
                "logger_msg"
            ] = f"Number of Things in STA: {things_number} and the list of Things ID in STA: {list_of_things_id}"
            Logger(self.logger_properties)
        else:
            self.logger_properties["logger_level"] = "ERROR"
            self.logger_properties[
                "logger_msg"
            ] = f"Number of Things in STA: {things_number} and length of the list of Things ID in STA: {len(list_of_things_id)} are not equal. So, it stops processing and you need to have a look at your given STA Things and run it again!"
            Logger(self.logger_properties)
            return

        for thing_index, thing_id_number in enumerate(list_of_things_id):
            if limited_number_of_things is not None:
                if thing_index + 1 == limited_number_of_things:
                    break
            self.logger_properties["logger_level"] = "INFO"
            self.logger_properties[
                "logger_msg"
            ] = f"Thing ID number: {thing_id_number}"
            Logger(self.logger_properties)
            # Defining the harvesting variables empty for each Thing to be filled by the harvester function
            self.harvesting_vars["item_datetime"] = None
            self.harvesting_vars["item_datetime_str"] = []
            self.harvesting_vars["item_bbox"] = []
            self.harvesting_vars["item_footprint"] = None
            self.harvesting_vars["item_geometry"] = ""
            self.harvesting_vars["item_variable_names"] = []
            self.harvesting_vars["item_variable_units"] = []
            self.harvesting_vars["item_variable_dimensions"] = []
            self.harvesting_vars["item_variable_descriptions"] = []
            self.harvesting_vars["item_variable_ids"] = []
            self.harvesting_vars["item_dimension_names"] = []
            for key in self.harvesting_vars.keys():
                if "sta2stac_thing_variable_" in key:
                    self.harvesting_vars[key] = None

            Harvester(
                logger_properties=self.logger_properties,
                harvesting_vars=self.harvesting_vars,
            ).item(
                link=sta_link,
                version=sta_version,
                number_of_things=thing_id_number,
                requests_properties=requests_properties,
                item_tuples=items_tuples,
                datacube_extension=datacube_extension,
                filter=filter,
            )

            Creator(logger_properties=self.logger_properties).STACItem(
                harvesting_vars=self.harvesting_vars,
                extra_metadata=extra_metadata,
                datacube_extension=datacube_extension,
                asset_properties=asset_properties,
            )

        # Sorting the collection list datetimes and getting the first and last datetime
        self.harvesting_vars["collection_datetime"] = Processing(
            logger_properties=self.logger_properties
        ).collection(self.harvesting_vars["collection_datetime"])
        # Extend the spatial and temporal extent of the collection
        spatial_extent = pystac.SpatialExtent(
            bboxes=[self.harvesting_vars["collection_bbox"]]
        )
        temporal_extent = pystac.TemporalExtent(
            intervals=[self.harvesting_vars["collection_datetime"]]
        )
        self.harvesting_vars["collection"].extent = pystac.Extent(
            spatial=spatial_extent,
            temporal=temporal_extent,
        )
        # Adding the collection to the catalog and saving it
        Creator(self.logger_properties).SaveCatalog(
            catalog=self.harvesting_vars["catalog"], stac_dir=stac_dir
        )
        self.logger_properties["logger_level"] = "INFO"
        self.logger_properties[
            "logger_msg"
        ] = "Harvesting and creating STAC-Metadata is finished!"
        Logger(self.logger_properties)
