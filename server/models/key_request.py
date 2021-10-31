# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import List, Dict  # noqa: F401

from server import util
from server.models.base_model_ import Model


class KeyRequest(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, number: int = None, size: int = None, additional_slave_sae_i_ds: List[str] = None,
                 extension_mandatory: List[object] = None, extension_optional: List[object] = None):  # noqa: E501
        """KeyRequest - a model defined in Swagger

        :param number: The number of this KeyRequest.  # noqa: E501
        :type number: int
        :param size: The size of this KeyRequest.  # noqa: E501
        :type size: int
        :param additional_slave_sae_i_ds: The additional_slave_sae_i_ds of this KeyRequest.  # noqa: E501
        :type additional_slave_sae_i_ds: List[str]
        :param extension_mandatory: The extension_mandatory of this KeyRequest.  # noqa: E501
        :type extension_mandatory: List[object]
        :param extension_optional: The extension_optional of this KeyRequest.  # noqa: E501
        :type extension_optional: List[object]
        """
        self.swagger_types = {
            'number': int,
            'size': int,
            'additional_slave_sae_i_ds': List[str],
            'extension_mandatory': List[object],
            'extension_optional': List[object]
        }

        self.attribute_map = {
            'number': 'number',
            'size': 'size',
            'additional_slave_sae_i_ds': 'additional_slave_SAE_IDs',
            'extension_mandatory': 'extension_mandatory',
            'extension_optional': 'extension_optional'
        }
        self._number = number
        self._size = size
        self._additional_slave_sae_i_ds = additional_slave_sae_i_ds
        self._extension_mandatory = extension_mandatory
        self._extension_optional = extension_optional

    @classmethod
    def from_dict(cls, dikt) -> 'KeyRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The KeyRequest of this KeyRequest.  # noqa: E501
        :rtype: KeyRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def number(self) -> int:
        """Gets the number of this KeyRequest.

        (Option) number of keys requested, default value is 1  # noqa: E501

        :return: The number of this KeyRequest.
        :rtype: int
        """
        return self._number

    @number.setter
    def number(self, number: int):
        """Sets the number of this KeyRequest.

        (Option) number of keys requested, default value is 1  # noqa: E501

        :param number: The number of this KeyRequest.
        :type number: int
        """

        self._number = number

    @property
    def size(self) -> int:
        """Gets the size of this KeyRequest.

        (Option) Size of each key in bits, default value is defined as key_size in Status data format  # noqa: E501

        :return: The size of this KeyRequest.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size: int):
        """Sets the size of this KeyRequest.

        (Option) Size of each key in bits, default value is defined as key_size in Status data format  # noqa: E501

        :param size: The size of this KeyRequest.
        :type size: int
        """

        self._size = size

    @property
    def additional_slave_sae_i_ds(self) -> List[str]:
        """Gets the additional_slave_sae_i_ds of this KeyRequest.

        (Option) Array of IDs of slave SAEs. It is used for specifying two or more slave SAEs to share identical keys. The maximum number of IDs is defined as max_SAE_ID_count in Status data format.  # noqa: E501

        :return: The additional_slave_sae_i_ds of this KeyRequest.
        :rtype: List[str]
        """
        return self._additional_slave_sae_i_ds

    @additional_slave_sae_i_ds.setter
    def additional_slave_sae_i_ds(self, additional_slave_sae_i_ds: List[str]):
        """Sets the additional_slave_sae_i_ds of this KeyRequest.

        (Option) Array of IDs of slave SAEs. It is used for specifying two or more slave SAEs to share identical keys. The maximum number of IDs is defined as max_SAE_ID_count in Status data format.  # noqa: E501

        :param additional_slave_sae_i_ds: The additional_slave_sae_i_ds of this KeyRequest.
        :type additional_slave_sae_i_ds: List[str]
        """

        self._additional_slave_sae_i_ds = additional_slave_sae_i_ds

    @property
    def extension_mandatory(self) -> List[object]:
        """Gets the extension_mandatory of this KeyRequest.

        (Option) Array of extension parameters specified as name/value pairs that KME shall handle or return an error. Parameter values may be of any type, including objects.  # noqa: E501

        :return: The extension_mandatory of this KeyRequest.
        :rtype: List[object]
        """
        return self._extension_mandatory

    @extension_mandatory.setter
    def extension_mandatory(self, extension_mandatory: List[object]):
        """Sets the extension_mandatory of this KeyRequest.

        (Option) Array of extension parameters specified as name/value pairs that KME shall handle or return an error. Parameter values may be of any type, including objects.  # noqa: E501

        :param extension_mandatory: The extension_mandatory of this KeyRequest.
        :type extension_mandatory: List[object]
        """

        self._extension_mandatory = extension_mandatory

    @property
    def extension_optional(self) -> List[object]:
        """Gets the extension_optional of this KeyRequest.

        (Option) Array of extension parameters specified as name/value pairs that KME may ignore. Parameter values may be of any type, including objects.  # noqa: E501

        :return: The extension_optional of this KeyRequest.
        :rtype: List[object]
        """
        return self._extension_optional

    @extension_optional.setter
    def extension_optional(self, extension_optional: List[object]):
        """Sets the extension_optional of this KeyRequest.

        (Option) Array of extension parameters specified as name/value pairs that KME may ignore. Parameter values may be of any type, including objects.  # noqa: E501

        :param extension_optional: The extension_optional of this KeyRequest.
        :type extension_optional: List[object]
        """

        self._extension_optional = extension_optional
