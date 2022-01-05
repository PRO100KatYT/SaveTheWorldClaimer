version = "1.6.0"
configVersion = "1.5.0"
print(f"Fortnite Save the World Claimer v{version} by PRO100KatYT\n")
try:
    import json
    import requests
    import os
    from configparser import ConfigParser
    from datetime import datetime
    import webbrowser
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
    rarities = {"common": "common", "uncommon": "common, uncommon", "rare": "common, uncommon, rare", "epic": "common, uncommon, rare, epic"}
    itemRarities = ""
    recycleResources = ["AccountResource:heroxp", "AccountResource:personnelxp", "AccountResource:phoenixxp", "AccountResource:phoenixxp_reward", "AccountResource:reagent_alteration_ele_fire", "AccountResource:reagent_alteration_ele_nature", "AccountResource:reagent_alteration_ele_water", "AccountResource:reagent_alteration_gameplay_generic", "AccountResource:reagent_alteration_generic", "AccountResource:reagent_alteration_upgrade_r", "AccountResource:reagent_alteration_upgrade_sr", "AccountResource:reagent_alteration_upgrade_uc", "AccountResource:reagent_alteration_upgrade_vr", "AccountResource:reagent_c_t01", "AccountResource:reagent_c_t02", "AccountResource:reagent_c_t03", "AccountResource:reagent_c_t04", "AccountResource:reagent_evolverarity_r", "AccountResource:reagent_evolverarity_sr", "AccountResource:reagent_evolverarity_vr", "AccountResource:reagent_people", "AccountResource:reagent_promotion_heroes", "AccountResource:reagent_promotion_survivors", "AccountResource:reagent_promotion_traps", "AccountResource:reagent_promotion_weapons", "AccountResource:reagent_traps", "AccountResource:reagent_weapons", "AccountResource:schematicxp"]

# Start a new requests session.
session = requests.Session()

# Error with a custom message.
def customError(text):
    input(f"ERROR: {text}\n\nPress ENTER to close the program.\n")
    exit()

# Error for invalid config values.
def configError(key, value, validValues): customError(f"You set the wrong {key} value in config.ini ({value}). Valid values: {validValues}. Please change it and run this program again.")

# Input loop until it's one of the correct values.
def validInput(text, values):
    response = input(f"{text}\n")
    print()
    while True:
        if response in values: break
        response = input("You priovided a wrong value. Please input it again.\n")
        print()
    return response

# Get the text from a request and check for errors.
def requestText(request, bCheckForErrors):
    requestText = json.loads(request.text)
    if ((bCheckForErrors) and ("errorMessage" in requestText)): customError(requestText['errorMessage'])
    return requestText

# Send token request.
def reqToken(loginLink):
    webbrowser.open_new_tab(loginLink)
    print(f"If the program didnt open it, copy this link to your browser: {(loginLink)}\n")
    reqTokenText = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "authorization_code", "code": input("Insert the auth code:\n")}), True)
    return reqTokenText

