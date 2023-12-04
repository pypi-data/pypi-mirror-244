"""NumPy codec to be used with remotecall library.

Usage:
    from remotecall.extracodecs.imagecodec import NumPyCodec
"""
from __future__ import annotations

import typing

import numpy as np
from numpy.typing import NDArray, DTypeLike

from remotecall import Codec


class NumPyCodec(Codec):
    """NumPy codec.

    Example NumPy codec.
    """

    @classmethod
    def is_matching_content_type(cls, content_type: str) -> bool:
        return content_type.startswith("application/numpy")

    @classmethod
    def is_matching_type(cls, type_: typing.Type) -> bool:
        return type_ == np.ndarray

    @classmethod
    def create_by_value(cls, array: NDArray) -> NumPyCodec:
        return cls(shape=array.shape, dtype=array.dtype)

    @classmethod
    def create_by_content_type(cls, content_type: str) -> NumPyCodec:
        shape, data_type = cls._get_shape_and_data_type(content_type)
        return cls(shape=shape, dtype=data_type)

    @classmethod
    def _get_shape_and_data_type(cls, content_type: str) -> tuple[list, DTypeLike]:
        """Extract shape and dtype from content-type.

        Content-type string is expected to be like "numpy-uint8-1080x1920x3".
        """
        fields = content_type.split("-")
        return (
            [int(dimension) for dimension in fields[2].split("x")],
            np.dtype(fields[1])
        )

    def __init__(self, shape: list, dtype: DTypeLike):
        self.shape = shape
        self.dtype = dtype

    @classmethod
    def get_type(cls) -> typing.Type:
        return np.ndarray

    def encode(self, array: NDArray) -> bytes:
        return array.tobytes()

    def decode(self, data: bytes) -> NDArray:
        return np.ndarray(shape=self.shape, dtype=self.dtype, buffer=data)

    def get_content_type(self) -> str:
        # Example output: "numpy-uint8-1080x1920x3"
        dtype_name = str(self.dtype)
        shape_name = "x".join(map(str, self.shape))
        return f"application/numpy-{dtype_name}-{shape_name}"
