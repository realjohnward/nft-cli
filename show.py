from argparse import ArgumentParser 
from contracts import CONTRACTS 
import jinja2
import requests
import pandas as pd 
from time import sleep 
import webbrowser 
from web3 import Web3 
import maya 
from io import BytesIO 
import matplotlib.pyplot as plt 
from base64 import b64encode 

ENV = jinja2.Environment(extensions=['jinja2.ext.loopcontrols'])

parser = ArgumentParser()
parser.add_argument("nfts")
parser.add_argument("template")
args = parser.parse_args()
# python show.py cryptopunks:60,61,62;<name of contract>:n1,n2,... <name of template (e.g sales)>

nfts_str = args.nfts 
contracts = {}

contract_strs = nfts_str.split(";")
for contract_str in contract_strs:
    cname, nft_ids_str = contract_str.split(":")
    nft_ids = nft_ids_str.split(",")
    contracts[CONTRACTS[cname]] = nft_ids 

template_str = args.template 
path_to_template = f'./templates/{template_str}.txt'

with open(path_to_template) as f:
    template_str = f.read()
    f.close()

def chart(ax, w=300, h=300):
    if ax:
        buf = BytesIO()
        plt.savefig(buf)
        buf.seek(0)
        img_html = f'<img width={w} height={h} src="data:image/png;base64,{b64encode(buf.getvalue()).decode()}" />'
        return img_html
    else:
        return f'<img src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=" width={w} height={h} alt="" />'    

def df_from_records(records):
    df = pd.DataFrame.from_records(records)
    df.to_json("./test/cryptopunks.json")
    return df

def groupby(df, column):
    gb = df.groupby(column)
    return [gb.get_group(g) for g in gb.groups]

def get_contract_events(c_addr, c_ids, event_type="successful"):
    url = "https://api.opensea.io/api/v1/events"
    querystring = {"only_opensea":"false","offset":"0",
                "limit":"20","asset_contract_address": c_addr, "event_type": event_type}
    events = []
    for c_id in c_ids:
        sleep(0.2)
        querystring["token_id"] = c_id 
        response = requests.request("GET", url, params=querystring)
        asset_events = response.json()
        # print(asset_events)
        if isinstance(asset_events, dict):
            asset_events = asset_events['asset_events']
        for ae in asset_events:
            events.append(ae)
    return events 

def assets_to_token_ids(assets):
    results = []
    for a in assets:
        c_addr = a["asset_contract"]["address"] 
        token_id = a["token_id"]
        token_id_html = f'<a href="https://opensea.io/assets/{c_addr}/{token_id}">{token_id}</a>' 
        print(token_id_html)
        results.append(token_id_html)
    
    return results  

def assets_to_figures(assets):
    results = []
    for a in assets:
        c_addr = a["asset_contract"]["address"]
        img_url = a['image_url']
        token_id = a["token_id"]
        token_id_html = f'<a href="https://opensea.io/assets/{c_addr}/{token_id}">{token_id}</a>'
        figure_html = f'''<figure>
                            <img src="{img_url}">
                            <figcaption>#{token_id_html}</figcaption>
                        </figure>'''
        results.append(figure_html)
    return results 

def txns_to_txn_hashes(txns):
    results = [] 
    for txn in txns:
        txn_hash = txn["transaction_hash"]
        txn_hash_html = f'<a href="https://etherscan.io/tx/{txn_hash}">{txn_hash[:20]}...</a>'
        results.append(txn_hash_html)
    return results 

def total_prices_to_ethers(total_prices):
    return [float(Web3.fromWei(int(tp), 'ether')) for tp in total_prices]

def created_dates_to_dates(created_dates):
    results = []
    for created_date in created_dates:
        d = maya.when(created_date).date
        # print(d)
        results.append(d)
    return results 

def dates_to_date2block_links(dates, txns):
    results = []
    for date, txn in zip(dates, txns):
        dt_str = date.strftime("%m/%d/%Y")
        block_num = txn["block_number"]
        date2block_link = f'<a href="https://etherscan.io/block/{block_num}">{dt_str}</a>'
        results.append(date2block_link)
    return results 

def transform(df, transformations):
    for t in transformations:
        df = df.eval(t)
    return df 

ENV.filters = {"get_contract_events": get_contract_events, 
                "df_from_records": df_from_records,
                "groupby": groupby, "transform": transform,"chart": chart,}

template = ENV.from_string(template_str)

html_content = template.render(contracts=contracts, list=list)

with open("./output.html", "w") as f:
    f.write(html_content)
    f.close()

webbrowser.open("./output.html")