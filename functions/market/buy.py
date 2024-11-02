import discord
import requests
from functions.market_cards_list import all_cards
from functions.market.url import URL_ONLINE


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


def check_balance(user_name, symbol):
    all_data = get_balance(user_name)
    filtered_data = [d for d in all_data if d['symbol'] == symbol and float(d['balance']) >= 0.001]

    if len(filtered_data) > 0:
        return filtered_data
    else:
        return None


async def buy_cards(user_name, card, number_of_cards, price, price_symbol):
    try:
        card_name = all_cards[card]['name']

        price_symbol = price_symbol.upper()
        card_name = card_name.replace(" ", "-")
        user_balance = check_balance(user_name, price_symbol)

        if user_balance is None or int(number_of_cards) > 50:
            return None

        if float(user_balance[0]['balance']) >= (float(number_of_cards) * float(price)):
            pass
        else:
            return None

        URL = f'{URL_ONLINE}/buy/CITY/{user_name}/{number_of_cards}/{card_name}/{price}/{price_symbol}'

        embed = discord.Embed(
            title=f'Buy {number_of_cards} {card_name}',
            description=f'Buy {number_of_cards} {card_name} at {price} {price_symbol} each',
            color=discord.Color.blue(),
            url=URL  # Set the URL here
        )

        return embed
    except KeyError:
        return None
