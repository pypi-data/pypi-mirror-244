# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
import pystac


class Assets:
    """
    A class to add assets to the STAC items and collections.
    """

    def __init__(self, logger_properties: dict = dict()):
        self.logger_properties = logger_properties

    def collection(
        self, collection: pystac.Collection, asset_properties: dict = dict()
    ):
        """
        Add assets to the STAC collection.
        """
        if (
            asset_properties["collection"].get("thumbnail") is not None
            and asset_properties["collection"].get("thumbnail") != ""
        ):
            collection.add_asset(
                key="thumbnail",
                asset=pystac.Asset(
                    href=asset_properties["collection"]["thumbnail"],
                    roles=["thumbnail"],
                    # title=without_slash,
                    media_type=pystac.MediaType.PNG,
                ),
            )
        if (
            asset_properties["collection"].get("jupyter_notebook") is not None
            and asset_properties["collection"].get("jupyter_notebook") != ""
        ):
            collection.add_asset(
                key="Jupyter_Notebook",
                asset=pystac.Asset(
                    href=asset_properties["collection"]["jupyter_notebook"],
                    title="Jupyter Notebook",
                    media_type=pystac.MediaType.HTML,
                ),
            )
        if (
            asset_properties["collection"].get("exploration") is not None
            and asset_properties["collection"].get("exploration") != ""
        ):
            collection.add_asset(
                key="Exploration",
                asset=pystac.Asset(
                    href=asset_properties["collection"]["exploration"],
                    title="Exploration",
                    media_type=pystac.MediaType.HTML,
                ),
            )

    def item(
        self,
        item: pystac.Item,
        asset_properties: dict = dict(),
        harvesting_vars: dict = dict(),
    ):
        """
        Add assets to the STAC item.
        """
        if asset_properties["item"].get(
            "thing_json"
        ) is not None and not asset_properties["item"].get("thing_json"):
            item.add_asset(
                key="JSON",
                asset=pystac.Asset(
                    href=harvesting_vars["item_thing_url_json"],
                    title="Thing JSON",
                    media_type=pystac.MediaType.JSON,
                ),
            )
        if asset_properties["item"].get(
            "all_observations_geojson"
        ) is not None and not asset_properties["item"].get(
            "all_observations_geojson"
        ):
            item.add_asset(
                key="GeoJSON",
                asset=pystac.Asset(
                    href=harvesting_vars["item_all_observations_geojson_url"],
                    title="All Variables GeoJSON",
                    media_type=pystac.MediaType.GEOJSON,
                ),
            )
        if asset_properties["item"].get(
            "all_observations_csv"
        ) is not None and not asset_properties["item"].get(
            "all_observations_csv"
        ):
            item.add_asset(
                key="CSV",
                asset=pystac.Asset(
                    href=harvesting_vars["item_all_observations_csv_url"],
                    title="All Variables CSV",
                    media_type="text/csv",
                ),
            )
        if asset_properties["item"].get(
            "all_observations_dataarray"
        ) is not None and not asset_properties["item"].get(
            "all_observations_dataarray"
        ):
            item.add_asset(
                key="DataArray",
                asset=pystac.Asset(
                    href=harvesting_vars[
                        "item_all_observations_dataarray_url"
                    ],
                    title="All Variables DataArray",
                    media_type="application/x-netcdf",
                ),
            )
        if (
            asset_properties["item"].get("jupyter_notebook") is not None
            and asset_properties["item"].get("jupyter_notebook") != ""
        ):
            item.add_asset(
                key="Jupyter_Notebook",
                asset=pystac.Asset(
                    href=asset_properties["item"]["jupyter_notebook"],
                    title="Jupyter Notebook",
                    media_type=pystac.MediaType.HTML,
                ),
            )
        if (
            asset_properties["item"].get("exploration") is not None
            and asset_properties["item"].get("exploration") != ""
        ):
            item.add_asset(
                key="Exploration",
                asset=pystac.Asset(
                    href=asset_properties["item"]["exploration"],
                    title="Exploration",
                    media_type=pystac.MediaType.HTML,
                ),
            )
        for key, value in harvesting_vars.items():
            if "sta2stac_thing_variable" in key and value is not None:
                if (
                    "sta2stac_thing_variable_geojson" in key
                    and asset_properties["item"].get(
                        "item_observations_geojson"
                    )
                    is not None
                    and not asset_properties["item"].get(
                        "item_observations_geojson"
                    )
                ):
                    item.add_asset(
                        key=key,
                        asset=pystac.Asset(
                            href=value,
                            title=key.replace(
                                "sta2stac_thing_variable_geojson_", ""
                            )
                            + " GeoJSON",
                            media_type=pystac.MediaType.GEOJSON,
                        ),
                    )
                elif (
                    "sta2stac_thing_variable_csv" in key
                    and asset_properties["item"].get("item_observations_csv")
                    is not None
                    and not asset_properties["item"].get(
                        "item_observations_csv"
                    )
                ):
                    item.add_asset(
                        key=key,
                        asset=pystac.Asset(
                            href=value,
                            title=key.replace(
                                "sta2stac_thing_variable_csv_", ""
                            )
                            + " CSV",
                            media_type="text/csv",
                        ),
                    )
                elif (
                    "sta2stac_thing_variable_dataarray" in key
                    and asset_properties["item"].get(
                        "item_observations_dataarray"
                    )
                    is not None
                    and not asset_properties["item"].get(
                        "item_observations_dataarray"
                    )
                ):
                    item.add_asset(
                        key=key,
                        asset=pystac.Asset(
                            href=value,
                            title=key.replace(
                                "sta2stac_thing_variable_dataarray_", ""
                            )
                            + " DataArray",
                            media_type="application/x-netcdf",
                        ),
                    )
