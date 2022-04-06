version = "1.9.0"
configVersion = "1.8.0"
print(f"Fortnite Save the World Claimer v{version} by PRO100KatYT\n")
try:
    import json
    import requests
    import os
    from configparser import ConfigParser
    from datetime import datetime
    import webbrowser
    import time
except Exception as emsg:
    input(f"ERROR: {emsg}. To run this program, please install it.\n\nPress ENTER to close the program.")
    exit()

# Links that will be used in the later part of code.
class links:
    loginLink1 = "https://www.epicgames.com/id/api/redirect?clientId={0}&responseType=code"
    loginLink2 = "https://www.epicgames.com/id/logout?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253D{0}%2526responseType%253Dcode"
    getOAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/{0}"
    getDeviceAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{0}/deviceAuth"
    getStorefront = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/storefront/v2/catalog"
    profileRequest = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/{1}?profileId={2}"

# Automatic llama loot recycling variables.
class autoRecycling:
    rarities = {"off": "", "common": "common", "uncommon": "common, uncommon", "rare": "common, uncommon, rare", "epic": "common, uncommon, rare, epic"}
    itemRarities = []
    recycleResources = ["AccountResource:heroxp", "AccountResource:personnelxp", "AccountResource:phoenixxp", "AccountResource:phoenixxp_reward", "AccountResource:reagent_alteration_ele_fire", "AccountResource:reagent_alteration_ele_nature", "AccountResource:reagent_alteration_ele_water", "AccountResource:reagent_alteration_gameplay_generic", "AccountResource:reagent_alteration_generic", "AccountResource:reagent_alteration_upgrade_r", "AccountResource:reagent_alteration_upgrade_sr", "AccountResource:reagent_alteration_upgrade_uc", "AccountResource:reagent_alteration_upgrade_vr", "AccountResource:reagent_c_t01", "AccountResource:reagent_c_t02", "AccountResource:reagent_c_t03", "AccountResource:reagent_c_t04", "AccountResource:reagent_evolverarity_r", "AccountResource:reagent_evolverarity_sr", "AccountResource:reagent_evolverarity_vr", "AccountResource:reagent_people", "AccountResource:reagent_promotion_heroes", "AccountResource:reagent_promotion_survivors", "AccountResource:reagent_promotion_traps", "AccountResource:reagent_promotion_weapons", "AccountResource:reagent_traps", "AccountResource:reagent_weapons", "AccountResource:schematicxp"]

# Start a new requests session.
session = requests.Session()

# Get the current date and time and neatly format it | by Salty-Coder :)
def getDateTimeString():
    dateTimeObj = datetime.now()
    return "[{:4d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}]".format(dateTimeObj.year,dateTimeObj.month,dateTimeObj.day, dateTimeObj.hour,dateTimeObj.minute,dateTimeObj.second)

# Error with a custom message.
def customError(text):
    if bShowDateTime == "true": input(f"{getDateTimeString()} ERROR: {text}\n\nPress ENTER to close the program.\n")
    else: input(f"ERROR: {text}\n\nPress ENTER to close the program.\n")
    exit()

# Error for invalid config values.
def configError(key, value, validValues): customError(f"You set the wrong {key} value in config.ini ({value}). Valid values: {validValues}. Please change it and run this program again.")

# Input loop until it's one of the correct values.
def validInput(text, values):
    response = input(f"{text}\n")
    print()
    while True:
        if values == "digit":
            if "," in response: response = response.replace(",", ".")
            if response.isdigit(): break
        if values == "url": # For Discord webhook | Salty-Coder
            if response.startswith("https://discord.com/api/webhooks/"): break
        elif response in values: break
        response = input("You priovided a wrong value. Please input it again.\n")
        print()
    return response

# Get the text from a request and check for errors.
def requestText(request, bCheckForErrors):
    requestText = json.loads(request.text)
    if ((bCheckForErrors) and ("errorMessage" in requestText)): customError(requestText['errorMessage'])
    return requestText

# Send token request.
def reqTokenText(loginLink, altLoginLink, authHeader):
    count = 0
    while True:
        count += 1
        if count > 1: loginLink = altLoginLink
        webbrowser.open_new_tab(loginLink)
        print(f"If the program didnt open it, copy this link to your browser: {(loginLink)}\n")
        reqToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": f"basic {authHeader}"}, data={"grant_type": "authorization_code", "code": input("Insert the auth code:\n")}), False)
        if not "errorMessage" in reqToken: break
        else: input(f"\n{reqToken['errorMessage']}.\nPress ENTER to open the website again and get the code.\n")
    return reqToken

# Print a message with or without the date and time.
def message(string):
    if bShowDateTime == "true":
        string = string.replace("\n", "\n     ")
        string = f"{getDateTimeString()} {string}"
    print(string)
    if bDiscordWebhookURL: # Check for Discord webhook
        webhook(bDiscordWebhookURL, string) # Send the webhook

