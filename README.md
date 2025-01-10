# Discord Auto-MiddleMan Bot !
The most secure discord auto middleman bot for your discord market server ! With somes features

## Table Of Content

✨ [Installation](#install) <br/>
🧪 [Configuration](#config)<br/>
📍 [Starting](#start)<br/>


## Installation
<div id="install"></div>

Clone the repository:
```
git clone https://github.com/Celentroft/AutoMm-bot.git
```
Install requirements:
```
pip install -r requirements.txt
```
(Don't forget to install python !)

## Configuration
<div id="config"></div>

After the installation you need to configure the `config.json` file
```json
{
    "developer": "patato", -> Dont be a skid lmao
    "token": "token", -> Your bot token
    "buyer": null, -> Your discord Id
    "color": "hex_color", -> Embeds Colors (Hex Code)
    "footer": "Your footer", -> Embeds Footer (strings)
    "blockcypher": "blockcypher", -> Blockcypher api key 
    "whitelist": [], -> Don't need to change (using with commands)
    "scammers": [], -> Useless
    "config": {
        "logs": {
            "status": "off",
            "channel": null
        },
        "tickets": {
            "category": null
        }
    }
}
```

## Starting
<div id="start"></div>

After the bot configuration, you need to run the bot :O
```
python main.py
```
And you may see a nice commands output logs !


## Please star this repository !
