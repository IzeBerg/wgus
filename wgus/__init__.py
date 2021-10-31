"""API for Wargaming Update Service (WGUS)"""

__version__ = "0.0.1"

from .metadata import Metadata, get_metadata
from .patches_chain import PatchesChains, get_patches_chain
