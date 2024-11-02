import discord
import requests
from discord.embeds import Embed
from collections import Counter
from functions.market_cards_list import all_cards


def get_nicknames():
    editions = {
        '1st': '1st Edition',
        '2nd': '2nd Edition',
        '3rd': '3rd Edition',
        'citizen': 'Citizen',
        'combined': 'Combined Buildings',
        'tech': 'Tech',
        'background': 'background',
        'other': 'other'
    }

    embed = Embed(title='Nicknames for cards!',
                  description='Find cards on market using !market <nick-name>',
                  colour=discord.Colour.blue())

    for edition_type, edition_name in editions.items():
        edition_data = [f'{key}: {value["name"]}' for key, value in all_cards.items() if value['type'] == edition_type]
        embed.add_field(name=edition_name,
                        value="\n".join(edition_data))

    return embed


def get_market_data(nick, offset):
    try:
        card_info = all_cards[nick]
    except KeyError:
        print(f"Invalid nickname '{nick}' provided.")
        return []

    q = {'grouping': card_info}
    url = "https://herpc.dtools.dev/contracts"
    params = {
        'contract': 'nftmarket',
        'table': 'CITYsellBook',
        'query': q,
        'limit': 1000,
        'offset': offset,
        'indexes': []
    }
    j = {'jsonrpc': '2.0', 'id': 1, 'method': 'find', 'params': params}

    try:
        response = requests.post(url, json=j)
        data = response.json()

        if len(data['result']) == 1000:
            data['result'] += get_market_data(nick, offset + 1000)

        return data['result']

    except requests.RequestException as e:
        print('Something')
        return []


def price_data(offset):
    url = "https://herpc.dtools.dev/contracts"
    params = {
        'contract': 'market',
        'table': 'sellBook',
        'query': {'symbol': 'SIM'},
        'limit': 1000,
        'offset': offset,
        'indexes': []
    }
    j = {'jsonrpc': '2.0', 'id': 1, 'method': 'find', 'params': params}

    try:
        response = requests.post(url, json=j)
        data = response.json()

        if len(data['result']) == 1000:
            data['result'] += get_market_data(offset + 1000)

        price = min(d['price'] for d in data['result'])

        return float(price) * 1000

    except requests.RequestException as e:
        print('Something')
        return []


def market_data(card):
    all_data = get_market_data(card, 0)
    sim_price = price_data(0)
    swap_hive_price = (1/sim_price) * 1000

    card_name = all_cards[card]['name']

    sim_data = sorted([d for d in all_data if d['priceSymbol'] == 'SIM'], key=lambda x: float(x['price']))

    sim_data_final = Counter(s['price'] for s in sim_data)

    swap_hive_data = sorted([d for d in all_data if d['priceSymbol'] == 'SWAP.HIVE'], key=lambda x: float(x['price']))

    swap_hive_data_final = Counter(s['price'] for s in swap_hive_data)

    embed = Embed(title=f'Market Data of {card_name}', description=f'1000 Sim = {sim_price} Swap.Hive', colour=discord.Colour.blue())

    sim_field_values = [f'{round(float(s), 2)}: {sim_data_final[s]}'
                        for s in sorted(sim_data_final.keys(), key=float)]
    swap_hive_field_values = [f'{round(float(s), 2)}: {swap_hive_data_final[s]}'
                              for s in sorted(swap_hive_data_final.keys(), key=float)]

    swap_hive_to_sim_values = [f'{round(float(s) * swap_hive_price , 2)}: {swap_hive_data_final[s]}'
                               for s in sorted(swap_hive_data_final.keys(), key=float)]

    embed.add_field(name='Sim Orders',
                    value="\n".join(sim_field_values))

    embed.add_field(name='Swap Hive Orders',
                    value="\n".join(swap_hive_field_values))

    embed.add_field(name='Swap Hive Orders (Approx Value in Sim)',
                    value="\n".join(swap_hive_to_sim_values))

    return embed
