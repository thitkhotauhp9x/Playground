"""Pydantic model representing SVG markup."""

from xml.etree import ElementTree

from pydantic import BaseModel, field_validator


class Svg(BaseModel):
    """An SVG document stored as its raw markup string."""

    data: str

    @field_validator("data")
    @classmethod
    def validate_svg_data(cls, data: str) -> str:
        try:
            root = ElementTree.fromstring(data)
        except ElementTree.ParseError as error:
            raise ValueError(f"SVG data is not well-formed XML: {error}") from error

        if root.tag != "svg":
            raise ValueError("SVG data must have an <svg> root element.")
        return data
