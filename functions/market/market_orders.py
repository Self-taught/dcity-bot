import discord
import requests


def get_orders_data(user_name, offset):
    url = "https://herpc.dtools.dev/contracts"
    params = {
        'contract': 'nftmarket',
        'table': 'CITYsellBook',
        'query': {'account': user_name},
        'limit': 1000,
        'indexes': []
    }
    j = {'jsonrpc': '2.0', 'id': 1, 'method': 'find', 'params': params}

    with requests.post(url, json=j) as r:
        data = r.json()
        if len(data['result']) == 1000:
            data['result'] += get_orders_data(user_name, offset + 1000)
    return data['result']


def get_market_data(username):
    print('Started....')
    all_data = get_orders_data(username, 0)
    print(all_data)

    market_orders = {}

    for d in all_data:
        grouping = d.get('grouping', {})
        grouping_name = grouping.get('name', '')
        price = d.get('price', 0)
        price_symbol = d.get('priceSymbol', '')

        if grouping_name:
            if grouping_name in market_orders:
                if price_symbol != market_orders[grouping_name]['priceSymbol']:
                    new_grouping_name = f"{grouping_name} ({price_symbol})"
                    market_orders[new_grouping_name] = {
                        'type': grouping.get('type', ''),
                        'price': price,
                        'priceSymbol': price_symbol,
                    }
                elif price < market_orders[grouping_name]['price']:
                    market_orders[grouping_name]['price'] = price
            else:
                market_orders[grouping_name] = {
                    'type': grouping.get('type', ''),
                    'price': price,
                    'priceSymbol': price_symbol,
                }

    embed = discord.Embed(
        title=f'Market Orders of {username}',
        description='Market orders',
        colour=discord.Colour.blue()
    )

    for m in market_orders:
        print(m)
        value_str = str(market_orders[m]).replace('{', '').replace('}', '')
        embed.add_field(name=m, value=value_str, inline=False)

    return embed


get_market_data('looftee')