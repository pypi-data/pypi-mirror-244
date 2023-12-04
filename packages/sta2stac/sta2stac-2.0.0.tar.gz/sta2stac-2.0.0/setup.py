# SPDX-FileCopyrightText: 2023 KIT - Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0

"""Setup script for the sta2stac package."""
import versioneer
from setuptools import setup

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
