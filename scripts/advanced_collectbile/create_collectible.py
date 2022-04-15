from scripts.advanced_collectbile import deploy_and_create
from brownie import AdvancedCollectible
from scripts.helpful_scripts import fund_with_link, get_account


def main():
    create()


def create():
    account = get_account()
    advance_collectible = AdvancedCollectible[-1]
    fund_with_link(advance_collectible.address)
    tx = advance_collectible.createCollectible({"from": account})
    print("new token created")
    tx.wait(1)
