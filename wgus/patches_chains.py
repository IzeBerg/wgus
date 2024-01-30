from typing import Dict, List, Optional
from xml.etree import ElementTree

from pydantic import BaseModel, HttpUrl

from . import requests
from .constants import INSTALLATION_ID, META_PROTOCOL_VERSION, PATCHES_PROTOCOL_VERSION
from .metadata import Metadata, get_metadata


class PatchTorrent(BaseModel):
    hash: str
    urls: List[str]

    @classmethod
    def parse(cls, xml: Optional[ElementTree.Element]) -> "PatchTorrent":
        return cls.parse_obj(
            dict(
                hash=xml.find("hash").text,
                urls=[u.text for u in xml.iterfind("urls/url")],
            )
        )


class PatchFile(BaseModel):
    name: str
    size: int
    unpacked_size: Optional[int]
    diffs_size: Optional[int]

    @classmethod
    def parse(cls, xml: ElementTree.Element) -> "PatchFile":
        return cls.parse_obj(
            dict(
                name=xml.find("name").text,
                size=xml.find("size").text,
                unpacked_size=xml.findtext("unpacked_size"),
                diffs_size=xml.findtext("diffs_size"),
            )
        )


class Patch(BaseModel):
    files: List[PatchFile]
    torrent: PatchTorrent
    part: str
    version_to: str

    @classmethod
    def parse(cls, xml: Optional[ElementTree.Element]) -> "Patch":
        return cls.parse_obj(
            dict(
                files=[PatchFile.parse(ct) for ct in xml.iterfind("files/file")],
                torrent=PatchTorrent.parse(xml.find("torrent")),
                part=xml.find("part").text,
                version_to=xml.find("version_to").text,
            )
        )


class WebSeedURL(BaseModel):
    url: HttpUrl
    threads: int
    name: str

    @classmethod
    def parse(cls, xml: ElementTree.Element) -> "WebSeedURL":
        return cls.parse_obj(
            dict(
                url=xml.text,
                threads=xml.get("threads"),
                name=xml.get("name"),
            )
        )


class PatchesChain(BaseModel):
    type: str
    patches: List[Patch]

    @classmethod
    def parse(cls, xml: ElementTree.Element) -> "PatchesChain":
        return cls.parse_obj(
            dict(
                type=xml.get("type"),
                patches=[Patch.parse(p) for p in xml.iterfind("patch")],
            )
        )


class PatchesChains(BaseModel):
    patches_chain: List[PatchesChain]
    webseeds: List[WebSeedURL]
    meta_need_update: bool
    version_name: str

    @classmethod
    def parse(cls, text: str) -> "PatchesChains":
        xml = ElementTree.fromstring(text)
        return cls.parse_obj(
            dict(
                patches_chain=[
                    PatchesChain.parse(pc) for pc in xml.iterfind("patches_chain")
                ],
                webseeds=[WebSeedURL.parse(p) for p in xml.iterfind("web_seeds/url")],
                meta_need_update=xml.find("meta_need_update").text,
                version_name=xml.find("version_name").text,
            )
        )


async def get_patches_chains(
    host: str,
    guid: str,
    versions: Optional[Dict[str, str]] = None,
    query: Optional[Dict[str, str]] = None,
    meta: Optional[Metadata] = None,
) -> PatchesChains:
    if query is None:
        query = {}
    if versions is None:
        versions = {}

    if meta is None:
        meta = await get_metadata(host, guid)

    query.update(
        {
            "game_id": guid,
            "protocol_version": PATCHES_PROTOCOL_VERSION,
            "metadata_protocol_version": META_PROTOCOL_VERSION,
            "installation_id": INSTALLATION_ID,
        }
    )
    client_type = query.setdefault(
        "client_type", meta.predefined_section.client_types.default
    )
    query.setdefault("lang", meta.predefined_section.default_language)
    query.setdefault("metadata_version", meta.version)

    client_type_info = meta.predefined_section.client_types.get(client_type)
    if client_type_info is None:
        raise Exception("unknown client_type")
    for p in client_type_info.parts:
        query.setdefault(f"{p.id}_current_version", versions.get(p.id, "0"))

    return PatchesChains.parse(
        await requests.get(host, "/api/v1/patches_chain/", query)
    )
