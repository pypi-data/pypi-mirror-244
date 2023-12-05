"""

Bloxlink API Wrapper
~~~~~~~~~~~~~~~~~~~

A basic wrapper for the Bloxlink API.

:copyright: (c) 2023-present Redacted-Nac
:license: MIT, see LICENSE for more details.

"""

__title__ = 'bloxlink.py'
__author__ = 'Redacted-Nac'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023-present Redacted-Nac'
__version__ = '0.1.0'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

import requests

from .exceptions import *


class Bloxlink:
    """
    Represents the Bloxlink client

    :arg token: Your bloxlink API token
    :arg guild: The Discord server ID associated with your token. This can be left blank if you are using a global API token
    """
    def __init__(self, token: str, guild=None):
        self._token = token
        self._guild = guild

    def guild_discord_to_roblox(self, userid: int):
        """
        Perform a lookup for the Discord user and resolve their Roblox ID. This user must be in your Discord server.
        :param userid: A Discord user ID
        :return: The Roblox user ID associated with the Discord user
        """
        headers = {
            "Authorization": self._token
        }

        response = requests.get(f'https://api.blox.link/v4/public/guilds/{self._guild}/discord-to-roblox/{userid}',  headers=headers)

        if response.status_code == 500:
            raise InternalServerError("An internal server error occurred")

        elif response.status_code == 429:
            raise TooManyRequests("Too many requests")

        elif response.status_code == 400:
            raise BadRequest("Bad request")

        elif response.status_code == 200:
            data = response.json()
            try:
                userid = data["robloxID"]
                return userid
            except:
                raise UserNotFound("User not found")
        elif response.status_code == 404:
            raise UserNotFound("User not found")
        else:
            raise Exception(f"{response.status_code}")

    def guild_roblox_to_discord(self, userid: int):
        """
        Performs a reverse lookup in your Discord server for the Roblox user and resolves the Discord ID(s) linked with that Roblox account. All Discord IDs returned are users in your Discord server.
        :param userid: A Roblox user ID
        :return: A list of discord user IDs associated with the Roblox account
        """

        headers = {
            "Authorization": self._token
        }

        response = requests.get(f'https://api.blox.link/v4/public/guilds/{self._guild}/roblox-to-discord/{userid}',  headers=headers)

        if response.status_code == 500:
            raise InternalServerError("An internal server error occurred")

        elif response.status_code == 429:
            raise TooManyRequests("Too many requests")

        elif response.status_code == 400:
            raise BadRequest("Bad request")

        elif response.status_code == 200:
            data = response.json()
            try:
                discordIDs = data["discordIDs"]
                return discordIDs
            except:
                raise UserNotFound("User not found")
        elif response.status_code == 404:
            raise UserNotFound("User not found")
        else:
            raise Exception(f"{response.status_code}")

    def guild_update_user(self, userid: int):
        """
        Programmatically update a Discord user. This is the equivalent as if the user ran /verify in your server.
        :param userid:
        :return: A dict containing the roles added and removed along with the user's new nickname
        """

        headers = {
            "Authorization": self._token
        }

        response = requests.post(f'https://api.blox.link/v4/public/guilds/{self._guild}/update-user/{userid}', headers=headers)

        if response.status_code == 500:
            raise InternalServerError("An internal server error occurred")

        elif response.status_code == 429:
            raise TooManyRequests("Too many requests")

        elif response.status_code == 400:
            raise BadRequest("Bad request")

        elif response.status_code == 200:
            data = response.json()
            try:
                returneddata = {
                    "addedRoles": data["addedRoles"],
                    "removedRoles": data["removedRoles"],
                    "nickname": data['nickname']
                }
            except:
                raise UserNotFound("User not found")
        elif response.status_code == 404:
            raise UserNotFound("User not found")
        else:
            raise Exception(f"{response.status_code}")

    def global_discord_to_roblox(self, userid: int):
        """
        Performs a lookup for the Discord user and resolves their Roblox ID. This user does not need to be in your Discord server.
        :param userid: A Discord user ID
        :return: The Roblox user ID associated with the Discord user.
        """

        headers = {
            "Authorization": self._token
        }

        response = requests.get(f'https://api.blox.link/v4/public/discord-to-roblox/{userid}',  headers=headers)

        if response.status_code == 500:
            raise InternalServerError("An internal server error occurred")

        elif response.status_code == 429:
            raise TooManyRequests("Too many requests")

        elif response.status_code == 400:
            raise BadRequest("Bad request")

        elif response.status_code == 200:
            data = response.json()
            try:
                userid = data["robloxID"]
                return userid
            except:
                raise UserNotFound("User not found")
        elif response.status_code == 404:
            raise UserNotFound("User not found")
        else:
            raise Exception(f"{response.status_code}")

    def global_roblox_to_discord(self, userid: int):
        """
        Performs a reverse lookup for the Roblox user and resolves the Discord ID(s) linked with that Roblox account.
        :param userid: A Roblox user ID
        :return: A list of discord user IDs associated with the Roblox account
        """

        headers = {
            "Authorization": self._token
        }

        response = requests.get(f'https://api.blox.link/v4/public/roblox-to-discord/{userid}',  headers=headers)

        if response.status_code == 500:
            raise InternalServerError("An internal server error occurred")

        elif response.status_code == 429:
            raise TooManyRequests("Too many requests")

        elif response.status_code == 400:
            raise BadRequest("Bad request")

        elif response.status_code == 200:
            data = response.json()
            try:
                discordIDs = data["discordIDs"]
                return discordIDs
            except:
                raise UserNotFound("User not found")
        elif response.status_code == 404:
            raise UserNotFound("User not found")
        else:
            raise Exception(f"{response.status_code}")