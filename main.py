import discord
from discord.ext import commands
import sqlite3
import requests
from discord import Embed
from keys import KEY
from functions.check_city import check_city
from functions.check_balance import check_balance
from functions.check_market import get_nicknames, market_data
from functions.richlist.richlist import get_rich_list
from functions.average_value_cards.average_value_cards import get_average
from functions.average_value_cards.average_value_card_list import all_cards_average
from functions.average_value_cards.city_value import check_value
from functions.market.buy import buy_cards
from functions.market.sell import sell_cards
from functions.market.change_price import change_price_fn
from functions.market.send import send_cards
from functions.market.cancel import cancel_fn
from functions.market.market_orders import get_market_data
from functions.market.richlist_sim import rich_list_sim

intents = discord.Intents(messages=True, guilds=True)
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print("Bot is ready!")


# ID of the allowed channel and direct message
allowed_channel_id = [708114657566654485, 1132573954691825786, 1143033634643771472, 1113150592228020306,
                      1113150592228020306]


@bot.event
async def on_message(message):
    # Check if the message is from the allowed channel or a direct message
    if message.channel.id in allowed_channel_id or isinstance(message.channel, discord.DMChannel):
        await bot.process_commands(message)


@bot.command(category='dCity', description='Register with your hive username(small letters)')
async def register(ctx, user_name):
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM userData WHERE ID = ?;', (ctx.author.id,))
        if cursor.fetchone():
            await ctx.send("You are already registered.")
        else:
            cursor.execute('INSERT INTO userData (ID, AUTHOR_NAME, USER_NAME) VALUES (?, ?, ?);',
                           (ctx.author.id, ctx.author.name, user_name))
            connection.commit()
            await ctx.send(f'{user_name} successfully registered.')
    except sqlite3.IntegrityError:
        await ctx.send(f'You cannot register with two accounts.')
    except sqlite3.OperationalError:
        await ctx.send('Something went wrong. Try again later.')
    finally:
        connection.close()


@bot.command(category='City', description="Unregister if you want to change the hive account you are registered with")
async def unregister(ctx):
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM userData WHERE ID = ?;', (ctx.author.id,))
        connection.commit()
        await ctx.send('Successfully unregistered')
    except sqlite3.OperationalError:
        await ctx.send('Something went wrong. Try again later.')
    finally:
        connection.close()


