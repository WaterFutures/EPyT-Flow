"""
Module provides functions and classes for serialization.
"""
from typing import Any
from abc import abstractmethod, ABC
import zipfile
from zipfile import ZipFile
import umsgpack
import numpy as np
import networkx
import scipy


SCIPY_BSRARRAY_ID               = -3
NETWORKX_GRAPH_ID               = -2
NUMPY_ARRAY_ID                  = -1
SENSOR_CONFIG_ID                = 0
SCENARIO_CONFIG_ID              = 1
MODEL_UNCERTAINTY_ID            = 2
SENSOR_NOISE_ID                 = 3
GAUSSIAN_UNCERTAINTY_ID         = 4
UNIFORM_UNCERTAINTY_ID          = 5
DEEP_UNIFORM_UNCERTAINTY_ID     = 6
DEEP_GAUSSIAN_UNCERTAINTY_ID    = 7
DEEP_UNCERTAINTY_ID             = 8
SENSOR_FAULT_CONSTANT_ID        = 9
SENSOR_FAULT_DRIFT_ID           = 10
SENSOR_FAULT_GAUSSIAN_ID        = 11
SENSOR_FAULT_PERCENTAGE_ID      = 12
SENSOR_FAULT_STUCKATZERO_ID     = 13
LEAKAGE_ID                      = 14
ABRUPT_LEAKAGE_ID               = 15
INCIPIENT_LEAKAGE_ID            = 16
SCADA_DATA_ID                   = 17


def my_packb(data: Any) -> bytes:
    return umsgpack.packb(data, ext_handlers=ext_handler_pack)


def my_unpackb(data: bytes) -> Any:
    return umsgpack.unpackb(data, ext_handlers=ext_handler_unpack)


def serializable(my_id: int, my_file_ext: str):
    """
    Decorator for a serializable class -- i.e. subclass of
    :class:`~epyt_flow.serialization.Serializable`.

    This decorator registers a new class as a serializable class.

    Parameters
    ----------
    my_id : `int`
        ID of the class.
    my_file_ext : `str`
        File extension.
    """
    def wrapper(my_class):
        @staticmethod
        def unpackb(data: bytes) -> Any:
            return my_class(**my_unpackb(data))
        setattr(my_class, "unpackb", unpackb)

        @staticmethod
        def file_ext() -> str:
            return my_file_ext
        setattr(my_class, "file_ext", file_ext)

        return umsgpack.ext_serializable(my_id)(my_class)

    return wrapper


class Serializable(ABC):
    """
    Base class for a serializable class -- must be used in conjunction with the 
    decorator `@serializable`.
    """
    def __init__(self, **kwds):
        super().__init__(**kwds)

    @abstractmethod
    def get_attributes(self) -> dict:
        """
        Gets all attributes to be serialized -- these attributes are passed to the
        constructor when the object is deserialized.

        Returns
        -------
        `dict`
            Dictionary of attributes -- i.e. pairs of attribute name + value.
        """
        return {}

    def packb(self) -> bytes:
        return my_packb(self.get_attributes())

    @staticmethod
    def load(data: bytes) -> Any:
        """
        Deserializes an instance of this class.

        Parameters
        ----------
        data : `bytes`
            Serialized data.

        Returns
        -------
        `Any`
            Deserialized object.
        """
        return load(data)

    @staticmethod
    def load_from_file(f_in: str, use_zip: bool = True) -> Any:
        """
        Deserializes an instance of this class from a (compressed) file.

        Parameters
        ----------
        f_in : `str`
            Path to the file from which to deserialize the object.
        use_zip : `bool`, optional
            If True, the file `f_in` is supposed to be zip compressed -- False,
            if no compression was used when serializing the object.

            The default is True.

        Returns
        -------
        `Any`
            Deserialized object.
        """
        return load_from_file(f_in, use_zip)

    def dump(self) -> bytes:
        """
        Serializes this object to a byte array.

        Returns
        -------
        `bytes`
            Serialized object.
        """
        return dump(self)

    def save_to_file(self, f_out: str, use_zip: bool = True) -> None:
        """
        Serializes this instance and stores it in a (compressed) file.

        Parameters
        ----------
        f_in : `str`
            Path to the file where this serialized object will be stored.
        use_zip : `bool`, optional
            If True, the file `f_in` is will be zip compressed -- False,
            if no compression is wanted.

            The default is True.
        """
        if not f_out.endswith(self.file_ext()):
            f_out += self.file_ext()

        return save_to_file(f_out, self, use_zip)


