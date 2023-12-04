# SPDX-FileCopyrightText: 2023 KIT - Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2

import os
from typing import Union

from ..logger import Logger


class ExistenceValidator(object):
    """
    A class for verifying the main STAC catalog's existence.
    This class is implemented in :class:`~sta2stac.STACCreator`.

    Args:
        stac_dir (str): Directory of the main STAC catalog (*)
        default_catalog_name (str, optional): Name of the main STAC catalog. default is `catalog.json`.
        logger_properties (dict, optional): A dictionary of properties for logger. default is `None`.

    """

    stac_dir: str
    """
    Directory of the main STAC catalog. It can be a relative or absolute path.
    """
    default_catalog_name: str
    """
    Name of the main STAC catalog. default is `catalog.json`.
    """

    logger_properties: Union[dict, None]
    """
    A dictionary of properties for logger. default is `None`.
    You can look at keys in :class:`~tds2stac.logger.Logger` class.
    """

    def __init__(
        self,
        stac_dir: str,
        default_catalog_name: str = "catalog.json",
        logger_properties: Union[dict, None] = dict(),
    ):
        self.stac_dir = stac_dir
        self.stac_dir = os.path.join(self.stac_dir, "/" + default_catalog_name)
        if os.path.exists(self.stac_dir):
            self.existance = True
        else:
            self.existance = False
        if logger_properties is not None:
            logger_properties["logger_msg"] = self.existance
        Logger(logger_properties)

    def __repr__(self):
        return "<STA2STACExistanceChecker existance: %s>" % (self.existance)