# Create and/or read the config.ini file.
config = ConfigParser()
configPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "config.ini")
if not os.path.exists(configPath):
    print("Starting to generate the config.ini file.\n")
    bStartSetup = validInput("Type 1 if you want to start the config setup and press ENTER.\nType 2 if you want to use the default config values and press ENTER.", ["1", "2"])
    if bStartSetup == "1":
        iAuthorization_Type = validInput("Which authentication method do you want the program to use?\nToken auth metod generates a refresh token to log in. After 23 days of not using this program this token will expire and you will have to regenerate the auth file.\nDevice auth method generates authorization credentials that don't have an expiration date, but can after some time cause epic to ask you to change your password.\nValid vaules: token, device.", ["token", "device"])
        iSpend_Research_Points = validInput("Do you want to automatically spend your Research Points whenever the program is unable to collect them because of their max accumulation?\nThe \"lowest\" method makes the program search for a Research stat with the lowest level.\nThe \"everyten\" method makes the program search for the closest Research stat to a full decimal level, e.g. level 10, 20, 40, etc.\nValid vaules: off, lowest, everyten.", ["off", "lowest", "everyten"])
        iOpen_Free_Llamas = validInput("Do you want the program to search for free Llamas and open them if they are avaiable?\nValid vaules: true, false.", ["true", "false"])
        bAutomaticRecycle = validInput("Do you want to Automatically recycle unwanted free Llama loot?\nValid vaules: true, false.", ["true", "false"])
        if bAutomaticRecycle == "false": iRecycle_Weapons = iRecycle_Traps = iRetire_Survivors = iRetire_Defenders = iRetire_Heroes = "off"
        else:
            iList = []
            itemTypeJson = {"Recycle_Weapons": {"name": "Weapon Schematics", "recycleWord": "recycle"}, "Recycle_Traps": {"name": "Trap Schematics", "recycleWord": "recycle"}, "Recycle_Survivors": {"name": "Survivors", "recycleWord": "retire"}, "Recycle_Defenders": {"name": "Defenders", "recycleWord": "retire"}, "Recycle_Heroes": {"name": "Heroes", "recycleWord": "retire"}}
            for itemType in itemTypeJson: iList.append(validInput(f"Input the rarity of {itemTypeJson[itemType]['name']} you want the program to automatically {itemTypeJson[itemType]['recycleWord']} at it or below.\nValid values: off, common, uncommon, rare, epic.", ["off", "common", "uncommon", "rare", "epic"]))
            iRecycle_Weapons, iRecycle_Traps, iRetire_Survivors, iRetire_Defenders, iRetire_Heroes = iList  
    else: iAuthorization_Type, iSpend_Research_Points, iOpen_Free_Llamas, iRecycle_Weapons, iRecycle_Traps, iRetire_Survivors, iRetire_Defenders, iRetire_Heroes = ["token", "lowest", "true", "uncommon", "uncommon", "rare", "rare", "uncommon"]           
    with open(configPath, "w") as configFile: configFile.write(f"[StW_Claimer_Config]\n\n# Which authentication method do you want the program to use?\n# Token auth metod generates a refresh token to log in. After 23 days of not using this program this token will expire and you will have to regenerate the auth file.\n# Device auth method generates authorization credentials that don't have an expiration date, but can after some time cause epic to ask you to change your password.\n# Valid vaules: token, device.\nAuthorization_Type = {iAuthorization_Type}\n\n# Do you want to automatically spend your Research Points whenever the program is unable to collect them because of their max accumulation?\n# The \"lowest\" method makes the program search for a Research stat with the lowest level.\n# The \"everyten\" method makes the program search for the closest Research stat to a full decimal level, e.g. level 10, 20, 40, etc.\n# Valid vaules: off, lowest, everyten.\nSpend_Research_Points = {iSpend_Research_Points}\n\n# Do you want the program to search for free Llamas and open them if they are avaiable?\n# Valid vaules: true, false.\nOpen_Free_Llamas = {iOpen_Free_Llamas}\n\n[Automatic_Recycle/Retire]\n\n# Automatically recycle Weapon schematics at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRecycle_Weapons = {iRecycle_Weapons}\n\n# Automatically recycle Trap schematics at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRecycle_Traps = {iRecycle_Traps}\n\n# Automatically retire Survivors at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRetire_Survivors = {iRetire_Survivors}\n\n# Automatically retire Defenders at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRetire_Defenders = {iRetire_Defenders}\n\n# Automatically retire Heroes at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRetire_Heroes = {iRetire_Heroes}\n\n[Config_Version]\n\nVersion = STWC_{configVersion}")
    print("The config.ini file was generated successfully.\n")
