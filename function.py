import time
import json
import string
import random
import discord
import requests
import blockcypher
from datetime import datetime
from typing import Dict, Any, Literal

def load_json() -> Dict[str, Any]:
    return json.load(open("config.json", 'r'))

def embed_color() -> int:
    config = load_json()
    return int(config['color'], 16)

def footer(bot, uid) -> str:
    now = datetime.now().strftime("%H:%M:%S")
    return f"[{now}] - {bot.user.name} | MiddleMan bot by Potato.Service| uid: {uid}"

async def unauthorized(interaction) -> None:
    embed = discord.Embed(
        title="`❌`・Unauthorized Command",
        description="*You cannot use this interaction.*",
        color=embed_color()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
def gen_uid(lenght=3, long=4) -> str:
    filename = ""
    for _ in range(lenght):
        letters = string.ascii_lowercase + string.ascii_lowercase + str("1234567890")
        for _ in range(long):
            filename += random.choice(letters)
        filename += "-"
    filename = filename[:-1]
    return filename

def create_wallet() -> (tuple[Any, Any, Any, Any] | tuple[Literal['Error'], None, None, None]):
    config = load_json()
    response = requests.post("https://api.blockcypher.com/v1/ltc/main/addrs", params={"token": config['blockcypher']})
    print(response.status_code)
    if response.status_code == 201:
        data = response.json()
        print(data)
        address = data['address']
        private = data['private']
        public = data['public']
        wif = data['wif']  
        return address, private, public, wif
    else:
        return "Error", None, None, None

def check_transactions(address) -> (tuple[Literal['detected but not confirmed'], Literal[0]] | tuple[Literal['confirmed'], Any] | tuple[Literal['balance are null'], Literal[0]] | tuple[Literal['any'], Literal[0]] | tuple[Literal['error'], Literal[0]] | None):
    url = f'https://api.blockcypher.com/v1/ltc/main/addrs/{address}/full'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        if 'txs' in data:
            if data['unconfirmed_balance'] != 0 and data['balance'] == 0:
                return "detected but not confirmed", 0
            if data['balance'] != 0 and data['unconfirmed_balance'] == 0:
                return "confirmed", data['balance']
            if data['balance'] == 0 and data['unconfirmed_balance'] == 0:
                return "balance are null", 0
        else:
            return "any", 0
    else:
        return "error", 0
    
def send_to_address(prvKey, toAddress) -> (Any | None):
    config = load_json()
    a = blockcypher.simple_spend(
        from_privkey=prvKey, 
        to_address=toAddress,
        api_key=config['blockcypher'], 
        coin_symbol="ltc",
        to_satoshis=-1
    )
    return a

def convertToLtc(amount) -> (Any | None):
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=eur'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        price = data['litecoin']['eur']
        converted = amount * price
        return converted
    else:
        print(response.text)
        return None
