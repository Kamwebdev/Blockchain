import pytest

from blockchain.blockchain import Blockchain


def pytest_runtest_setup():
    print("Start test")


@pytest.fixture()
def backend(tmpdir):
    temp_file = tmpdir.join("test.txt")
    temp_file.write("")
    return temp_file


@pytest.fixture(params=[None, "backend"], name="my_blockchain")
def fixture_my_blockchain(backend, request):
    if request.param == "backend":
        my_blockchain = Blockchain(backend=backend)
    else:
        my_blockchain = Blockchain()
    yield my_blockchain
    assert my_blockchain.verify_full_block_history()


@pytest.fixture(name="my_filled_blockchain")
def fixture_my_filled_blockchain(my_blockchain, request):
    my_blockchain.add_new_transaction("test")
    my_blockchain.mine()
    yield my_blockchain
    assert my_blockchain.verify_full_block_history()
