import requests
import discord


def get_token_holders(offset):
    url = "https://herpc.dtools.dev/contracts"
    params = {
        'contract': 'tokens',
        'table': 'balances',
        'query': {'symbol': 'SIM', 'balance': {'$gt': '10000'}},
        'limit': 1000,
        'offset': offset,
        'indexes': []
    }
    j = {'jsonrpc': '2.0', 'id': 1, 'method': 'find', 'params': params}

    with requests.post(url, json=j) as response:
        if response.status_code == 200:
            data = response.json()

            if len(data['result']) == 1000:
                data['result'] += get_token_holders(offset + 1000)

            if 'result' in data:
                return data['result']
            else:
                print("Response doesn't contain 'result' field:", data)
        else:
            print("Request failed with status code:", response.status_code)


def rich_list_sim():
    all_data = get_token_holders(0)
    accounts_to_ignore = ['dcitygame', 'dcitybids', 'dcityrewards', 'dcitycards']

    all_data = sorted(all_data, key=lambda x: float(x['balance']), reverse=True)
    all_data = [data for data in all_data if float(data['balance']) > 50000 and
                data['account'] not in accounts_to_ignore][
               :50]

    embed = discord.Embed(title=f'Richlist of SIM Holders', description='Richlist', colour=discord.Colour.yellow())

    holder_list_25 = "\n".join(f'{index + 1}. {data["account"]}: {round(float(data["balance"]), 2)}'
                            for index, data in enumerate(all_data)
                            if index < 25)
    holder_list_50 = "\n".join(f'{index + 1}. {data["account"]}: {round(float(data["balance"]), 2)}'
                            for index, data in enumerate(all_data)
                            if 25 <= index < 50)

    embed.add_field(name='Top 1-25 Holders', value=holder_list_25)
    embed.add_field(name='Top 25-50 Holders', value=holder_list_50)

    return embed
