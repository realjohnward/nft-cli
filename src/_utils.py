from web3 import Web3 
import pandas as pd 
import matplotlib.pyplot as plt 
import requests 
from datetime import datetime 
from argparse import ArgumentParser 
import json 
import webbrowser 
import jinja2 
import logging 
from io import BytesIO 
from base64 import b64encode 

with open("./stylesheet.css") as f:
    stylesheet_txt = f.read()
    f.close()

defaults = json.load(open("../defaults.json"))

parser = ArgumentParser()
parser.add_argument("contract")
parser.add_argument("template")
parser.add_argument("ids")
parser.add_argument("--fromBlock")
parser.add_argument("--toBlock")

args = parser.parse_args()
template_name = args.template 

with open(f"templates/{template_name}.txt", "r") as f:
    template = f.read()
    f.close() 

# list of punk ids (separate by comma)
ids = args.ids.split(",")
save = False 
prompt_save = True 

# Passed to template as an argument
contract = args.contract 
config = json.load(open(f"./contracts/{contract}/config.json"))
contract_addr_str = config['address']
contract_address = Web3.toChecksumAddress(contract_addr_str)

# Web3 client for connecting to Ethereum mainnet
w3 = Web3(Web3.HTTPProvider(defaults['mainnet_url']))

# Contract interface 
abi = json.load(open(f"./contracts/{contract}/abi.json"))
contract = w3.eth.contract(address=contract_address, abi=abi)

# latest block
latest_block_number = w3.eth.get_block('latest')['number']

# Block Numbers from command line 
fromBlock = args.fromBlock 
if fromBlock in [None, ""]:
    fromBlock = 0
else:
    fromBlock = int(fromBlock)

toBlock = args.toBlock 
if toBlock in [None, ""]:
    toBlock = latest_block_number
else:
    toBlock = int(toBlock)

print(f"FROM BLOCK: {fromBlock} ; TO BLOCK: {toBlock}")

def chart(ax, w=100, h=100):
    if ax:
        buf = BytesIO()
        plt.savefig(buf)
        buf.seek(0)
        img_html = f'<img width={w} height={h} src="data:image/png;base64,{b64encode(buf.getvalue()).decode()}" />'
        return img_html
    else:
        return f'<img src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=" width={w} height={h} alt="" />'

def parse_txn_receipts(event_name, id_key, fromBlock=fromBlock, toBlock=toBlock):
    epoch_size = toBlock - fromBlock
    
    def get_epochs(fb,tb,es):
        current = fb 
        epochs = []             
        while True:
            next_current = current + es 
            if next_current >= toBlock:
                epochs.append((current, 'latest'))
                break 
            else:
                epochs.append((current,next_current))
                current = next_current 
        return epochs 
    
    def get_records(fb,tb,esize):
        records = []
        _epochs = get_epochs(fb,tb,esize)
        for e in _epochs:
            fb, tb = e 
            # query for events pertaining to each NFT
            for nft_id in ids:
                if nft_id == "all":
                    arg_filters = {}
                else:
                    arg_filters = {id_key: int(nft_id)}
                
                event_filter = getattr(contract.events, event_name).createFilter(fromBlock=fb, 
                                                                                    toBlock=tb, 
                                                                                    argument_filters=arg_filters)
                # request for transaction receipts pertaining to each event
                for event in event_filter.get_all_entries():
                    receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
                    result = getattr(contract.events, event_name)().processReceipt(receipt)[0]
                    # print("RESULT: ", result)
                    # extract data from receipt
                    record = {k: eval(v, {"result": result}) for k,v in config['txn_receipt_keys'].items()}

                    # get NFT image using opensea api

                    # fmtd_record = {"ID": fmt_id(nft_id, img_url),"Date": fmt_date(block), "Txn": fmt_txn_hash(txnhash), "Value (Eth)": fmt_value(value)}
                    records.append(record)

            return records 

    retries = 0
    empty_record = {k: None for k in list(config['txn_receipt_keys'].keys())}
    while True:
        try:
            rs = get_records(fromBlock,toBlock,epoch_size)
            if len(rs) == 0:
                rs = [empty_record]
            return rs
        except Exception as e:
            logging.error(f"WHILE LOOP ERROR: {e}. Dividing epoch size by 2")
            epoch_size /= 2
            retries += 1
        if retries > max_retries:
            return [empty_record]
    return records

# formatting functions
def fmt_addr(contract_addr_str=None, **kwargs):
    if contract_addr_str:
        return f'<a href="https://etherscan.io/address/{contract_addr_str}">{contract_addr_str}</a>'    
    else:
        return ''

