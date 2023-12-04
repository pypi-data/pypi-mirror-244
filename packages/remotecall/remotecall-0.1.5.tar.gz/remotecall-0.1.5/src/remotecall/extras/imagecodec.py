"""Image codec to be used with remotecall library.

Usage:
    from remotecall.extracodecs.imagecodec import ImageCodec
"""
import typing
import io
import base64

from PIL import Image

from remotecall import Codec


class ImageCodec(Codec):
    IMAGE_FORMAT = "png"

    @classmethod
    def is_matching_content_type(cls, content_type: str) -> bool:
        return content_type.startswith("application/image")

    @classmethod
    def is_matching_type(cls, type_: typing.Type) -> bool:
        return issubclass(type_, cls.get_type())

    @classmethod
    def get_type(cls) -> typing.Type:
        return Image.Image

    def get_content_type(self) -> str:
        return f"application/image-{self.IMAGE_FORMAT}"

    def encode(self, image: Image) -> bytes:
        buffer = io.BytesIO()
        image.save(buffer, format=self.IMAGE_FORMAT)
        return base64.b64encode(buffer.getvalue())

    def decode(self, data: bytes) -> Image:
        base64_str = io.BytesIO(base64.b64decode(data))
        return Image.open(base64_str)
