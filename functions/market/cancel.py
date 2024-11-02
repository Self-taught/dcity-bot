import discord
from functions.market_cards_list import all_cards
from functions.market.url import URL_ONLINE


async def cancel_fn(user_name, card, number_of_cards, price, price_symbol):
    try:
        card_name = all_cards[card]['name']

        price_symbol = price_symbol.upper()

        card_name = card_name.replace(" ", "-")

        if int(number_of_cards) > 50:
            return None

        URL = f'{URL_ONLINE}/cancel/CITY/{user_name}/{number_of_cards}/' \
              f'{card_name}/{price}/{price_symbol}'

        embed = discord.Embed(
            title=f'Remove {number_of_cards} {card_name} from market',
            description=f'You are trying to remove {number_of_cards} {card_name} at price {price} from market',
            color=discord.Color.blue(),
            url=URL
        )

        return embed
    except KeyError:
        return None
