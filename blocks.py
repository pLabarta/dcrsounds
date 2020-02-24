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



def get_last_blocks_tx_outputs(amount_of_blocks):
    blocks = get_last_blocks(amount_of_blocks)
    blocks_outputs = []
    for each in blocks:
        blocks_outputs.append(get_block_total_output(each['height']))
    print(blocks_outputs)
    return blocks_outputs

def normalize_list(list):
    norm = [float(i)/max(list) for i in list]
    return norm


### REGENERATE SAMPLES

block_sample = get_last_blocks_tx_outputs(100)
norm = normalize_list(block_sample)

with open('100_block_tx_sample.json','w') as json_file:
    json.dump(block_sample, json_file,indent=1)

with open('100_block_tx_sample_norm.json','w') as json_file:
    json.dump(norm, json_file,indent=1) 

### END REGENERATE SAMPLES

### TICKET TRANSACTIONS

def get_block_stx(block):
    block_txs = get_block_txs(get_last_height())
    stx = block_txs['stx']
    return stx

# get_block_stx(get_last_height())

def get_tx_details(tx):
    tx_details = dcrdata_req(f'/tx/{tx}?spends=true')
    return tx_details

# get_tx_details('4917dd9313e11ff12087380a9797eb3953ac399e5642e29761b62928e2815f5a')

voting_block = get_block_txs(get_last_height())
print(voting_block)

def tx_is_vote(tx):
    tx_details = get_tx_details(tx)
    if 'stakebase' in tx_details['vin'][0]:
        # print('Esta TX es un voto')
        return True
    else:
        # print('Esta TX NO es un voto')
        return False

# tx_is_vote('7e66a8e348fac27015a36ee46fcd82508542793bc6c3130879865fef46445b79')

def tx_is_newticket(tx):
    tx_details = get_tx_details(tx)
    # print(tx_details['vout'])
    if ['type'] in tx_details['vout']:
        if tx_details['vout'][0]['type'] == 'stakesubmission':
            # print('Esta TX es una compra de ticket')
            return True
        else:
            # print('Esta TX no es una compra de ticket')
            return False
    else:
        # print('Esta TX no es una compra de ticket')
        return False

def count_votes(block):
    block_txs = get_block_txs(block)
    vote_count = 0
    for each in block_txs['stx']:
        if tx_is_vote(each):
            vote_count += 1
        else:
            pass
    return vote_count

# print(count_votes(get_last_height()))

def get_last_heights(number):
    last = get_last_height()
    first = int(get_last_height()) - number + 1
    height_list = []
    for each in range(number):
        height_list.append(first+each)
    return height_list

## VOTE SAMPLE

vote_list = []
for each in get_last_heights(100):
    vote_list.append(count_votes(each))
print(vote_list)

with open('100_block_vote_sample.json','w') as json_file:
    json.dump(vote_list, json_file,indent=1)
