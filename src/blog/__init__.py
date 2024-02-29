"""
Blog project - main module.

This module provides an API system for a simple blog application.

Required Python version is 3.8+.
"""

import sys

MIN_PYTHON = (3, 8)
if sys.version_info < MIN_PYTHON:  # pragma: no cover
    sys.exit(
        "Python %s.%s or later is required.\n" % MIN_PYTHON  # pylint: disable=C0209
    )
