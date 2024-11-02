import discord
from functions.market_cards_list import all_cards
from functions.market.url import URL_ONLINE


async def change_price_fn(user_name, card, number_of_cards, price_old, price_new, price_symbol):
    try:
        card_name = all_cards[card]['name']

        price_symbol = price_symbol.upper()

        card_name = card_name.replace(" ", "-")

        if int(number_of_cards) > 50:
            return None

        URL = f'{URL_ONLINE}/changePrice/CITY/{user_name}/{number_of_cards}/' \
              f'{card_name}/{price_old}/{price_new}/{price_symbol}'

        embed = discord.Embed(
            title=f'Change price of {number_of_cards} {card_name}',
            description=f'You are trying to change {number_of_cards} {card_name} price from {price_old} to {price_new} each',
            color=discord.Color.blue(),
            url=URL
        )

        return embed
    except KeyError:
        return None
