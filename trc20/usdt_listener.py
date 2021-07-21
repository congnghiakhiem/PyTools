import sys
from time import sleep
from tronpy import Tron
from tronpy.keys import to_base58check_address
from tronpy.providers import HTTPProvider

API_KEY = "25dba915-xxx-yyyy-zzzz-34c683cdecea"
MAIN_NET="https://api.trongrid.io"
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

def check_trasaction(trans):
    for trx in trans:
        trx_id = trx["txID"]
        
        if trx["ret"][0]["contractRet"] == "SUCCESS":
            contract = trx["raw_data"]["contract"][0]
            contract_type = contract["type"]

            if contract_type == "TriggerSmartContract":
                contract_address = contract["parameter"]["value"]["contract_address"]
                if contract_address == USDT_CONTRACT:
                    print(trx_id)
                    data = contract["parameter"]["value"]["data"]
                    
                    if data[:8] == "a9059cbb":
                        to_addr = to_base58check_address('41' + (data[8:72])[-40:])
                        print('To', to_addr)
                        amount = int(data[-64:], 16)
                        print('Amount', amount / 1_000_000)
                    elif data[:8] == "23b872dd":
                        from_addr = to_base58check_address('41' + (data[8:72])[-40:])
                        print('From', from_addr)
                        to_addr = to_base58check_address('41' + (data[72:136])[-40:])
                        print('To', to_addr)
                        amount = int(data[-64:], 16)
                        print('Amount', amount / 1_000_000)

def listen_usdt_transfer():
    provider = HTTPProvider(endpoint_uri=MAIN_NET, api_key=API_KEY)
    client = Tron(provider=provider)
    start_block = client.get_latest_block_number()

    # block = await client.get_block(start_block)
    # check_trasaction(block["transactions"])

    while (start_block):
        print(start_block)
        try:
            block = client.get_block(start_block)
            check_trasaction(block["transactions"])
            start_block = start_block + 1
            sleep(5)
        except:
            print(str(sys.exc_info()))
        
                


        


if __name__ == "__main__":
    listen_usdt_transfer()
