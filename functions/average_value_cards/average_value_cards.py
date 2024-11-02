import aiohttp
import asyncio


async def get_data(card):
    URL = f'https://api.dcity.io/stats_cards?type={card}'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            data = await response.json()
    return data


async def get_average(card, symbol):
    total_data = []
    all_data = (await get_data(card))['full']
    all_data.reverse()

    for d in all_data:
        if len(total_data) <= 30:
            try:
                if d['average_price']:
                    average_price_data = d['average_price']
                    for a in average_price_data:
                        average_prices = average_price_data[a][symbol]
                        for av in average_prices:
                            total_data.append(av)
            except KeyError:
                pass
    return total_data


async def get_average_single(card):
    sales_data = await get_average(card, 'SIM')
    if len(sales_data) > 0:
        final = sum(sales_data) / len(sales_data)
    else:
        final = 0
    final = round(final, 2)
    return final
