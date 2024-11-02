import discord
import requests
from discord import Embed
from functions.card_list import first_edition, second_editiion, third_edition, \
    citizen_list_1, citizen_list_2, combined_buildings, tech_list


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


def check_city(user_name):
    all_data = get_data(user_name)

    if all_data is None:
        return "Failed to retrieve data. Please try again later."

    all_stats = all_data.get('last', {})
    all_cards_list = all_stats.get('cards', {})

    # for a in all_cards_list:
    #     if a[0] == 't':
    #         print(f'{a}: {all_cards_list[a]}')

    # for f in all_stats:
    #     print(f)

    embed = Embed(title=f'{user_name} City', description='Stats', colour=discord.Colour.blue())

    # Base Stats
    base_stats = all_stats.get('stats', {})
    base_stats['Unemployed'] = all_stats.get('unemployment', {})
    base_stats['Sim_power'] = all_stats.get('sim_power', {})
    base_stats['Crime chance'] = all_stats.get('crime_chance', {})
    base_stats['Tax Refund'] = all_stats.get('guaranteed_income', {})

    if not base_stats:
        return "City data not found!"

    embed.add_field(name='Base Stats',
                    value="\n".join([f'{key}: {value}' for key, value in base_stats.items()]),
                    inline=False)

    # First Edition
    embed.add_field(name='First Edition',
                    value="\n".join([f'{value}: {all_cards_list.get(key, 0)}' for key, value in first_edition.items()
                                     if all_cards_list.get(key, 0) > 0]))
    # Second Edition
    embed.add_field(name='Second Edition',
                    value="\n".join(
                        [f'{value}: {all_cards_list.get(key, 0)}' for key, value in second_editiion.items()
                         if all_cards_list.get(key, 0) > 0]))
    # Third Edition
    embed.add_field(name='Third Edition',
                    value="\n".join([f'{value}: {all_cards_list.get(key, 0)}' for key, value in third_edition.items()
                                     if all_cards_list.get(key, 0) > 0]))

    # Citizen List 1
    embed.add_field(name='Citizen List',
                    value="\n".join([f'{value}: {all_cards_list.get(key, 0)}' for key, value in citizen_list_1.items()
                                     if all_cards_list.get(key, 0) > 0]))

    # Citizen List 2
    embed.add_field(name='Citizen List',
                    value="\n".join([f'{value}: {all_cards_list.get(key, 0)}' for key, value in citizen_list_2.items()
                                     if all_cards_list.get(key, 0) > 0]))

    # Combined Buildings
    embed.add_field(name='Combined Buildings',
                    value="\n".join(
                        [f'{value}: {all_cards_list.get(key, 0)}' for key, value in combined_buildings.items()
                         if all_cards_list.get(key, 0) > 0]))

    # Tech List
    for category, technology in tech_list.items():
        embed.add_field(name=category,
                        value="\n".join(
                            [f'{value}: {all_cards_list.get(key, 0)}' for key, value in technology.items()
                             if all_cards_list.get(key, 0) > 0]))
    return embed