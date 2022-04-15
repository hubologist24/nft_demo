from eth_account import Account
from scripts.advanced_collectbile.deploy_and_create import deploy_and_create
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
)
from brownie import network
import pytest


def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    advanced_collectible, creation_tx = deploy_and_create()
    request_Id = creation_tx.events["requestedCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_Id, random_number, advanced_collectible.address, {"from": get_account()}
    )
    assert advanced_collectible.tokenCounter() > 0
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
