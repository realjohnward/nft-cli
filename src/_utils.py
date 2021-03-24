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

with open("./stylesheet.css") as f:
    stylesheet_txt = f.read()
    f.close()

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

# data found from blocks between these 2 will be shown. 
fromBlock = args.fromBlock 
if not fromBlock:
    fromBlock = 0

toBlock = args.toBlock 
if not toBlock:
    toBlock = 'latest'

# Passed to template as an argument
contract = args.contract 
config = json.load(open(f"./contracts/{contract}/config.json"))
contract_addr_str = config['address']
contract_address = Web3.toChecksumAddress(contract_addr_str)

# Web3 client for connecting to Ethereum mainnet
defaults = json.load(open("../defaults.json"))
w3 = Web3(Web3.HTTPProvider(defaults['mainnet_url']))

# Contract interface 
abi = json.load(open(f"./contracts/{contract}/abi.json"))
contract = w3.eth.contract(address=contract_address, abi=abi)



def get_nft_images(ids, addr):
    results = []
    for id in ids:
        resp_data = requests.get(f'https://api.opensea.io/api/v1/asset/{contract_addr_str}/{nft_id}/', headers={'User-Agent': 'Mozilla/5.0'}).json()
        img_url = resp_data['image_url']
        results.append(img_url)
    return results 

def parse_txn_receipts(event_name, id_key, fromBlock=fromBlock, toBlock=toBlock):

    records = []

    # query for events pertaining to each NFT
    for nft_id in ids:
        if nft_id == "all":
            arg_filters = {}
        else:
            arg_filters = {id_key: int(nft_id)}
        
        event_filter = getattr(contract.events, event_name).createFilter(fromBlock=fromBlock, 
                                                                            toBlock=toBlock, 
                                                                            argument_filters=arg_filters)
        # request for transaction receipts pertaining to each event
        for event in event_filter.get_all_entries():
            receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
            result = getattr(contract.events, event_name)().processReceipt(receipt)[0]
            # print("RESULT: ", result)
            # extract data from receipt
            record = {k: fmt(k, eval(v, {"result": result})) for k,v in config['txn_receipt_keys'].items()}

            # get NFT image using opensea api

            # fmtd_record = {"ID": fmt_id(nft_id, img_url),"Date": fmt_date(block), "Txn": fmt_txn_hash(txnhash), "Value (Eth)": fmt_value(value)}
            records.append(record)

        return records 

# formatting functions


def fmt_addr(contract_addr_str=None, **kwargs):
    if contract_addr_str:
        return f'<a href="https://etherscan.io/address/{contract_addr_str}">{contract_addr_str}</a>'    
    else:
        return ''

def fmt_date(Block='latest', fmt='%m/%d/%y', **kwargs):
    if Block:
        try:
            ts = w3.eth.get_block(block).timestamp
            dt = datetime.fromtimestamp(ts)
            dstr = dt.strftime(fmt)
            return f'<a href="https://etherscan.io/block/{block}">{dstr}</a>'
        except:
            return "--"
    return "--"

def fmt_id(ID=None, **kwargs):
    return f'<a href="https://opensea.io/assets/{contract_addr_str}/{ID}">#{ID}</figcaption>'


def fmt_txn_hash(Txn=None, **kwargs):
    if Txn:
        return f'<a href="https://etherscan.io/tx/{Txn}">{Txn[:20]}...</a>'

def fmt_value(value, **kwargs):
    return float('%.40f' % w3.fromWei(value, 'ether'))

def fmt(k, v, **kwargs):
    if k == "Value":
        return fmt_value(v, **kwargs)
    elif k == "Txn":
        return fmt_txn_hash(v, **kwargs)
    elif k == "ID":
        return fmt_id(v, **kwargs)
    elif k == "Block":
        return fmt_date(v, **kwargs)
    elif k == "Address":
        return fmt_addr(v, **kwargs)
    else:
        return v 

def df_from_records(records):
    return pd.DataFrame.from_records(records)

def groupby(df, col, **kwargs):
    gb = df.groupby(col, **kwargs)
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
    resp_data = requests.get(f'https://api.opensea.io/api/v1/asset/{contract_addr_str}/{id_}/', headers={'User-Agent': 'Mozilla/5.0'}).json()
    try:
        return resp_data['image_url']
    except KeyError:
        print("KEYERROR IMAGE_URL. DATA: ", resp_data)

@report_tag 
def img_by_url(url, w=100, h=100):
    return f'<img src={url} width={w} height={h}>'

@report_tag 
def figure(img_html, figcaption_html):
    return f'<figure>{img_html}{figcaption_html}</figure>'

@report_tag
def figcaption(val):
    return f'<figcaption>{val}</figcaption>'
# template filters 

@report_tag 
def table(df, classes='Table'):
    try:
        return df.to_html(classes=classes,index=False, border=2, justify='left', escape=False)
    except KeyError:
        print("Empty table.")
        return "--"

def log(v):
    logging.error(v)

ENV = jinja2.Environment(extensions=['jinja2.ext.loopcontrols'])
ENV.filters = {'parse_txn_receipts': parse_txn_receipts, 'df_from_records': df_from_records, 'groupby': groupby, 'row1cv': row1cv, 
                'div': div, 's': s, 'spaces': spaces, 'breaks': breaks, 'h4': h4, 'centered': centered, 'img_by_url': img_by_url, 'opensea_img_url_by_id': opensea_img_url_by_id, 
                'figure': figure, 'figcaption': figcaption, 'table': table, 'log': log}