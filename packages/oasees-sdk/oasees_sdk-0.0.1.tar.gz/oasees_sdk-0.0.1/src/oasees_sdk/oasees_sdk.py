from web3 import Web3
from dotenv import load_dotenv
import ipfshttpclient
import json
import requests
import os


load_dotenv()
IPFS_HOST = os.getenv('IPFS_HOST')
BLOCKCHAIN_HOST = os.getenv('BLOCKCHAIN_HOST')
account_addr = ''

###### INITIALIZE THE CONNECTIONS TO THE SERVICES AND CONTRACTS INVOLVED ######

web3 = Web3(Web3.HTTPProvider(f"http://{BLOCKCHAIN_HOST}:8545"))                    # BLOCKCHAIN
response = requests.get(f'http://{IPFS_HOST}:6002/get_marketplace_ipfs_hash')
data = response.json()
ipfs_hash = data['ipfs_hash']

client = ipfshttpclient.connect(f"/ip4/{IPFS_HOST}/tcp/5001")                       # IPFS
ipfs_json = client.cat(ipfs_hash)
ipfs_json = ipfs_json.decode("UTF-8")
ipfs_json = json.loads(ipfs_json)

nft_abi = ipfs_json['nft_abi']['abi']                
nft_address = ipfs_json['nft_address']
marketplace_abi = ipfs_json['marketplace_abi']['abi']
marketplace_address = ipfs_json['marketplace_address']


nft = web3.eth.contract(address=nft_address, abi=nft_abi)                           # NFT contract
nft_marketplace = web3.eth.contract(address=marketplace_address, 
                                    abi=marketplace_abi)                            # Marketplace contract




def login():
    # Placeholder association with the user's purchased items
    global account_addr
    address_given = input("Please provide your account's address: ")
    if (Web3.isAddress(address_given)):
        account_addr = address_given
    else:
        print("The address you provided is invalid. Try again: ")
        login()


def getPurchases():
    # Retrieves the account's purchases and returns them in a list
    if (account_addr!=''):

        _filter=nft_marketplace.events.Bought.createFilter(fromBlock="0x0", argument_filters={"buyer":account_addr})
        results=_filter.get_new_entries()

        purchases=[]

        for r in results:
            token_id = r['args']['tokenId']
            token_uri=nft.functions.tokenURI(token_id).call()

            nft_ipfs_json = client.cat(token_uri)
            nft_ipfs_json = nft_ipfs_json.decode("UTF-8")
            nft_ipfs_json = json.loads(json.loads(nft_ipfs_json))
            purchases.append(nft_ipfs_json)

        
        return purchases




def list():
    # Retrieves the filenames of the purchased items.

    if not account_addr:
        login()

    purchases = getPurchases()
    for purchase in purchases:
        print (purchase['title'])



def deploy(name:str):
    # Indicative method of a specific purchased item's deployment

    if not account_addr:
        login()

    purchases = getPurchases()

    found = False
    for purchase in purchases:
        if found:
            break

        if(purchase['title']==name):
            algo = client.cat(purchase['contentURI'])

            with open(purchase['title'] + ".py", "wb") as binary_file:
                binary_file.write(algo)

            found = True

    if not found:
        print("The file you requested was not found in your purchases.")