def webhook(url, string): # Sending Discord webhooks :) | Salty-Coder
    data = {
    "content" : string,
    "username" : "Save The World Claimer"
    }
    result = requests.post(url, json = data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return err
    else:
        return True

# Create and/or read the config.ini file.
config, configPath = [ConfigParser(), os.path.join(os.path.split(os.path.abspath(__file__))[0], "config.ini")]
langValues, boolValues = [["ar", "de", "en", "es", "es-419", "fr", "it", "ja", "ko", "pl", "pt-BR", "ru", "tr", "zh-CN", "zh-Hant"], ["true", "false"]]
if not os.path.exists(configPath):
    print("Starting to generate the config.ini file.\n") # Don't want to initiate message() before bShowDateTime exists... - Salty-Coder
    bStartSetup = validInput("Type 1 if you want to start the config setup and press ENTER.\nType 2 if you want to use the default config values and press ENTER.", ["1", "2"])
    if bStartSetup == "1":
        iLanguage = validInput(f"What language do you want the Fortnite item names to be?\nValid vaules: {', '.join(langValues)}", langValues)
        iSpend_Research_Points = validInput("Do you want to automatically spend your Research Points whenever the program is unable to collect them because of their max accumulation?\nThe \"lowest\" method makes the program search for a Research stat with the lowest level.\nThe \"everyten\" method makes the program search for the closest Research stat to a full decimal level, e.g. level 10, 20, 40, etc.\nValid vaules: off, lowest, everyten.", ["off", "lowest", "everyten"])
        iOpen_Free_Llamas = validInput("Do you want the program to search for free Llamas and open them if they are avaiable?\nValid vaules: true, false.", boolValues)
        bAutomaticRecycle = validInput("Do you want to Automatically recycle unwanted free Llama loot?\nValid vaules: true, false.", boolValues)
        if bAutomaticRecycle == "false": iRecycle_Weapons = iRecycle_Traps = iRetire_Survivors = iRetire_Defenders = iRetire_Heroes = "off"
        else:
            iList = []
            itemTypeJson = {"Recycle_Weapons": {"name": "Weapon Schematics", "recycleWord": "recycle"}, "Recycle_Traps": {"name": "Trap Schematics", "recycleWord": "recycle"}, "Recycle_Survivors": {"name": "Survivors", "recycleWord": "retire"}, "Recycle_Defenders": {"name": "Defenders", "recycleWord": "retire"}, "Recycle_Heroes": {"name": "Heroes", "recycleWord": "retire"}}
            for itemType in itemTypeJson: iList.append(validInput(f"Input the rarity of {itemTypeJson[itemType]['name']} you want the program to automatically {itemTypeJson[itemType]['recycleWord']} at it or below.\nValid values: off, common, uncommon, rare, epic.", ["off", "common", "uncommon", "rare", "epic"]))
            iRecycle_Weapons, iRecycle_Traps, iRetire_Survivors, iRetire_Defenders, iRetire_Heroes = iList  
        iLoop_Time = validInput("Do you want the progam to loop itself every X minutes?\nSet this to 0 to not loop the program.\nValid values: a number (1, 15, 60, etc.).", "digit")
        iShow_Date_Time = validInput("Do you want the program to show the date and time when sending messages?\nValid vaules: true, false.", boolValues)
        iDiscord_Webhook = validInput("Do you want the program to post output to a Discord webhook?\nValid vaules: true, false.", boolValues)
        iDiscord_Webhook_URL = ""
        if iDiscord_Webhook == "true":
            iDiscord_Webhook_URL = validInput("Discord webhook URL:", "url")
    else: iLanguage, iSpend_Research_Points, iOpen_Free_Llamas, iRecycle_Weapons, iRecycle_Traps, iRetire_Survivors, iRetire_Defenders, iRetire_Heroes, iLoop_Time, iShow_Date_Time, iDiscord_Webhook, iDiscord_Webhook_URL = ["en", "lowest", "true", "uncommon", "uncommon", "rare", "rare", "uncommon", 0, "false", "false", ""]           
    with open(configPath, "w") as configFile: configFile.write(f"[StW_Claimer_Config]\n\n# What language do you want the Fortnite item names to be?\n# Valid vaules: ar, de, en, es, es-419, fr, it, ja, ko, pl, pt-BR, ru, tr, zh-CN, zh-Hant.\nLanguage = {iLanguage}\n\n# Do you want to automatically spend your Research Points whenever the program is unable to collect them because of their max accumulation?\n# The \"lowest\" method makes the program search for a Research stat with the lowest level.\n# The \"everyten\" method makes the program search for the closest Research stat to a full decimal level, e.g. level 10, 20, 40, etc.\n# Valid vaules: off, lowest, everyten.\nSpend_Research_Points = {iSpend_Research_Points}\n\n# Do you want the program to search for free Llamas and open them if they are avaiable?\n# Valid vaules: true, false.\nOpen_Free_Llamas = {iOpen_Free_Llamas}\n\n[Automatic_Recycle/Retire]\n\n# Automatically recycle Weapon schematics at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRecycle_Weapons = {iRecycle_Weapons}\n\n# Automatically recycle Trap schematics at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRecycle_Traps = {iRecycle_Traps}\n\n# Automatically retire Survivors at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRetire_Survivors = {iRetire_Survivors}\n\n# Automatically retire Defenders at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRetire_Defenders = {iRetire_Defenders}\n\n# Automatically retire Heroes at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRetire_Heroes = {iRetire_Heroes}\n\n[Loop]\n\n# Do you want the progam to loop itself every X minutes?\n# Set this to 0 to not loop the program.\n# Valid values: a number (1, 15, 60, etc.).\nLoop_Minutes = {iLoop_Time}\n\n[Misc]\n\n# Do you want the program to show the date and time when sending messages?\n# Valid vaules: true, false.\nShow_Date_Time = {iShow_Date_Time}\n\n# Do you want the program to post output to a Discord webhook?\nDiscord_Webhook_URL = {iDiscord_Webhook_URL}\n\n[Config_Version]\n\nVersion = STWC_{configVersion}")
    print("The config.ini file was generated successfully.\n")
try:
    config.read(configPath)
    configVer, lang, spendAutoResearch, bOpenFreeLlamas, loopMinutes, bShowDateTime, bDiscordWebhookURL = [config['Config_Version']['Version'], config['StW_Claimer_Config']['Language'].lower(), config['StW_Claimer_Config']['Spend_Research_Points'].lower(), config['StW_Claimer_Config']['Open_Free_Llamas'].lower(), config['Loop']['Loop_Minutes'], config['Misc']['Show_Date_Time'].lower(), config['Misc']['Discord_Webhook_URL']]
    autoRecycling.itemRarities = {"weapon": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Recycle_Weapons'].lower()].split(", "), "trap": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Recycle_Traps'].lower()].split(", "), "survivor": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Retire_Survivors'].lower()].split(", "), "defender": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Retire_Defenders'].lower()].split(", "), "hero": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Retire_Heroes'].lower()].split(", ")}
