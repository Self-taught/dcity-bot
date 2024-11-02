import asyncio as asyncio
import discord
import aiohttp
from discord.embeds import Embed
from collections import Counter
from functions.richlist.all_cards_stats_list import all_cards_stats
from collections import defaultdict

last_dead_citizen_id = 2012424


async def fetch_data(session, offset):
    url = "https://herpc.dtools.dev/contracts"
    print("request made")
    params = {
        'contract': 'nft',
        'table': 'CITYinstances',
        'query': {"properties.type": "citizen", "properties.name": "Student (debt)"},
        'limit': 1000,
        'offset': offset,
        'indexes': []
    }
    j = {'jsonrpc': '2.0', 'id': 1, 'method': 'find', 'params': params}

    async with session.post(url, json=j) as response:
        response.raise_for_status()  # Raise an exception for non-successful status codes
        data = await response.json()
        return data['result']


async def get_all_cards_data(offset):
    async with aiohttp.ClientSession() as session:
        data_list = []
        while True:
            data = await fetch_data(session, offset)
            if not data:
                break
            # if len(data_list) >= 1000:
            #     break
            data_list.extend(data)
            offset += 1000
        return data_list


# Place your code here (without the final print statement)

# Run the async function within the asyncio event loop
if __name__ == "__main__":
    result = asyncio.run(get_all_cards_data(0))
    for r in result:
        print(r)
    # For dead citizens
    # player_citizen_at_risk = defaultdict(int)
    # for r in result:
    #     account = r.get('account')
    #     if account:
    #         player_citizen_at_risk[account] += 1
    # sorted_risk = sorted(player_citizen_at_risk.items(), key=lambda x: x[1], reverse=True)
    # for account, count in sorted_risk:
    #     print(f'{account}: {count}')
    # print(result)


# Student debt data
# {'_id': 2802015, 'account': 'unicron', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'income': -2, 'popularity': 1, 'type': 'citizen', 'population': 1, 'education': '0', 'creativity': '0'}}
# {'_id': 2802023, 'account': 'doombot75', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'income': -2, 'popularity': 1, 'type': 'citizen', 'population': 1, 'education': '0', 'creativity': '0'}}
# {'_id': 2802026, 'account': 'nftmarket', 'soulBound': False, 'ownedBy': 'c', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'income': -2, 'popularity': 1, 'type': 'citizen', 'population': 1, 'education': '0', 'creativity': '0'}, 'previousAccount': 'mapac', 'previousOwnedBy': 'u'}
# {'_id': 2802036, 'account': 'treasure.hoard', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'income': -2, 'popularity': 1, 'type': 'citizen', 'population': 1, 'education': '0', 'creativity': '0'}}
# {'_id': 2802040, 'account': 'treasure.hoard', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'income': -2, 'popularity': 1, 'type': 'citizen', 'population': 1, 'education': '0', 'creativity': '0'}}
# {'_id': 2802042, 'account': 'treasure.hoard', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'income': -2, 'popularity': 1, 'type': 'citizen', 'population': 1, 'education': '0', 'creativity': '0'}}
# {'_id': 2802292, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2802417, 'account': 'lynliss', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2802422, 'account': 'jujani', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}, 'previousAccount': 'nftmarket', 'previousOwnedBy': 'c'}
# {'_id': 2803522, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2803537, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2803739, 'account': 'senstless', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2804144, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2804817, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2804949, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2805718, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2806524, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2807117, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2807132, 'account': 'senstless', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2808684, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2808816, 'account': 'senstless', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2809073, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2809103, 'account': 'soteyapanbot', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2809921, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2810411, 'account': 'tengolotodo', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2810787, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2811722, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2812582, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2812617, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2813631, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2814358, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2815035, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2815308, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2815654, 'account': 'bowess', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2815715, 'account': 'juanvegetarian', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}, 'previousAccount': 'barks', 'previousOwnedBy': 'u'}
# {'_id': 2816440, 'account': 'dalz', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2816568, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2817330, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2817754, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2817761, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2818357, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2818375, 'account': 'juanvegetarian', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}, 'previousAccount': 'barks', 'previousOwnedBy': 'u'}
# {'_id': 2818633, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2819509, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2819713, 'account': 'soteyapanbot', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2820393, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2820544, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2820824, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2820840, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2821388, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2821430, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2822540, 'account': 'lynliss', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2822717, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2823189, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2823570, 'account': 'tengolotodo', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2823587, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2824297, 'account': 'tengolotodo', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2824743, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2825368, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2825665, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2825848, 'account': 'lynliss', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2826168, 'account': 'soteyapanbot', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2826725, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2826744, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2827822, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2828305, 'account': 'soteyapanbot', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2828749, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2828896, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2829311, 'account': 'tengolotodo', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2829772, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2831022, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2831050, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2831057, 'account': 'soteyapanbot', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2831263, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2831676, 'account': 'tengolotodo', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2831998, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2832199, 'account': 'bitcoinflood', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2832473, 'account': 'metzli', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2832494, 'account': 'soteyapanbot', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2833040, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2835167, 'account': 'bfciv', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}, 'previousAccount': 'nftmarket', 'previousOwnedBy': 'c'}
# {'_id': 2835283, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2835981, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2836022, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2836806, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2838277, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2838551, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2838710, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2839648, 'account': 'bfciv', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}, 'previousAccount': 'nftmarket', 'previousOwnedBy': 'c'}
# {'_id': 2841668, 'account': 'tengolotodo', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2842254, 'account': 'tengolotodo', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2842361, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2843063, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2843074, 'account': 'princekham', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}, 'previousAccount': 'nftmarket', 'previousOwnedBy': 'c'}
# {'_id': 2843170, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2844019, 'account': 'tengolotodo', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2844263, 'account': 'bulliontools', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}, 'previousAccount': 'thebighigg', 'previousOwnedBy': 'u'}
# {'_id': 2844743, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2845893, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2846012, 'account': 'bulliontools', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}, 'previousAccount': 'thebighigg', 'previousOwnedBy': 'u'}
# {'_id': 2846167, 'account': 'dalz', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2846452, 'account': 'bulliontools', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}, 'previousAccount': 'thebighigg', 'previousOwnedBy': 'u'}
# {'_id': 2846587, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2847318, 'account': 'bulliontools', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}, 'previousAccount': 'thebighigg', 'previousOwnedBy': 'u'}
# {'_id': 2847330, 'account': 'bulliontools', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}, 'previousAccount': 'thebighigg', 'previousOwnedBy': 'u'}
# {'_id': 2848202, 'account': 'bulliontools', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}, 'previousAccount': 'thebighigg', 'previousOwnedBy': 'u'}
# {'_id': 2848676, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2848780, 'account': 'juanvegetarian', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2849063, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2850092, 'account': 'notaboutme', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}
# {'_id': 2852722, 'account': 'nervi', 'soulBound': False, 'ownedBy': 'u', 'lockedTokens': {'SIM': '1'}, 'properties': {'name': 'Student (debt)', 'population': 1, 'income': -2, 'popularity': 1, 'type': 'citizen'}}