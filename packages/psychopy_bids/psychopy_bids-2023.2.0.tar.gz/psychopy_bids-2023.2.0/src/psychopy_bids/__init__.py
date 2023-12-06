"""
    Package to support the creation of valid bids-datasets.
"""

import os
import shutil
import sys
from importlib.metadata import version

import psychopy

__version__ = version("psychopy_bids")


def addBuilderElements():
    """
    With the help of this function the Bids Event component and Bids Export routine get copied to
    the correct psychopy path.

    This option is only temporarily supported until the psychopy plugin system is fully implemented.

    Examples
    --------
    >>> psychopy_bids.addBuilderElements()
    """
    src_path = os.path.dirname(__file__)
    try:
        dst_path = os.path.dirname(psychopy.__file__)
    except NameError:
        sys.exit("Psychopy is not installed!")
    try:
        shutil.copytree(
            f"{src_path}{os.sep}bids_task",
            f"{dst_path}{os.sep}experiment{os.sep}components{os.sep}bids_task",
        )
        shutil.copytree(
            f"{src_path}{os.sep}bids_beh",
            f"{dst_path}{os.sep}experiment{os.sep}components{os.sep}bids_beh",
        )
        shutil.copytree(
            f"{src_path}{os.sep}bids_settings",
            f"{dst_path}{os.sep}experiment{os.sep}routines{os.sep}bids_settings",
        )
    except FileExistsError:
        sys.exit("Bids Event and Bids Export are already added!")
