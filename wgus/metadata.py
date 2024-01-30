from typing import List, Optional
from xml.etree import ElementTree

from pydantic import BaseModel

from . import requests
from .constants import META_PROTOCOL_VERSION


class ClientTypePart(BaseModel):
    id: str
    app_type: Optional[str]
    integrity: Optional[bool]
    lang: Optional[bool]

    @classmethod
    def parse(cls, xml: Optional[ElementTree.Element]) -> "ClientTypePart":
        return cls.parse_obj(
            dict(
                id=xml.get("id"),
                integrity=xml.get("integrity"),
                app_type=xml.get("app_type"),
                lang=xml.get("lang"),
            )
        )


class ClientType(BaseModel):
    id: str
    arch: Optional[str]
    parts: List[ClientTypePart]

    @classmethod
    def parse(cls, xml: Optional[ElementTree.Element]) -> "ClientType":
        return cls.parse_obj(
            dict(
                id=xml.get("id"),
                arch=xml.get("arch"),
                parts=[
                    ClientTypePart.parse(ctp)
                    for ctp in xml.iterfind("client_parts/client_part")
                ],
            )
        )


class ClientTypes(BaseModel):
    types: List[ClientType]
    default: str

    def get(self, _id: Optional[str] = None) -> Optional[ClientType]:
        if _id is None:
            _id = self.default
        for x in self.types:
            if x.id == _id:
                return x
        return None

    @classmethod
    def parse(cls, xml: Optional[ElementTree.Element]) -> "ClientTypes":
        return cls.parse_obj(
            dict(
                types=[ClientType.parse(ct) for ct in xml.iterfind("client_type")],
                default=xml.get("default"),
            )
        )


class PredefinedSection(BaseModel):
    app_id: str
    chain_id: str
    supported_languages: List[str]
    default_language: str

    client_types: ClientTypes

    @classmethod
    def parse(cls, xml: Optional[ElementTree.Element]) -> "PredefinedSection":
        return cls.parse_obj(
            dict(
                app_id=xml.find("app_id").text,
                chain_id=xml.find("chain_id").text,
                supported_languages=xml.find("supported_languages").text.split(","),
                default_language=xml.find("default_language").text,
                client_types=ClientTypes.parse(xml.find("client_types")),
            )
        )


class Metadata(BaseModel):
    version: str
    predefined_section: PredefinedSection

    @classmethod
    def parse(cls, text: str) -> "Metadata":
        xml = ElementTree.fromstring(text)
        return cls.parse_obj(
            dict(
                version=xml.find("version").text,
                predefined_section=PredefinedSection.parse(
                    xml.find("predefined_section")
                ),
            )
        )


async def get_metadata(
    host: str, guid: str, chain_id: Optional[str] = None
) -> Metadata:
    return Metadata.parse(
        await requests.get(
            host,
            "/api/v1/metadata/",
            {
                "guid": guid,
                "chain_id": chain_id or "unknown",
                "protocol_version": META_PROTOCOL_VERSION,
            },
        )
    )
