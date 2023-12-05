# bloxlink.py

## Overview
Bloxlink.py is a lightweight wrapper for the [Bloxlink](https://blox.link) API.

## Installation
To install the latest stable version of bloxlink.py, run the following command:

`python3 -m pip install bloxlink.py`

To install the latest **unstable** version of bloxlink.py, install [git-scm](https://git-scm.com/downloads) and run the following:

`python3 -m pip install git+https://github.com/Redacted-Nac/bloxlink.py.git`

## Basic Usage

### Fetch ROBLOX user ID from Discord ID with the guild API

```python

from src import bloxlink

client = bloxlink.Bloxlink(token="YOUR TOKEN HERE", guild=GUILDIDHERE)

userid = client.guild_discord_to_roblox(userid=IDHERE)

print(userid)
```

### Fetch Discord user ID from ROBLOX ID with the guild API

```python

from src import bloxlink

client = bloxlink.Bloxlink(token="YOUR TOKEN HERE", guild=DISCORDGUILDIDHERE)

userid = client.guild_roblox_to_discord(userid=IDHERE)

print(userid)
```