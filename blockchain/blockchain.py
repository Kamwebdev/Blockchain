# -*- coding: utf-8 -*-
from datetime import datetime

from blockchain.block import Block


class Blockchain(object):
    """It is a conceptual representation of the class of a simple
    blockchain.

    :param difficulty: int
    """

    __name__ = "Mini blockchain class"
    __author__ = "Kamil Mirończuk"
    __license__ = "GNU General Public License v3.0"
    __version__ = "1.0"
    __status__ = "production"

    def __init__(self, difficulty=2, backend=None):
        """Constructor method"""
        self.__backend = backend
        self.__difficulty = difficulty
        self.__chain = []
        self.__unconfirmed_transactions = []
        self.__hash = None
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create first blockchain block.

        :return: None
        """
        genesis_block: Block = Block(0, [], datetime.now(), "0")
        genesis_block.hash = genesis_block.compute_hash
        self.__chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        """Return last block added to blockchain.

        :return: last block
        :rtype: Block
        """
        return self.__chain[-1]

    def add_new_transaction(self, data):
        """Add new unconfirmed transaction to Blockchain.

        :param data: str
        :return: None
        """
        if self.__backend:
            self.save_transactions(data)
        else:
            self.__unconfirmed_transactions.append(data)

    def proof_of_work(self, block) -> str:
        """Return valid computed hash for Block.

        :param block: Block
        :return: str
        """
        block.nonce = 0
        computed_hash = block.compute_hash
        while not computed_hash.startswith("0" * self.__difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash
        return computed_hash

    def mine(self) -> bool:
        """Add unconfirmed transactions as new Block.

        :return: true when the block has been mined
        :rtype: bool
        """
        if self.__backend:
            self.read_transactions()
        if not self.__unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.__unconfirmed_transactions,
            timestamp=datetime.now(),
            previous_hash=last_block.hash,
        )
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.__unconfirmed_transactions = []
        if self.__backend:
            open(self.__backend.strpath, "w").close()
        return True

    def is_valid_proof(self, block, block_hash) -> bool:
        """Check if is valid proof of work.

        :return: true when block start with "0" x difficulty
        :rtype: bool
        """
        return (
            block_hash.startswith("0" * self.__difficulty)
            and block_hash == block.compute_hash
        )

    def add_block(self, new_block, proof) -> bool:
        """Add block to Blockchain.

        :return: true when block has been appended
        :rtype: bool
        """
        previous_hash = self.last_block.hash
        if previous_hash != new_block.previous_hash:
            return False
        if not self.is_valid_proof(new_block, proof):
            return False

        new_block.hash = proof
        self.__chain.append(new_block)
        return True

    def get_full_block(self):
        """Print full blockchain into console.

        :return: None
        """
        for block in self.__chain:
            print(block())

    def verify_full_block_history(self):
        """Verify Blockchain history.

        :raises Exception: No backend defined
        :return: true, if block is correct
        """
        for block in self.__chain:
            if block.index != 0:
                block_before_hash = self.__chain[
                    block.index - 1
                ].compute_hash
                if block_before_hash == block.previous_hash:
                    print("Correct block")
                else:
                    raise Exception("Block invalid")
        return True

    def save_transactions(self, data):
        """Save actual transactions to file.

        :raises Exception: No backend defined
        :return: true, if all transactions has been saved
        """
        if not self.__backend:
            raise Exception("No backend defined.")
        self.__backend.write("{}\n".format(data))

        return True

    def read_transactions(self):
        """Read actual transactions from file.

        :raises Exception: No backend defined
        :raises Exception: Unconfirmed transactions lists is not empty
        :return: true, if all transactions has been read
        """
        if not self.__backend:
            raise Exception("No backend defined.")

        for line in self.__backend.readlines():
            self.__unconfirmed_transactions.append(line.strip())