def fmt_date_from_block(Block='latest', fmt='%m/%d/%y', **kwargs):
    if Block:
        try:
            ts = w3.eth.get_block(Block).timestamp
            dt = datetime.fromtimestamp(ts)
            dstr = dt.strftime(fmt)
            return f'<a href="https://etherscan.io/block/{Block}">{dstr}</a>'
        except Exception as e:
            print(e)
            return "--"
    return "--"

def fmt_dates_from_blocks(blocks, **kwargs):
    return [fmt_date_from_block(block, **kwargs) for block in blocks]

def fmt_id(ID=None):
    return f'<a href="https://opensea.io/assets/{contract_addr_str}/{ID}">#{ID}</a>'

def fmt_ids(ids):
    return [fmt_id(id) for id in ids]

def fmt_txn(Txn=None, **kwargs):
    if Txn:
        return f'<a href="https://etherscan.io/tx/{Txn}">{Txn[:20]}...</a>'

def fmt_txns(txns):
    return [fmt_txn(txn) for txn in txns]

def wei_to_ether(wei):
    if not wei:
        return 0
    return float('%.40f' % w3.fromWei(wei, 'ether'))

def weis_to_ethers(weis):
    return [wei_to_ether(wei) for wei in weis]

def df_from_records(records):
    return pd.DataFrame.from_records(records)

def transform(df, transformations):
    for t in transformations:
        if isinstance(t, tuple):
            t, *args = t 
            for i, a in enumerate(list(args)):
                t = t.replace(f'*|{i}|*', a)
        df.eval(t, inplace=True)
    return df 

def groupby(df, col, **kwargs):
    try:
        gb = df.groupby(col, **kwargs)
    except Exception as e:
        print(e)
        print("Returning one dataframe group")
        return [df]
    return [gb.get_group(g) for g in gb.groups]

def row1cv(vs):
    return vs.values[0]

def report_tag(func):
    def inner(*args, sp=0, br=0, **kwargs):
        try:
            result = func(*args, **kwargs)
            if isinstance(result, str):
                return result + spaces(sp) + breaks(br)
            else:
                return result 
        except IndexError:
            return "--"
            # return "SKIPPAGE"
    return inner  


@report_tag
def s(v):
    return f"<strong>{v}</strong>"

def spaces(num):
    return "".join(["&nbsp;" for i in range(num)])

def breaks(num):
    return "".join(["<br/>" for i in range(num)])

@report_tag
def h4(v):
    return f'<h4>{v}</h4>'

@report_tag
def centered(v):
    return f'<center>{v}</center>'

@report_tag
def div(v, classes=None):
    class_str = ""
    if classes:
        class_str = f" class={classes}"
    return f'<div{class_str}>{v}</div>'

def opensea_img_url_by_id(id_):
    print(f"CONTRACT_ADDR_STR: {contract_addr_str} ; ID: {id_}")
    resp_data = requests.get(f'https://api.opensea.io/api/v1/asset/{contract_addr_str}/{id_}/', headers={'User-Agent': 'Mozilla/5.0'}).json()
    try:
        return resp_data['image_url']
    except KeyError:
        print("KEYERROR IMAGE_URL. DATA: ", resp_data)

def ids_to_opensea_img_urls(ids):
    return [opensea_img_url_by_id(id) for id in ids]

@report_tag 
def img_by_url(url, w=100, h=100):
    return f'<img src={url} width={w} height={h} />'

def img_urls_to_imgs(img_urls):
    return [img_by_url(img_url) for img_url in img_urls]

@report_tag 
def figure(img_html, figcaption_html):
    return f'<figure>{img_html}{figcaption_html}</figure>'

@report_tag
def figcaption(val):
    return f'<figcaption>{val}</figcaption>'
# template filters 

@report_tag 
def table(df, classes='Table', columns=None):
    try:
        return df.to_html(columns=columns, classes=classes,index=False, border=2, justify='left', escape=False, na_rep='--')
    except KeyError:
        print("Empty table.")
        return "--"

def rank(df, col, **kwargs):
    s = df[col]
    results = []
    for i in range(len(s)):
        results.append(i+1)
    df['Rank'] = results 
    return df         

def log(v):
    logging.error(v)

ENV = jinja2.Environment(extensions=['jinja2.ext.loopcontrols'])
ENV.filters = {'chart': chart, 'parse_txn_receipts': parse_txn_receipts, 'df_from_records': df_from_records, 'groupby': groupby, 'row1cv': row1cv, 'transform': transform, 'rank': rank,
                'div': div, 's': s, 'spaces': spaces, 'breaks': breaks, 'h4': h4, 'centered': centered, 'img_by_url': img_by_url, 'opensea_img_url_by_id': opensea_img_url_by_id, 
                'figure': figure, 'figcaption': figcaption, 'table': table, 'log': log, 'fmt_id': fmt_id}