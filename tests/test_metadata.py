import pytest

from wgus import get_metadata


@pytest.mark.asyncio
async def test_get_patches_chains():
    metadata = await get_metadata("wgus-woteu.wargaming.net", "WOT.EU.PRODUCTION")
    assert metadata