try:
    config.read(configPath)
    configVer, authType, spendAutoResearch, bOpenFreeLlamas = [config['Config_Version']['Version'], config['StW_Claimer_Config']['Authorization_Type'].lower(), config['StW_Claimer_Config']['Spend_Research_Points'].lower(), config['StW_Claimer_Config']['Open_Free_Llamas'].lower()]
    autoRecycling.itemRarities = {"weapon": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Recycle_Weapons'].lower()].split(", "), "trap": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Recycle_Traps'].lower()].split(", "), "survivor": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Retire_Survivors'].lower()].split(", "), "defender": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Retire_Defenders'].lower()].split(", "), "hero": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Retire_Heroes'].lower()].split(", ")}
except: customError("The program is unable to read the config.ini file. Delete the config.ini file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")
if not (configVer == f"STWC_{configVersion}"): customError("The config file is outdated. Delete the config.ini file and run this program again to generate a new one.")
checkValuesJson = {"Authorization_Type": {"value": authType, "validValues": ["token", "device"]}, "Spend_Research_Points": {"value": spendAutoResearch, "validValues": ["off", "lowest", "everyten"]}, "Open_Free_Llamas": {"value": bOpenFreeLlamas, "validValues": ["true", "false"]}}
for option in checkValuesJson:
    if not (checkValuesJson[option]['value'] in checkValuesJson[option]['validValues']): configError(option, checkValuesJson[option]['value'], ", ".join(checkValuesJson[option]['validValues']))
recycleOptions = ["Recycle_Weapons", "Recycle_Traps", "Retire_Survivors", "Retire_Defenders", "Retire_Heroes"]
recycleOn = False
for key in recycleOptions:
    keyValue = config['Automatic_Recycle/Retire'][f'{key}'].lower()
    if not (keyValue == "off"): recycleOn == True
    if not (keyValue in ("off", "common", "uncommon", "rare", "epic")): configError(key, keyValue, "off, common, uncommon, rare, epic")

# Create and/or read the auth.json file.
authPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "auth.json")
if not os.path.exists(authPath):
    isLoggedIn = validInput("Starting to generate the auth.json file.\n\nAre you logged into your Epic account that you would like the program to use in your browser?\nType 1 if yes and press ENTER.\nType 2 if no and press ENTER.\n", ["1", "2"])
    input("The program is going to open an Epic Games webpage.\nTo continue, press ENTER.\n")
    if isLoggedIn == "1": loginLink = links.loginLink1
    else: loginLink = links.loginLink2
    if authType == "token":
        reqTokenText = reqToken(loginLink.format("34a02cf8f4414e29b15921876da36f9a"))
        refreshToken, accountId, expirationDate = [reqTokenText["refresh_token"], reqTokenText["account_id"], reqTokenText["refresh_expires_at"]]
        with open(authPath, "w") as authFile: json.dump({"WARNING": "Don't show anyone the contents of this file, because it contains information with which the program logs into the account.", "authType": "token", "refreshToken": refreshToken, "accountId": accountId, "refresh_expires_at": expirationDate}, authFile, indent = 2)
    else:
        reqTokenText = reqToken(loginLink.format("3446cd72694c4a4485d81b77adbb2141"))
        accessToken, accountId = [reqTokenText["access_token"], reqTokenText["account_id"]]
        reqDeviceAuthText = requestText(session.post(links.getDeviceAuth.format(accountId), headers={"Authorization": f"bearer {accessToken}"}, data={}), True)
        deviceId, secret = [reqDeviceAuthText["deviceId"], reqDeviceAuthText["secret"]]
        with open(authPath, "w") as authFile: json.dump({"WARNING": "Don't show anyone the contents of this file, because it contains information with which the program logs into the account.", "authType": "device",  "deviceId": deviceId, "accountId": accountId, "secret": secret}, authFile, indent = 2)
    print("\nThe auth.json file was generated successfully.\n")
