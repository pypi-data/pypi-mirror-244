# SPDX-FileCopyrightText: 2023 KIT - Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2

"""STA2STAC

A Python Ecosystem for Harvesting Time Series data information from SensorthingsAPI (STA) and Cultivating STAC-Metadata.
"""
from sta2stac.analysers.item_info_retriever import ItemInfoHandler
from sta2stac.analysers.processing import Processing
from sta2stac.analysers.properties_verifier import Verifier
from sta2stac.analysers.utils import Utils
from sta2stac.creator import Creator
from sta2stac.harvester import Harvester
from sta2stac.main import STA2STAC

from . import _version

__all__ = [
    "__version__",
    "STA2STAC",
    "Processing",
    "Verifier",
    "Utils",
    "Harvester",
    "Creator",
    "ItemInfoHandler",
]


__version__ = _version.get_versions()["version"]

__author__ = "Mostafa Hadizadeh"
__copyright__ = "2023 KIT - Karlsruher Institut für Technologie"
__credits__ = [
    "Mostafa Hadizadeh",
]
__license__ = "EUPL-1.2"

__maintainer__ = "Mostafa Hadizadeh"
__email__ = "mostafa.hadizadeh@kit.edu"

__status__ = "Pre-Alpha"

__version__ = _version.get_versions()["version"]

__version__ = _version.get_versions()["version"]

__version__ = _version.get_versions()["version"]
