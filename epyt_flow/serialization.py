"""
Module provides functions and classes for serialization.
"""
from typing import Any, Union
from abc import abstractmethod, ABC
from io import BufferedIOBase
import pathlib
import importlib
import json
import gzip
import umsgpack
import numpy as np
import networkx
import scipy


SCIPY_BSRARRAY_ID                       = -3
NETWORKX_GRAPH_ID                       = -2
NUMPY_ARRAY_ID                          = -1
SENSOR_CONFIG_ID                        = 0
SCENARIO_CONFIG_ID                      = 1
MODEL_UNCERTAINTY_ID                    = 2
SENSOR_NOISE_ID                         = 3
ABSOLUTE_GAUSSIAN_UNCERTAINTY_ID        = 4
RELATIVE_GAUSSIAN_UNCERTAINTY_ID        = 5
ABSOLUTE_UNIFORM_UNCERTAINTY_ID         = 6
RELATIVE_UNIFORM_UNCERTAINTY_ID         = 7
PERCENTAGE_DEVIATON_UNCERTAINTY_ID      = 8
ABSOLUTE_DEEP_UNIFORM_UNCERTAINTY_ID    = 9
RELATIVE_DEEP_UNIFORM_UNCERTAINTY_ID    = 10
ABSOLUTE_DEEP_GAUSSIAN_UNCERTAINTY_ID   = 11
RELATIVE_DEEP_GAUSSIAN_UNCERTAINTY_ID   = 12
ABSOLUTE_DEEP_UNCERTAINTY_ID            = 13
RELATIVE_DEEP_UNCERTAINTY_ID            = 14
SENSOR_FAULT_CONSTANT_ID                = 15
SENSOR_FAULT_DRIFT_ID                   = 16
SENSOR_FAULT_GAUSSIAN_ID                = 17
SENSOR_FAULT_PERCENTAGE_ID              = 18
SENSOR_FAULT_STUCKATZERO_ID             = 19
LEAKAGE_ID                              = 20
ABRUPT_LEAKAGE_ID                       = 21
INCIPIENT_LEAKAGE_ID                    = 22
SCADA_DATA_ID                           = 23
SENSOR_ATTACK_OVERRIDE_ID               = 24
SENSOR_ATTACK_REPLAY_ID                 = 25
NETWORK_TOPOLOGY_ID                     = 26
PUMP_STATE_EVENT_ID                     = 28
PUMP_SPEED_EVENT_ID                     = 29
VALVE_STATE_EVENT_ID                    = 30
SPECIESINJECTION_EVENT_ID               = 31


def my_packb(data: Any) -> bytes:
    """
    Overriden `umsgpack.packb <https://msgpack-python.readthedocs.io/en/latest/api.html#msgpack.packb>`_
    method to support custom serialization handlers.
    """
    return umsgpack.packb(data, ext_handlers=ext_handler_pack)


def my_unpackb(data: Any) -> Any:
    """
    Overriden `umsgpack.unpackb <https://msgpack-python.readthedocs.io/en/latest/api.html#msgpack.unpackb>`_
    method to support custom serialization handlers.
    """
    return umsgpack.unpackb(data, ext_handlers=ext_handler_unpack)