try:
    getAuthJson = json.loads(open(authPath, "r").read())
    if authType == "token":
        expirationDate, refreshToken = [getAuthJson["refresh_expires_at"], getAuthJson["refreshToken"]]
        if getAuthJson["authType"] == "device": customError("The authorization type in config is set to token, but the auth.json file contains device auth credentials.\nDelete the auth.json file and run this program again to generate a token one or change authorization type back to device in config.ini.")
        if expirationDate < datetime.now().isoformat(): customError("The refresh token has expired. Delete the auth.json file and run this program again to generate a new one.")
    if authType == "device":
        deviceId, secret = [getAuthJson["deviceId"], getAuthJson["secret"]]
        if getAuthJson["authType"] == "token": customError("The authorization type in config is set to device, but the auth.json file contains token auth credentials.\nDelete the auth.json file and run this program again to generate a device one or change authorization type back to token in config.ini.")
    accountId = getAuthJson["accountId"]
except:
    customError("The program is unable to read the auth.json file. Delete the auth.json file and run this program again to generate a new one.")

# Load the stringlist.json file.
stringListPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "stringlist.json")
if not os.path.exists(stringListPath): customError("The stringlist.json file doesn't exist. Get it from this program's repository on Github, add it back and run this program again.")
try: getStringList = json.loads(open(stringListPath, "r").read())
except: customError("The program is unable to read the stringlist.json file. Delete the stringlist.json file, download it from this program's repository on Github, add it back here and run this program again.")

# Log in.
if authType == "token": # Shoutout to BayGamerYT for telling me about this login method.
    reqRefreshTokenText = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "refresh_token", "refresh_token": refreshToken}), True)
    with open(authPath, "r") as getAuthFile: authFile = json.loads(getAuthFile.read())
    authFile['refreshToken'], authFile['refresh_expires_at'] = [reqRefreshTokenText["refresh_token"], reqRefreshTokenText["refresh_expires_at"]]
    with open(authPath, "w") as getAuthFile: json.dump(authFile, getAuthFile, indent = 2)
    reqExchangeText = requestText(session.get(links.getOAuth.format("exchange"), headers={"Authorization": f"bearer {reqRefreshTokenText['access_token']}"}, data={"grant_type": "authorization_code"}), True)
    reqTokenText = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "exchange_code", "exchange_code": reqExchangeText["code"], "token_type": "eg1"}), True)
if authType == "device": reqTokenText = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "device_auth", "device_id": deviceId, "account_id": accountId, "secret": secret, "token_type": "eg1"}), True)
accessToken, displayName = [reqTokenText['access_token'], reqTokenText['displayName']]
print(f"Logged in as {displayName}.\n")

# Headers for MCP requests.
headers = {"Authorization": f"bearer {accessToken}", "Content-Type": "application/json"}

# Check whether the account has the campaign access token and founder's token.
# The founder's token is not required, but instead of V-Bucks the account will recieve X-Ray Tickets.
reqCheckTokensText = json.dumps(requestText(session.post(links.profileRequest.format(accountId, "QueryProfile", "common_core"), headers=headers, data="{}"), False))
bCampaignAccess = False
bFounder = False
if "Token:campaignaccess" in reqCheckTokensText: bCampaignAccess = True
if "Token:founderspack" in reqCheckTokensText: bFounder = True
if not bCampaignAccess: customError(f"{displayName} doesn't have access to Save the World.")

# Claim the Daily Reward.
reqClaimDailyRewardText = requestText(session.post(links.profileRequest.format(accountId, "ClaimLoginReward", "campaign"), headers=headers, data="{}"), True)
cdrItems, cdrDaysLoggedIn = [reqClaimDailyRewardText['notifications'][0]['items'], reqClaimDailyRewardText['notifications'][0]['daysLoggedIn']]
cdrDaysModified = int(cdrDaysLoggedIn) % 336 # Credit to dippyshere for this and the next line of code.
if cdrDaysModified == 0: cdrDaysModified = 336
if not cdrItems: print(f"The daily reward for {displayName} has been already claimed today!")
else: print(f"Today's daily reward for {displayName} has been successfully claimed!")
reward = getStringList['Daily Rewards'][f'{cdrDaysModified}']
if (("V-Bucks" in reward) and (not bFounder)): reward = reward.replace("V-Bucks", "X-Ray Tickets")
print(f"Day: {cdrDaysLoggedIn}\nReward: {reward}\n")

