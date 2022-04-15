from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible

sample_token_uri = "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8"


def deploy_and_create():
    account = get_account()
    simpleCollectible = SimpleCollectible.deploy({"from": account})
    tx = simpleCollectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"you can view your NFT a {OPENSEA_URL.format(simpleCollectible.address,simpleCollectible.tokenCounter()-1)}"
    )
    print("refresh meta data in 20 minutes")
    return simpleCollectible


def main():
    deploy_and_create()
