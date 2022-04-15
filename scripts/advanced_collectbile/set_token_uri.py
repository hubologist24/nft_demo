from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import get_account, get_breed, OPENSEA_URL

dog_metadata_dic = {
    "PUG": "https://ipfs.io/ipfs/Qme1xyzT4Qw4ckzXktJCV28ZupDjDpjR4Tec1wWQwh2N4P?filename=0-SHIBA_INU.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def main():
    print(f"wonking on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"you have {number_of_collectibles} tokens")
    for tokenId in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(tokenId))
        # if not number_of_collectibles.tokenURI(tokenId).startswith("https://"):
        if not advanced_collectible.tokenURI(tokenId).startswith("https://"):
            print("setting tokenuri")
            set_tokenURI(tokenId, advanced_collectible, dog_metadata_dic[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenUri(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"awesome you can see your url at{OPENSEA_URL.format(nft_contract.address,token_id)}"
    )