except: customError("The program is unable to read the config.ini file. Delete the config.ini file and run this program again to generate a new one.")
if not (configVer == f"STWC_{configVersion}"): customError("The config file is outdated. Delete the config.ini file and run this program again to generate a new one.")
checkValuesJson = {"Language": {"value": lang, "validValues": langValues}, "Spend_Research_Points": {"value": spendAutoResearch, "validValues": ["off", "lowest", "everyten"]}, "Open_Free_Llamas": {"value": bOpenFreeLlamas, "validValues": boolValues}, "Show_Date_Time": {"value": bShowDateTime, "validValues": boolValues}}
for option in checkValuesJson:
    if not (checkValuesJson[option]['value'] in checkValuesJson[option]['validValues']): configError(option, checkValuesJson[option]['value'], ", ".join(checkValuesJson[option]['validValues']))
recycleOptions = ["Recycle_Weapons", "Recycle_Traps", "Retire_Survivors", "Retire_Defenders", "Retire_Heroes"]
recycleOn = False
for key in recycleOptions:
    keyValue = config['Automatic_Recycle/Retire'][f'{key}'].lower()
    if not (keyValue == "off"): recycleOn = True
    if not (keyValue in ("off", "common", "uncommon", "rare", "epic")): configError(key, keyValue, "off, common, uncommon, rare, epic")
try:
    if not (("," in loopMinutes) or ("." in loopMinutes)): loopMinutes = float(f"{loopMinutes}.0")
    else: loopMinutes = float(loopMinutes.replace(",", "."))
except: configError("Loop_Minutes", loopMinutes, "a number (1, 15, 60, etc.)")

# Load the stringlist.json file and create and load the auth.json file.
stringListPath, authPath = [os.path.join(os.path.split(os.path.abspath(__file__))[0], "stringlist.json"), os.path.join(os.path.split(os.path.abspath(__file__))[0], "auth.json")]
if not os.path.exists(stringListPath): customError("The stringlist.json file doesn't exist. Get it from this program's repository on Github (https://github.com/PRO100KatYT/SaveTheWorldClaimer), add it back and run this program again.")
try: stringList = json.loads(open(stringListPath, "r", encoding = "utf-8").read())
except: customError("The program is unable to read the stringlist.json file. Delete the stringlist.json file, download it from this program's repository on Github (https://github.com/PRO100KatYT/SaveTheWorldClaimer), add it back here and run this program again.")
if not os.path.exists(authPath):
    with open(authPath, "w") as authJson: authJson.write("[]")
try: authJson = json.loads(open(authPath, "r", encoding = "utf-8").read())
except: customError("The program is unable to read the auth.json file. Delete the auth.json file and run this program again.")
if not isinstance(authJson, list): customError("Your auth.json file is in the pre-1.9.0 format, so the program cannot properly read it. To fix this issue, delete it and generate it by running this program again.")

