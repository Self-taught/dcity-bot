import asyncio as asyncio
import discord
import aiohttp
from discord.embeds import Embed
from collections import Counter
from functions.richlist.all_cards_stats_list import all_cards_stats


async def fetch_data(session, card_info, offset):
    url = "https://herpc.dtools.dev/contracts"
    print("request made")
    params = {
        'contract': 'nft',
        'table': 'CITYinstances',
        'query': {'properties.name': card_info},
        'limit': 1000,
        'offset': offset,
        'indexes': []
    }
    j = {'jsonrpc': '2.0', 'id': 1, 'method': 'find', 'params': params}

    async with session.post(url, json=j) as response:
        response.raise_for_status()  # Raise an exception for non-successful status codes
        data = await response.json()
        return data['result']


async def get_all_cards_data(card, offset):
    async with aiohttp.ClientSession() as session:
        card_info = all_cards_stats[card]['name']
        data_list = []
        while True:
            data = await fetch_data(session, card_info, offset)
            if not data:
                break
            data_list.extend(data)
            offset += 1000
            print(data)
        return data_list


async def get_rich_list(card):
    try:
        all_cards_data = await get_all_cards_data(card, 0)
        for curr_card in all_cards_data:
            print(curr_card)
        current_card = all_cards_stats[card]['name']
        rich_list_stats = Counter(a['account'] for a in all_cards_data)

        accounts_to_ignore = {'dcityload', 'nft', 'nftmarket', 'null', 'dcity2'}

        sorted_rich_list_stats = sorted(rich_list_stats.items(), key=lambda x: x[1], reverse=True)

        sorted_rich_list_stats = [item for item in sorted_rich_list_stats if item[0] not in accounts_to_ignore]

        embed = Embed(title=f'Richlist of {current_card}', description='Richlist', colour=discord.Colour.blue())

        # Add the top 25 cities
        top_25_holders = "\n".join([f"{index + 1}. {account}: {count}"
                                    for index, (account, count) in enumerate(sorted_rich_list_stats)
                                    if account not in accounts_to_ignore][:25])
        embed.add_field(name='Top 50 Card Holders', value=top_25_holders, inline=True)

        embed.add_field(name='\n', value='\n')

        # Add the next 25 cities
        top_26_50_holders = "\n".join([f"{index + 1}. {account}: {count}"
                                       for index, (account, count) in enumerate(sorted_rich_list_stats)
                                       if account not in accounts_to_ignore][25:50])
        embed.add_field(name='\u200b', value=top_26_50_holders, inline=True)

        return embed
    except Exception as e:
        return f"An unexpected error occurred."
