import warnings
warnings.filterwarnings("ignore", message="Can not find any timezone configuration, defaulting to UTC.", module="tzlocal")
import os
import json
import fortnitepy
import requests
import aiohttp
import asyncio
import random
import functools
import re


url = "https://package.lobbybots.xyz/skins"
response = requests.get(url)
if response.status_code == 200:
    skins = response.json()

url = "https://package.lobbybots.xyz/backpacks"
response = requests.get(url)
if response.status_code == 200:
    backpacks = response.json()

url = "https://package.lobbybots.xyz/pickaxes"
response = requests.get(url)
if response.status_code == 200:
    pickaxes = response.json()

url = "https://package.lobbybots.xyz/emotes"
response = requests.get(url)
if response.status_code == 200:
    emotes = response.json()

async def set_skin(client, skin_input):
    # Remove any leading or trailing spaces
    skin_input = skin_input.strip()

    # Split input into a list of words
    skin_words = skin_input.split()

    # Look up skin by name
    for skin in skins:
        skin_name_words = skin["name"].lower().split()
        if all(word in skin_name_words for word in skin_words):
            await client.party.me.set_outfit(skin["id"])
            return

    # Look up skin by ID
    for skin in skins:
        if skin["id"] == skin_input:
            await client.party.me.set_outfit(skin["id"])

async def set_backpack(client, backpack_input):
    # Remove any leading or trailing spaces
    backpack_input = backpack_input.strip()

    # Split input into a list of words
    backpack_words = backpack_input.split()

    # Look up backpack by name
    for backpack in backpacks:
        backpack_name_words = backpack["name"].lower().split()
        if all(word in backpack_name_words for word in backpack_words):
            await client.party.me.set_backpack(backpack["id"])
            return

    # Look up backpack by ID
    for backpack in backpacks:
        if backpack["id"] == backpack_input:
            await client.party.me.set_backpack(backpack["id"])

async def set_pickaxe(client, pickaxe_input):
    # Remove any leading or trailing spaces
    pickaxe_input = pickaxe_input.strip()

    # Split input into a list of words
    pickaxe_words = pickaxe_input.split()

    # Look up pickaxe by name
    for pickaxe in pickaxes:
        pickaxe_name_words = pickaxe["name"].lower().split()
        if all(word in pickaxe_name_words for word in pickaxe_words):
            await client.party.me.set_pickaxe(pickaxe["id"])
            return

    # Look up pickaxe by ID
    for pickaxe in pickaxes:
        if pickaxe["id"] == pickaxe_input:
            await client.party.me.set_pickaxe(pickaxe["id"])

async def set_emote(client, emote_input):
    # Remove any leading or trailing spaces
    emote_input = emote_input.strip()

    # Split input into a list of words
    emote_words = emote_input.split()

    # Look up emote by name
    for emote in emotes:
        emote_name_words = emote["name"].lower().split()
        if all(word in emote_name_words for word in emote_words):
            await client.party.me.set_emote(emote["id"])
            return

    # Look up emote by ID
    for emote in emotes:
        if emote["id"] == emote_input:
            await client.party.me.set_emote(emote["id"])