# Startup (Account Manager)
def startup():
    def addAccount(bGoBack = True):
        if bGoBack: isLoggedIn = validInput("Are you logged into your Epic account that you would like the program to use in your browser?\nType 1 if yes and press ENTER.\nType 2 if no and press ENTER.\nType 3 to go back and press ENTER.\n", ["1", "2", "3"])
        else: isLoggedIn = validInput("Are you logged into your Epic account that you would like the program to use in your browser?\nType 1 if yes and press ENTER.\nType 2 if no and press ENTER.\n", ["1", "2"])
        if isLoggedIn != "3":
            authType = validInput("Which authentication method do you want the program to use?\nToken auth metod generates a refresh token to log in. The limit per IP is 1. It's recommended if you plan to use only one account.\nDevice auth method generates authorization credentials that don't have an expiration date and limit per IP, but can after some time cause epic to ask you to change your password. It's recommended if you plan to use multiple accounts.\nValid vaules: token, device.", ["token", "device"])
            input("The program is going to open an Epic Games webpage.\nTo continue, press ENTER.\n")
            if isLoggedIn == "1": loginLink = links.loginLink1
            elif isLoggedIn == "2": loginLink = links.loginLink2
            if authType == "token":
                reqToken = reqTokenText(loginLink.format("34a02cf8f4414e29b15921876da36f9a"), links.loginLink1.format("34a02cf8f4414e29b15921876da36f9a"), "MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y=")
                refreshToken, accountId, displayName, expirationDate = [reqToken["refresh_token"], reqToken["account_id"], reqToken["displayName"], reqToken["refresh_expires_at"]]
                jsonToAppend = {"WARNING": "Don't show anyone the contents of this file, because it contains information with which the program logs into the account.", "authType": "token", "refreshToken": refreshToken, "accountId": accountId, "displayName": displayName, "refresh_expires_at": expirationDate}
            else:
                reqToken = reqTokenText(loginLink.format("3446cd72694c4a4485d81b77adbb2141"), links.loginLink1.format("3446cd72694c4a4485d81b77adbb2141"), "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=")
                accessToken, accountId, displayName = [reqToken["access_token"], reqToken["account_id"], reqToken["displayName"]]
                reqDeviceAuth = requestText(session.post(links.getDeviceAuth.format(accountId), headers={"Authorization": f"bearer {accessToken}"}, data={}), True)
                deviceId, secret = [reqDeviceAuth["deviceId"], reqDeviceAuth["secret"]]
                jsonToAppend = {"WARNING": "Don't show anyone the contents of this file, because it contains information with which the program logs into the account.", "authType": "device",  "deviceId": deviceId, "accountId": accountId, "displayName": displayName, "secret": secret}
            bAlreadyLoggedIn = False
            for account in authJson:
                if account['accountId'] == accountId: bAlreadyLoggedIn = True
            if bAlreadyLoggedIn: message(f"\n{displayName} is already added to the program's account list. If you want to log in again with this account, remove it from the list and then add it using the Account Manager.\n")
            else:
                authJson.append(jsonToAppend)
                with open(authPath, "w", encoding = "utf-8") as authFile: json.dump(authJson, authFile, indent = 2, ensure_ascii = False)
                message(f"\n{displayName} has been successfully added to the program's account list.\n")

    def listAccounts():
        message("Account list:")
        if not authJson: message("There are no accounts added to this program.\n")
        else:
            for account in authJson:
                try: message(f"{authJson.index(account) + 1}: {account['displayName']}")
                except: message(f"{authJson.index(account) + 1}: (unknown display name)")

    def removeAccount():
        listAccounts()
        if authJson:
            message("To remove an account from this program, type the number next to it's display name and press ENTER.\nTo go back, type 0 and press ENTER.")
            accountCountList = []
            for account in authJson: accountCountList.append(str(authJson.index(account)))
            accountToRemove = int(validInput("", accountCountList + [str(int(accountCountList[-1]) + 1)]))
            if accountToRemove != 0:
                message(f"{authJson[accountToRemove - 1]['displayName']} has been successfully removed from the program's account list.\n")
                authJson.pop(accountToRemove - 1)
                with open(authPath, "w", encoding = "utf-8") as authFile: json.dump(authJson, authFile, indent = 2, ensure_ascii = False)

    while True:
        if not authJson: addAccount(False)
        bStartClaimer = validInput("Main menu:\nType 1 if you want to start this program and press ENTER.\nType 2 if you want to go the Account Manager and press ENTER.", ["1", "2"])
        if bStartClaimer == "1": break
        else:
            while True:
                whatToDo = validInput("Account Manager:\nType 1 if you want to add an account to this program and press ENTER.\nType 2 if you want to remove an account from this program and press ENTER.\nType 3 if you want to see the list of accounts added to this program and press ENTER.\nType 4 to go back and press ENTER.", ["1", "2", "3", "4"])
                if whatToDo == "1": addAccount()
                elif whatToDo == "2": removeAccount()
                elif whatToDo == "3":
                    listAccounts()
                    input("Press ENTER to continue.\n")
                else: break