# Claim and automatically spend the Research Points.
reqCampaignProfileCheckText = requestText(session.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}"), True)
reqCampaignProfileCheckResearchLevels = reqCampaignProfileCheckText['profileChanges'][0]['profile']['stats']['attributes']['research_levels']
if (reqCampaignProfileCheckResearchLevels['fortitude'] == 120 and reqCampaignProfileCheckResearchLevels['offense'] == 120 and reqCampaignProfileCheckResearchLevels['resistance'] == 120 and reqCampaignProfileCheckResearchLevels['technology'] == 120): print(f"Skipping Research Points claiming because {displayName} has max F.O.R.T. stats.\n")
else:
    reqCampaignProfileCheckItems = reqCampaignProfileCheckText['profileChanges'][0]['profile']['items']
    for key in reqCampaignProfileCheckItems: # Credit to Lawin for helping me figuring out how to write this and the next line of code.
        if reqCampaignProfileCheckItems[key]['templateId'] == "CollectedResource:Token_collectionresource_nodegatetoken01":
            tokenToClaim = key
            break
    reqClaimCollectedResourcesText = requestText(session.post(links.profileRequest.format(accountId, "ClaimCollectedResources", "campaign"), headers=headers, json={"collectorsToClaim": [tokenToClaim]}), False)
    if "errorMessage" in reqClaimCollectedResourcesText: print(f"ERROR: {reqClaimCollectedResourcesText['errorMessage']}\n") # Error without exit()
    else:
        storedMaxPoints = False
        try:
            totalItemGuid, rpToClaim = [reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['itemGuid'], reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][tokenToClaim]['attributes']['stored_value']]
            rpStored, rpClaimedQuantity = [reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][totalItemGuid]['quantity'], int(reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['quantity'])]
            if float(rpToClaim) >= 1: storedMaxPoints = True
            pointsWord = "Points"
            if rpClaimedQuantity == 1: pointsWord = "Point"
            print(f"Claimed {rpClaimedQuantity} Research {pointsWord}. Total Research Points: {reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity']}\n")
        except:
            for key in reqCampaignProfileCheckItems:
                if reqCampaignProfileCheckItems[key]['templateId'] == "Token:collectionresource_nodegatetoken01":
                    totalItemGuid = key
                    break
            rpToClaim, rpStored, storedMaxPoints = [reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{tokenToClaim}']['attributes']['stored_value'], reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity'], True]
            if int(rpToClaim) < 1:
                storedMaxPoints = False
                print(f"The program is unable to claim {round(rpToClaim, 2)} Research Point because in order to collect it, at least 1 point must be available for claiming. In other words, just wait a few seconds and run this program again.\n")
        if storedMaxPoints == True:
            if spendAutoResearch == "off": print(f"The program is unable to claim {round(rpToClaim, 2)} Research Points because you have the maximum number of accumulated Research Points at once ({rpStored}).\nIn this situation if you want to automatically spend them, change the Spend_Research_Points value in config.ini to lowest or everyten and run this program again.\n")
            else:
                print(f"You have the maximum number of accumulated Research Points at once ({rpStored}).\nStarting to automatically spend Research Points...\n")
                while True:
                    reqFORTLevelsCheckText = requestText(session.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}"), True)['profileChanges'][0]['profile']['stats']['attributes']['research_levels']
                    if spendAutoResearch == "lowest":
                        levelsList = [int(reqFORTLevelsCheckText['fortitude']), int(reqFORTLevelsCheckText['offense']), int(reqFORTLevelsCheckText['resistance']), int(reqFORTLevelsCheckText['technology'])]
                        level = min(levelsList)
                    elif spendAutoResearch == "everyten":
                        levelsList, levelsJson = [[int(reqFORTLevelsCheckText['fortitude']) % 10, int(reqFORTLevelsCheckText['offense']) % 10, int(reqFORTLevelsCheckText['resistance']) % 10, int(reqFORTLevelsCheckText['technology']) % 10], {int(reqFORTLevelsCheckText['fortitude']) % 10: int(reqFORTLevelsCheckText['fortitude']), int(reqFORTLevelsCheckText['offense']) % 10: int(reqFORTLevelsCheckText['offense']), int(reqFORTLevelsCheckText['resistance']) % 10: int(reqFORTLevelsCheckText['resistance']), int(reqFORTLevelsCheckText['technology']) % 10: int(reqFORTLevelsCheckText['technology'])}]
                        level = levelsJson[max(levelsList)]
                    for key in reqFORTLevelsCheckText:
                        if reqFORTLevelsCheckText[key] == int(level):
                            statToClaim = key
                            break
                    reqPurchaseResearchStatUpgradeText = requestText(session.post(links.profileRequest.format(accountId, "PurchaseResearchStatUpgrade", "campaign"), headers=headers, json={"statId": f'{statToClaim}'}), False)
                    if "errorMessage" in reqPurchaseResearchStatUpgradeText: break # Error without exit()
                    else: print(f"Bought 1 {statToClaim.capitalize()} level. New level: {reqPurchaseResearchStatUpgradeText['profileChanges'][0]['profile']['stats']['attributes']['research_levels'][statToClaim]}.")
                print("\nCannot buy more F.O.R.T. levels.\n")
                reqClaimCollectedResourcesText = requestText(session.post(links.profileRequest.format(accountId, "ClaimCollectedResources", "campaign"), headers=headers, json={"collectorsToClaim": [tokenToClaim]}), True)
                try:
                    totalItemGuid = reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['itemGuid']
                    print(f"Claimed {reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['quantity']} Research Points. Total Research Points: {reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][totalItemGuid]['quantity']}\n")
                except: []

