import discord
import inflect
import requests
import asyncio
from discord import Embed
from functions.card_list import first_edition, second_editiion, third_edition, \
    citizen_list_1, citizen_list_2, combined_buildings, tech_list
from functions.average_value_cards.average_value_cards import get_average_single


def get_data(user_name):
    url = "https://api.dcity.io/stats"
    params = {'user': user_name}
    try:
        with requests.get(url, params) as r:
            data = r.json()
        return data
    except requests.RequestException as e:
        print(f"Error while fetching data for '{user_name}': {e}")
        return None


async def check_value(user_name):
    loop = asyncio.get_event_loop()

    all_data = await loop.run_in_executor(None, get_data, user_name)

    if all_data is None:
        return "Failed to retrieve data. Please try again later."

    all_stats = all_data.get('last', {})
    all_cards_list = all_stats.get('cards', {})

    embed = Embed(title=f'{user_name} City Value', description='Stats', colour=discord.Colour.blue())

    # Base Stats
    base_stats = all_stats.get('stats', {})
    base_stats['Unemployed'] = all_stats.get('unemployment', {})
    base_stats['Sim_power'] = all_stats.get('sim_power', {})
    base_stats['Crime chance'] = all_stats.get('crime_chance', {})
    base_stats['Tax Refund'] = all_stats.get('guaranteed_income', {})

    if not base_stats:
        return "City data not found!"

    total_sum = 0

    async def calculate_value(key):
        nonlocal total_sum  # Use the total_sum variable from the outer scope
        value = round((await get_average_single(key)) * all_cards_list.get(key, 0), 0)
        total_sum += value  # Add the value to the total_sum
        return value

    embed.add_field(name='Base Stats',
                    value="\n".join([f'{key}: {value}' for key, value in base_stats.items()]),
                    inline=False)

    # First Edition
    embed.add_field(name='First Edition',
                    value="\n".join([f'{value}: {await calculate_value(key)}'
                                     for key, value in first_edition.items()
                                     if all_cards_list.get(key, 0) > 0]))
    # Second Edition
    embed.add_field(name='Second Edition',
                    value="\n".join(
                        [f'{value}: {await calculate_value(key)}'
                         for key, value in second_editiion.items()
                         if all_cards_list.get(key, 0) > 0]))
    # Third Edition
    embed.add_field(name='Third Edition',
                    value="\n".join([f'{value}: {await calculate_value(key)}'
                                     for key, value in third_edition.items()
                                     if all_cards_list.get(key, 0) > 0]))

    # Citizen List
    embed.add_field(name='Citizen List',
                    value="\n".join([f'{value}: {await calculate_value(key)}'
                                     for key, value in citizen_list_1.items()
                                     if all_cards_list.get(key, 0) > 0]))

    # Citizen List
    embed.add_field(name='Citizen List',
                    value="\n".join([f'{value}: {await calculate_value(key)}'
                                     for key, value in citizen_list_2.items()
                                     if all_cards_list.get(key, 0) > 0]))

    # Combined Buildings
    embed.add_field(name='Combined Buildings',
                    value="\n".join(
                        [f'{value}: {await calculate_value(key)}'
                         for key, value in combined_buildings.items()
                         if all_cards_list.get(key, 0) > 0]))

    # Tech List
    for category, technology in tech_list.items():
        embed.add_field(name=category,
                        value="\n".join(
                            [f'{value}: {await calculate_value(key)}'
                             for key, value in technology.items()
                             if all_cards_list.get(key, 0) > 0]))

    def number_to_words(number):
        p = inflect.engine()
        words_nm = p.number_to_words(number)
        capitalized = words_nm.title()
        return capitalized

    total_sum = round(total_sum, 0)
    words = number_to_words(total_sum)
    embed.add_field(name='Average value of total city assets',
                    value=f'{total_sum}\n{words}',
                    inline=False)
    return embed

