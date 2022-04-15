from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    config,
    network,
    get_contract,
    fund_with_link,
)
from brownie import AdvancedCollectible

sample_token_uri = "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8"


def deploy_and_create():
    account = get_account()
    advance_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    fund_with_link(advance_collectible.address)
    tx = advance_collectible.createCollectible({"from": account})
    tx.wait(1)
    print(
        f"you can view your NFT a {OPENSEA_URL.format(advance_collectible.address,advance_collectible.tokenCounter()-1)}"
    )
    print("refresh meta data in 20 minutes")
    print("new token created")
    return advance_collectible, tx


def main():
    deploy_and_create()