def serializable(my_id: int, my_file_ext: str) -> Any:
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
    :func:`~epyt_flow.serialization.serializable` decorator.
    """
    def __init__(self, _parent_path: str = "", **kwds):
        self._parent_path = _parent_path

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

    def file_ext(self) -> str:
        """
        Returns the file extension of this class.

        This function is automatically implemented by applying the
        :func:`~epyt_flow.serialization.serializable` decorator.

        Returns
        -------
        `str`
            File extension.
        """
        raise NotImplementedError()

    def packb(self) -> bytes:
        """
        Serializes the attributes of this object.

        Returns
        -------
        `bytes`
            Serialized object.
        """
        return my_packb(self.get_attributes())

    @staticmethod
    def load(data: Union[bytes, BufferedIOBase]) -> Any:
        """
        Deserializes an instance of this class.

        Parameters
        ----------
        data : `bytes` or `io.BufferedIOBase`
            Serialized data or stream from which serialized data can be read.

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

    def dump(self, stream_out: BufferedIOBase = None) -> Any:
        """
        Serializes this object to a byte array.

        Parameters
        ----------
        stream_out : `io.BufferedIOBase`, optional
            Stream to which the serialized object is written.
            If None, the serialized object is returned as a `bytes` array.

            The default is None.

        Returns
        -------
        `bytes`
            If `stream_out` is None, the serialized object is returned as a `bytes` array.
        """
        return dump(self, stream_out)

    def save_to_file(self, f_out: str, use_zip: bool = True) -> None:
        """
        Serializes this instance and stores it in a (compressed) file.

        Parameters
        ----------
        f_in : `str`
            Path to the file where this serialized object will be stored.
        use_zip : `bool`, optional
            If True, the file `f_in` will be zip compressed -- False,
            if no compression is wanted.

            The default is True.
        """
        if not f_out.endswith(self.file_ext()):
            f_out += self.file_ext()

        return save_to_file(f_out, self, use_zip)


def my_to_json(obj: Any) -> str:
    """
    Serializes a given object to JSON.

    Parameters
    ----------
    obj : `Any`
        Object to be serialized.

    Returns
    -------
    `str`
        JSON data.
    """
    def __json_serialize(obj_: Any) -> dict:
        if isinstance(obj_, JsonSerializable):
            my_class_name = (obj_.__module__, obj_.__class__.__name__)
            return obj_.get_attributes() | {"__type__": my_class_name}
        elif isinstance(obj_, np.ndarray):
            return obj_.tolist()
        else:
            return obj_

    return json.dumps(obj, default=__json_serialize)


def my_load_from_json(data: str) -> Any:
    """
    Loads (i.e. deserializes) an object from given JSON data.

    Parameters
    ----------
    data : `str`
        JSON data.

    Returns
    -------
    `Any`
        Deserialized object.
    """
    def __object_hook(obj: dict) -> dict:
        if "__type__" in obj:
            module_name, class_name = obj["__type__"]
            cls = getattr(importlib.import_module(module_name), class_name)
            del obj["__type__"]

            for attr in obj:
                if isinstance(attr, dict):
                    obj[attr] = __object_hook(obj[attr])

            return cls(**obj)
        return obj

    return json.loads(data, object_hook=__object_hook)


class JsonSerializable(Serializable):
    """
    Base class for JSON serializable classes.
    Inherits from :class:`~epyt_flow.serialization.Serializable`.
    """

    def to_json(self) -> str:
        """
        Serializes this instance to JSON.

        Returns
        -------
        `str`
            JSON data.
        """
        return my_to_json(self)

    @staticmethod
    def load_from_json(data: str) -> Any:
        """
        Loads (i.e. deserializes) an instance of this class from given JSON data.

        Parameters
        ----------
        data : `str`
            JSON data.

        Returns
        -------
        `Any`
            Deserialized instance of this class.
        """
        return my_load_from_json(data)

    @staticmethod
    def load_from_json_file(f_in: str) -> Any:
        """
        Deserializes an instance of this class from a JSON file.

        Parameters
        ----------
        f_in : `str`
            Path to the JSON file from which to deserialize the object.

        Returns
        -------
        `Any`
            Deserialized object.
        """
        with open(f_in, "r", encoding="utf-8") as f:
            return my_load_from_json(f.read())

    def save_to_json_file(self, f_out: str) -> None:
        """
        Serializes this instance and stores it in a JSON file.

        Parameters
        ----------
        f_in : `str`
            Path to the JSON file where this serialized object will be stored.
        """
        if not f_out.endswith(self.file_ext()):
            f_out += self.file_ext()

        with open(f_out, "w", encoding="utf-8") as f:
            f.write(self.to_json())


