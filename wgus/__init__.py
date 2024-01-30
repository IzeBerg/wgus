"""API for Wargaming Update Service (WGUS)"""

__version__ = "0.0.10"

from .metadata import Metadata, get_metadata
from .patches_chains import PatchesChains, get_patches_chains
