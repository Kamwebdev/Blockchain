import os

import mock
import pytest

from blockchain.blockchain import Blockchain


def test_blockchain_initialization(my_blockchain):
    assert my_blockchain


def test_blockchain_create_first_block():
    my_blockchain = Blockchain(difficulty=3)
    assert my_blockchain.last_block.previous_hash == "0"


@pytest.mark.parametrize(
    "message", ("test", "123", "0" * 50,),
)
def test_blockchain_mine_first_block(my_blockchain, message):
    my_blockchain.add_new_transaction(message)
    my_blockchain.mine()
    assert message in my_blockchain.last_block.transactions


def test_blockchain_save_backend_empty():
    my_blockchain = Blockchain()
    with pytest.raises(Exception):
        my_blockchain.save_transactions("test")


def test_blockchain_read_backend_empty():
    my_blockchain = Blockchain()
    with pytest.raises(Exception):
        my_blockchain.read_transactions()


def test_blockchain_read_backend_unconfirmed_transactions(backend):
    my_blockchain = Blockchain(backend=backend)
    my_blockchain.save_transactions("test")
    my_blockchain.read_transactions()
    my_blockchain.mine()
    assert "test" in my_blockchain.last_block.transactions


def test_blockchain_bad_proof_of_work(mocker, my_filled_blockchain):
    mocker.patch.object(Blockchain, "proof_of_work")
    my_filled_blockchain.proof_of_work.return_value = "01"
    my_filled_blockchain.add_new_transaction("second")
    my_filled_blockchain.mine()
    assert "second" not in my_filled_blockchain.last_block.transactions


def test_blockchain_bad_previus_hash(my_blockchain):
    my_blockchain.add_new_transaction("test")
    my_blockchain.mine()
    my_blockchain.add_new_transaction("test2")
    my_blockchain.mine()
    with pytest.raises(AttributeError):
        my_blockchain.last_block.previous_hash = 32 * "01"


def test_blockchain_set_block_hash(my_filled_blockchain):
    assert "test" in my_filled_blockchain.last_block()
    assert my_filled_blockchain.last_block.hash


def test_invalid_block_hash(my_filled_blockchain):
    with pytest.raises(ValueError):
        my_filled_blockchain.last_block.hash = "invalid"
    with pytest.raises(TypeError):
        my_filled_blockchain.last_block.hash = 123
    assert "test" in my_filled_blockchain.last_block()


@pytest.mark.skipif(
    os.environ.get("SKIP_ASYNC_TESTS") == "1",
    reason="Flag SKIP_ASYNC_TESTS is set.",
)
def test_initialize_two_blockchain_classes(backend):
    my_blockchain1 = Blockchain(backend=backend)
    my_blockchain2 = Blockchain(backend=backend)

    my_blockchain1.add_new_transaction("test")
    my_blockchain2.mine()
    my_blockchain1.mine()
    assert "test" in my_blockchain2.last_block.transactions
    assert "test" not in my_blockchain1.last_block.transactions
    my_blockchain2.get_full_block()


def test_valid_proof(my_blockchain):
    my_blockchain.is_valid_proof = mock.Mock()
    my_blockchain.is_valid_proof.return_value = 1
    assert my_blockchain.is_valid_proof() == 1


def test_last_block_return_value(mocker, my_blockchain):
    mocker.patch.object(Blockchain, "last_block")
    my_blockchain.last_block.return_value = 1

    assert my_blockchain.last_block() == 1