# The main part of the program that can be looped.
def main():
    for account in authJson:
        # Read the auth.json file.
        try:
            authType, accountId = [account['authType'], account["accountId"]]
            try: displayName = account['displayName']
            except: displayName = "(unknown display name)"
            if authType == "token":
                expirationDate, refreshToken = [account["refresh_expires_at"], account["refreshToken"]]
                if expirationDate < datetime.now().isoformat(): customError(f"The refresh token has expired. To fix this issue, remove {displayName} from the account list and add this account back. If this problem persists try to log in using the device auth type.")
            if authType == "device":
                deviceId, secret = [account["deviceId"], account["secret"]]
        except:
            customError(f"The program is unable to read the {displayName}'s auth.json file part. To fix this issue, remove {displayName} from the account list and add this account back.")

        # Log in.
        message(f"Logging in as {displayName}...")
        if authType == "token": # Shoutout to BayGamerYT for telling me about this login method.
            reqRefreshToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "refresh_token", "refresh_token": refreshToken}), False)
            if "errorMessage" in reqRefreshToken: customError(f"{reqRefreshToken['errorMessage']}. To fix this issue, remove {displayName} from the account list and add this account back. If this problem persists try to log in using the device auth type.")
            account['refreshToken'], account['refresh_expires_at'] = [reqRefreshToken["refresh_token"], reqRefreshToken["refresh_expires_at"]]
            with open(authPath, "w", encoding = "utf-8") as saveAuthFile: json.dump(authJson, saveAuthFile, indent = 2, ensure_ascii = False)
            reqExchange = requestText(session.get(links.getOAuth.format("exchange"), headers={"Authorization": f"bearer {reqRefreshToken['access_token']}"}, data={"grant_type": "authorization_code"}), True)
            reqToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "exchange_code", "exchange_code": reqExchange["code"], "token_type": "eg1"}), True)
        if authType == "device": reqToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "device_auth", "device_id": deviceId, "account_id": accountId, "secret": secret, "token_type": "eg1"}), True)
        accessToken, displayName = [reqToken['access_token'], reqToken['displayName']]
        message(f"Successfully logged in.\n")

        # Headers for MCP requests.
        headers = {"User-Agent": "Fortnite/++Fortnite+Release-19.40-CL-19215531 Windows/10.0.19043.1.768.64bit", "Authorization": f"bearer {accessToken}", "Content-Type": "application/json"}

        # Check whether the account has the campaign access token and is able to receive V-Bucks.
        # The receivemtxcurrency token is not required, but instead of V-Bucks the account will recieve X-Ray Tickets.
        reqCheckTokens = [json.dumps(requestText(session.post(links.profileRequest.format(accountId, "QueryProfile", "common_core"), headers=headers, data="{}"), False)), json.dumps(requestText(session.post(links.profileRequest.format(accountId, "ClientQuestLogin", "campaign"), headers=headers, data="{}"), False))]
        bCampaignAccess = bReceiveMtx = False
        if "Token:campaignaccess" in reqCheckTokens[0]: bCampaignAccess = True
        if "Token:receivemtxcurrency" in reqCheckTokens[1]: bReceiveMtx = True

        # Claim the Daily Reward.
        if bCampaignAccess == True:
            reqClaimDailyReward = requestText(session.post(links.profileRequest.format(accountId, "ClaimLoginReward", "campaign"), headers=headers, data="{}"), True)
            cdrItems, cdrDaysLoggedIn, totalAmount = [reqClaimDailyReward['notifications'][0]['items'], reqClaimDailyReward['notifications'][0]['daysLoggedIn'], 0]
            cdrDaysModified = int(cdrDaysLoggedIn) % 336 # Credit to dippyshere for this and the next line of code.
            if cdrDaysModified == 0: cdrDaysModified = 336
            rewardTemplateIds, rewardWord, rewardName = [[stringList['Daily Rewards'][f'{cdrDaysModified}']['templateId']], "Reward", stringList['Items'][stringList['Daily Rewards'][f'{cdrDaysModified}']['templateId']]['name'][lang]]
            if rewardTemplateIds[0].startswith("ConditionalResource:"):
                if bReceiveMtx == True: rewardTemplateIds.append("AccountResource:currency_xrayllama")
                else: rewardTemplateIds = ["AccountResource:currency_xrayllama"]
            if len(rewardTemplateIds) > 1: rewardWord = "Rewards"
            if not cdrItems: dailyMessage = f"The daily reward for {displayName} has been already claimed today!\nDay: {cdrDaysLoggedIn}\n{rewardWord}: "
            else: dailyMessage = f"Today's daily reward for {displayName} has been successfully claimed!\nDay: {cdrDaysLoggedIn}\n{rewardWord} "
            for rewardTemplateId in rewardTemplateIds:
                rewardQuantity, rewardName = [stringList['Daily Rewards'][f'{cdrDaysModified}']['quantity'], stringList['Items'][rewardTemplateId]['name'][lang]]
                if rewardTemplateId.startswith("ConditionalResource:"):
                    if bReceiveMtx == True: rewardName = rewardName['PassedConditionItem']
                    else: rewardName = rewardName['FailedConditionItem']
                if rewardQuantity == 1: dailyMessage += f'{stringList["Item Rarities"][stringList["Items"][rewardTemplateId]["rarity"]][lang]} | {stringList["Item Types"][stringList["Items"][rewardTemplateId]["type"]][lang]}: {rewardName}'
                else: dailyMessage += f'{stringList["Item Rarities"][stringList["Items"][rewardTemplateId]["rarity"]][lang]} | {stringList["Item Types"][stringList["Items"][rewardTemplateId]["type"]][lang]}: {rewardQuantity}x {rewardName}'
                if rewardTemplateId.startswith(("ConditionalResource:", "AccountResource:", "ConsumableAccountItem:")):
                    if rewardTemplateId.startswith("ConditionalResource:"):
                        reqGetCommonCore = requestText(session.post(links.profileRequest.format(accountId, "QueryProfile", "common_core"), headers=headers, data="{}"), True)
                        for item in reqGetCommonCore['profileChanges'][0]['profile']['items']:
                            if reqGetCommonCore['profileChanges'][0]['profile']['items'][item]['templateId'].lower().startswith("currency:mtx"): totalAmount += int(reqGetCommonCore['profileChanges'][0]['profile']['items'][item]['quantity'])     
                    else:
                        for item in reqClaimDailyReward['profileChanges'][0]['profile']['items']:
                            if reqClaimDailyReward['profileChanges'][0]['profile']['items'][item]['templateId'] == rewardTemplateId: totalAmount = int(reqClaimDailyReward['profileChanges'][0]['profile']['items'][item]['quantity'])
                    dailyMessage += f". Total amount: {totalAmount}\n"
                else: dailyMessage += "\n"
            message(f"{dailyMessage}")
        else: message(f"Skipping Daily Reward claiming because {displayName} doesn't have access to Save the World.\n")

        # Claim and automatically spend the Research Points.
        reqCampaignProfileCheck = requestText(session.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}"), True)
        reqCampaignProfileCheckResearchLevels, bTryToClaimRP, tokenToClaim = [reqCampaignProfileCheck['profileChanges'][0]['profile']['stats']['attributes']['research_levels'], True, []]
        try:
            if (reqCampaignProfileCheckResearchLevels['fortitude'] == 120 and reqCampaignProfileCheckResearchLevels['offense'] == 120 and reqCampaignProfileCheckResearchLevels['resistance'] == 120 and reqCampaignProfileCheckResearchLevels['technology'] == 120): bTryToClaimRP = False
        except: []
        if bTryToClaimRP:
            reqCampaignProfileCheckItems = reqCampaignProfileCheck['profileChanges'][0]['profile']['items']
            for key in reqCampaignProfileCheckItems: # Shoutout to Lawin for helping me figuring out how to write this and the next line of code.
                if reqCampaignProfileCheckItems[key]['templateId'] == "CollectedResource:Token_collectionresource_nodegatetoken01":
                    tokenToClaim = key
                    break
            if tokenToClaim:
                reqClaimCollectedResources = requestText(session.post(links.profileRequest.format(accountId, "ClaimCollectedResources", "campaign"), headers=headers, json={"collectorsToClaim": [tokenToClaim]}), False)
                if "errorMessage" in reqClaimCollectedResources: message(f"ERROR: {reqClaimCollectedResources['errorMessage']}\n") # Error without exit()
                else:
                    storedMaxPoints = False
                    try:
                        totalItemGuid, rpToClaim = [reqClaimCollectedResources['notifications'][0]['loot']['items'][0]['itemGuid'], reqClaimCollectedResources['profileChanges'][0]['profile']['items'][tokenToClaim]['attributes']['stored_value']]
                        rpStored, rpClaimedQuantity = [reqClaimCollectedResources['profileChanges'][0]['profile']['items'][totalItemGuid]['quantity'], int(reqClaimCollectedResources['notifications'][0]['loot']['items'][0]['quantity'])]
                        if float(rpToClaim) >= 1: storedMaxPoints = True
                        pointsWord = "Points"
                        if rpClaimedQuantity == 1: pointsWord = "Point"
                        message(f"Claimed {rpClaimedQuantity} Research {pointsWord}. Total Research Points: {reqClaimCollectedResources['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity']}\n")
                    except:
                        for key in reqCampaignProfileCheckItems:
                            if reqCampaignProfileCheckItems[key]['templateId'] == "Token:collectionresource_nodegatetoken01":
                                totalItemGuid = key
                                break
                        rpToClaim, rpStored, storedMaxPoints = [reqClaimCollectedResources['profileChanges'][0]['profile']['items'][f'{tokenToClaim}']['attributes']['stored_value'], reqClaimCollectedResources['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity'], True]
                        if int(rpToClaim) < 1:
                            storedMaxPoints = False
                            message(f"The program is unable to claim {round(rpToClaim, 2)} Research Point because in order to collect it, at least 1 point must be available for claiming. In other words, just wait a few seconds and run this program again.\n")
                    if storedMaxPoints == True:
                        if spendAutoResearch == "off": message(f"The program is unable to claim {round(rpToClaim, 2)} Research Points because you have the maximum number of accumulated Research Points at once ({rpStored}).\nIn this situation if you want to automatically spend them, change the Spend_Research_Points value in config.ini to lowest or everyten and run this program again.\n")
                        else:
                            message(f"You have the maximum number of accumulated Research Points at once ({rpStored}).\nStarting to automatically spend Research Points...\n")
                            while True:
                                reqFORTLevelsCheck = requestText(session.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}"), True)['profileChanges'][0]['profile']['stats']['attributes']['research_levels']
                                if spendAutoResearch == "lowest":
                                    levelsList = [int(reqFORTLevelsCheck['fortitude']), int(reqFORTLevelsCheck['offense']), int(reqFORTLevelsCheck['resistance']), int(reqFORTLevelsCheck['technology'])]
                                    level = min(levelsList)
                                elif spendAutoResearch == "everyten":
                                    levelsList, levelsJson = [[int(reqFORTLevelsCheck['fortitude']) % 10, int(reqFORTLevelsCheck['offense']) % 10, int(reqFORTLevelsCheck['resistance']) % 10, int(reqFORTLevelsCheck['technology']) % 10], {int(reqFORTLevelsCheck['fortitude']) % 10: int(reqFORTLevelsCheck['fortitude']), int(reqFORTLevelsCheck['offense']) % 10: int(reqFORTLevelsCheck['offense']), int(reqFORTLevelsCheck['resistance']) % 10: int(reqFORTLevelsCheck['resistance']), int(reqFORTLevelsCheck['technology']) % 10: int(reqFORTLevelsCheck['technology'])}]
                                    level = levelsJson[max(levelsList)]
                                for key in reqFORTLevelsCheck:
                                    if reqFORTLevelsCheck[key] == int(level):
                                        statToClaim = key
                                        break
                                reqPurchaseResearchStatUpgrade = requestText(session.post(links.profileRequest.format(accountId, "PurchaseResearchStatUpgrade", "campaign"), headers=headers, json={"statId": f'{statToClaim}'}), False)
                                if "errorMessage" in reqPurchaseResearchStatUpgrade: break # Error without exit()
                                else: message(f"Bought 1 {statToClaim.capitalize()} level. New level: {reqPurchaseResearchStatUpgrade['profileChanges'][0]['profile']['stats']['attributes']['research_levels'][statToClaim]}.")
                            message("Cannot buy more F.O.R.T. levels.\n")
                            reqClaimCollectedResources = requestText(session.post(links.profileRequest.format(accountId, "ClaimCollectedResources", "campaign"), headers=headers, json={"collectorsToClaim": [tokenToClaim]}), True)
                            try:
                                totalItemGuid = reqClaimCollectedResources['notifications'][0]['loot']['items'][0]['itemGuid']
                                message(f"Claimed {reqClaimCollectedResources['notifications'][0]['loot']['items'][0]['quantity']} Research Points. Total Research Points: {reqClaimCollectedResources['profileChanges'][0]['profile']['items'][totalItemGuid]['quantity']}\n")
                            except: []
            else: message(f"Skipping Research Points claiming because {displayName} doesn't have access to the Research Lab.\n")

        # Search for a free Llama and open it if available.
        alreadyOpenedFreeLlamas, freeLlamasCount, cpspStorefront = [0, 0, []]
        if bOpenFreeLlamas == "true":
            reqGetStorefront = requestText(session.get(links.getStorefront, headers=headers, data={}), True)['storefronts']
            for key in reqGetStorefront:
                if key['name'] == "CardPackStorePreroll":
                    cpspStorefront = key['catalogEntries']
                    break
            if not cpspStorefront: customError("Failed to find the Llama shop. Is it even possible? Maybe a new Fortnite update could break it, but it's very unlikely...")
            else:
                freeLlamas = []
                for key in cpspStorefront:
                    if (not "always" in key['devName'].lower()) and (key['prices'][0]['finalPrice'] == 0): freeLlamas.append(key)
                freeLlamasCount = len(freeLlamas)
                if not freeLlamas: message("There are no free Llamas available at the moment.\n")
                else:
                    message(f"There are free llamas avaiable!")
                    itemsfromLlamas, openedLlamas = [[], 0]
                    for llama in freeLlamas:
                        llamaToClaimOfferId, llamaToClaimName = [llama['offerId'], []]
                        try: llamaToClaimTitle = llama['title']
                        except: llamaToClaimTitle = []
                        llamaToClaimCPId = llama['itemGrants'][0]['templateId']
                        try: llamaToClaimName = stringList['Items'][llamaToClaimCPId]['name'][lang]
                        except:
                            if llamaToClaimTitle: llamaToClaimName = llamaToClaimTitle
                        if not llamaToClaimName: llamaToClaimName = llamaToClaimCPId
                        while True:
                            reqPopulateLlamas = requestText(session.post(links.profileRequest.format(accountId, "PopulatePrerolledOffers", "campaign"), headers=headers, data="{}"), True)
                            llamaTier = []
                            for key in reqPopulateLlamas['profileChanges'][0]['profile']['items']:
                                if (reqPopulateLlamas['profileChanges'][0]['profile']['items'][key]['templateId'].lower().startswith("prerolldata") and reqPopulateLlamas['profileChanges'][0]['profile']['items'][key]['attributes']['offerId'] == llamaToClaimOfferId):
                                    llamaTier = reqPopulateLlamas['profileChanges'][0]['profile']['items'][key]['attributes']['highest_rarity']
                                    llamaTier = stringList['Llama tiers'][f'{llamaTier}']
                            reqBuyFreeLlama = requestText(session.post(links.profileRequest.format(accountId, "PurchaseCatalogEntry", "common_core"), headers=headers, json={"offerId": llamaToClaimOfferId, "purchaseQuantity": 1, "currency": "GameItem", "currencySubType": "AccountResource:currency_xrayllama", "expectedTotalPrice": 0, "gameContext": "Frontend.None"}), False)
                            if "errorMessage" in reqBuyFreeLlama:
                                if "limit of" in reqBuyFreeLlama['errorMessage']:
                                    if openedLlamas == 0: alreadyOpenedFreeLlamas += 1
                                if "because fulfillment" in reqBuyFreeLlama['errorMessage']: message(f"\n{displayName} is unable to claim the free {llamaToClaimTitle}.\n")
                                break
                            else:
                                message(f"\nOpening: {llamaToClaimName}\nTier: {llamaTier}\nLoot result:")
                                llamaLoot, llamaLootCount = [reqBuyFreeLlama['notifications'][0]['lootResult']['items'], 0]
                                openedLlamas += 1
                                for key in llamaLoot:
                                    templateId, itemGuid, itemQuantity = [key['itemType'], key['itemGuid'], key['quantity']]
                                    try: itemName = stringList['Items'][templateId]['name'][lang]
                                    except: itemName = templateId
                                    itemRarity, itemType = [stringList['Items'][templateId]['rarity'], stringList['Items'][templateId]['type']]
                                    llamaLootCount += 1
                                    if itemRarity in ("common", "uncommon", "rare", "epic"): itemsfromLlamas.append({"itemName": itemName, "itemType": itemType, "templateId": templateId, "itemGuid": itemGuid, "itemRarity": itemRarity, "itemQuantity": itemQuantity})
                                    message(f"{llamaLootCount}: {stringList['Item Rarities'][stringList['Items'][templateId]['rarity']][lang]} | {stringList['Item Types'][stringList['Items'][templateId]['type']][lang]}: {itemQuantity}x {itemName}")
                    if int(alreadyOpenedFreeLlamas) == freeLlamasCount:
                        message(f"\nFree Llamas that are currently avaiable in the shop have been already opened on this account. Remember that you can open a maximum of 2 free one hour rotation Llamas per one shop rotation.\n")
                    else:
                        llamasWord = "Llamas"
                        if int(openedLlamas) == 1: llamasWord = "Llama"
                        if openedLlamas > 0: message(f"\nSuccesfully opened {openedLlamas} free {llamasWord}.\n")

        # Automatically recycle selected llama loot.
        if (recycleOn) and (not(int(alreadyOpenedFreeLlamas) == freeLlamasCount)):
            itemsToRecycle, itemGuidsToRecycle, recycleResources, recycledItemsCount, recycleResourcesCount = [[], [], [], 0, 0]
            for item in itemsfromLlamas:
                itemType, itemRarity, itemGuid = [item['itemType'], item['itemRarity'], item['itemGuid']]
                try:
                    if itemRarity in autoRecycling.itemRarities[itemType]:
                        itemGuidsToRecycle.append(itemGuid)
                        itemsToRecycle.append(item)
                except: []
            if not (len(itemGuidsToRecycle) == 0):
                message(f"Recycling/Retiring selected items from {openedLlamas} free {llamasWord}...\n")
                reqGetResources = requestText(session.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}"), True)
                for resource in autoRecycling.recycleResources:
                    for item in reqGetResources['profileChanges'][0]['profile']['items']:
                        if reqGetResources['profileChanges'][0]['profile']['items'][item]['templateId'] == resource: recycleResources.append({"itemGuid": item, "templateId": resource, "itemName": stringList['Items'][resource]['name'][lang], "quantity": reqGetResources['profileChanges'][0]['profile']['items'][item]['quantity']})
                requestText(session.post(links.profileRequest.format(accountId, "RecycleItemBatch", "campaign"), headers=headers, json={"targetItemIds": itemGuidsToRecycle}), True)
                recycleMessage = "The following items have been succesfully Recycled/Retired:\n"
                for item in itemsToRecycle:
                    recycledItemsCount += 1
                    recycleMessage += f"{recycledItemsCount}: {stringList['Item Rarities'][item['itemRarity']][lang]} | {stringList['Item Types'][item['itemType']][lang]}: {item['itemQuantity']}x {item['itemName']}\n"
                message(f"{recycleMessage}")
                reqGetResources2 = requestText(session.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}"), True)
                resourcesMessage = "Resources received:\n"
                for resource in recycleResources:
                    resourceQuantity = int(reqGetResources2['profileChanges'][0]['profile']['items'][resource['itemGuid']]['quantity']) - int(resource['quantity'])
                    if resourceQuantity > 0:
                        recycleResourcesCount += 1
                        resourcesMessage += f"{recycleResourcesCount}: {resourceQuantity}x {resource['itemName']}. Total amount: {reqGetResources2['profileChanges'][0]['profile']['items'][resource['itemGuid']]['quantity']}\n"
                message(f"{resourcesMessage}")

# Start the program.
startup()
if loopMinutes > 0:
    while True:
        main()
        if str(loopMinutes).endswith(".0"): loopMinutes = int(str(loopMinutes).split(".")[0])
        minutesWord = "minutes"
        if loopMinutes == 1: minutesWord = "minute"
        print(f"The program will run again in {loopMinutes} {minutesWord}.\n")
        time.sleep(loopMinutes * 60)
else: main()

input("Press ENTER to close the program.\n")
exit()