# Search for a free Llama and open it if available.
alreadyOpenedFreeLlamas, freeLlamasCount, cpspStorefront = [0, 0, []]
if bOpenFreeLlamas == "true":
    reqGetStorefrontText = requestText(session.get(links.getStorefront, headers=headers, data={}), True)['storefronts']
    for key in reqGetStorefrontText:
        if key['name'] == "CardPackStorePreroll":
            cpspStorefront = key['catalogEntries']
            break
    if not cpspStorefront: print("ERROR: Failed to find the Llama shop. Is it even possible? Maybe a new Fortnite update could break it, but it's very unlikely...\n")
    else:
        freeLlamas = []
        for key in cpspStorefront:
            if (not "always" in key['devName'].lower()) and (key['prices'][0]['finalPrice'] == 0): freeLlamas.append(key)
        freeLlamasCount = len(freeLlamas)
        if not freeLlamas: print("There are no free Llamas available at the moment.\n")
        else:
            print(f"There are free llamas avaiable!")
            itemsfromLlamas, openedLlamas = [[], 0]
            for llama in freeLlamas:
                llamaToClaimOfferId = llama['offerId']
                try: llamaToClaimTitle = llama['title']
                except: llamaToClaimTitle = []
                llamaToClaimCPId = llama['itemGrants'][0]['templateId']
                if llamaToClaimTitle: llamaToClaimName = llamaToClaimTitle
                else:
                    try: llamaToClaimName = getStringList['Llama names'][llamaToClaimCPId]
                    except: llamaToClaimName = llamaToClaimCPId
                while True:
                    reqPopulateLlamasText = requestText(session.post(links.profileRequest.format(accountId, "PopulatePrerolledOffers", "campaign"), headers=headers, data="{}"), True)
                    llamaTier = []
                    for key in reqPopulateLlamasText['profileChanges'][0]['profile']['items']:
                        if (reqPopulateLlamasText['profileChanges'][0]['profile']['items'][key]['templateId'].lower().startswith("prerolldata") and reqPopulateLlamasText['profileChanges'][0]['profile']['items'][key]['attributes']['offerId'] == llamaToClaimOfferId):
                            llamaTier = reqPopulateLlamasText['profileChanges'][0]['profile']['items'][key]['attributes']['highest_rarity']
                            llamaTier = getStringList['Llama tiers'][f'{llamaTier}']
                    reqBuyFreeLlamaText = requestText(session.post(links.profileRequest.format(accountId, "PurchaseCatalogEntry", "common_core"), headers=headers, json={"offerId": llamaToClaimOfferId, "purchaseQuantity": 1, "currency": "MtxCurrency", "currencySubType": "", "expectedTotalPrice": 0, "gameContext": "Frontend.None"}), False)
                    if "errorMessage" in reqBuyFreeLlamaText:
                        if "limit of" in reqBuyFreeLlamaText['errorMessage']:
                            if openedLlamas == 0: alreadyOpenedFreeLlamas += 1
                        break
                    else:
                        print(f"\nOpening: {llamaToClaimName}\nTier: {llamaTier}\nLoot result:")
                        llamaLoot, llamaLootCount = [reqBuyFreeLlamaText['notifications'][0]['lootResult']['items'], 0]
                        openedLlamas += 1
                        for key in llamaLoot:
                            templateId, itemGuid, itemQuantity = [key['itemType'], key['itemGuid'], key['quantity']]
                            try: itemName = getStringList['Items'][templateId]['name']
                            except: itemName = templateId
                            itemRarity, itemType = [getStringList['Items'][templateId]['rarity'], getStringList['Items'][templateId]['type']]
                            llamaLootCount += 1
                            if itemRarity in ("common", "uncommon", "rare", "epic"): itemsfromLlamas.append({"itemName": itemName, "itemType": itemType, "templateId": templateId, "itemGuid": itemGuid, "itemRarity": itemRarity, "itemQuantity": itemQuantity})
                            print(f"{llamaLootCount}: {itemQuantity}x {itemName}")
            if int(alreadyOpenedFreeLlamas) == freeLlamasCount:
                print(f"\nFree Llamas that are currently avaiable in the shop have been already opened on this account. Remember that you can open a maximum of 2 free one hour rotation Llamas per one shop rotation.\n")
            else:
                llamasWord = "Llamas"
                if int(openedLlamas) == 1: llamasWord = "Llama"
                print(f"\nSuccesfully opened {openedLlamas} free {llamasWord}.\n")

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
        print(f"Recycling/Retiring selected items from {openedLlamas} free {llamasWord}...\n")
        reqGetResourcesText = requestText(session.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}"), True)
        for resource in autoRecycling.recycleResources:
            for item in reqGetResourcesText['profileChanges'][0]['profile']['items']:
                if reqGetResourcesText['profileChanges'][0]['profile']['items'][item]['templateId'] == resource: recycleResources.append({"itemGuid": item, "templateId": resource, "itemName": getStringList['Items'][resource]['name'], "quantity": reqGetResourcesText['profileChanges'][0]['profile']['items'][item]['quantity']})
        reqRecycleItemsText = requestText(session.post(links.profileRequest.format(accountId, "RecycleItemBatch", "campaign"), headers=headers, json={"targetItemIds": itemGuidsToRecycle}), True)
        print("The following items have been succesfully Recycled/Retired:")
        for item in itemsToRecycle:
            recycledItemsCount += 1
            print(f"{recycledItemsCount}: {item['itemQuantity']}x {item['itemName']}")
        reqGetResources2Text = requestText(session.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}"), True)
        print("\nResources received:")
        for resource in recycleResources:
            resourceQuantity = int(reqGetResources2Text['profileChanges'][0]['profile']['items'][resource['itemGuid']]['quantity']) - int(resource['quantity'])
            if resourceQuantity > 0:
                recycleResourcesCount += 1
                print(f"{recycleResourcesCount}: {resourceQuantity}x {resource['itemName']}. Total amount: {reqGetResources2Text['profileChanges'][0]['profile']['items'][resource['itemGuid']]['quantity']}")
        print() # Extra newline

input("Press ENTER to close the program.\n")
exit()