# import time
#
# import requests
# import json
#
# import asyncio as asyncio
# import discord
# import aiohttp
# from discord.embeds import Embed
# from collections import Counter
# from functions.richlist.all_cards_stats_list import all_cards_stats
# from collections import defaultdict
#
#
# # def get_account_history():
# #     URL = "https://history.hive-engine.com/accountHistory"
# #     all_data = []
# #     offset = 0
# #     limit = 1000
# #
# #     while True:
# #         params = {
# #             "account": "dcity1",
# #             "limit": limit,
# #             "offset": offset,
# #             'operation': 'nft_setProperties',
# #         }
# #
# #         try:
# #             response = requests.get(URL, params=params)
# #             response.raise_for_status()  # Raise an error for bad responses
# #             data = response.json()
# #
# #             if not data:
# #                 break  # Exit the loop if no data is returned
# #
# #             all_data.extend(data)
# #             # if len(data) < limit:
# #             #     break  # Exit if fewer than the limit, meaning no more data
# #
# #             if len(data) > limit:
# #                 time.sleep(2)
# #
# #             offset += limit  # Move to the next batch
# #         except requests.exceptions.RequestException as e:
# #             print("An error occurred:", e)
# #             break
# #
# #     return all_data
#
#
# # last_dead_citizen_id = 2012424
#
# counter = 0
#
#
# async def fetch_data(session, offset):
#     global counter
#     counter += 1
#     url = "https://history.hive-engine.com/accountHistory"
#     print("request made", counter)
#     params = {
#         "account": "dcity1",
#         "limit": 1000,
#         "offset": offset,
#     }
#
#     async with session.get(url, params=params) as response:
#         response.raise_for_status()  # Raise an exception for non-successful status codes
#         data = await response.json()
#         return data
#
#
# async def get_all_cards_data(offset):
#     async with aiohttp.ClientSession() as session:
#         data_list = []
#
#         while True:
#             print(len(data_list))
#             if len(data_list) >= 2000:
#                 break
#             data = await fetch_data(session, offset)
#             if not data:
#                 break
#             # if len(data_list) >= 1000:
#             #     break
#             # Filter to include only entries with operation 'nft_setProperties'
#             filtered_data = [d_ for d_ in data if d_.get('operation') == 'nft_setProperties']
#             data_list.extend(filtered_data)
#             # data_list.extend(data)
#             offset += 1000
#         return data_list
#
#
# # Fetch and print the account history
# if __name__ == "__main__":
#     data = asyncio.run(get_all_cards_data(0))
#     for d in data:
#         # print(d)
#         if d['operation'] == 'nft_setProperties':
#             if len(d['nfts']) > 0:
#                 for n in d['nfts']:
#                     try:
#                         if n['properties']['name'] in n == 'Student (debt)':
#                             print(d)
#                     except KeyError:
#                         print("Key error")
