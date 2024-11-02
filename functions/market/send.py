import discord
from functions.market_cards_list import all_cards
from functions.market.url import URL_ONLINE


async def send_cards(user_name, hive_account, card, number_of_cards):
    try:
        card_name = all_cards[card]['name']

        card_name = card_name.replace(" ", "-")

        if int(number_of_cards) > 50:
            return None

        URL = f'{URL_ONLINE}/transfer/CITY/{user_name}/{hive_account}/{number_of_cards}/{card_name}'

        embed = discord.Embed(
            title=f'Transfer {number_of_cards} {card_name}',
            description=f'Sending {number_of_cards} {card_name} to {hive_account}',
            color=discord.Color.blue(),
            url=URL
        )

        return embed
    except KeyError:
        return None
