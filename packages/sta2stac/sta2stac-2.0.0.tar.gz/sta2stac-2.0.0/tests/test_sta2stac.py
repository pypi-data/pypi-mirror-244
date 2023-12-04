# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0

import os

from sta2stac import STA2STAC, ItemInfoHandler


def test_item_info_handler():
    ItemInfoHandler(
        logger_properties={"logger_handler": "StreamHandler"}
    ).get_entity_tuples_info(
        sta_link="https://sensorthings.imk-ifu.kit.edu/",
        sta_version="v1.1",
        entity="Things",
    )


def test_sta2stac_init():
    STA2STAC(
        sta_link="https://sensorthings.imk-ifu.kit.edu/",
        sta_version="v1.1",
        stac_dir=os.getcwd() + "/stac/",
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_sta2stac_id_title_desc_dir():
    STA2STAC(
        sta_link="https://sensorthings.imk-ifu.kit.edu/",
        sta_version="v1.1",
        stac_dir=os.getcwd() + "/stac/",
        stac_id="test-id",
        stac_title="This is a test title",
        stac_description="This is a test description",
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_sta2atac_items_tuples():
    items_tuples = [
        ("BE_K_000", "test-id", "test title", "test description"),
        ("ACH_MET_000", "test-id1", "test title1", "test description2"),
    ]
    STA2STAC(
        sta_link="https://sensorthings.imk-ifu.kit.edu/",
        sta_version="v1.1",
        stac_dir=os.getcwd() + "/stac/",
        items_tuples=items_tuples,
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_sta2stac_datacube():
    STA2STAC(
        sta_link="https://sensorthings.imk-ifu.kit.edu/",
        sta_version="v1.1",
        stac_dir=os.getcwd() + "/stac/",
        datacube_extension=True,
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_STA2STAC():
    STA2STAC(
        sta_link="https://sensorthings.imk-ifu.kit.edu/",
        sta_version="v1.1",
        stac_dir=os.getcwd() + "/stac/",
        extra_metadata={"extra_metadata": True},
        datacube_extension=True,
        asset_properties={
            "item": {
                "thing_json": True,
                "all_observations_csv": True,
                "all_observations_geojson": True,
                "all_observations_dataarray": True,
                "item_observations_csv": True,
                "item_observations_geojson": True,
                "item_observations_dataarray": True,
                "jupyter_notebook": "",
                "exploration": "",
            },
            "collection": {
                "thumbnail": "link",
                "jupyter_notebook": "link",
                "exploration": "link",
            },
        },
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_ItemInfoHarvester():
    ItemInfoHandler(
        logger_properties={"logger_handler": "StreamHandler"}
    ).get_entity_tuples_info(
        sta_link="https://sensorthings.imk-ifu.kit.edu/",
        sta_version="v1.1",
        entity="Things",
    )
