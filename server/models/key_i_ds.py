# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from server.models.base_model_ import Model
from server.models.key_i_ds_key_i_ds import KeyIDsKeyIDs  # noqa: F401,E501
from server import util


class KeyIDs(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, key_i_ds: List[KeyIDsKeyIDs] = None, key_i_ds_extension: object = None):  # noqa: E501
        """KeyIDs - a model defined in Swagger

        :param key_i_ds: The key_i_ds of this KeyIDs.  # noqa: E501
        :type key_i_ds: List[KeyIDsKeyIDs]
        :param key_i_ds_extension: The key_i_ds_extension of this KeyIDs.  # noqa: E501
        :type key_i_ds_extension: object
        """
        self.swagger_types = {
            'key_i_ds': List[KeyIDsKeyIDs],
            'key_i_ds_extension': object
        }

        self.attribute_map = {
            'key_i_ds': 'key_IDs',
            'key_i_ds_extension': 'key_IDs_extension'
        }
        self._key_i_ds = key_i_ds
        self._key_i_ds_extension = key_i_ds_extension

    @classmethod
    def from_dict(cls, dikt) -> 'KeyIDs':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The KeyIDs of this KeyIDs.  # noqa: E501
        :rtype: KeyIDs
        """
        return util.deserialize_model(dikt, cls)

    @property
    def key_i_ds(self) -> List[KeyIDsKeyIDs]:
        """Gets the key_i_ds of this KeyIDs.

        Array of key IDs  # noqa: E501

        :return: The key_i_ds of this KeyIDs.
        :rtype: List[KeyIDsKeyIDs]
        """
        return self._key_i_ds

    @key_i_ds.setter
    def key_i_ds(self, key_i_ds: List[KeyIDsKeyIDs]):
        """Sets the key_i_ds of this KeyIDs.

        Array of key IDs  # noqa: E501

        :param key_i_ds: The key_i_ds of this KeyIDs.
        :type key_i_ds: List[KeyIDsKeyIDs]
        """

        self._key_i_ds = key_i_ds

    @property
    def key_i_ds_extension(self) -> object:
        """Gets the key_i_ds_extension of this KeyIDs.

        (Option) for future use  # noqa: E501

        :return: The key_i_ds_extension of this KeyIDs.
        :rtype: object
        """
        return self._key_i_ds_extension

    @key_i_ds_extension.setter
    def key_i_ds_extension(self, key_i_ds_extension: object):
        """Sets the key_i_ds_extension of this KeyIDs.

        (Option) for future use  # noqa: E501

        :param key_i_ds_extension: The key_i_ds_extension of this KeyIDs.
        :type key_i_ds_extension: object
        """

        self._key_i_ds_extension = key_i_ds_extension