@bot.command(category='city', description='check city of a user')
async def city(ctx, user_name=None):
    try:
        if user_name is None or user_name.strip() == '':
            # If no user_name provided, get the user from the database based on the Discord ID
            user = get_user(ctx.author.id)
            if user is None:
                await ctx.send("You are not registered. Use `!register <user_name>` to register.")
                return
            result = check_city(user)
        else:
            # If user_name provided, directly check the city
            result = check_city(user_name)

        # Send the resulting embed
        await ctx.send(embed=result)
    except KeyError:
        await ctx.send("City not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command(category='Balance', description="Check Balance of user with !balance user_name")
async def wallet(ctx, user_name=None):
    try:
        if user_name is None or user_name.strip() == '':
            # If no user_name provided, get the user from the database based on the Discord ID
            user = get_user(ctx.author.id)
            if user is None:
                await ctx.send("You are not registered. Use `!register <user_name>` to register.")
                return
            result = check_balance(user)
        else:
            # If user_name provided, directly check the city
            result = check_balance(user_name)

        # Send the resulting embed
        await ctx.send(embed=result)
    except KeyError:
        await ctx.send("Account not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command(category='Nicknames', description="Find Nicknames of each card!")
async def nicknames(ctx):
    nick_value = get_nicknames()
    await ctx.send(embed=nick_value)


@bot.command(category='Market', description="Market Orders")
async def market(ctx, card):
    try:
        result = market_data(card)
        await ctx.send(embed=result)
    except Exception as e:
        await ctx.send(f"An error occurred while fetching market data for '{card}'"
                       f"Use !nicknames command to see if you have entered the right nickname for the card.")


@bot.command(category='Richlist', description="Top 50 Holders of Cards")
async def rich(ctx, card):
    try:
        await ctx.send('Compiling richlist. Please wait...')
        result = await get_rich_list(card)
        await ctx.send(embed=result)
    except KeyError:
        await ctx.send(f"Invalid nickname '{card}' provided. "
                       f"Use !nicknames command to see if you have entered the right nickname for the card.")
    except requests.RequestException as e:
        await ctx.send(f"An error occurred while fetching data for '{card}' "
                       f"Use !nicknames command to see if you have entered the right nickname for the card.")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: "
                       f"Use !nicknames command to see if you have entered the right nickname for the card.")


@bot.command(category='Average Values', description='Use !avg <card_name(from !nicknames)> SIM/SWAP_HIVE')
async def avg(ctx, card, symbol):
    try:
        card_name = all_cards_average[card]
    except KeyError:
        await ctx.send(f"Invalid card name '{card}'. Use !check_avg <valid_card_name> SIM/SWAP_HIVE")
        return

    symbol = symbol.upper()

    if symbol not in ['SIM', 'SWAP_HIVE']:
        await ctx.send("Invalid symbol. Use !check_avg <card_name(from !nicknames)> SIM/SWAP_HIVE")
        return
    try:
        sales_data = await get_average(card_name, symbol)
        if len(sales_data) > 0:
            final_value = sum(sales_data) / len(sales_data)
        else:
            final_value = 0
        final_value = round(final_value, 2)

        embed = Embed(title=f'Last 30 sales of {card}',
                      description=f'Sales Values',
                      colour=discord.Colour.blue())

        embed.add_field(name='Sales 1-30',
                        value='\n'.join(f'{index + 1}: {value}' for index, value in enumerate(sales_data) if index < 30))
        embed.add_field(name='Average price based on last 30 sales',
                        value=f'Average Price: {final_value}',
                        inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("An error occurred while processing the request. Please try again later.")
        print(f"Error: {e}")


@bot.command(category='City Value', description='Average value of all cards of a city')
async def city_value(ctx, user_name):
    await ctx.send('Calculating average value of all cards, it might take a minute...')
    city_data = await check_value(user_name)
    await ctx.send(embed=city_data)


@bot.command(category="Market", description="Use !buy <numberOfCards> <cardName(see !nicknames)> <price> <priceSymbol>")
async def buy(ctx,  number_of_cards, card_name, price, price_symbol):
    if card_name is None or number_of_cards is None or price is None or price_symbol is None:
        await ctx.send('Wrong format. Use !buy <numberOfCards> <cardName(see !nicknames)> <price> <priceSymbol>')
        return
    else:
        user_name = get_user(ctx.author.id)
        if user_name is None:
            await ctx.send("You are not registered. Use `!register <user_name>` to register.")
            return
        buy_data = await buy_cards(user_name, card_name, number_of_cards, price, price_symbol)
        if buy_data is None:
            await ctx.send("Either you entered the wrong data, or you do not have enough balance. "
                           "Check your balance with !balance and try again.")
            return
        await ctx.send(embed=buy_data)


@bot.command(category="Market", description="Use !sell <numberOfCards> <cardName(see !nicknames)> <price> <priceSymbol>")
async def sell(ctx, number_of_cards, card_name, price, price_symbol):
    if card_name is None or number_of_cards is None or price is None or price_symbol is None:
        await ctx.send('Wrong format. Use !sell <numberOfCards> <cardName(see !nicknames)> <price> <priceSymbol>')
        return
    else:
        user_name = get_user(ctx.author.id)
        if user_name is None:
            await ctx.send("You are not registered. Use `!register <user_name>` to register.")
            return
        sell_data = await sell_cards(user_name, card_name, number_of_cards, price, price_symbol)
        if sell_data is None:
            await ctx.send("Error, You might have entered wrong data. Please try again.")
            return
        await ctx.send(embed=sell_data)


@bot.command(category="Market", description="Use !change_price <numberOfCards> <cardName(see !nicknames)> "
                                            "<priceOld> <priceNew> <priceSymbol>")
async def change(ctx, number_of_cards, card_name, price_old, price_new, price_symbol):
    if card_name is None or number_of_cards is None or price_old is None or price_new is None or price_symbol is None:
        await ctx.send('Wrong format. Use !change_price'
                       ' <numberOfCards> <cardName(see !nicknames)> <priceOld> <priceNew> <priceSymbol>')
        return
    else:
        user_name = get_user(ctx.author.id)
        if user_name is None:
            await ctx.send("You are not registered. Use `!register <user_name>` to register.")
            return
        new_price_data = await change_price_fn(user_name, card_name, number_of_cards, price_old, price_new, price_symbol)
        if new_price_data is None:
            await ctx.send("Error, You might have entered wrong data. Please try again.")
            return
        await ctx.send(embed=new_price_data)


@bot.command(category="Market", description="Use !cancel <numberOfCards> <cardName(see !nicknames)> "
                                            " <price> <priceSymbol>")
async def cancel(ctx, number_of_cards, card_name, price, price_symbol):
    if card_name is None or number_of_cards is None or price is None or price_symbol is None:
        await ctx.send('Wrong format. Use !cancel'
                       ' <numberOfCards> <cardName(see !nicknames)> <price> <priceSymbol>')
        return
    else:
        user_name = get_user(ctx.author.id)
        if user_name is None:
            await ctx.send("You are not registered. Use `!register <user_name>` to register.")
            return
        cancel_data = await cancel_fn(user_name, card_name, number_of_cards, price, price_symbol)
        if cancel_data is None:
            await ctx.send("Error, You might have entered wrong data. Please try again.")
            return
        await ctx.send(embed=cancel_data)


@bot.command(category="Market", description="Send NFT cards using !send <hive_account_to_transfer> "
                                            "<number_of_cards> <card_name>")
async def send(ctx, hive_account, number_of_cards, card_name):
    if card_name is None or number_of_cards is None or hive_account is None:
        await ctx.send('Wrong format. Use !send <Hive_account_name> <cardName(see !nicknames)> '
                       '<numberOfCards> <priceOld> <priceNew> <priceSymbol>')
        return
    else:
        user_name = get_user(ctx.author.id)
        if user_name is None:
            await ctx.send("You are not registered. Use `!register <user_name>` to register.")
            return
        transfer_cards = await send_cards(user_name, hive_account, card_name, number_of_cards)
        if transfer_cards is None:
            await ctx.send("Error, You might have entered wrong data. Please try again.")
            return
        await ctx.send(embed=transfer_cards)


@bot.command(category="Market", description="Get your market orders !market_orders "
                                            "Or !market_orders username for someone else market orders", hidden=True)
async def market_orders(ctx, hive_account= None):
    try:
        await ctx.send("Feature not working anymore.")
        return
        # if hive_account is None or hive_account.strip() == '':
        #     # If no user_name provided, get the user from the database based on the Discord ID
        #     user = get_user(ctx.author.id)
        #     if user is None:
        #         await ctx.send("You are not registered. Use `!register <user_name>` to register.")
        #         return
        #     result = get_market_data(user)
        #     await ctx.send(embed=result)
        # else:
        #     # If user_name provided, directly check the city
        #     result = get_market_data(hive_account)
        #
        #     # Send the resulting embed
        #     await ctx.send(embed=result)
    except KeyError:
        await ctx.send("Account not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command(category="Market", description="Richlist of top 150 SIM Holders")
async def richlist(ctx):
    try:
        result = rich_list_sim()
        await ctx.send(embed=result)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")



def get_user(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM userData WHERE ID = ?;', (user_id,))
    row = cursor.fetchone()
    connection.close()
    if row:
        return row[2]
    return None


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use `!help` to see available commands.")
    else:
        print(f"An error occurred: {error}")


bot.run(KEY)
