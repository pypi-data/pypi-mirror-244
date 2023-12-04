# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0

import os

from .. import logger

default_extra_metadata_file = (
    os.path.dirname(os.path.abspath(logger.__file__)) + "/extra_metadata.json"
)
