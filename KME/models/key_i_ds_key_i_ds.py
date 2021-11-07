# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from KME.models.base_model_ import Model
from KME import util


class KeyIDsKeyIDs(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, key_id: str = None, key_id_extension: object = None):  # noqa: E501
        """KeyIDsKeyIDs - a model defined in Swagger

        :param key_id: The key_ID of this KeyIDsKeyIDs.  # noqa: E501
        :type key_id: str
        :param key_id_extension: The key_ID_extension of this KeyIDsKeyIDs.  # noqa: E501
        :type key_id_extension: object
        """
        self.swagger_types = {
            'key_ID': str,
            'key_ID_extension': object
        }

        self.attribute_map = {
            'key_ID': 'key_ID',
            'key_ID_extension': 'key_ID_extension'
        }
        self._key_id = key_id
        self._key_id_extension = key_id_extension

    @classmethod
    def from_dict(cls, dikt) -> 'KeyIDsKeyIDs':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The KeyIDs_key_IDs of this KeyIDsKeyIDs.  # noqa: E501
        :rtype: KeyIDsKeyIDs
        """
        return util.deserialize_model(dikt, cls)

    @property
    def key_id(self) -> str:
        """Gets the key_ID of this KeyIDsKeyIDs.

        ID of the key in UUID format  # noqa: E501

        :return: The key_ID of this KeyIDsKeyIDs.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id: str):
        """Sets the key_ID of this KeyIDsKeyIDs.

        ID of the key in UUID format  # noqa: E501

        :param key_id: The key_ID of this KeyIDsKeyIDs.
        :type key_id: str
        """
        if key_id is None:
            raise ValueError("Invalid value for `key_ID`, must not be `None`")  # noqa: E501

        self._key_id = key_id

    @property
    def key_id_extension(self) -> object:
        """Gets the key_ID_extension of this KeyIDsKeyIDs.

        (Option) for future use  # noqa: E501

        :return: The key_ID_extension of this KeyIDsKeyIDs.
        :rtype: object
        """
        return self._key_id_extension

    @key_id_extension.setter
    def key_id_extension(self, key_id_extension: object):
        """Sets the key_ID_extension of this KeyIDsKeyIDs.

        (Option) for future use  # noqa: E501

        :param key_id_extension: The key_ID_extension of this KeyIDsKeyIDs.
        :type key_id_extension: object
        """

        self._key_id_extension = key_id_extension