def load(data: Union[bytes, BufferedIOBase]) -> Any:
    """
    Deserializes data.

    Parameters
    ----------
    data : `bytes` or `io.BufferedIOBase`
        Serialized data or stream from which serialized data can be read.

    Returns
    -------
    `Any`
        Deserialized data.
    """
    if isinstance(data, bytes):
        return my_unpackb(data)
    elif isinstance(data, BufferedIOBase):
        return my_unpackb(data.read())
    else:
        raise TypeError("Invalid type of 'data' -- must be either instance of 'bytes' or " +
                        f"'io.BufferedIOBase' but not of '{type(data)}'")


def dump(data: Any, stream_out: BufferedIOBase = None) -> Union[bytes, None]:
    """
    Serializes some given data to a byte array.

    Parameters
    ----------
    stream_out : `io.BufferedIOBase`, optional
        Stream to which the serialized object is written.
        If None, the serialized object is returned as a `bytes` array.

        The default is None.

    Returns
    -------
    `bytes`
        Serialized data if `stream_out` is None -- otherwise, nothing is returned.
    """
    if stream_out is None:
        return my_packb(data)
    else:
        if not isinstance(stream_out, BufferedIOBase):
            raise TypeError("'stream_out' must be an instance of 'io.BufferedIOBase' " +
                            f"but not of '{type(stream_out)}'")

        stream_out.write(my_packb(data))


def load_from_file(f_in: str, use_compression: bool = True) -> Any:
    """
    Deserializes data from a (compressed) file.

    Parameters
    ----------
    f_in : `str`
        Path to the file from which to deserialize the data.
    use_compression : `bool`, optional
        If True, the file `f_in` is supposed to be gzip compressed -- False,
        if no compression was used when serializing the data.

        The default is True.

    Returns
    -------
    `Any`
        Deserialized data.
    """
    inst = None

    if use_compression is False:
        with open(f_in, "rb") as f:
            inst = load(f.read())
    else:
        with gzip.open(f_in, "rb") as f:
            inst = load(f.read())

    if isinstance(inst, Serializable):
        inst._parent_path = pathlib.Path(f_in).parent.resolve()

    return inst


def save_to_file(f_out: str, data: Any, use_compression: bool = True) -> None:
    """
    Serializes data and stores it in a (compressed) file.

    Parameters
    ----------
    f_in : `str`
        Path to the file where the serialized data will be stored.
    use_compression : `bool`, optional
        If True, the file `f_in` will be gzip compressed -- False, if no compression is wanted.

        The default is True.
    """
    if use_compression is False:
        with open(f_out, "wb") as f:
            umsgpack.pack(data, f, ext_handlers=ext_handler_pack)
    else:
        with gzip.open(f_out, "wb") as f:
            f.write(dump(data))


# Add numpy.ndarray, networkx.Graph, and scipy.sparse.bsr_array support
def __encode_bsr_array(array: scipy.sparse.bsr_array
                       ) -> tuple[tuple[int, int], tuple[list[float], tuple[list[int], list[int]]]]:
    shape = array.shape
    data = []
    rows = []
    cols = []

    array_ = array.tocsr()   # Bug workaround: BSR arrays do not implement __getitem__
    for i, j in zip(*array_.nonzero()):
        rows.append(int(i))
        cols.append(int(j))
        data.append(float(array_[i, j]))

    return shape, (data, (rows, cols))


def __decode_bsr_array(ext_data: tuple[tuple[int, int],
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
                                             umsgpack.packb(__encode_bsr_array(arr)))}
ext_handler_unpack = {NUMPY_ARRAY_ID: lambda ext: np.array(umsgpack.unpackb(ext.data)),
                      NETWORKX_GRAPH_ID:
                      lambda ext: networkx.node_link_graph(umsgpack.unpackb(ext.data)),
                      SCIPY_BSRARRAY_ID: lambda ext: __decode_bsr_array(umsgpack.unpackb(ext.data))}
