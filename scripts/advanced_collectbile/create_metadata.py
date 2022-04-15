from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests, json, time, os

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def main2():
    # print(Path.cwd())
    # print(Path(__file__).resolve())
    p1 = str(Path.cwd()) + "/img/"
    print(p1)


def main():
    advanced_collectible = AdvancedCollectible[-1]
    collectible_number = advanced_collectible.tokenCounter()
    print(f"you have {collectible_number} number of collectibles")
    for token_id in range(collectible_number):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = f"{str(Path.cwd())}/metadata/{network.show_active()}/{token_id}-{breed}.json"
        print(metadata_file_name)
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exist delete to overwrite")
        else:
            print(f"creating meta file {metadata_file_name} ")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pupp! "
            print(collectible_metadata)
            main_path = Path.cwd()
            image_path = (
                str(Path.cwd()) + "/img/" + breed.lower().replace("_", "-") + ".png"
            )
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == True:
                image_uri = upload_ipfs(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
            # image_path = ".img/pug.png"
            collectible_metadata["image"] = image_uri
            # collectible_metadata["image"]=?
            # ipfs_url = "http://127.0.0.1:5001"
            file = open(metadata_file_name, "w")
            try:
                json.dump(collectible_metadata, file)
            finally:
                file.close()
            if os.getenv("UPLOAD_IPFS") == True:
                upload_ipfs(metadata_file_name)


def upload_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        end_point = "/api/v0/add"
        response = requests.post(ipfs_url + end_point, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
