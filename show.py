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
# ...             cryptopunks:60-70;
# python show.py cryptopunks:60,61,62;<name of contract>:n1,n2,... <name of template (e.g sales)>

nfts_str = args.nfts 
contracts = {}

contract_strs = nfts_str.split(";")
for contract_str in contract_strs:
    cname, nft_ids_str = contract_str.split(":")
    if "-" in nft_ids_str:
        nft_id_start, nft_id_end = nft_ids_str.split("-") 
        nft_ids = [str(nid) for nid in list(range(int(nft_id_start), int(nft_id_end) + 1))]
    else:
        nft_ids = nft_ids_str.split(",")
    contracts[CONTRACTS[cname]] = nft_ids 

template_str = args.template 
path_to_template = f'./templates/{template_str}.txt'

with open(path_to_template) as f:
    template_str = f.read()
    f.close()

def chart(ax, w=300, h=300, rotation='vertical'):
    if ax:
        plt.xticks(rotation = rotation)
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf)
        buf.seek(0)
        img_html = f'<img width={w} height={h} src="data:image/png;base64,{b64encode(buf.getvalue()).decode()}" />'
        return img_html
    else:
        return f'<img src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=" width={w} height={h} alt="" />'    

def get_colors(value_series, condition_mapping):
    results = []
    for v in value_series:
        if v in condition_mapping:
            results.append(condition_mapping[v])
        else:
            results.append("#000000")
    return results 

def df_from_records(records):
    df = pd.DataFrame.from_records(records)
    df.to_json("./test/cryptopunks.json")
    # quit()
    return df

def groupby(df, column):
    gb = df.groupby(column)
    return [gb.get_group(g) for g in gb.groups]

def sort_values(df, column, ascending=True):
    return df.sort_values(column, ascending=ascending)

# event_types = ['created', 'successful', 'cancelled', 'bid_entered', 'bid_withdrawn']
event_types = ['successful', 'bid_entered']
# 2018-08-18T18:55:21

def get_contract_events(c_addr, c_ids, event_type=event_types, occurred_after='01/01/2017'):
    oa_datetime = maya.when(occurred_after).datetime().strftime("%Y-%m-%dT%H:%M:%S")
    url = "https://api.opensea.io/api/v1/events"
    querystring = {"only_opensea":"false","offset":"0",
                "limit":"20","asset_contract_address": c_addr}
    events = []
    timeout = 0.2
    for et in event_types:
        querystring['event_type'] = et 
        querystring['occurred_after'] = oa_datetime
        while True:
            current_i = 0
            repeat = False 
            for i, c_id in enumerate(c_ids[current_i:]):
                current_i = i
                sleep(timeout)
                if c_id != "all":
                    querystring["token_id"] = c_id 
                response = requests.request("GET", url, params=querystring)
                asset_events = response.json()
                # print(asset_events)
                if isinstance(asset_events, dict):
                    if 'Request was throttled' in str(asset_events):
                        repeat = True 
                        timeout += 1
                        break 
                    print(asset_events)
                    asset_events = asset_events['asset_events']
                for ae in asset_events:
                    events.append(ae)
                 
            if repeat is False:
                break 
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

def assets_to_figures(assets, w=50, h=50):
    results = []
    for a in assets:
        c_addr = a["asset_contract"]["address"]
        img_url = a['image_url']
        token_id = a["token_id"]
        token_id_html = f'<a href="https://opensea.io/assets/{c_addr}/{token_id}">{token_id}</a>'
        figure_html = f'''<figure>
                            <img src="{img_url}" width="{w}" height="{h}">
                            <figcaption>#{token_id_html}</figcaption>
                        </figure>'''
        results.append(figure_html)
    return results 

def txns_to_txn_hashes(txns):
    results = [] 
    for txn in txns:
        txn_hash = txn["transaction_hash"]
        txn_hash_html = f'<a href="https://etherscan.io/tx/{txn_hash}">&rarr;</a>'
        results.append(txn_hash_html)
    return results 

def total_prices_to_ethers(total_prices, bid_amounts):
    results = []
    for tp, ba in zip(total_prices, bid_amounts):
        if tp:
            print("WEI PRICE BEFORE: ", int(tp))
            eth_price = float(Web3.fromWei(int(tp), 'ether'))
            print("ETH PRICE AFTER: ", eth_price)
            results.append(eth_price)
        elif ba:
            print("WEI PRICE BEFORE: ", int(ba))
            eth_price = float(Web3.fromWei(int(ba), 'ether'))
            print("ETH PRICE AFTER: ", eth_price)
            results.append(eth_price)            
        else:
            results.append(0)
    return results 

def ethers_to_pct_changes(ethers):
    print(ethers)
    result = ethers.pct_change()
    print(result)
    return result 

def created_dates_to_dates(created_dates):
    results = []
    for created_date in created_dates:
        d = maya.when(created_date).date
        # print(d)
        results.append(d)
    return results 

def dates_to_date_strings(dates, fmt='%m/%d/%y'):
    results = []
    for d in dates:
        dstr = d.strftime(fmt)
        results.append(dstr)
    return results 

def dates_to_date2block_links(dates, txns):
    results = []
    for date, txn in zip(dates, txns):
        dt_str = date.strftime("%m/%d/%Y")
        block_num = txn["block_number"]
        date2block_link = f'<a href="https://etherscan.io/block/{block_num}">{dt_str}</a>'
        results.append(date2block_link)
    return results 

def pct_change_colorer(pct_change):
    # 
    is_numpy_float = False
    if 'numpy.float64' in str(type(pct_change)):
        print('PCTC TYPE: ', type(pct_change))
        pct_change = float(pct_change)
        print('PCTC TYPE AFTER: ', type(pct_change))
        is_numpy_float = True 
    try:
        pct_change = float(format(pct_change, '.2f'))
    except:
        return 0 
    if is_numpy_float is True:
        print("PCTC PRE COMPARISON: ", pct_change)
    if pct_change > 0:
        return f'<span style="color: green;">{pct_change}</span>'
    elif pct_change < 0:
        return f'<span style="color: red;">{pct_change}</span>'
    else:
        return pct_change 

# FORMATTERS = {
#     "PctChange": pct_change_colorer,
# }

FORMATTERS = None

def table(df, columns=None, index=False, escape=False, classes=None, formatters=FORMATTERS):
    return df.to_html(columns=columns, index=index, escape=escape, classes=classes, formatters=formatters)

def transform(df, transformations):
    for t in transformations:
        df = df.eval(t)
    return df 

ENV.filters = {"get_contract_events": get_contract_events, 
                "df_from_records": df_from_records, "get_colors": get_colors,
                "groupby": groupby, "sort_values": sort_values, "table": table, "transform": transform,"chart": chart,}

template = ENV.from_string(template_str)

style_str = '''a {{ color: green; }}
                .row {{ display: inline; }}
            '''

html_content = f"<html><head><style>{style_str}</style></head><body>" + template.render(contracts=contracts, list=list) + "</body></html>"

with open("./output.html", "w") as f:
    f.write(html_content)
    f.close()

webbrowser.open("./output.html")