import requests, json

api = 'https://dcrdata.decred.org/api'


def dcrdata_req(req):
    response = requests.get(api+req).json()
    return response

def get_last_height():
    last = dcrdata_req('/block/best')
    last_height = last['height']
    return last_height

def get_height(block):
    height = block['height']
    return height

def get_last_blocks(amount):
    last_blocks = dcrdata_req(f'/block/range/{get_last_height()-amount+1}/{get_last_height()}')
    # print(last_blocks)
    return(last_blocks)

block_attr_list = ['heigh','size','hash','ticketpool']

### TRANSACTIONS

def get_block_txs(block_index):
    block_txs = dcrdata_req(f'/block/{block_index}/tx')
    return block_txs

def get_tx_total_output(tx):
    tx_outputs = dcrdata_req(f'/tx/{tx}/out')
    total_output = 0
    for each in tx_outputs:
        total_output += each['value']
    return total_output
    # print(tx_outputs)
    # print(total_output)

def get_block_total_output(block):
    block_txs = get_block_txs(block)
    block_total_output = 0
    for each in block_txs['tx']:
        block_total_output += get_tx_total_output(each)
    return block_total_output
    # print(block_total_output)



get_block_total_output(426215)

blocks = get_last_blocks(100)
blocks_outputs = []
for each in blocks:
    blocks_outputs.append(get_block_total_output(each['height']))
print(blocks_outputs)



def normalize_list(list):
    norm = [float(i)/max(list) for i in list]
    return norm

norm = normalize_list(blocks_outputs)

with open('100_block_sample.json','w') as json_file:
    json.dump(blocks_outputs, json_file,indent=1)

with open('100_block_sample_norm.json','w') as json_file:
    json.dump(norm, json_file,indent=1)    

#get_last_blocks(3)

# get_block_tx(get_last_height)



    