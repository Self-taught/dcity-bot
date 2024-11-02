import discord
import requests
from discord import Embed


def get_balance(user_name):
    url = "https://herpc.dtools.dev/contracts"
    params = {
        'contract': 'tokens',
        'table': 'balances',
        'query': {'account': user_name},
        'limit': 1000,
        'indexes': []
    }
    j = {'jsonrpc': '2.0', 'id': 1, 'method': 'find', 'params': params}

    with requests.post(url, json=j) as r:
        data = r.json()
    return data['result']


def check_balance(user_name):
    all_data = get_balance(user_name)
    show_balance = ['SWAP.HIVE', 'SIM', 'ENTRY', 'STARBITS', 'DEC', 'SPS', 'SWAP.BTC', 'VOUCHER',
                    'LICENSE', 'SWAP.DOGE', 'PART', 'CHAOS', 'SWAP.ETH', 'SWAP.LTC', 'GLX', 'LEO', 'SCRAP',
                    'SWAP.BUSD', 'SWAP.HBD', 'CROP']
    filtered_data = [d for d in all_data if d['symbol'] in show_balance and float(d['balance']) >= 0.01]

    embed = Embed(title=f'{user_name} Balance', description='Balance', colour=discord.Colour.green())

    embed.add_field(name='Balance',
                    value="\n".join(f'{d["symbol"]}:  {d["balance"]}' for d in filtered_data))

    return embed
