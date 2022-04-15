from eth_account import Account
from scripts.advanced_collectbile.deploy_and_create import deploy_and_create
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
)
from brownie import network
import pytest, time


def test_can_create_simple_collectible_int():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    advanced_collectible, creation_tx = deploy_and_create()
    time.sleep(60)
    assert advanced_collectible.tokenCounter() > 0
