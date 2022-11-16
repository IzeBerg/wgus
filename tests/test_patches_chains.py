import pytest

from wgus import get_patches_chains


@pytest.mark.asyncio
async def test_get_patches_chains():
    await get_patches_chains("wgus-woteu.wargaming.net", "WOT.EU.PRODUCTION")