def load(data: bytes) -> Any:
    """
    Deserializes data.

    Parameters
    ----------
    data : `bytes`
        Serialized data.

    Returns
    -------
    `Any`
        Deserialized data.
    """
    return my_unpackb(data)


def dump(data: Any) -> bytes:
    """
    Serializes some given data to a byte array.

    Returns
    -------
    `bytes`
        Serialized data.
    """
    return my_packb(data)


def load_from_file(f_in: str, use_zip: bool = True) -> Any:
    """
    Deserializes data from a (compressed) file.

    Parameters
    ----------
    f_in : `str`
        Path to the file from which to deserialize the data.
    use_zip : `bool`, optional
        If True, the file `f_in` is supposed to be zip compressed -- False,
        if no compression was used when serializing the data.

        The default is True.

    Returns
    -------
    `Any`
        Deserialized data.
    """
    if use_zip is False:
        with open(f_in, "rb") as f:
            return umsgpack.unpack(f, ext_handlers=ext_handler_unpack)
    else:
        with ZipFile(f_in, "r", zipfile.ZIP_DEFLATED) as myzip:
            with myzip.open("data.epyt_flow") as f:
                return load(f.read())


def save_to_file(f_out: str, data: Any, use_zip: bool = True) -> None:
    """
    Serializes data and stores it in a (compressed) file.

    Parameters
    ----------
    f_in : `str`
        Path to the file where the serialized data will be stored.
    use_zip : `bool`, optional
        If True, the file `f_in` is will be zip compressed -- False, if no compression is wanted.

        The default is True.
    """
    if use_zip is False:
        with open(f_out, "wb") as f:
            umsgpack.pack(data, f, ext_handlers=ext_handler_pack)
    else:
        with ZipFile(f_out, "w", zipfile.ZIP_DEFLATED) as myzip:
            myzip.writestr("data.epyt_flow", dump(data))


# Add numpy.ndarray, networkx.Graph, and scipy.sparse.bsr_array support
def encode_bsr_array(array: scipy.sparse.bsr_array
                     ) -> tuple[tuple[int, int], tuple[list[float], tuple[list[int], list[int]]]]:
    shape = array.shape
    data = array.data.flatten().tolist()
    rows = array.nonzero()[0].tolist()
    cols = array.nonzero()[1].tolist()

    return shape, (data, (rows, cols))


def decode_bsr_array(ext_data: tuple[tuple[int, int],
                                     tuple[list[float], tuple[list[int], list[int]]]]
                     ) -> scipy.sparse.bsr_array:
    shape, data = ext_data
    return scipy.sparse.bsr_array((data[0], (data[1][0], data[1][1])), shape=(shape[0], shape[1]))


ext_handler_pack = {np.ndarray:
                    lambda arr: umsgpack.Ext(NUMPY_ARRAY_ID, umsgpack.packb(arr.tolist())),
                    networkx.Graph:
                        lambda graph:
                            umsgpack.Ext(NETWORKX_GRAPH_ID,
                                         umsgpack.packb(networkx.node_link_data(graph))),
                    scipy.sparse.bsr_array:
                    lambda arr: umsgpack.Ext(SCIPY_BSRARRAY_ID,
                                             umsgpack.packb(encode_bsr_array(arr)))}
ext_handler_unpack = {NUMPY_ARRAY_ID: lambda ext: np.array(umsgpack.unpackb(ext.data)),
                      NETWORKX_GRAPH_ID:
                      lambda ext: networkx.node_link_graph(umsgpack.unpackb(ext.data)),
                      SCIPY_BSRARRAY_ID: lambda ext: decode_bsr_array(umsgpack.unpackb(ext.data))}
