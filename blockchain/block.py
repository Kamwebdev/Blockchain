# -*- coding: utf-8 -*-
import json
from datetime import datetime
from hashlib import sha256


class Block(object):
    """It is a conceptual representation of the class of a simple block
     fragment that makes up the entire blockchain.

    :param index: int
    :param transactions: array
    :param timestamp: datetime
    :param previous_hash: str
    :param nonce: int, optional
    """

    __name__ = "Mini block class"
    __author__ = "Kamil Mirończuk"
    __license__ = "GNU General Public License v3.0"
    __version__ = "1.0"
    __status__ = "production"

    def __init__(
        self, index, transactions, timestamp, previous_hash, nonce=0
    ):
        """Constructor method"""
        super().__init__()
        self.__index = index
        self.__transactions = transactions
        self.__timestamp = datetime.timestamp(timestamp)
        self.__previous_hash = previous_hash
        self.__nonce = nonce
        self.hash = "0" * 64

    def __call__(self) -> str:
        """Return block main information.

        :return: the index and stored transactions data
        :rtype: str
        """
        return "Block nr {} -> data {}".format(
            self.__index, self.__transactions
        )

    @property
    def compute_hash(self) -> str:
        """Generate actual block hash.

        :return: block hash
        :rtype: str
        """
        block_string: str = json.dumps(
            dict(
                filter(
                    lambda elem: elem[0] != "_Block__hash",
                    self.__dict__.items(),
                )
            ),
            sort_keys=True,
        )
        return sha256(block_string.encode()).hexdigest()

    @property
    def hash(self) -> str:
        """Get actual block hash.

        :return: block hash
        :rtype: str
        """
        return self.__hash

    @hash.setter
    def hash(self, value):
        """Set block hash.

        :raises TypeError: Hash type is not valid
        :raises ValueError: Hash character number is not valid
        :return: block hash
        :rtype: str
        """
        if type(value) != str:
            raise TypeError("Hash must be a string.")
        if len(value) != 64:
            raise ValueError("Hash must have 64 characters.")
        self.__hash: str = value

    @property
    def index(self) -> int:
        """Get actual block index.

        :return: block index
        :rtype: int
        """
        return self.__index

    @property
    def previous_hash(self) -> str:
        """Get last block hash.

        :return: last block hash
        :rtype: str
        """
        return self.__previous_hash

    @property
    def transactions(self) -> str:
        """Get all stored transatcions

        :return: all transactions
        :rtype: str
        """
        return self.__transactions