def login_to_fortnite(device_auth_file, config_file):
    # Read device auth details from file
    with open(device_auth_file) as file:
        device_auths = json.load(file)

    # Get the latest device auth details
    device_auth = device_auths[-1]

    # Initialize the Fortnite client
    client = fortnitepy.Client(
        auth=fortnitepy.DeviceAuth(
            device_id=device_auth['device_id'],
            account_id=device_auth['account_id'],
            secret=device_auth['secret'],
        )
    )

    async def set_and_update_party_prop(schema_key: str, new_value: str):
        prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}
        await client.party.patch(updated=prop)

    # Define a function to calculate the Levenshtein distance between two strings
    def levenshtein_distance(s1, s2):
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)

        for i, c1 in enumerate(s1):
            current_row = [i + 1]

            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)

                current_row.append(min(insertions, deletions, substitutions))

            previous_row = current_row

        return previous_row[-1]

    # Define event handlers
    @client.event
    async def event_ready():
        print('\033[36m' + "[FnLobbyBot] " + '\033[32m' + f"Logged in as {client.user.display_name}" + '\033[0m')
        async with aiohttp.ClientSession() as session:
            async with session.get('https://package.lobbybots.xyz/on_ready') as resp:
                if resp.status != 200:
                    print(f'Error connecting to api. Error code: {resp.status}')
                    return

                data = await resp.json()

                status = data[0]['Status']
                status2 = data[1]['Status2']
            await client.set_presence(status)
            await client.party.me.set_banner(season_level=100)
            await client.party.me.set_battlepass_info(has_purchased=True, level=100)
            await client.set_presence(status2)
            await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            # Accept all pending friend requests
            with open(config_file, 'r') as f:
                config = json.load(f)

            accept_friend_requests = str(config.get('accept_friend_requests', False))

            if accept_friend_requests == 'True':
                pending_friends = client.incoming_pending_friends
                for friend in pending_friends:
                    await friend.accept()
                    print('\033[36m' + "[FnLobbyBot] " + '\033[97m' + f'Accepted friend request from {friend.display_name}' + '\033[0m')

    @client.event
    async def event_party_member_leave(member: fortnitepy.PartyMember):
        if len(client.party.members) == 1:
            print('\033[36m' + "[FnLobbyBot] " + "Bot is the only one in the party." + '\033[0m')
            await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

    @client.event
    async def event_party_invite(invite: fortnitepy.ReceivedPartyInvitation):
        print('\033[36m' + "[FnLobbyBot] " + '\033[97m' + f'Received party invite from {invite.sender.display_name}' + '\033[0m')
        with open(config_file, 'r') as f:
            config = json.load(f)

        accept_invites = str(config.get('accept_invites', False))

        if accept_invites == 'True':
            await invite.accept()
            print('\033[36m' + "[FnLobbyBot] " + '\033[97m' + f'Accepted party invite from {invite.sender.display_name}' + '\033[0m')

    @client.event
    async def event_party_member_join(member: fortnitepy.PartyMember):
        print('\033[36m' + "[FnLobbyBot] " + f"{member.display_name} joined the party." + '\033[0m')

        async with aiohttp.ClientSession() as session:
            async with session.get('https://package.lobbybots.xyz/member_join') as resp:
                if resp.status != 200:
                    print(f'Error connecting to api. Error code: {resp.status}')
                    await client.party.send(f'Error connecting to api. Error code: {resp.status}')
                    return

                data = await resp.json()

                join_message = config['join_message'] + '\n' + data[0]['Join_message']
                if '{member.display_name}' in join_message:
                    join_message = join_message.replace('{member.display_name}', member.display_name)
                skin = data[2]['Skin'] if config['skin'] == 'auto' else config['skin']
                backpack = data[3]['Backpack'] if config['backpack'] == 'auto' else config['backpack']
                pickaxe = data[4]['Pickaxe'] if config['pickaxe'] == 'auto' else config['pickaxe']
                emote = data[5]['Emote'] if config['emote'] == 'auto' else config['emote']
                level = data[6]['Level'] if config['level'] == 'auto' else config['level']

                await client.party.me.set_outfit(skin)
                await client.party.me.set_backpack(backpack)
                await client.party.me.set_pickaxe(pickaxe)
                await client.party.me.set_emote(emote)
                await client.party.me.set_banner(season_level=level)
                await client.party.me.set_battlepass_info(has_purchased=True, level=level)

                # Send a message in the party chat
                await client.party.send(join_message)

    @client.event
    async def event_friend_request(request):
        print('\033[36m' + "[FnLobbyBot] " + '\033[97m' + f'Received friend request from: {request.display_name}.' + '\033[0m')

        with open(config_file, 'r') as f:
            config = json.load(f)

        accept_friend_requests = str(config.get('accept_friend_requests', False))

        if accept_friend_requests == 'True':
            await request.accept()
            print('\033[36m' + "[FnLobbyBot] " + '\033[97m' + f'Accepted friend request from {request.display_name}' + '\033[0m')

    @client.event
    async def event_party_message(message: fortnitepy.PartyMessage):
        content = message.content.lower()
        args = message.content.lower().split()

        if message.content.lower() == '!update':
            await message.reply("Updating packages...")

            try:
                response = requests.get("https://package.lobbybots.xyz/newest_version")
                response.raise_for_status()  # Raise an exception for non-2xx status codes

                newest_version = response.json()[0].get('Version', None)
                if newest_version:
                    await message.reply(f"Newest version available: {newest_version}")

                    # Perform the necessary actions to update the package to the newest version
                    os.system(f"pip install --upgrade fortnitepy > /dev/null 2>&1; pip install --upgrade -i https://test.pypi.org/simple/ testlobby=={newest_version} > /dev/null 2>&1")

                    await message.reply("Package update completed.")
                else:
                    await message.reply("Failed to retrieve the newest version.")

            except requests.exceptions.RequestException as e:
                await message.reply(f"An error occurred while updating packages: {e}")

        if message.content.lower() == '!ready':
            await client.party.me.set_ready(fortnitepy.ReadyState.READY)
            await message.reply("Ready! Note: Bots can't play games!")

        if message.content.lower() == '!unready':
            await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
            await message.reply("Unready! Note: Bots can't play games!")

        if message.content.lower() == '!sitout':
            await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
            await message.reply("Sitting Out! Note: Bots can't play games!")

        if message.content.lower().startswith('!crowns'):
            args = message.content.split()
            if len(args) == 1:
                amount = 100
            else:
                amount = int(args[1])
            meta = client.party.me.meta
            data = (meta.get_prop('Default:AthenaCosmeticLoadout_j'))['AthenaCosmeticLoadout']

            try:
                data['cosmeticStats'][1]['statValue'] = amount
            except KeyError:
                data['cosmeticStats'] = [{"statName": "TotalVictoryCrowns", "statValue": amount},
                                        {"statName": "TotalRoyalRoyales", "statValue": amount},
                                        {"statName": "HasCrown", "statValue": 0}]

            final = {'AthenaCosmeticLoadout': data}
            key = 'Default:AthenaCosmeticLoadout_j'
            prop = {key: meta.set_prop(key, final)}

            await client.party.me.patch(updated=prop)
            await client.party.me.clear_emote()
            await client.party.me.set_emote('EID_Coronet')
            await message.reply("Emoteing Crowning Achievement!")

        if args[0] == '!skin':
            # Check if there are enough arguments
            if len(args) < 2:
                return await message.reply("Please specify a skin name.")

            # Get the skin name from the user's message
            skin_name = " ".join(args[1:])

            # Set the user's skin
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method="GET",
                        url=f"https://package.lobbybots.xyz/skins"
                ) as request:
                    data = (await request.json())

            # Find the closest matching skin using Levenshtein distance
            closest_match = None
            lowest_distance = float('inf')

            for skin in data:
                distance = levenshtein_distance(skin_name.lower(), skin.get("name", "").lower())
                if distance < lowest_distance:
                    closest_match = skin
                    lowest_distance = distance

            if lowest_distance > 3:  # You can adjust this threshold as needed
                return await message.reply(f"No close match found for {skin_name}.")

            if "brcosmetics" in closest_match['path'].lower():
                path = f"AthenaCharacterItemDefinition'/BRCosmetics/Athena/Items/Cosmetics/Characters/{closest_match['id']}.{closest_match['id']}'"
                await client.party.me.set_outfit(asset=path)
            else:
                await client.party.me.set_outfit(asset=closest_match['id'])

            await message.reply(f"Skin set to {closest_match['name']}.")

        if args[0] == '!backpack':
            # Check if there are enough arguments
            if len(args) < 2:
                return await message.reply("Please specify a backpack name.")

            # Get the backpack name from the user's message
            backpack_name = " ".join(args[1:])

            # Set the user's backpack
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method="GET",
                        url=f"https://package.lobbybots.xyz/backpacks"
                ) as request:
                    data = (await request.json())

            # Find the closest matching backpack using Levenshtein distance
            closest_match = None
            lowest_distance = float('inf')

            for backpack in data:
                distance = levenshtein_distance(backpack_name.lower(), backpack.get("name", "").lower())
                if distance < lowest_distance:
                    closest_match = backpack
                    lowest_distance = distance

            if lowest_distance > 3:  # You can adjust this threshold as needed
                return await message.reply(f"No close match found for {backpack_name}.")

            if "brcosmetics" in closest_match['path'].lower():
                path = f"AthenaBackpackItemDefinition'/BRCosmetics/Athena/Items/Cosmetics/Backpacks/{closest_match['id']}.{closest_match['id']}'"
                await client.party.me.set_backpack(asset=path)
            else:
                await client.party.me.set_backpack(asset=closest_match['id'])

            await message.reply(f"Backpack set to {closest_match['name']}.")

        if args[0] == '!pickaxe':
            # Check if there are enough arguments
            if len(args) < 2:
                return await message.reply("Please specify a pickaxe name.")

            # Get the pickaxe name from the user's message
            pickaxe_name = " ".join(args[1:])

            # Set the user's pickaxe
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method="GET",
                        url=f"https://package.lobbybots.xyz/pickaxes"
                ) as request:
                    data = (await request.json())

            # Find the closest matching pickaxe using Levenshtein distance
            closest_match = None
            lowest_distance = float('inf')

            for pickaxe in data:
                distance = levenshtein_distance(pickaxe_name.lower(), pickaxe.get("name", "").lower())
                if distance < lowest_distance:
                    closest_match = pickaxe
                    lowest_distance = distance

            if lowest_distance > 3:  # You can adjust this threshold as needed
                return await message.reply(f"No close match found for {pickaxe_name}.")

            if "brcosmetics" in closest_match['path'].lower():
                path = f"AthenaPickaxeItemDefinition'/BRCosmetics/Athena/Items/Cosmetics/PickAxes/{closest_match['id']}.{closest_match['id']}'"
                await client.party.me.set_pickaxe(asset=path)
                await client.party.me.set_emote("EID_IceKing")
            else:
                await client.party.me.set_pickaxe(asset=closest_match['id'])
                await client.party.me.set_emote("EID_IceKing")

            await message.reply(f"Pickaxe set to {closest_match['name']}.")

        if args[0] == '!emote':
            # Check if there are enough arguments
            if len(args) < 2:
                return await message.reply("Please specify an emote name.")

            # Get the emote name from the user's message
            emote_name = " ".join(args[1:])

            # Set the user's emote
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method="GET",
                        url=f"https://package.lobbybots.xyz/emotes"
                ) as request:
                    data = (await request.json())

            # Find the closest matching emote using Levenshtein distance
            closest_match = None
            lowest_distance = float('inf')

            for emote in data:
                distance = levenshtein_distance(emote_name.lower(), emote.get("name", "").lower())
                if distance < lowest_distance:
                    closest_match = emote
                    lowest_distance = distance

            if lowest_distance > 3:  # You can adjust this threshold as needed
                return await message.reply(f"No close match found for {emote_name}.")

            if "brcosmetics" in closest_match['path'].lower():
                await client.party.me.clear_emote()
                path = f"AthenaDanceItemDefinition'/BRCosmetics/Athena/Items/Cosmetics/Dances/{closest_match['id']}.{closest_match['id']}'"
                await client.party.me.set_emote(asset=path)
            else:
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset=closest_match['id'])

            await message.reply(f"Emote set to {closest_match['name']}.")

        if message.content.lower().startswith('!level'):
            level = message.content.split(' ')[1]
            await client.party.me.set_banner(season_level=level)
            await message.reply(f"Level set to {level}!")

        if message.content.lower().startswith('!bp'):
            teir = message.content.split(' ')[1]
            await client.party.me.set_battlepass_info(
            has_purchased=True, level=teir)
            await message.reply(f"Teir set to {teir}!")

        if message.content.lower().startswith('!echo'):
            message_parts = message.content.split(' ')[1:]
            echoed_message = ' '.join(message_parts)
            await client.party.send(echoed_message)

        if message.content.lower() == '!point':
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_IceKing")
            await message.reply("Pointing out my pickaxe!")

        if message.content.lower().startswith('!privacy'):
            privacy = message.content.split(' ')[1]
            if privacy.lower() == 'public':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                await message.reply("Privacy set to PUBLIC!")
            elif privacy.lower() == 'friends_allow_friends_of_friends':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS_ALLOW_FRIENDS_OF_FRIENDS)
                await message.reply("Privacy set to FRIENDS_ALLOW_FRIENDS_OF_FRIENDS!")
            elif privacy.lower() == 'friends':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS)
                await message.reply("Privacy set to FRIENDS!")
            elif privacy.lower() == 'private_allow_friends_of_friends':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE_ALLOW_FRIENDS_OF_FRIENDS)
                await message.reply("Privacy set to PRIVATE_ALLOW_FRIENDS_OF_FRIENDS!")
            elif privacy.lower() == 'private':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
                await message.reply("Privacy set to PRIVATE!")
            else:
                await message.reply('Invalid privacy setting. Please use "public"/"friends_allow_friends_of_friends"/"friends"/"private_allow_friends_of_friends" or "private"!')

        if message.content.lower() == '!rareskins':
            await message.reply("Showing all Rare Skins!")
            purpleskull_skin_variants = client.party.me.create_variants(
                clothing_color=1
            )
            await client.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=purpleskull_skin_variants
        )
            await message.reply("Skin set to Purple Skull Trooper!")
            await asyncio.sleep(2)
            await client.party.me.set_outfit("CID_028_Athena_Commando_F")
            await message.reply("Skin set to Renegade Raider!")
            await asyncio.sleep(2)
            pinkghoul_skin_variants = client.party.me.create_variants(
                material=3
            )
            await client.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=pinkghoul_skin_variants
        )
            await message.reply("Skin set to Pink Ghoul Trooper!")
            await asyncio.sleep(2)
            await client.party.me.set_outfit("CID_017_Athena_Commando_M")
            await message.reply("Skin set to Aerial Assault Trooper!")
            await message.reply("Those are all of the Rare Skins!")

        if message.content.lower() == '!rarebackpacks':
            await message.reply("Showing all Rare Backpacks!")
            await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await asyncio.sleep(1)
            await client.party.me.set_backpack("BID_140_StreetOpsMale")
            await message.reply("Backpack set to Response Unit!")
            await asyncio.sleep(4)
            await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await asyncio.sleep(1)
            await client.party.me.set_backpack("BID_027_Scavenger")
            await message.reply("Backpack set to Rust Bucket!")
            await asyncio.sleep(4)
            await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await asyncio.sleep(1)
            await client.party.me.set_backpack("BID_029_RetroGrey")
            await message.reply("Backpack set to Backup Plan!")
            await asyncio.sleep(4)
            await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await asyncio.sleep(1)
            await client.party.me.set_backpack("BID_138_Celestial")
            await message.reply("Backpack set to Galactic Disc!")
            await asyncio.sleep(4)
            await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await asyncio.sleep(1)
            await client.party.me.set_backpack("BID_114_ModernMilitaryRed")
            await message.reply("Backpack set to Telemetry!")
            await message.reply("Those are all of the Rare Backpacks!")

        if message.content.lower() == '!rarepickaxes':
            await message.reply("Showing all Rare Pickaxes!")
            await client.party.me.clear_emote()
            await client.party.me.set_pickaxe("Pickaxe_ID_376_FNCS")
            await message.reply("Pickaxe set to Axe Of Champions!")
            await client.party.me.set_emote("EID_IceKing")
            await asyncio.sleep(8)
            await client.party.me.clear_emote()
            await client.party.me.set_pickaxe("Pickaxe_ID_069_DarkViking")
            await message.reply("Pickaxe set to Permafrost!")
            await client.party.me.set_emote("EID_IceKing")
            await asyncio.sleep(8)
            await client.party.me.clear_emote()
            await client.party.me.set_pickaxe("Pickaxe_Lockjaw")
            await message.reply("Pickaxe set to Raiders Revenge!")
            await client.party.me.set_emote("EID_IceKing")
            await asyncio.sleep(8)
            await client.party.me.clear_emote()
            await client.party.me.set_pickaxe("Pickaxe_ID_189_StreetOpsStealth")
            await message.reply("Pickaxe set to Stealth Angular Axe!")
            await client.party.me.set_emote("EID_IceKing")
            await asyncio.sleep(8)
            await client.party.me.clear_emote()
            await client.party.me.set_pickaxe("Pickaxe_ID_075_Huya")
            await message.reply("Pickaxe set to Pointer!")
            await client.party.me.set_emote("EID_IceKing")
            await message.reply("Those are all of the Rare Pickaxe!")

        if message.content.lower() == '!rareemotes':
            await message.reply("Showing all Rare Emotes!")
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_Fresh")
            await message.reply("Emote set to Fresh!")
            await asyncio.sleep(4)
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_AshtonBoardwalk")
            await message.reply("Emote set to Widow’s Pirouette!")
            await asyncio.sleep(4)
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_RunningManv3")
            await message.reply("Emote set to Pick It Up!")
            await asyncio.sleep(4)
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_TapShuffle")
            await message.reply("Emote set to Hootenanny!")
            await asyncio.sleep(4)
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_CycloneHeadBang")
            await message.reply("Emote set to Head Banger!")
            await message.reply("Those are all of the Rare Emotes!")

        if message.content.lower() == '!invite':
            # invite the user who sent the message
            member = await client.fetch_profile(message.author.id, cache=False, raw=False)
            await client.party.invite(member.id)
            await message.reply(f"Invited {member.display_name} to the party.")

        if message.content.startswith('!invite '):
            username = message.content[8:].strip()
            members = client.friends
            member = next((m for m in members if m.display_name.lower() == username.lower() or m.id == username), None)
            if member:
                await client.party.invite(member.id)
                await message.reply(f"Invited {member.display_name} to the party.")
            else:
                await message.reply("Could not find a member with that name or ID!")

        if message.content.lower() == '!stop':
            await client.party.me.clear_emote()
            await message.reply("Stopped emoteing!")

        if message.content.startswith("!join"):
            try:
                user = await client.fetch_profile(message.author.id)
                friend = client.get_friend(user.id)

                await friend.join_party()
                await message.reply(f"Joined {friend.display_name}'s party.")
            except fortnitepy.Forbidden:
                await message.reply("I can't join your party because it's private.")
            except fortnitepy.PartyError:
                await message.reply("I am already in the party.")
            except fortnitepy.HTTPException:
                await message.reply("Something went wrong while joining the party.")
            except AttributeError:
                await message.reply("I couldn't find that user.")

        if message.content.startswith("!promote"):
            user = await client.fetch_user(message.author.id)
            member = client.party.get_member(user.id)

            try:
                await member.promote()
                await message.reply(f"Promoted: {member.display_name}")
            except fortnitepy.Forbidden:
                await message.reply("I am not party leader.")
            except fortnitepy.PartyError:
                await message.reply("You already are the party leader.")
            except fortnitepy.HTTPException:
                await message.reply("Something went wrong trying to promote you.")
            except AttributeError:
                await message.reply("I couldn't find you.")

        if message.content.startswith("!kick"):
            content = message.content.split()
            member = None

            if len(content) > 1:
                member = content[1]

            try:
                if member is None:
                    user = await client.fetch_user(message.author.display_name)
                    member = client.party.get_member(user.id)
                else:
                    user = await client.fetch_user(member)
                    member = client.party.get_member(user.id)

                if member is None:
                    await message.reply("Couldn't find that user, are they in the party?")
                    return

                await member.kick()
                await message.reply(f"Kicked: {member.display_name}")
            except fortnitepy.Forbidden:
                await message.reply("I can't kick that user, I am not the party leader.")
            except fortnitepy.PartyError:
                await message.reply("Nice try, but I can't kick myself.")
            except AttributeError:
                await message.reply("I couldn't find that user.")
            except fortnitepy.HTTPException:
                await message.reply("I couldn't find that user.")

        if message.content.lower() == '!leave':
            await message.reply("Leaveing the party!")
            await client.party.me.leave()

        if message.content.lower() == '!griddy':
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_Griddles")
            await message.reply("Emote set to Get Griddy")

        if message.content.lower() == '!purpleskull':
            purpleskull_skin_variants = client.party.me.create_variants(
                clothing_color=1
            )
            await client.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=purpleskull_skin_variants
        )
            await message.reply("Skin set to Purple Skull Trooper")

        if message.content.lower() == '!renegaderaider':
            await client.party.me.set_outfit("CID_028_Athena_Commando_F")
            await message.reply("Skin set to Renegade Raider")

        if message.content.lower() == '!pinkghoul':
            pinkghoul_skin_variants = client.party.me.create_variants(
                material=3
            )
            await client.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=pinkghoul_skin_variants
        )
            await message.reply("Skin set to Pink Ghoul Trooper")

        if message.content.lower() == '!aerial':
            await client.party.me.set_outfit("CID_017_Athena_Commando_M")
            await message.reply("Skin set to Aerial Assault Trooper")

        if message.content.lower() == '!ikonik':
            await client.party.me.set_outfit("CID_313_Athena_Commando_M_KpopFashion")
            await message.reply("Skin set to Ikonik")

        if message.content.lower() == '!ninja':
            await client.party.me.set_outfit("CID_605_Athena_Commando_M_TourBus")
            await message.reply("Skin set to Ninja")

        if message.content.lower() == "!hologram":
            await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await message.reply("Skin set to Hologram")

        if message.content.lower().startswith("!gift"):
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_NeverGonna")
            await message.reply("Nice try but I can't gift!")

        if message.content.lower() == "!tbd":
            response = requests.get("https://package.lobbybots.xyz/skins")
            data = response.json()
            await message.reply("Showing all TBD skins!")

            for item in data:
                if item.get("name") == "TBD":
                    skin_name = item.get("name")
                    await client.party.me.set_outfit(item.get("id"))
                    await message.reply(f"Skin set to {skin_name}")
                    await asyncio.sleep(2)

            await message.reply("Those are all of the TBD skins!")

        if message.content.lower() == "!shop skins":
            response = requests.get("https://package.lobbybots.xyz/shop/skins")
            data = response.json()

            if not data:
                await message.reply("Theres no new skins!")
            else:
                await message.reply("Showing all new skins!")
                for item in data:
                    skin_name = item.get("name")
                    await client.party.me.clear_emote()
                    await client.party.me.set_outfit(item.get("id"))
                    await message.reply(f"Skin set to {skin_name}")
                    await asyncio.sleep(2)

                await message.reply("Thats it for now!")

        if message.content.lower() == "!shop backpacks":
            response = requests.get("https://package.lobbybots.xyz/shop/backpacks")
            data = response.json()

            if not data:
                await message.reply("Theres no new backpacks!")
            else:
                await message.reply("Showing all new backpacks!")
                await client.party.me.clear_backpack()
                await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
                for item in data:
                    backpack_name = item.get("name")
                    await client.party.me.clear_emote()
                    await client.party.me.set_backpack(item.get("id"))
                    await message.reply(f"Backpack set to {backpack_name}")
                    await asyncio.sleep(2)

                await message.reply("Thats it for now!")

        if message.content.lower() == "!shop pickaxes":
            response = requests.get("https://package.lobbybots.xyz/shop/pickaxes")
            data = response.json()

            if not data:
                await message.reply("Theres no new pickaxes!")
            else:
                await message.reply("Showing all new pickaxes!")
                for item in data:
                    pickaxe_name = item.get("name")
                    await client.party.me.clear_emote()
                    await client.party.me.set_pickaxe(item.get("id"))
                    await client.party.me.set_emote("EID_IceKing")
                    await message.reply(f"Pickaxe set to {pickaxe_name}")
                    await asyncio.sleep(6)

                await message.reply("Thats it for now!")

        if message.content.lower() == "!shop emotes":
            response = requests.get("https://package.lobbybots.xyz/shop/emotes")
            data = response.json()

            if not data:
                await message.reply("Theres no new emotes!")
            else:
                await message.reply("Showing all new emotes!")
                for item in data:
                    emote_name = item.get("name")
                    await client.party.me.clear_emote()
                    await client.party.me.set_emote(item.get("id"))
                    await message.reply(f"Emote set to {emote_name}")
                    await asyncio.sleep(4)

                await message.reply("Thats it for now!")

        if message.content.lower() == '!hatlessrecon':
            skin_variants = client.party.me.create_variants(
                parts=2
            )

            await client.party.me.set_outfit(
                asset='CID_022_Athena_Commando_F',
                variants=skin_variants
            )
            await message.reply("Skin set to Recon Expert!")

        if message.content.lower() == '!henchman':
            random_henchman = random.choice(
                [
                    "CID_794_Athena_Commando_M_HenchmanBadShorts_D",
                    "CID_NPC_Athena_Commando_F_HenchmanSpyDark",
                    "CID_791_Athena_Commando_M_HenchmanGoodShorts_D",
                    "CID_780_Athena_Commando_M_HenchmanBadShorts",
                    "CID_NPC_Athena_Commando_M_HenchmanGood",
                    "CID_692_Athena_Commando_M_HenchmanTough",
                    "CID_707_Athena_Commando_M_HenchmanGood",
                    "CID_792_Athena_Commando_M_HenchmanBadShorts_B",
                    "CID_793_Athena_Commando_M_HenchmanBadShorts_C",
                    "CID_NPC_Athena_Commando_M_HenchmanBad",
                    "CID_790_Athena_Commando_M_HenchmanGoodShorts_C",
                    "CID_779_Athena_Commando_M_HenchmanGoodShorts",
                    "CID_NPC_Athena_Commando_F_RebirthDefault_Henchman",
                    "CID_NPC_Athena_Commando_F_HenchmanSpyGood",
                    "CID_706_Athena_Commando_M_HenchmanBad",
                    "CID_789_Athena_Commando_M_HenchmanGoodShorts_B"
                ]
            )

            await client.party.me.set_outfit(
                asset=random_henchman
            )
            await message.reply("Skin set to a random henchman!")

        if message.content.lower() == '!marauder':
            random_marauder = random.choice(
                [
                    "CID_NPC_Athena_Commando_M_MarauderHeavy",
                    "CID_NPC_Athena_Commando_M_MarauderElite",
                    "CID_NPC_Athena_Commando_M_MarauderGrunt"
                ]
            )

            await client.party.me.set_outfit(
                asset=random_marauder
            )
            await message.reply("Skin set to a random marauder!")

        if message.content.lower() == '!goldenbrutus':
            await client.party.me.set_outfit(
                asset='CID_692_Athena_Commando_M_HenchmanTough',
                variants=client.party.me.create_variants(progressive=4),
                enlightenment=(2, 180)
            )
            await message.reply("Skin set to Golden Brutus!")

        if message.content.lower() == '!goldenmeowscles':
            await client.party.me.set_outfit(
                asset='CID_693_Athena_Commando_M_BuffCat',
                variants=client.party.me.create_variants(progressive=4),
                enlightenment=(2, 220)
            )
            await message.reply("Skin set to Golden Meowscles!")

        if message.content.lower() == '!goldenmidas':
            await client.party.me.set_outfit(
                asset='CID_694_Athena_Commando_M_CatBurglar',
                variants=client.party.me.create_variants(progressive=4),
                enlightenment=(2, 140)
            )
            await message.reply("Skin set to Golden Midas!")

        if message.content.lower() == '!goldenskye':
            await client.party.me.set_outfit(
                asset='CID_690_Athena_Commando_F_Photographer',
                variants=client.party.me.create_variants(progressive=4),
                enlightenment=(2, 300)
            )
            await message.reply("Skin set to Golden Skye!")

        if message.content.lower() == '!goldenpeely':
            await client.party.me.set_outfit(
                asset='CID_701_Athena_Commando_M_BananaAgent',
                variants=client.party.me.create_variants(progressive=4),
                enlightenment=(2, 350)
            )
            await message.reply("Skin set to Golden Peely!")
            
        if message.content.lower() == '!goldentntina':
            await client.party.me.set_outfit(
                asset='CID_691_Athena_Commando_F_TNTina',
                variants=client.party.me.create_variants(progressive=7),
                enlightenment=(2, 260)
            )
            await message.reply("Skin set to Golden TNTina!")
            
        if message.content.lower() == '!checkerredrenegade':
            skin_variants = client.party.me.create_variants(
                material=2
            )

            await client.party.me.set_outfit(
                asset='CID_028_Athena_Commando_F',
                variants=skin_variants
            )
            await message.reply("Skin set to Renegade Raider!")

        if message.content.lower() == '!mintyelf':
            skin_variants = client.party.me.create_variants(
                material=2
            )

            await client.party.me.set_outfit(
                asset='CID_051_Athena_Commando_M_HolidayElf',
                variants=skin_variants
            )
            await message.reply("Skin set to Minty Elf!")

        if message.content.lower() == '!floss':
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_Floss")
            await message.reply("Emote set to Floss!")

        if message.content.lower() == '!scenario':
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_KPopDance03")
            await message.reply("Emote set to Scenario!")

        if message.content.lower() == '!wave':
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_Wave")
            await message.reply("Emote set to Wave!")

        if message.content.lower() == '!ponpon':
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_TourBus")
            await message.reply("Emote set to Ninja Style")

        if message.content.lower() == '!nobackpack':
            await client.party.me.clear_backpack()
            await message.reply("Removed Backpack!")

        if message.content.lower() == '!nopet':
            await client.party.me.clear_pet()
            await message.reply("Removed Pet!")

        if message.content.lower() == '!purpleportal':
            skin_variants = client.party.me.create_variants(
                config_overrides={
                    'particle': 'Particle{}'
                },
                particle=1
            )
            await client.party.me.set_backpack(
                asset='BID_105_GhostPortal',
                variants=skin_variants
            )
            await message.reply("Backpack set to Ghost Portal!")

        if message.content.startswith('!copy'):
            epic_username = message.content.split(' ')[1] if len(message.content.split(' ')) > 1 else None
            
            if epic_username is None:
                member = [m for m in client.party.members if m.id == message.author.id][0]
            else:
                user = await client.fetch_user(epic_username)
                member = [m for m in client.party.members if m.id == user.id][0]

            await client.party.me.edit(
                functools.partial(
                    fortnitepy.ClientPartyMember.set_outfit,
                    asset=member.outfit,
                    variants=member.outfit_variants
                ),
                functools.partial(
                    fortnitepy.ClientPartyMember.set_backpack,
                    asset=member.backpack,
                    variants=member.backpack_variants
                ),
                functools.partial(
                    fortnitepy.ClientPartyMember.set_pickaxe,
                    asset=member.pickaxe,
                    variants=member.pickaxe_variants
                ),
                functools.partial(
                    fortnitepy.ClientPartyMember.set_banner,
                    icon=member.banner[0],
                    color=member.banner[1],
                    season_level=member.banner[2]
                ),
                functools.partial(
                    fortnitepy.ClientPartyMember.set_battlepass_info,
                    has_purchased=True,
                    level=member.battlepass_info[1]
                )
            )

            if member.emote is not None:
                await client.party.me.set_emote(asset=member.emote)

            await message.reply(f'Copied the loadout of {member.display_name}.')

        if message.content.startswith('!variants'):
            args = re.findall(r'"[^"]+"|\S+', message.content)[1:]
            if len(args) < 3:
                await message.reply('Usage: !variants "<cosmetic_id>" <variant_type> <variant_index>')
                return

            cosmetic_id = args[0].strip('"')
            variant_type = args[1]
            variant_index = args[2]

            if not variant_index.isdigit():
                await message.reply('Variant index must be a number.')
                return

            if 'cid' in cosmetic_id.lower() and 'jersey_color' not in variant_type.lower():
                skin_variants = client.party.me.create_variants(
                    **{variant_type: variant_index}
                )

                await client.party.me.set_outfit(
                    asset=cosmetic_id,
                    variants=skin_variants
                )

            elif 'cid' in cosmetic_id.lower() and 'jersey_color' in variant_type.lower():
                cosmetic_variants = client.party.me.create_variants(
                    pattern=0,
                    numeric=69,
                    **{variant_type: variant_index}
                )

                await client.party.me.set_outfit(
                    asset=cosmetic_id,
                    variants=cosmetic_variants
                )

            elif 'bid' in cosmetic_id.lower():
                cosmetic_variants = client.party.me.create_variants(
                    **{variant_type: variant_index}
                )

                await client.party.me.set_backpack(
                    asset=cosmetic_id,
                    variants=cosmetic_variants
                )
            elif 'pickaxe_id' in cosmetic_id.lower():
                cosmetic_variants = client.party.me.create_variants(
                    **{variant_type: variant_index}
                )

                await client.party.me.set_pickaxe(
                    asset=cosmetic_id,
                    variants=cosmetic_variants
                )

            else:
                await message.reply(f'Invalid cosmetic ID: {cosmetic_id}')

        if message.content.startswith('!style'):
            args = re.findall(r'"[^"]+"|\S+', message.content)[1:]
            if len(args) < 3:
                await message.reply('Usage: !style "<cosmetic_id>" <variant_type> <variant_index>')
                return

            cosmetic_id = args[0].strip('"')
            variant_type = args[1]
            variant_index = args[2]

            if not variant_index.isdigit():
                await message.reply('Variant index must be a number.')
                return

            if 'cid' in cosmetic_id.lower() and 'jersey_color' not in variant_type.lower():
                skin_variants = client.party.me.create_variants(
                    **{variant_type: variant_index}
                )

                await client.party.me.set_outfit(
                    asset=cosmetic_id,
                    variants=skin_variants
                )

            elif 'cid' in cosmetic_id.lower() and 'jersey_color' in variant_type.lower():
                cosmetic_variants = client.party.me.create_variants(
                    pattern=0,
                    numeric=69,
                    **{variant_type: variant_index}
                )

                await client.party.me.set_outfit(
                    asset=cosmetic_id,
                    variants=cosmetic_variants
                )

            elif 'bid' in cosmetic_id.lower():
                cosmetic_variants = client.party.me.create_variants(
                    **{variant_type: variant_index}
                )

                await client.party.me.set_backpack(
                    asset=cosmetic_id,
                    variants=cosmetic_variants
                )
            elif 'pickaxe_id' in cosmetic_id.lower():
                cosmetic_variants = client.party.me.create_variants(
                    **{variant_type: variant_index}
                )

                await client.party.me.set_pickaxe(
                    asset=cosmetic_id,
                    variants=cosmetic_variants
                )

            else:
                await message.reply(f'Invalid cosmetic ID: {cosmetic_id}')

        if message.content.lower() == "!new skins":
            response = requests.get("https://package.lobbybots.xyz/new/skins")
            data = response.json()

            if not data:
                await message.reply("Theres no new skins!")
            else:
                await message.reply("Showing all new skins!")
                for item in data:
                    skin_name = item.get("name")
                    await client.party.me.clear_emote()
                    await client.party.me.set_outfit(item.get("id"))
                    await message.reply(f"Skin set to {skin_name}")
                    await asyncio.sleep(2)

                await message.reply("Thats it for now!")

        if message.content.lower() == "!new backpacks":
            response = requests.get("https://package.lobbybots.xyz/new/backpacks")
            data = response.json()

            if not data:
                await message.reply("Theres no new backpacks!")
            else:
                await message.reply("Showing all new backpacks!")
                await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
                for item in data:
                    backpack_name = item.get("name")
                    await client.party.me.clear_emote()
                    await client.party.me.set_backpack(item.get("id"))
                    await message.reply(f"Backpack set to {backpack_name}")
                    await asyncio.sleep(2)

                await message.reply("Thats it for now!")

        if message.content.lower() == "!new pickaxes":
            response = requests.get("https://package.lobbybots.xyz/new/pickaxes")
            data = response.json()

            if not data:
                await message.reply("Theres no new pickaxes!")
            else:
                await message.reply("Showing all new pickaxes!")
                for item in data:
                    pickaxe_name = item.get("name")
                    await client.party.me.clear_emote()
                    await client.party.me.set_pickaxe(item.get("id"))
                    await client.party.me.set_emote("EID_IceKing")
                    await message.reply(f"Pickaxe set to {pickaxe_name}")
                    await asyncio.sleep(6)

                await message.reply("Thats it for now!")

        if message.content.lower() == "!new emotes":
            response = requests.get("https://package.lobbybots.xyz/new/emotes")
            data = response.json()

            if not data:
                await message.reply("Theres no new emotes!")
            else:
                await message.reply("Showing all new emotes!")
                for item in data:
                    emote_name = item.get("name")
                    await client.party.me.clear_emote()
                    await client.party.me.set_emote(item.get("id"))
                    await message.reply(f"Emote set to {emote_name}")
                    await asyncio.sleep(4)

                await message.reply("Thats it for now!")

        if message.content.lower().startswith('!random'):
            item = message.content.split(' ')[1]
            if item.lower() == 'skin':
                skin_response = requests.get('https://package.lobbybots.xyz/skins')
                skin_data = random.choice(skin_response.json())
                await client.party.me.set_outfit(f"{skin_data['id']}")
                await message.reply(f"Skin set to: {skin_data['name']}")
            elif item.lower() == 'backpack':
                backpack_response = requests.get('https://package.lobbybots.xyz/backpacks')
                backpack_data = random.choice(backpack_response.json())
                await client.party.me.set_backpack(f"{backpack_data['id']}")
                await message.reply(f"Backpack set to: {backpack_data['name']}")
            elif item.lower() == 'pickaxe':
                pickaxe_response = requests.get('https://package.lobbybots.xyz/pickaxes')
                pickaxe_data = random.choice(pickaxe_response.json())
                await client.party.me.set_pickaxe(f"{pickaxe_data['id']}")
                await client.party.me.clear_emote()
                await client.party.me.set_emote("EID_IceKing")
                await message.reply(f"Pickaxe set to: {pickaxe_data['name']}")
            elif item.lower() == 'emote':
                await client.party.me.clear_emote()
                emote_response = requests.get('https://package.lobbybots.xyz/emotes')
                emote_data = random.choice(emote_response.json())
                await client.party.me.set_emote(f"{emote_data['id']}")
                await message.reply(f"Emote set to: {emote_data['name']}")
            elif item.lower() == 'all':
                await client.party.me.clear_emote()
                skin_response = requests.get('https://package.lobbybots.xyz/skins')
                backpack_response = requests.get('https://package.lobbybots.xyz/backpacks')
                pickaxe_response = requests.get('https://package.lobbybots.xyz/pickaxes')
                emote_response = requests.get('https://package.lobbybots.xyz/emotes')
                skin_data = random.choice(skin_response.json())
                backpack_data = random.choice(backpack_response.json())
                pickaxe_data = random.choice(pickaxe_response.json())
                emote_data = random.choice(emote_response.json())
                await client.party.me.set_outfit(f"{skin_data['id']}")
                await client.party.me.set_backpack(f"{backpack_data['id']}")
                await client.party.me.set_pickaxe(f"{pickaxe_data['id']}")
                await client.party.me.set_emote(f"{emote_data['id']}")
                await message.reply(f"Skin set to: {skin_data['name']}.\nBackpack set to: {backpack_data['name']}.\nPickaxe set to: {pickaxe_data['name']}.\nEmote set to: {emote_data['name']}.")
            else:
                await message.reply("Invalid! Please user !random skin/backpack/pickaxe/emote/all.")

        if message.content.startswith("!hide"):
            if client.party.me.leader:
                try:
                    raw_squad_assignments = client.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]
                    for m in raw_squad_assignments:
                        raw_squad_assignments.remove(m)

                    await set_and_update_party_prop(
                        'Default:RawSquadAssignments_j',
                        {
                            'RawSquadAssignments': raw_squad_assignments
                        }
                    )

                    await message.reply("Hid everyone in the party.")
                except fortnitepy.HTTPException:
                    await message.reply("I am not party leader.")
            else:
                await message.reply("I need party leader to do this!")

        if message.content.startswith('!unhide'):
            if client.party.me.leader:
                try:
                    raw_squad_assignments = [{'memberId': m.id, 'absoluteMemberIdx': i + 1} for i, m in enumerate(client.party.members)]

                    await set_and_update_party_prop(
                        'Default:RawSquadAssignments_j',
                        {
                            'RawSquadAssignments': raw_squad_assignments
                        }
                    )

                    await message.reply("Unhid everyone in the party.")
                except fortnitepy.HTTPException:
                    await message.reply("I am not party leader.")
            else:
                await message.reply("I need party leader to do this!")

        if message.content.lower() == '!friends':
            await message.reply(f'I have {len(client.friends)} friends!')

        # Load the config file
        with open(config_file, 'r') as f:
            config = json.load(f)

        admins = config.get('admins', [])

        if message.content.startswith("!admin add"):
            if message.author.id not in config['admins']:
                await message.reply("You do not have permission to add admins.")
                return

            command_parts = message.content.split()
            if len(command_parts) != 3:
                await message.reply("Invalid command usage. Please use '!admin add [user_id]' to add an admin.")
                return

            action, admin = command_parts[1], command_parts[2]
            if action == "add":
                if admin in config['admins']:
                    await message.reply(f"{admin} is already an admin.")
                    return

                config['admins'].append(admin)

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"{admin} has been added as an admin.")
            else:
                await message.reply("Invalid command usage. Please use '!admin add [user_id]' to add an admin.")

        if message.content.startswith("!admin remove"):
            if message.author.id not in config['admins']:
                await message.reply("You do not have permission to remove admins.")
                return

            command_parts = message.content.split()
            if len(command_parts) != 3:
                await message.reply("Invalid command usage. Please use '!admin remove [user_id]' to remove an admin.")
                return

            action, admin = command_parts[1], command_parts[2]
            if action == "remove":
                if admin not in config['admins']:
                    await message.reply(f"{admin} is not an admin.")
                    return

                config['admins'].remove(admin)

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"{admin} has been removed from admins.")
            else:
                await message.reply("Invalid command usage. Please use '!admin remove [user_id]' to remove an admin.")

        if message.content.startswith("!admin list"):
            if message.author.id not in config.get('admins', []):
                await message.reply("You do not have permission to list admins.")
                return

            admins = config.get('admins', [])
            if not admins:
                await message.reply("There are no admins currently.")
            else:
                admin_list = "\n".join(admins)
                await message.reply(f"List of admins:\n{admin_list}")

        if message.content.startswith('!default skin'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the default skin.")
                return

            command_parts = message.content.split()
            if len(command_parts) < 3:
                await message.reply("Invalid command usage. Please use '!default skin [skin_names]' to set the default skin.")
                return

            action = command_parts[1]
            skins = command_parts[2:]

            if action == "skin":
                config['skin'] = ' '.join(skins)

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"The default skin has been set to: {' '.join(skins)}")
            else:
                await message.reply("Invalid command usage. Please use '!default skin [skin_names]' to set the default skin.")

        if message.content.lower().startswith('!default backpack'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the default backpack.")
                return

            command_parts = message.content.split()
            if len(command_parts) < 3:
                await message.reply("Invalid command usage. Please use '!default backpack [backpack_names]' to set the default backpack.")
                return

            action = command_parts[1]
            backpacks = command_parts[2:]

            if action == "backpack":
                config['backpack'] = ' '.join(backpacks)

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"The default backpack has been set to: {' '.join(backpacks)}")
            else:
                await message.reply("Invalid command usage. Please use '!default backpack [backpack_names]' to set the default backpack.")


        if message.content.lower().startswith('!default pickaxe'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the default pickaxe.")
                return

            command_parts = message.content.split()
            if len(command_parts) < 3:
                await message.reply("Invalid command usage. Please use '!default pickaxe [pickaxe_names]' to set the default pickaxe.")
                return

            action = command_parts[1]
            pickaxes = command_parts[2:]

            if action == "pickaxe":
                config['pickaxe'] = ' '.join(pickaxes)

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"The default pickaxe has been set to: {' '.join(pickaxes)}")
            else:
                await message.reply("Invalid command usage. Please use '!default pickaxe [pickaxe_names]' to set the default pickaxe.")


        if message.content.lower().startswith('!default emote'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the default emote.")
                return

            command_parts = message.content.split()
            if len(command_parts) < 3:
                await message.reply("Invalid command usage. Please use '!default emote [emote_names]' to set the default emote.")
                return

            action = command_parts[1]
            emotes = command_parts[2:]

            if action == "emote":
                config['emote'] = ' '.join(emotes)

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"The default emote has been set to: {' '.join(emotes)}")
            else:
                await message.reply("Invalid command usage. Please use '!default emote [emote_names]' to set the default emote.")

        if message.content.lower().startswith('!default level'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the default level.")
                return

            command_parts = message.content.split()
            if len(command_parts) != 3:
                await message.reply("Invalid command usage. Please use '!default level [level]' to set the default level.")
                return

            action, level = command_parts[1], command_parts[2]

            if action == "level":
                try:
                    level = int(level)
                except ValueError:
                    await message.reply("Invalid level value. Please provide a valid number.")
                    return

                config['level'] = level

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"The default level has been set to: {level}")
            else:
                await message.reply("Invalid command usage. Please use '!default level [level]' to set the default level.")

        if message.content.startswith('!auto_update'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the auto_update variable.")
                return

            command_parts = message.content.split()
            if len(command_parts) != 2:
                await message.reply("Invalid command usage. Please use '!auto_update [True/False]' to set the auto_update variable.")
                return

            auto_update = command_parts[1].lower()
            if auto_update not in ['true', 'false']:
                await message.reply("Invalid command usage. Please use '!auto_update [True/False]' to set the auto_update variable.")
                return

            config['auto_update'] = (auto_update == 'true')

            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)

            await message.reply(f"The auto_update variable has been set to: {auto_update}")

        if message.content.startswith('!accept_friend_requests'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the accept_friend_requests variable.")
                return

            command_parts = message.content.split()
            if len(command_parts) != 2:
                await message.reply("Invalid command usage. Please use '!accept_friend_requests [True/False]' to set the accept_friend_requests variable.")
                return

            accept_friend_requests = command_parts[1].lower()
            if accept_friend_requests not in ['true', 'false']:
                await message.reply("Invalid command usage. Please use '!accept_friend_requests [True/False]' to set the accept_friend_requests variable.")
                return

            config['accept_friend_requests'] = (accept_friend_requests == 'true')

            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)

            await message.reply(f"The accept_friend_requests variable has been set to: {accept_friend_requests}")

        if message.content.startswith('!accept_invites'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the accept_invites variable.")
                return

            command_parts = message.content.split()
            if len(command_parts) != 2:
                await message.reply("Invalid command usage. Please use '!accept_invites [True/False]' to set the accept_invites variable.")
                return

            accept_invites = command_parts[1].lower()
            if accept_invites not in ['true', 'false']:
                await message.reply("Invalid command usage. Please use '!accept_invites [True/False]' to set the accept_invites variable.")
                return

            config['accept_invites'] = (accept_invites == 'true')

            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)

            await message.reply(f"The accept_invites variable has been set to: {accept_invites}")

        if message.content.lower().startswith('!join_message'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the join message.")
                return

            command_parts = message.content.split(maxsplit=1)
            if len(command_parts) < 2:
                await message.reply("Invalid command usage. Please use '!join_message [message]' to set the join message.")
                return

            join_message = command_parts[1]
            config['join_message'] = join_message

            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)

            await message.reply(f"The join message has been set to: {join_message}")

    @client.event
    async def event_friend_message(message: fortnitepy.FriendMessage):
        content = message.content.lower()
        args = message.content.lower().split()

        if message.content.lower() == '!update':
            await message.reply("Updating packages...")

            try:
                response = requests.get("https://package.lobbybots.xyz/newest_version")
                response.raise_for_status()  # Raise an exception for non-2xx status codes

                newest_version = response.json()[0].get('Version', None)
                if newest_version:
                    await message.reply(f"Newest version available: {newest_version}")

                    # Perform the necessary actions to update the package to the newest version
                    os.system(f"pip install --upgrade fortnitepy > /dev/null 2>&1; pip install --upgrade -i https://test.pypi.org/simple/ testlobby=={newest_version} > /dev/null 2>&1")

                    await message.reply("Package update completed.")
                else:
                    await message.reply("Failed to retrieve the newest version.")

            except requests.exceptions.RequestException as e:
                await message.reply(f"An error occurred while updating packages: {e}")

        if message.content.lower() == '!ready':
            await client.party.me.set_ready(fortnitepy.ReadyState.READY)
            await message.reply("Ready! Note: Bots can't play games!")

        if message.content.lower() == '!unready':
            await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
            await message.reply("Unready! Note: Bots can't play games!")

        if message.content.lower() == '!sitout':
            await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
            await message.reply("Sitting Out! Note: Bots can't play games!")

        if message.content.lower().startswith('!crowns'):
            args = message.content.split()
            if len(args) == 1:
                amount = 100
            else:
                amount = int(args[1])
            meta = client.party.me.meta
            data = (meta.get_prop('Default:AthenaCosmeticLoadout_j'))['AthenaCosmeticLoadout']

            try:
                data['cosmeticStats'][1]['statValue'] = amount
            except KeyError:
                data['cosmeticStats'] = [{"statName": "TotalVictoryCrowns", "statValue": amount},
                                        {"statName": "TotalRoyalRoyales", "statValue": amount},
                                        {"statName": "HasCrown", "statValue": 0}]

            final = {'AthenaCosmeticLoadout': data}
            key = 'Default:AthenaCosmeticLoadout_j'
            prop = {key: meta.set_prop(key, final)}

            await client.party.me.patch(updated=prop)
            await client.party.me.clear_emote()
            await client.party.me.set_emote('EID_Coronet')
            await message.reply("Emoteing Crowning Achievement!")

        if args[0] == '!skin':
            # Check if there are enough arguments
            if len(args) < 2:
                return await message.reply("Please specify a skin name.")

            # Get the skin name from the user's message
            skin_name = " ".join(args[1:])

            # Set the user's skin
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method="GET",
                        url=f"https://package.lobbybots.xyz/skins"
                ) as request:
                    data = (await request.json())

            # Find the closest matching skin using Levenshtein distance
            closest_match = None
            lowest_distance = float('inf')

            for skin in data:
                distance = levenshtein_distance(skin_name.lower(), skin.get("name", "").lower())
                if distance < lowest_distance:
                    closest_match = skin
                    lowest_distance = distance

            if lowest_distance > 3:  # You can adjust this threshold as needed
                return await message.reply(f"No close match found for {skin_name}.")

            if "brcosmetics" in closest_match['path'].lower():
                path = f"AthenaCharacterItemDefinition'/BRCosmetics/Athena/Items/Cosmetics/Characters/{closest_match['id']}.{closest_match['id']}'"
                await client.party.me.set_outfit(asset=path)
            else:
                await client.party.me.set_outfit(asset=closest_match['id'])

            await message.reply(f"Skin set to {closest_match['name']}.")

        if args[0] == '!backpack':
            # Check if there are enough arguments
            if len(args) < 2:
                return await message.reply("Please specify a backpack name.")

            # Get the backpack name from the user's message
            backpack_name = " ".join(args[1:])

            # Set the user's backpack
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method="GET",
                        url=f"https://package.lobbybots.xyz/backpacks"
                ) as request:
                    data = (await request.json())

            # Find the closest matching backpack using Levenshtein distance
            closest_match = None
            lowest_distance = float('inf')

            for backpack in data:
                distance = levenshtein_distance(backpack_name.lower(), backpack.get("name", "").lower())
                if distance < lowest_distance:
                    closest_match = backpack
                    lowest_distance = distance

            if lowest_distance > 3:  # You can adjust this threshold as needed
                return await message.reply(f"No close match found for {backpack_name}.")

            if "brcosmetics" in closest_match['path'].lower():
                path = f"AthenaBackpackItemDefinition'/BRCosmetics/Athena/Items/Cosmetics/Backpacks/{closest_match['id']}.{closest_match['id']}'"
                await client.party.me.set_backpack(asset=path)
            else:
                await client.party.me.set_backpack(asset=closest_match['id'])

            await message.reply(f"Backpack set to {closest_match['name']}.")

        if args[0] == '!pickaxe':
            # Check if there are enough arguments
            if len(args) < 2:
                return await message.reply("Please specify a pickaxe name.")

            # Get the pickaxe name from the user's message
            pickaxe_name = " ".join(args[1:])

            # Set the user's pickaxe
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method="GET",
                        url=f"https://package.lobbybots.xyz/pickaxes"
                ) as request:
                    data = (await request.json())

            # Find the closest matching pickaxe using Levenshtein distance
            closest_match = None
            lowest_distance = float('inf')

            for pickaxe in data:
                distance = levenshtein_distance(pickaxe_name.lower(), pickaxe.get("name", "").lower())
                if distance < lowest_distance:
                    closest_match = pickaxe
                    lowest_distance = distance

            if lowest_distance > 3:  # You can adjust this threshold as needed
                return await message.reply(f"No close match found for {pickaxe_name}.")

            if "brcosmetics" in closest_match['path'].lower():
                path = f"AthenaPickaxeItemDefinition'/BRCosmetics/Athena/Items/Cosmetics/PickAxes/{closest_match['id']}.{closest_match['id']}'"
                await client.party.me.set_pickaxe(asset=path)
                await client.party.me.set_emote("EID_IceKing")
            else:
                await client.party.me.set_pickaxe(asset=closest_match['id'])
                await client.party.me.set_emote("EID_IceKing")

            await message.reply(f"Pickaxe set to {closest_match['name']}.")

        if args[0] == '!emote':
            # Check if there are enough arguments
            if len(args) < 2:
                return await message.reply("Please specify an emote name.")

            # Get the emote name from the user's message
            emote_name = " ".join(args[1:])

            # Set the user's emote
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method="GET",
                        url=f"https://package.lobbybots.xyz/emotes"
                ) as request:
                    data = (await request.json())

            # Find the closest matching emote using Levenshtein distance
            closest_match = None
            lowest_distance = float('inf')

            for emote in data:
                distance = levenshtein_distance(emote_name.lower(), emote.get("name", "").lower())
                if distance < lowest_distance:
                    closest_match = emote
                    lowest_distance = distance

            if lowest_distance > 3:  # You can adjust this threshold as needed
                return await message.reply(f"No close match found for {emote_name}.")

            if "brcosmetics" in closest_match['path'].lower():
                await client.party.me.clear_emote()
                path = f"AthenaDanceItemDefinition'/BRCosmetics/Athena/Items/Cosmetics/Dances/{closest_match['id']}.{closest_match['id']}'"
                await client.party.me.set_emote(asset=path)
            else:
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset=closest_match['id'])

            await message.reply(f"Emote set to {closest_match['name']}.")

        if message.content.lower().startswith('!level'):
            level = message.content.split(' ')[1]
            await client.party.me.set_banner(season_level=level)
            await message.reply(f"Level set to {level}!")

        if message.content.lower().startswith('!bp'):
            teir = message.content.split(' ')[1]
            await client.party.me.set_battlepass_info(
            has_purchased=True, level=teir)
            await message.reply(f"Teir set to {teir}!")

        if message.content.lower().startswith('!echo'):
            message_parts = message.content.split(' ')[1:]
            echoed_message = ' '.join(message_parts)
            await client.party.send(echoed_message)

        if message.content.lower() == '!point':
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_IceKing")
            await message.reply("Pointing out my pickaxe!")

        if message.content.lower().startswith('!privacy'):
            privacy = message.content.split(' ')[1]
            if privacy.lower() == 'public':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                await message.reply("Privacy set to PUBLIC!")
            elif privacy.lower() == 'friends_allow_friends_of_friends':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS_ALLOW_FRIENDS_OF_FRIENDS)
                await message.reply("Privacy set to FRIENDS_ALLOW_FRIENDS_OF_FRIENDS!")
            elif privacy.lower() == 'friends':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS)
                await message.reply("Privacy set to FRIENDS!")
            elif privacy.lower() == 'private_allow_friends_of_friends':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE_ALLOW_FRIENDS_OF_FRIENDS)
                await message.reply("Privacy set to PRIVATE_ALLOW_FRIENDS_OF_FRIENDS!")
            elif privacy.lower() == 'private':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
                await message.reply("Privacy set to PRIVATE!")
            else:
                await message.reply('Invalid privacy setting. Please use "public"/"friends_allow_friends_of_friends"/"friends"/"private_allow_friends_of_friends" or "private"!')

        if message.content.lower() == '!rareskins':
            await message.reply("Showing all Rare Skins!")
            purpleskull_skin_variants = client.party.me.create_variants(
                clothing_color=1
            )
            await client.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=purpleskull_skin_variants
        )
            await message.reply("Skin set to Purple Skull Trooper!")
            await asyncio.sleep(2)
            await client.party.me.set_outfit("CID_028_Athena_Commando_F")
            await message.reply("Skin set to Renegade Raider!")
            await asyncio.sleep(2)
            pinkghoul_skin_variants = client.party.me.create_variants(
                material=3
            )
            await client.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=pinkghoul_skin_variants
        )
            await message.reply("Skin set to Pink Ghoul Trooper!")
            await asyncio.sleep(2)
            await client.party.me.set_outfit("CID_017_Athena_Commando_M")
            await message.reply("Skin set to Aerial Assault Trooper!")
            await message.reply("Those are all of the Rare Skins!")

        if message.content.lower() == '!rarebackpacks':
            await message.reply("Showing all Rare Backpacks!")
            await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await asyncio.sleep(1)
            await client.party.me.set_backpack("BID_140_StreetOpsMale")
            await message.reply("Backpack set to Response Unit!")
            await asyncio.sleep(4)
            await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await asyncio.sleep(1)
            await client.party.me.set_backpack("BID_027_Scavenger")
            await message.reply("Backpack set to Rust Bucket!")
            await asyncio.sleep(4)
            await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await asyncio.sleep(1)
            await client.party.me.set_backpack("BID_029_RetroGrey")
            await message.reply("Backpack set to Backup Plan!")
            await asyncio.sleep(4)
            await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await asyncio.sleep(1)
            await client.party.me.set_backpack("BID_138_Celestial")
            await message.reply("Backpack set to Galactic Disc!")
            await asyncio.sleep(4)
            await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await asyncio.sleep(1)
            await client.party.me.set_backpack("BID_114_ModernMilitaryRed")
            await message.reply("Backpack set to Telemetry!")
            await message.reply("Those are all of the Rare Backpacks!")

        if message.content.lower() == '!rarepickaxes':
            await message.reply("Showing all Rare Pickaxes!")
            await client.party.me.clear_emote()
            await client.party.me.set_pickaxe("Pickaxe_ID_376_FNCS")
            await message.reply("Pickaxe set to Axe Of Champions!")
            await client.party.me.set_emote("EID_IceKing")
            await asyncio.sleep(8)
            await client.party.me.clear_emote()
            await client.party.me.set_pickaxe("Pickaxe_ID_069_DarkViking")
            await message.reply("Pickaxe set to Permafrost!")
            await client.party.me.set_emote("EID_IceKing")
            await asyncio.sleep(8)
            await client.party.me.clear_emote()
            await client.party.me.set_pickaxe("Pickaxe_Lockjaw")
            await message.reply("Pickaxe set to Raiders Revenge!")
            await client.party.me.set_emote("EID_IceKing")
            await asyncio.sleep(8)
            await client.party.me.clear_emote()
            await client.party.me.set_pickaxe("Pickaxe_ID_189_StreetOpsStealth")
            await message.reply("Pickaxe set to Stealth Angular Axe!")
            await client.party.me.set_emote("EID_IceKing")
            await asyncio.sleep(8)
            await client.party.me.clear_emote()
            await client.party.me.set_pickaxe("Pickaxe_ID_075_Huya")
            await message.reply("Pickaxe set to Pointer!")
            await client.party.me.set_emote("EID_IceKing")
            await message.reply("Those are all of the Rare Pickaxe!")

        if message.content.lower() == '!rareemotes':
            await message.reply("Showing all Rare Emotes!")
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_Fresh")
            await message.reply("Emote set to Fresh!")
            await asyncio.sleep(4)
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_AshtonBoardwalk")
            await message.reply("Emote set to Widow’s Pirouette!")
            await asyncio.sleep(4)
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_RunningManv3")
            await message.reply("Emote set to Pick It Up!")
            await asyncio.sleep(4)
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_TapShuffle")
            await message.reply("Emote set to Hootenanny!")
            await asyncio.sleep(4)
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_CycloneHeadBang")
            await message.reply("Emote set to Head Banger!")
            await message.reply("Those are all of the Rare Emotes!")

        if message.content.lower() == '!invite':
            # invite the user who sent the message
            member = await client.fetch_profile(message.author.id, cache=False, raw=False)
            await client.party.invite(member.id)
            await message.reply(f"Invited {member.display_name} to the party.")

        if message.content.startswith('!invite '):
            username = message.content[8:].strip()
            members = client.friends
            member = next((m for m in members if m.display_name.lower() == username.lower() or m.id == username), None)
            if member:
                await client.party.invite(member.id)
                await message.reply(f"Invited {member.display_name} to the party.")
            else:
                await message.reply("Could not find a member with that name or ID!")

        if message.content.lower() == '!stop':
            await client.party.me.clear_emote()
            await message.reply("Stopped emoteing!")

        if message.content.startswith("!join"):
            try:
                user = await client.fetch_profile(message.author.id)
                friend = client.get_friend(user.id)

                await friend.join_party()
                await message.reply(f"Joined {friend.display_name}'s party.")
            except fortnitepy.Forbidden:
                await message.reply("I can't join your party because it's private.")
            except fortnitepy.PartyError:
                await message.reply("I am already in the party.")
            except fortnitepy.HTTPException:
                await message.reply("Something went wrong while joining the party.")
            except AttributeError:
                await message.reply("I couldn't find that user.")

        if message.content.startswith("!promote"):
            user = await client.fetch_user(message.author.id)
            member = client.party.get_member(user.id)

            try:
                await member.promote()
                await message.reply(f"Promoted: {member.display_name}")
            except fortnitepy.Forbidden:
                await message.reply("I am not party leader.")
            except fortnitepy.PartyError:
                await message.reply("You already are the party leader.")
            except fortnitepy.HTTPException:
                await message.reply("Something went wrong trying to promote you.")
            except AttributeError:
                await message.reply("I couldn't find you.")

        if message.content.startswith("!kick"):
            content = message.content.split()
            member = None

            if len(content) > 1:
                member = content[1]

            try:
                if member is None:
                    user = await client.fetch_user(message.author.display_name)
                    member = client.party.get_member(user.id)
                else:
                    user = await client.fetch_user(member)
                    member = client.party.get_member(user.id)

                if member is None:
                    await message.reply("Couldn't find that user, are they in the party?")
                    return

                await member.kick()
                await message.reply(f"Kicked: {member.display_name}")
            except fortnitepy.Forbidden:
                await message.reply("I can't kick that user, I am not the party leader.")
            except fortnitepy.PartyError:
                await message.reply("Nice try, but I can't kick myself.")
            except AttributeError:
                await message.reply("I couldn't find that user.")
            except fortnitepy.HTTPException:
                await message.reply("I couldn't find that user.")

        if message.content.lower() == '!leave':
            await message.reply("Leaveing the party!")
            await client.party.me.leave()

        if message.content.lower() == '!griddy':
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_Griddles")
            await message.reply("Emote set to Get Griddy")

        if message.content.lower() == '!purpleskull':
            purpleskull_skin_variants = client.party.me.create_variants(
                clothing_color=1
            )
            await client.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=purpleskull_skin_variants
        )
            await message.reply("Skin set to Purple Skull Trooper")

        if message.content.lower() == '!renegaderaider':
            await client.party.me.set_outfit("CID_028_Athena_Commando_F")
            await message.reply("Skin set to Renegade Raider")

        if message.content.lower() == '!pinkghoul':
            pinkghoul_skin_variants = client.party.me.create_variants(
                material=3
            )
            await client.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=pinkghoul_skin_variants
        )
            await message.reply("Skin set to Pink Ghoul Trooper")

        if message.content.lower() == '!aerial':
            await client.party.me.set_outfit("CID_017_Athena_Commando_M")
            await message.reply("Skin set to Aerial Assault Trooper")

        if message.content.lower() == '!ikonik':
            await client.party.me.set_outfit("CID_313_Athena_Commando_M_KpopFashion")
            await message.reply("Skin set to Ikonik")

        if message.content.lower() == '!ninja':
            await client.party.me.set_outfit("CID_605_Athena_Commando_M_TourBus")
            await message.reply("Skin set to Ninja")

        if message.content.lower() == "!hologram":
            await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await message.reply("Skin set to Hologram")

        if message.content.lower().startswith("!gift"):
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_NeverGonna")
            await message.reply("Nice try but I can't gift!")

        if message.content.lower() == "!tbd":
            response = requests.get("https://package.lobbybots.xyz/skins")
            data = response.json()
            await message.reply("Showing all TBD skins!")

            for item in data:
                if item.get("name") == "TBD":
                    skin_name = item.get("name")
                    await client.party.me.set_outfit(item.get("id"))
                    await message.reply(f"Skin set to {skin_name}")
                    await asyncio.sleep(2)

            await message.reply("Those are all of the TBD skins!")

        if message.content.lower() == "!shop skins":
            response = requests.get("https://package.lobbybots.xyz/shop/skins")
            data = response.json()

            if not data:
                await message.reply("Theres no new skins!")
            else:
                await message.reply("Showing all new skins!")
                for item in data:
                    skin_name = item.get("name")
                    await client.party.me.clear_emote()
                    await client.party.me.set_outfit(item.get("id"))
                    await message.reply(f"Skin set to {skin_name}")
                    await asyncio.sleep(2)

                await message.reply("Thats it for now!")

        if message.content.lower() == "!shop backpacks":
            response = requests.get("https://package.lobbybots.xyz/shop/backpacks")
            data = response.json()

            if not data:
                await message.reply("Theres no new backpacks!")
            else:
                await message.reply("Showing all new backpacks!")
                await client.party.me.clear_backpack()
                await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
                for item in data:
                    backpack_name = item.get("name")
                    await client.party.me.clear_emote()
                    await client.party.me.set_backpack(item.get("id"))
                    await message.reply(f"Backpack set to {backpack_name}")
                    await asyncio.sleep(2)

                await message.reply("Thats it for now!")

        if message.content.lower() == "!shop pickaxes":
            response = requests.get("https://package.lobbybots.xyz/shop/pickaxes")
            data = response.json()

            if not data:
                await message.reply("Theres no new pickaxes!")
            else:
                await message.reply("Showing all new pickaxes!")
                for item in data:
                    pickaxe_name = item.get("name")
                    await client.party.me.clear_emote()
                    await client.party.me.set_pickaxe(item.get("id"))
                    await client.party.me.set_emote("EID_IceKing")
                    await message.reply(f"Pickaxe set to {pickaxe_name}")
                    await asyncio.sleep(6)

                await message.reply("Thats it for now!")

        if message.content.lower() == "!shop emotes":
            response = requests.get("https://package.lobbybots.xyz/shop/emotes")
            data = response.json()

            if not data:
                await message.reply("Theres no new emotes!")
            else:
                await message.reply("Showing all new emotes!")
                for item in data:
                    emote_name = item.get("name")
                    await client.party.me.clear_emote()
                    await client.party.me.set_emote(item.get("id"))
                    await message.reply(f"Emote set to {emote_name}")
                    await asyncio.sleep(4)

                await message.reply("Thats it for now!")

        if message.content.lower() == '!hatlessrecon':
            skin_variants = client.party.me.create_variants(
                parts=2
            )

            await client.party.me.set_outfit(
                asset='CID_022_Athena_Commando_F',
                variants=skin_variants
            )
            await message.reply("Skin set to Recon Expert!")

        if message.content.lower() == '!henchman':
            random_henchman = random.choice(
                [
                    "CID_794_Athena_Commando_M_HenchmanBadShorts_D",
                    "CID_NPC_Athena_Commando_F_HenchmanSpyDark",
                    "CID_791_Athena_Commando_M_HenchmanGoodShorts_D",
                    "CID_780_Athena_Commando_M_HenchmanBadShorts",
                    "CID_NPC_Athena_Commando_M_HenchmanGood",
                    "CID_692_Athena_Commando_M_HenchmanTough",
                    "CID_707_Athena_Commando_M_HenchmanGood",
                    "CID_792_Athena_Commando_M_HenchmanBadShorts_B",
                    "CID_793_Athena_Commando_M_HenchmanBadShorts_C",
                    "CID_NPC_Athena_Commando_M_HenchmanBad",
                    "CID_790_Athena_Commando_M_HenchmanGoodShorts_C",
                    "CID_779_Athena_Commando_M_HenchmanGoodShorts",
                    "CID_NPC_Athena_Commando_F_RebirthDefault_Henchman",
                    "CID_NPC_Athena_Commando_F_HenchmanSpyGood",
                    "CID_706_Athena_Commando_M_HenchmanBad",
                    "CID_789_Athena_Commando_M_HenchmanGoodShorts_B"
                ]
            )

            await client.party.me.set_outfit(
                asset=random_henchman
            )
            await message.reply("Skin set to a random henchman!")

        if message.content.lower() == '!marauder':
            random_marauder = random.choice(
                [
                    "CID_NPC_Athena_Commando_M_MarauderHeavy",
                    "CID_NPC_Athena_Commando_M_MarauderElite",
                    "CID_NPC_Athena_Commando_M_MarauderGrunt"
                ]
            )

            await client.party.me.set_outfit(
                asset=random_marauder
            )
            await message.reply("Skin set to a random marauder!")

        if message.content.lower() == '!goldenbrutus':
            await client.party.me.set_outfit(
                asset='CID_692_Athena_Commando_M_HenchmanTough',
                variants=client.party.me.create_variants(progressive=4),
                enlightenment=(2, 180)
            )
            await message.reply("Skin set to Golden Brutus!")

        if message.content.lower() == '!goldenmeowscles':
            await client.party.me.set_outfit(
                asset='CID_693_Athena_Commando_M_BuffCat',
                variants=client.party.me.create_variants(progressive=4),
                enlightenment=(2, 220)
            )
            await message.reply("Skin set to Golden Meowscles!")

        if message.content.lower() == '!goldenmidas':
            await client.party.me.set_outfit(
                asset='CID_694_Athena_Commando_M_CatBurglar',
                variants=client.party.me.create_variants(progressive=4),
                enlightenment=(2, 140)
            )
            await message.reply("Skin set to Golden Midas!")

        if message.content.lower() == '!goldenskye':
            await client.party.me.set_outfit(
                asset='CID_690_Athena_Commando_F_Photographer',
                variants=client.party.me.create_variants(progressive=4),
                enlightenment=(2, 300)
            )
            await message.reply("Skin set to Golden Skye!")

        if message.content.lower() == '!goldenpeely':
            await client.party.me.set_outfit(
                asset='CID_701_Athena_Commando_M_BananaAgent',
                variants=client.party.me.create_variants(progressive=4),
                enlightenment=(2, 350)
            )
            await message.reply("Skin set to Golden Peely!")
            
        if message.content.lower() == '!goldentntina':
            await client.party.me.set_outfit(
                asset='CID_691_Athena_Commando_F_TNTina',
                variants=client.party.me.create_variants(progressive=7),
                enlightenment=(2, 260)
            )
            await message.reply("Skin set to Golden TNTina!")
            
        if message.content.lower() == '!checkerredrenegade':
            skin_variants = client.party.me.create_variants(
                material=2
            )

            await client.party.me.set_outfit(
                asset='CID_028_Athena_Commando_F',
                variants=skin_variants
            )
            await message.reply("Skin set to Renegade Raider!")

        if message.content.lower() == '!mintyelf':
            skin_variants = client.party.me.create_variants(
                material=2
            )

            await client.party.me.set_outfit(
                asset='CID_051_Athena_Commando_M_HolidayElf',
                variants=skin_variants
            )
            await message.reply("Skin set to Minty Elf!")

        if message.content.lower() == '!floss':
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_Floss")
            await message.reply("Emote set to Floss!")

        if message.content.lower() == '!scenario':
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_KPopDance03")
            await message.reply("Emote set to Scenario!")

        if message.content.lower() == '!wave':
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_Wave")
            await message.reply("Emote set to Wave!")

        if message.content.lower() == '!ponpon':
            await client.party.me.clear_emote()
            await client.party.me.set_emote("EID_TourBus")
            await message.reply("Emote set to Ninja Style")

        if message.content.lower() == '!nobackpack':
            await client.party.me.clear_backpack()
            await message.reply("Removed Backpack!")

        if message.content.lower() == '!nopet':
            await client.party.me.clear_pet()
            await message.reply("Removed Pet!")

        if message.content.lower() == '!purpleportal':
            skin_variants = client.party.me.create_variants(
                config_overrides={
                    'particle': 'Particle{}'
                },
                particle=1
            )
            await client.party.me.set_backpack(
                asset='BID_105_GhostPortal',
                variants=skin_variants
            )
            await message.reply("Backpack set to Ghost Portal!")

        if message.content.startswith('!copy'):
            epic_username = message.content.split(' ')[1] if len(message.content.split(' ')) > 1 else None
            
            if epic_username is None:
                member = [m for m in client.party.members if m.id == message.author.id][0]
            else:
                user = await client.fetch_user(epic_username)
                member = [m for m in client.party.members if m.id == user.id][0]

            await client.party.me.edit(
                functools.partial(
                    fortnitepy.ClientPartyMember.set_outfit,
                    asset=member.outfit,
                    variants=member.outfit_variants
                ),
                functools.partial(
                    fortnitepy.ClientPartyMember.set_backpack,
                    asset=member.backpack,
                    variants=member.backpack_variants
                ),
                functools.partial(
                    fortnitepy.ClientPartyMember.set_pickaxe,
                    asset=member.pickaxe,
                    variants=member.pickaxe_variants
                ),
                functools.partial(
                    fortnitepy.ClientPartyMember.set_banner,
                    icon=member.banner[0],
                    color=member.banner[1],
                    season_level=member.banner[2]
                ),
                functools.partial(
                    fortnitepy.ClientPartyMember.set_battlepass_info,
                    has_purchased=True,
                    level=member.battlepass_info[1]
                )
            )

            if member.emote is not None:
                await client.party.me.set_emote(asset=member.emote)

            await message.reply(f'Copied the loadout of {member.display_name}.')

        if message.content.startswith('!variants'):
            args = re.findall(r'"[^"]+"|\S+', message.content)[1:]
            if len(args) < 3:
                await message.reply('Usage: !variants "<cosmetic_id>" <variant_type> <variant_index>')
                return

            cosmetic_id = args[0].strip('"')
            variant_type = args[1]
            variant_index = args[2]

            if not variant_index.isdigit():
                await message.reply('Variant index must be a number.')
                return

            if 'cid' in cosmetic_id.lower() and 'jersey_color' not in variant_type.lower():
                skin_variants = client.party.me.create_variants(
                    **{variant_type: variant_index}
                )

                await client.party.me.set_outfit(
                    asset=cosmetic_id,
                    variants=skin_variants
                )

            elif 'cid' in cosmetic_id.lower() and 'jersey_color' in variant_type.lower():
                cosmetic_variants = client.party.me.create_variants(
                    pattern=0,
                    numeric=69,
                    **{variant_type: variant_index}
                )

                await client.party.me.set_outfit(
                    asset=cosmetic_id,
                    variants=cosmetic_variants
                )

            elif 'bid' in cosmetic_id.lower():
                cosmetic_variants = client.party.me.create_variants(
                    **{variant_type: variant_index}
                )

                await client.party.me.set_backpack(
                    asset=cosmetic_id,
                    variants=cosmetic_variants
                )
            elif 'pickaxe_id' in cosmetic_id.lower():
                cosmetic_variants = client.party.me.create_variants(
                    **{variant_type: variant_index}
                )

                await client.party.me.set_pickaxe(
                    asset=cosmetic_id,
                    variants=cosmetic_variants
                )

            else:
                await message.reply(f'Invalid cosmetic ID: {cosmetic_id}')

        if message.content.startswith('!style'):
            args = re.findall(r'"[^"]+"|\S+', message.content)[1:]
            if len(args) < 3:
                await message.reply('Usage: !style "<cosmetic_id>" <variant_type> <variant_index>')
                return

            cosmetic_id = args[0].strip('"')
            variant_type = args[1]
            variant_index = args[2]

            if not variant_index.isdigit():
                await message.reply('Variant index must be a number.')
                return

            if 'cid' in cosmetic_id.lower() and 'jersey_color' not in variant_type.lower():
                skin_variants = client.party.me.create_variants(
                    **{variant_type: variant_index}
                )

                await client.party.me.set_outfit(
                    asset=cosmetic_id,
                    variants=skin_variants
                )

            elif 'cid' in cosmetic_id.lower() and 'jersey_color' in variant_type.lower():
                cosmetic_variants = client.party.me.create_variants(
                    pattern=0,
                    numeric=69,
                    **{variant_type: variant_index}
                )

                await client.party.me.set_outfit(
                    asset=cosmetic_id,
                    variants=cosmetic_variants
                )

            elif 'bid' in cosmetic_id.lower():
                cosmetic_variants = client.party.me.create_variants(
                    **{variant_type: variant_index}
                )

                await client.party.me.set_backpack(
                    asset=cosmetic_id,
                    variants=cosmetic_variants
                )
            elif 'pickaxe_id' in cosmetic_id.lower():
                cosmetic_variants = client.party.me.create_variants(
                    **{variant_type: variant_index}
                )

                await client.party.me.set_pickaxe(
                    asset=cosmetic_id,
                    variants=cosmetic_variants
                )

            else:
                await message.reply(f'Invalid cosmetic ID: {cosmetic_id}')

        if message.content.lower().startswith('!random'):
            item = message.content.split(' ')[1]
            if item.lower() == 'skin':
                skin_response = requests.get('https://package.lobbybots.xyz/skins')
                skin_data = random.choice(skin_response.json())
                await client.party.me.set_outfit(f"{skin_data['id']}")
                await message.reply(f"Skin set to: {skin_data['name']}")
            elif item.lower() == 'backpack':
                backpack_response = requests.get('https://package.lobbybots.xyz/backpacks')
                backpack_data = random.choice(backpack_response.json())
                await client.party.me.set_backpack(f"{backpack_data['id']}")
                await message.reply(f"Backpack set to: {backpack_data['name']}")
            elif item.lower() == 'pickaxe':
                pickaxe_response = requests.get('https://package.lobbybots.xyz/pickaxes')
                pickaxe_data = random.choice(pickaxe_response.json())
                await client.party.me.set_pickaxe(f"{pickaxe_data['id']}")
                await client.party.me.clear_emote()
                await client.party.me.set_emote("EID_IceKing")
                await message.reply(f"Pickaxe set to: {pickaxe_data['name']}")
            elif item.lower() == 'emote':
                await client.party.me.clear_emote()
                emote_response = requests.get('https://package.lobbybots.xyz/emotes')
                emote_data = random.choice(emote_response.json())
                await client.party.me.set_emote(f"{emote_data['id']}")
                await message.reply(f"Emote set to: {emote_data['name']}")
            elif item.lower() == 'all':
                await client.party.me.clear_emote()
                skin_response = requests.get('https://package.lobbybots.xyz/skins')
                backpack_response = requests.get('https://package.lobbybots.xyz/backpacks')
                pickaxe_response = requests.get('https://package.lobbybots.xyz/pickaxes')
                emote_response = requests.get('https://package.lobbybots.xyz/emotes')
                skin_data = random.choice(skin_response.json())
                backpack_data = random.choice(backpack_response.json())
                pickaxe_data = random.choice(pickaxe_response.json())
                emote_data = random.choice(emote_response.json())
                await client.party.me.set_outfit(f"{skin_data['id']}")
                await client.party.me.set_backpack(f"{backpack_data['id']}")
                await client.party.me.set_pickaxe(f"{pickaxe_data['id']}")
                await client.party.me.set_emote(f"{emote_data['id']}")
                await message.reply(f"Skin set to: {skin_data['name']}.\nBackpack set to: {backpack_data['name']}.\nPickaxe set to: {pickaxe_data['name']}.\nEmote set to: {emote_data['name']}.")
            else:
                await message.reply("Invalid! Please user !random skin/backpack/pickaxe/emote/all.")

        if message.content.startswith("!hide"):
            if client.party.me.leader:
                try:
                    raw_squad_assignments = client.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]
                    for m in raw_squad_assignments:
                        raw_squad_assignments.remove(m)

                    await set_and_update_party_prop(
                        'Default:RawSquadAssignments_j',
                        {
                            'RawSquadAssignments': raw_squad_assignments
                        }
                    )

                    await message.reply("Hid everyone in the party.")
                except fortnitepy.HTTPException:
                    await message.reply("I am not party leader.")
            else:
                await message.reply("I need party leader to do this!")

        if message.content.startswith('!unhide'):
            if client.party.me.leader:
                try:
                    raw_squad_assignments = [{'memberId': m.id, 'absoluteMemberIdx': i + 1} for i, m in enumerate(client.party.members)]

                    await set_and_update_party_prop(
                        'Default:RawSquadAssignments_j',
                        {
                            'RawSquadAssignments': raw_squad_assignments
                        }
                    )

                    await message.reply("Unhid everyone in the party.")
                except fortnitepy.HTTPException:
                    await message.reply("I am not party leader.")
            else:
                await message.reply("I need party leader to do this!")

        if message.content.lower() == '!friends':
            await message.reply(f'I have {len(client.friends)} friends!')

        # Load the config file
        with open(config_file, 'r') as f:
            config = json.load(f)

        admins = config.get('admins', [])

        if message.content.startswith("!admin add"):
            if message.author.id not in config['admins']:
                await message.reply("You do not have permission to add admins.")
                return

            command_parts = message.content.split()
            if len(command_parts) != 3:
                await message.reply("Invalid command usage. Please use '!admin add [user_id]' to add an admin.")
                return

            action, admin = command_parts[1], command_parts[2]
            if action == "add":
                if admin in config['admins']:
                    await message.reply(f"{admin} is already an admin.")
                    return

                config['admins'].append(admin)

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"{admin} has been added as an admin.")
            else:
                await message.reply("Invalid command usage. Please use '!admin add [user_id]' to add an admin.")

        if message.content.startswith("!admin remove"):
            if message.author.id not in config['admins']:
                await message.reply("You do not have permission to remove admins.")
                return

            command_parts = message.content.split()
            if len(command_parts) != 3:
                await message.reply("Invalid command usage. Please use '!admin remove [user_id]' to remove an admin.")
                return

            action, admin = command_parts[1], command_parts[2]
            if action == "remove":
                if admin not in config['admins']:
                    await message.reply(f"{admin} is not an admin.")
                    return

                config['admins'].remove(admin)

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"{admin} has been removed from admins.")
            else:
                await message.reply("Invalid command usage. Please use '!admin remove [user_id]' to remove an admin.")

        if message.content.startswith("!admin list"):
            if message.author.id not in config.get('admins', []):
                await message.reply("You do not have permission to list admins.")
                return

            admins = config.get('admins', [])
            if not admins:
                await message.reply("There are no admins currently.")
            else:
                admin_list = "\n".join(admins)
                await message.reply(f"List of admins:\n{admin_list}")

        if message.content.startswith('!default skin'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the default skin.")
                return

            command_parts = message.content.split()
            if len(command_parts) < 3:
                await message.reply("Invalid command usage. Please use '!default skin [skin_names]' to set the default skin.")
                return

            action = command_parts[1]
            skins = command_parts[2:]

            if action == "skin":
                config['skin'] = ' '.join(skins)

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"The default skin has been set to: {' '.join(skins)}")
            else:
                await message.reply("Invalid command usage. Please use '!default skin [skin_names]' to set the default skin.")

        if message.content.lower().startswith('!default backpack'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the default backpack.")
                return

            command_parts = message.content.split()
            if len(command_parts) < 3:
                await message.reply("Invalid command usage. Please use '!default backpack [backpack_names]' to set the default backpack.")
                return

            action = command_parts[1]
            backpacks = command_parts[2:]

            if action == "backpack":
                config['backpack'] = ' '.join(backpacks)

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"The default backpack has been set to: {' '.join(backpacks)}")
            else:
                await message.reply("Invalid command usage. Please use '!default backpack [backpack_names]' to set the default backpack.")


        if message.content.lower().startswith('!default pickaxe'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the default pickaxe.")
                return

            command_parts = message.content.split()
            if len(command_parts) < 3:
                await message.reply("Invalid command usage. Please use '!default pickaxe [pickaxe_names]' to set the default pickaxe.")
                return

            action = command_parts[1]
            pickaxes = command_parts[2:]

            if action == "pickaxe":
                config['pickaxe'] = ' '.join(pickaxes)

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"The default pickaxe has been set to: {' '.join(pickaxes)}")
            else:
                await message.reply("Invalid command usage. Please use '!default pickaxe [pickaxe_names]' to set the default pickaxe.")


        if message.content.lower().startswith('!default emote'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the default emote.")
                return

            command_parts = message.content.split()
            if len(command_parts) < 3:
                await message.reply("Invalid command usage. Please use '!default emote [emote_names]' to set the default emote.")
                return

            action = command_parts[1]
            emotes = command_parts[2:]

            if action == "emote":
                config['emote'] = ' '.join(emotes)

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"The default emote has been set to: {' '.join(emotes)}")
            else:
                await message.reply("Invalid command usage. Please use '!default emote [emote_names]' to set the default emote.")

        if message.content.lower().startswith('!default level'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the default level.")
                return

            command_parts = message.content.split()
            if len(command_parts) != 3:
                await message.reply("Invalid command usage. Please use '!default level [level]' to set the default level.")
                return

            action, level = command_parts[1], command_parts[2]

            if action == "level":
                try:
                    level = int(level)
                except ValueError:
                    await message.reply("Invalid level value. Please provide a valid number.")
                    return

                config['level'] = level

                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                await message.reply(f"The default level has been set to: {level}")
            else:
                await message.reply("Invalid command usage. Please use '!default level [level]' to set the default level.")

        if message.content.startswith('!auto_update'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the auto_update variable.")
                return

            command_parts = message.content.split()
            if len(command_parts) != 2:
                await message.reply("Invalid command usage. Please use '!auto_update [True/False]' to set the auto_update variable.")
                return

            auto_update = command_parts[1].lower()
            if auto_update not in ['true', 'false']:
                await message.reply("Invalid command usage. Please use '!auto_update [True/False]' to set the auto_update variable.")
                return

            config['auto_update'] = (auto_update == 'true')

            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)

            await message.reply(f"The auto_update variable has been set to: {auto_update}")

        if message.content.startswith('!accept_friend_requests'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the accept_friend_requests variable.")
                return

            command_parts = message.content.split()
            if len(command_parts) != 2:
                await message.reply("Invalid command usage. Please use '!accept_friend_requests [True/False]' to set the accept_friend_requests variable.")
                return

            accept_friend_requests = command_parts[1].lower()
            if accept_friend_requests not in ['true', 'false']:
                await message.reply("Invalid command usage. Please use '!accept_friend_requests [True/False]' to set the accept_friend_requests variable.")
                return

            config['accept_friend_requests'] = (accept_friend_requests == 'true')

            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)

            await message.reply(f"The accept_friend_requests variable has been set to: {accept_friend_requests}")

        if message.content.startswith('!accept_invites'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the accept_invites variable.")
                return

            command_parts = message.content.split()
            if len(command_parts) != 2:
                await message.reply("Invalid command usage. Please use '!accept_invites [True/False]' to set the accept_invites variable.")
                return

            accept_invites = command_parts[1].lower()
            if accept_invites not in ['true', 'false']:
                await message.reply("Invalid command usage. Please use '!accept_invites [True/False]' to set the accept_invites variable.")
                return

            config['accept_invites'] = (accept_invites == 'true')

            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)

            await message.reply(f"The accept_invites variable has been set to: {accept_invites}")

        if message.content.lower().startswith('!join_message'):
            if message.author.id not in admins:
                await message.reply("You do not have permission to change the join message.")
                return

            command_parts = message.content.split(maxsplit=1)
            if len(command_parts) < 2:
                await message.reply("Invalid command usage. Please use '!join_message [message]' to set the join message.")
                return

            join_message = command_parts[1]
            config['join_message'] = join_message

            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)

            await message.reply(f"The join message has been set to: {join_message}")

    with open(config_file, 'r') as f:
        config = json.load(f)

    auto_update = str(config.get('auto_update', False))

    if auto_update == 'True':
        print('\033[36m' + "[FnLobbyBot] " + '\033[97m' + 'Updating packages...' + '\033[0m')
        try:
            response = requests.get("https://package.lobbybots.xyz/newest_version")
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            newest_version = response.json()[0].get('Version', None)
            if newest_version:
                print('\033[36m' + "[FnLobbyBot] " + '\033[97m' + f'Newest version available: {newest_version}' + '\033[0m')

                # Perform the necessary actions to update the package to the newest version
                os.system(f"pip install --upgrade fortnitepy > /dev/null 2>&1; pip install --upgrade -i https://test.pypi.org/simple/ testlobby=={newest_version} > /dev/null 2>&1")
                print('\033[36m' + "[FnLobbyBot] " + '\033[97m' + 'Package update completed.' + '\033[0m')
            else:
                print('\033[36m' + "[FnLobbyBot] " + '\033[97m' + 'Failed to retrieve the newest version.' + '\033[0m')

        except requests.exceptions.RequestException as e:
            print('\033[36m' + "[FnLobbyBot] " + '\033[91m' + f'An error occurred while updating packages: {e}' + '\033[0m')
    else:
        print('\033[36m' + "[FnLobbyBot] " + '\033[97m' + 'Auto update is disabled. (Not recommended)' + '\033[0m')

    # Start the client
    try:
        client.run()
    except Exception:
        print('\033[36m' + "[FnLobbyBot] " + '\033[31m' + "Can't login because your device auths are wrong." + '\033[0m')
        print('\033[36m' + "[FnLobbyBot] " + '\033[36m' + "Video tutorial: https://youtu.be/HoPHUgkQNYY." + '\033[0m')
        print('\033[36m' + "[FnLobbyBot] " + '\033[36m' + "Login to the account you want the bot to use and go to this website https://lobbybots.xyz/authcode and code the authorizationCode only! " + '\033[31m' + "IF THE AUTH CODE SAYS NULL THEN YOU NEED TO LOGIN TO THE ACCOUNT AGAIN!" + '\033[0m')
        print('\033[36m' + "[FnLobbyBot] " + '\033[31m' + "DONT USE YOUR MAIN ACCOUNT!" + '\033[0m')
        auth_code = input('\033[36m' + "[FnLobbyBot] " + '\033[97m' + 'Enter your authorizationCode: ' + '\033[0m')

        # Send a POST request to the website with the auth code
        response = requests.post("http://authorization.lobbybots.xyz/get_auth", data={"auth_code": auth_code})

        # Check if the response is successful
        if response.status_code == 200:
            # If the response is successful, print the device ID, account ID, and secret
            data = response.json()
            device_id = data["device_id"]
            account_id = data["account_id"]
            secret = data["secret"]
            print('\033[36m' + "[FnLobbyBot] " + '\033[32m' + "Device Auths saved! Restart the project to get your bot online!"+ '\033[0m')

            # Save the device ID, account ID, and secret to a file
            device_auth = [{"device_id": device_id, "account_id": account_id, "secret": secret}]
            with open(device_auth_file, "w") as f:
                json.dump(device_auth, f)
        else:
            # If the response is not successful, print an error message
            print('\033[36m' + "[FnLobbyBot] " + '\033[31m' + "Error processing auth code please try again later." + '\033[0m')