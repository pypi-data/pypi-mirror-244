"""
This package provides classes that supports the creation of a BIDS-compliant dataset with modality
agnostic files describing the dataset and participants, as well as the creation of modality specific
files describing task events and behavioral experiments.
"""
from .bidsbehevent import BIDSBehEvent
from .bidshandler import BIDSHandler
from .bidstaskevent import BIDSError, BIDSTaskEvent

__all__ = ["BIDSBehEvent", "BIDSTaskEvent", "BIDSError", "BIDSHandler"]
