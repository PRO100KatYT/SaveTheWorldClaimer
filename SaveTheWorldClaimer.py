print("Fortnite StW Daily Reward & Research Points claimer v1.4.0 by PRO100KatYT\n")
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
    rarities = {"off": "nic", "common": "common", "uncommon": "common, uncommon", "rare": "common, uncommon, rare", "epic": "common, uncommon, rare, epic"}
    itemRarities = ""
    recycleResources = ["AccountResource:heroxp", "AccountResource:personnelxp", "AccountResource:phoenixxp", "AccountResource:phoenixxp_reward", "AccountResource:reagent_alteration_ele_fire", "AccountResource:reagent_alteration_ele_nature", "AccountResource:reagent_alteration_ele_water", "AccountResource:reagent_alteration_gameplay_generic", "AccountResource:reagent_alteration_generic", "AccountResource:reagent_alteration_upgrade_r", "AccountResource:reagent_alteration_upgrade_sr", "AccountResource:reagent_alteration_upgrade_uc", "AccountResource:reagent_alteration_upgrade_vr", "AccountResource:reagent_c_t01", "AccountResource:reagent_c_t02", "AccountResource:reagent_c_t03", "AccountResource:reagent_c_t04", "AccountResource:reagent_evolverarity_r", "AccountResource:reagent_evolverarity_sr", "AccountResource:reagent_evolverarity_vr", "AccountResource:reagent_people", "AccountResource:reagent_promotion_heroes", "AccountResource:reagent_promotion_survivors", "AccountResource:reagent_promotion_traps", "AccountResource:reagent_promotion_weapons", "AccountResource:reagent_traps", "AccountResource:reagent_weapons", "AccountResource:schematicxp"]

# Creating and/or reading the config.ini file.
config = ConfigParser()
configPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "config.ini")
if not os.path.exists(configPath):
    print("Starting to generate the config.ini file.\n")
    configFile = open(configPath, "a")
    configFile.write("[StW_Claimer_Config]\n\n# Which authentication method do you want the program to use? Valid vaules: token, device.\n# Token auth metod generates a refresh token to log in. After 23 days of not using this program this token will expire and you will have to regenerate the auth file.\n# Device auth method generates authorization credentials that don't have an expiration date, but can after some time cause epic to ask you to change your password.\nAuthorization_Type = token\n\n# Do you want to automatically spend your Research Points whenever the program is unable to collect them because of their max accumulation? Valid vaules: true, false.\nSpend_Research_Points = true\n\n# Do you want the program to search for free Llamas and open them if they are avaiable? Valid vaules: true, false.\nOpen_Free_Llamas = true\n\n[Automatic_Recycle/Retire]\n\n# Automatically recycle Weapon schematics at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRecycle_Weapons = off\n\n# Automatically recycle Trap schematics at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRecycle_Traps = off\n\n# Automatically retire Survivors at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRetire_Survivors = off\n\n# Automatically retire Defenders at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRetire_Defenders = off\n\n# Automatically retire Heroes at this rarity or below.\n# Valid values: off, common, uncommon, rare, epic.\nRetire_Heroes = off\n\n[Config_Version]\n\nVersion = STWC_1.4.0")
    configFile.close()
    print("The config.ini file was generated successfully.\n")
try:
    getConfigIni = config.read(configPath)
    configVer = config['Config_Version']['Version']
    authType = config['StW_Claimer_Config']['Authorization_Type'].lower()
    bSpendAutoResearch = config['StW_Claimer_Config']['Spend_Research_Points'].lower()
    bOpenFreeLlamas = config['StW_Claimer_Config']['Open_Free_Llamas'].lower()
    autoRecycling.itemRarities = {"weapon": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Recycle_Weapons'].lower()].split(", "), "trap": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Recycle_Traps'].lower()].split(", "), "survivor": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Retire_Survivors'].lower()].split(", "), "defender": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Retire_Defenders'].lower()].split(", "), "hero": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Retire_Heroes'].lower()].split(", ")}
except:
    input("ERROR: The program is unable to read the config.ini file. Delete the config.ini file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")
    exit()
if not (configVer == "STWC_1.4.0"):
    input("ERROR: The config file is outdated. Delete the config.ini file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")
    exit()
if not (authType == "token" or authType == "device"):
    input(f"ERROR: You set the wrong \"Authorization_Type\" value in config.ini ({authType}). Valid values: token, device. Change it and run this program again.\n\nPress ENTER to close the program.\n")
    exit()
boolOptions = ["Spend_Research_Points", "Open_Free_Llamas"]
for key in boolOptions:
    keyValue = config['StW_Claimer_Config'][f'{key}'].lower()
    if not (keyValue in ("true", "false")):
        input(f"ERROR: You set the wrong {key} value in config.ini ({keyValue}). Valid values: true, false. Change it and run this program again.\n\nPress ENTER to close the program.\n")
        exit()
recycleOptions = ["Recycle_Weapons", "Recycle_Traps", "Retire_Survivors", "Retire_Defenders", "Retire_Heroes"]
recycleOn = 0
for key in recycleOptions:
    keyValue = config['Automatic_Recycle/Retire'][f'{key}'].lower()
    if not (keyValue == "off"): recycleOn += 1
    if not (keyValue in ("off", "common", "uncommon", "rare", "epic")):
        input(f"ERROR: You set the wrong {key} value in config.ini ({keyValue}). Valid values: off, common, uncommon, rare, epic. Change it and run this program again.\n\nPress ENTER to close the program.\n")
        exit()

# Creating and/or reading the auth.json file.
authPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "auth.json")
if not os.path.exists(authPath):
    isLoggedIn = input("Starting to generate the auth.json file.\n\nAre you logged into your Epic account that you would like the program to use in your browser?\nType 1 if yes and press ENTER.\nType 2 if no and press ENTER.\n")
    while True:
        if (isLoggedIn == "1" or isLoggedIn == "2"): break
        else: isLoggedIn = input("\nYou priovided a wrong value. Please input it again.\n")
    input("\nThe program is going to open an Epic Games webpage.\nTo continue, press ENTER.\n")
    if isLoggedIn == "1": loginLink = links.loginLink1
    else: loginLink = links.loginLink2
    if authType == "token":
        loginLink = loginLink.format("34a02cf8f4414e29b15921876da36f9a")
        webbrowser.open_new_tab(loginLink)
        print(f"If the program didnt open it, copy this link to your browser: {(loginLink)}\n")
        reqToken = requests.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "authorization_code", "code": input("Insert the auth code:\n")})
        reqTokenText = json.loads(reqToken.text)
        if "errorMessage" in reqTokenText:
            input(f"\nERROR: {reqTokenText['errorMessage']}\n\nPress ENTER to close the program.\n") 
            exit()
        else:
            refreshToken = reqTokenText["refresh_token"]
            accountId = reqTokenText["account_id"]
            expirationDate = reqTokenText["refresh_expires_at"]
            jsontosave = {"WARNING": "Don't show anyone the contents of this file, because it contains information with which the program logs into the account.", "authType": "token", "refreshToken": refreshToken, "accountId": accountId, "refresh_expires_at": expirationDate}
            json.dump(jsontosave, open(authPath, "w"), indent = 2)
    if authType == "device":
        loginLink = loginLink.format("3446cd72694c4a4485d81b77adbb2141")
        webbrowser.open_new_tab(loginLink)
        print(f"If the program didnt open it, copy this link to your browser: {loginLink}\n")
        reqToken = requests.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "authorization_code", "code": input("Insert the auth code:\n")})
        reqTokenText = json.loads(reqToken.text)
        if "errorMessage" in reqTokenText:
            input(f"\nERROR: {reqTokenText['errorMessage']}\n\nPress ENTER to close the program.\n") 
            exit()
        else:
            accessToken = reqTokenText["access_token"]
            accountId = reqTokenText["account_id"]
        reqDeviceAuth = requests.post(links.getDeviceAuth.format(accountId), headers={"Authorization": f"bearer {accessToken}"}, data={})
        reqDeviceAuthText = json.loads(reqDeviceAuth.text)
        if "errorMessage" in reqDeviceAuthText:
            input(f"\nERROR: {reqDeviceAuthText['errorMessage']}\n\nPress ENTER to close the program.\n") 
            exit()
        else:
            deviceId = reqDeviceAuthText["deviceId"]
            secret = reqDeviceAuthText["secret"]
            jsontosave = {"WARNING": "Don't show anyone the contents of this file, because it contains information with which the program logs into the account.", "authType": "device",  "deviceId": deviceId, "accountId": accountId, "secret": secret}
            json.dump(jsontosave, open(authPath, "w"), indent = 2)
    print("\nThe auth.json file was generated successfully.\n")
try:
    getAuthJson = json.loads(open(authPath, "r").read())
    if authType == "token":
        if getAuthJson["authType"] == "device":
            input("The authorization type in config is set to token, but the auth.json file contains device auth credentials.\nDelete the auth.json file and run this program again to generate a token one or change authorization type back to device in config.ini.\n\nPress ENTER to close the program.\n")
            exit = 1
        expirationDate = getAuthJson["refresh_expires_at"]
        if expirationDate < datetime.now().isoformat():
            input("The refresh token has expired. Delete the auth.json file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")
            exit = 1
        refreshToken = getAuthJson["refreshToken"]
    if authType == "device":
        if getAuthJson["authType"] == "token":
            input("The authorization type in config is set to device, but the auth.json file contains token auth credentials.\nDelete the auth.json file and run this program again to generate a device one or change authorization type back to token in config.ini.\n\nPress ENTER to close the program.\n")
            exit = 1
        deviceId = getAuthJson["deviceId"]
        secret = getAuthJson["secret"]
    accountId = getAuthJson["accountId"]
except:
    if exit == 1: exit()
    input("ERROR: The program is unable to read the auth.json file. Delete the auth.json file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")
    exit()
if exit == 1: exit()

stringListPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "stringlist.json")
if not os.path.exists(stringListPath):
    input("ERROR: The stringlist.json file doesn't exist. Get it from this program's repository on Github, add it back and run this program again.\n\nPress ENTER to close the program.\n")
    exit()
try: getStringList = json.loads(open(stringListPath, "r").read())
except:
    input("ERROR: The program is unable to read the stringlist.json file. Delete the stringlist.json file, download it from this program's repository on Github, add it back here and run this program again.\n\nPress ENTER to close the program.\n")
    exit()

# Logging in.
if authType == "token": # Shoutout to BayGamerYT for telling me about this login method.
    reqRefreshToken = requests.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "refresh_token", "refresh_token": refreshToken})
    reqRefreshTokenText = json.loads(reqRefreshToken.text)
    if "errorMessage" in reqRefreshTokenText:
        input(f"ERROR: At least one variable in the auth.json file is no longer valid. Delete the auth.json file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n") 
        exit()
    getAuthFile = open(authPath, "r").read()
    authReplaceToken = getAuthFile.replace(refreshToken, reqRefreshTokenText["refresh_token"])
    authReplaceDate = authReplaceToken.replace(expirationDate, reqRefreshTokenText["refresh_expires_at"])
    authFile = open(authPath, "w")
    authFile.write(authReplaceDate)
    authFile.close()
    accessToken = reqRefreshTokenText["access_token"]
    reqExchange = requests.get(links.getOAuth.format("exchange"), headers={"Authorization": f"bearer {accessToken}"}, data={"grant_type": "authorization_code"})
    reqExchangeText = json.loads(reqExchange.text)
    exchangeCode = reqExchangeText["code"]
    reqToken = requests.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "exchange_code", "exchange_code": exchangeCode, "token_type": "eg1"})
if authType == "device":
    reqToken = requests.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "device_auth", "device_id": deviceId, "account_id": accountId, "secret": secret, "token_type": "eg1"})
reqTokenText = json.loads(reqToken.text)
if "errorMessage" in reqTokenText:
    input(f"ERROR: At least one variable in the auth.json file is no longer valid. Delete the auth.json file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n") 
    exit()
accessToken = reqTokenText['access_token']
displayName = reqTokenText['displayName']
print(f"Logged in as {displayName}.\n")

headers = {"Authorization": f"bearer {accessToken}", "Content-Type": "application/json"}

# Checking whether the account has the campaign access token and founder's token. The founder's token is not required, but instead of V-Bucks the account will recieve X-Ray Tickets.
reqCommonCoreProfileCheck = requests.post(links.profileRequest.format(accountId, "QueryProfile", "common_core"), headers=headers, data="{}")
bCampaignAccess = 0
bFounder = 0
if "Token:campaignaccess" in reqCommonCoreProfileCheck.text: bCampaignAccess = 1
if "Token:founderspack" in reqCommonCoreProfileCheck.text: bFounder = 1
if bCampaignAccess == 0:
    input(f"ERROR: {displayName} doesn't have access to Save the World.\n\nPress ENTER to close the program.\n")
    exit()

# Claiming the Daily Reward.
print("Claiming the Daily Reward...\n")
reqClaimDailyReward = requests.post(links.profileRequest.format(accountId, "ClaimLoginReward", "campaign"), headers=headers, data="{}")
reqClaimDailyRewardText = json.loads(reqClaimDailyReward.text)
if "errorMessage" in reqClaimDailyRewardText:
    input(f"ERROR: {reqClaimDailyRewardText['errorMessage']}\n\nPress ENTER to close the program.\n")
    exit()
cdrItems = reqClaimDailyRewardText['notifications'][0]['items']
cdrDaysLoggedIn = reqClaimDailyRewardText['notifications'][0]['daysLoggedIn']
cdrDaysModified = int(cdrDaysLoggedIn) % 336 # Credit to dippyshere for this and the next line of code.
if cdrDaysModified == 0: cdrDaysModified = 336
if not cdrItems:
    print(f"The daily reward for {displayName} has been already claimed today!")
else: print(f"Today's daily reward for {displayName} has been successfully claimed!")
reward = getStringList['Daily Rewards'][f'{cdrDaysModified}']
if "V-Bucks" in reward:
    if bFounder == 0: reward = reward.replace("V-Bucks", "X-Ray Tickets")
print(f"Day: {cdrDaysLoggedIn}\nReward: {reward}\n")

# Claiming and automatic spending the Research Points
reqCampaignProfileCheck = requests.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}")
reqCampaignProfileCheckText = json.loads(reqCampaignProfileCheck.text)
reqCampaignProfileCheckResearchLevels = reqCampaignProfileCheckText['profileChanges'][0]['profile']['stats']['attributes']['research_levels']
if (reqCampaignProfileCheckResearchLevels['fortitude'] == 120 and reqCampaignProfileCheckResearchLevels['offense'] == 120 and reqCampaignProfileCheckResearchLevels['resistance'] == 120 and reqCampaignProfileCheckResearchLevels['technology'] == 120):
    print(f"Skipping claiming Research Points because {displayName} has max F.O.R.T. stats.\n")
else: 
    print("Claiming the Research Points...\n")
    reqCampaignProfileCheckItems = reqCampaignProfileCheckText['profileChanges'][0]['profile']['items']
    for key in reqCampaignProfileCheckItems: # Credit to Lawin for helping me figuring out how to write this and the next line of code.
        if reqCampaignProfileCheckItems[f'{key}']['templateId'] == "CollectedResource:Token_collectionresource_nodegatetoken01":
            tokenToClaim = key
            break
    reqClaimCollectedResources = requests.post(links.profileRequest.format(accountId, "ClaimCollectedResources", "campaign"), headers=headers, json={"collectorsToClaim": [f"{tokenToClaim}"]})
    reqClaimCollectedResourcesText = json.loads(reqClaimCollectedResources.text)
    if "errorMessage" in reqClaimCollectedResourcesText:
        print(f"ERROR: {reqClaimCollectedResourcesText['errorMessage']}\n")
    else:
        try:
            totalItemGuid = reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['itemGuid']
            print(f"Claimed {reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['quantity']} Research Points. Total Research Points: {reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity']}\n")
        except:
            for key in reqCampaignProfileCheckItems:
                if reqCampaignProfileCheckItems[f'{key}']['templateId'] == "Token:collectionresource_nodegatetoken01":
                    totalItemGuid = key
                    break
            rpToClaim = reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{tokenToClaim}']['attributes']['stored_value']
            rpStored = reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity']
            if int(rpToClaim) < 1: print(f"The program is unable to claim {rpToClaim} Research Point because in order to collect it, at least 1 point must be available for claiming. In other words, just wait a few seconds and run this program again.\n")
            else:
                if bSpendAutoResearch == "false": print(f"The program is unable to claim {rpToClaim} Research Points because you have the maximum number of accumulated Research Points at once ({rpStored}).\nIn this situation if you want to automatically spend them, change the Spend_Research_Points value in config.ini from false to true and run this program again.\n")
                else:
                    print(f"You have the maximum number of accumulated Research Points at once ({rpStored}).\nStarting to automatically spend Research Points...\n")
                    while True:
                        reqFORTLevelsCheck = requests.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}")
                        reqFORTLevelsCheckText = json.loads(reqFORTLevelsCheck.text)['profileChanges'][0]['profile']['stats']['attributes']['research_levels']
                        levelsList = [int(reqFORTLevelsCheckText['fortitude']), int(reqFORTLevelsCheckText['offense']), int(reqFORTLevelsCheckText['resistance']), int(reqFORTLevelsCheckText['technology'])]
                        lowestLevel = min(levelsList)
                        for key in reqFORTLevelsCheckText:
                            if reqFORTLevelsCheckText[f'{key}'] == int(lowestLevel):
                                statToClaim = key
                                break
                        reqPurchaseResearchStatUpgrade = requests.post(links.profileRequest.format(accountId, "PurchaseResearchStatUpgrade", "campaign"), headers=headers, json={"statId": f'{statToClaim}'})
                        reqPurchaseResearchStatUpgradeText = json.loads(reqPurchaseResearchStatUpgrade.text)
                        if "errorMessage" in reqPurchaseResearchStatUpgradeText: break
                        else: print(f"Bought 1 {statToClaim.capitalize()} level. New level: {reqPurchaseResearchStatUpgradeText['profileChanges'][0]['profile']['stats']['attributes']['research_levels'][f'{statToClaim}']}.")
                    print("\nCannot buy more F.O.R.T. levels. Claiming the Research Points...\n")
                    reqClaimCollectedResources = requests.post(links.profileRequest.format(accountId, "ClaimCollectedResources", "campaign"), headers=headers, json={"collectorsToClaim": [f"{tokenToClaim}"]})
                    reqClaimCollectedResourcesText = json.loads(reqClaimCollectedResources.text)
                    totalItemGuid = reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['itemGuid']
                    print(f"Claimed {reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['quantity']} Research Points. Total Research Points: {reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity']}\n")

# Searching for a free Llama and opening it if available
if bOpenFreeLlamas == "true":
    print("Searching for free Llamas...\n")
    reqGetStorefront = requests.get(links.getStorefront, headers=headers, data={})
    reqGetStorefrontText = json.loads(reqGetStorefront.text)['storefronts']
    for key in reqGetStorefrontText:
        if key['name'] == "CardPackStorePreroll":
            cpspStorefront = key['catalogEntries']
            break
        else: cpspStorefront = []
    if not cpspStorefront: print("ERROR: Failed to find the Llama shop. Is it even possible? Maybe a new Fortnite update could break it, but it's very unlikely...\n")
    else:
        freeLlamas = []
        for key in cpspStorefront:
            if (not "always" in key['devName'].lower()) and (key['prices'][0]['finalPrice'] == 0):
                freeLlamas.append(key)
        freeLlamasCount = len(freeLlamas)
        if not freeLlamas: print("There are no free Llamas available at the moment.\n")
        else:
            print(f"There are free llamas avaiable!")
            itemsfromLlamas = []
            openedLlamas = 0
            alreadyOpenedFreeLlamas = 0
            for llama in freeLlamas:
                llamaToClaimOfferId = llama['offerId']
                try: llamaToClaimTitle = llama['title']
                except: llamaToClaimTitle = []
                llamaToClaimCPId = llama['itemGrants'][0]['templateId']
                if llamaToClaimTitle: llamaToClaimName = llamaToClaimTitle
                else:
                    try: llamaToClaimName = getStringList['Llama names'][f'{llamaToClaimCPId}']
                    except: llamaToClaimName = llamaToClaimCPId
                while True:
                    reqPopulateLlamas = requests.post(links.profileRequest.format(accountId, "PopulatePrerolledOffers", "campaign"), headers=headers, data="{}")
                    reqPopulateLlamasText = json.loads(reqPopulateLlamas.text)
                    llamaTier = []
                    for key in reqPopulateLlamasText['profileChanges'][0]['profile']['items']:
                        if (reqPopulateLlamasText['profileChanges'][0]['profile']['items'][f'{key}']['templateId'].lower().startswith("prerolldata") and reqPopulateLlamasText['profileChanges'][0]['profile']['items'][f'{key}']['attributes']['offerId'] == llamaToClaimOfferId):
                            llamaTier = reqPopulateLlamasText['profileChanges'][0]['profile']['items'][f'{key}']['attributes']['highest_rarity']
                            llamaTier = getStringList['Llama tiers'][f'{llamaTier}']
                    reqBuyFreeLlama = requests.post(links.profileRequest.format(accountId, "PurchaseCatalogEntry", "common_core"), headers=headers, json={"offerId": f"{llamaToClaimOfferId}", "purchaseQuantity": 1, "currency": "MtxCurrency", "currencySubType": "", "expectedTotalPrice": 0, "gameContext": "Frontend.None"})
                    reqBuyFreeLlamaText = json.loads(reqBuyFreeLlama.text)
                    if "errorMessage" in reqBuyFreeLlamaText:
                        if "limit of" in reqBuyFreeLlamaText['errorMessage']:
                            if openedLlamas == 0: alreadyOpenedFreeLlamas += 1
                        break
                    else:
                        print(f"\nOpening: {llamaToClaimName}\nTier: {llamaTier}\nLoot result:")
                        llamaLoot = reqBuyFreeLlamaText['notifications'][0]['lootResult']['items']
                        openedLlamas += 1
                        llamaLootCount = 0
                        for key in llamaLoot:
                            templateId = key['itemType']
                            itemGuid = key['itemGuid']
                            itemQuantity = key['quantity']
                            try: itemName = getStringList['Item names'][f'{templateId}']
                            except: itemName = templateId
                            itemRarity = itemName.split(" ")[0].lower()
                            if templateId.startswith("Schematic:"):
                                if (templateId.startswith("Schematic:sid_ceiling") or templateId.startswith("Schematic:sid_floor") or templateId.startswith("Schematic:sid_wall")): itemType = "trap"
                                else: itemType = "weapon"
                            elif templateId.startswith("Hero:"): itemType = "hero"
                            elif templateId.startswith("Worker:"): itemType = "survivor"
                            elif templateId.startswith("Defender:"): itemType = "defender"
                            else: itemType = "niewiemjaktakmozebyc"
                            llamaLootCount += 1
                            if itemRarity.lower() in ("common", "uncommon", "rare", "epic"):
                                itemsfromLlamas.append({"itemName": itemName, "itemType": itemType, "templateId": templateId, "itemGuid": itemGuid, "itemRarity": itemRarity, "itemQuantity": itemQuantity})
                            print(f"{llamaLootCount}: {itemQuantity}x {itemName}")
            if int(alreadyOpenedFreeLlamas) == freeLlamasCount:
                print(f"\nFree Llamas that are currently avaiable in the shop have been already opened on this account. Remember that you can open a maximum of 2 free one hour rotation Llamas in 24 hours.\n")
            else:
                llamasWord = "Llamas"
                if int(openedLlamas) == 1: llamasWord = "Llama"
                print(f"\nSuccesfully opened {openedLlamas} free {llamasWord}.\n")

# Automatic selected llama loot recycling.
if (not (recycleOn == 0)) and (not(int(alreadyOpenedFreeLlamas) == freeLlamasCount)):
    itemsToRecycle = []
    itemGuidsToRecycle = []
    recycleResources = []
    recycledItemsCount = 0
    recycleResourcesCount = 0
    for item in itemsfromLlamas:
        itemType = item['itemType']
        itemRarity = item['itemRarity']
        itemGuid = item['itemGuid']
        if itemRarity in autoRecycling.itemRarities[f'{itemType}']:
            itemGuidsToRecycle.append(itemGuid)
            itemsToRecycle.append(item)
    if not (len(itemGuidsToRecycle) == 0):
        print(f"Recycling/Retiring selected items from {openedLlamas} free {llamasWord}...\n")
        reqGetResources = requests.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}")
        reqGetResourcesText = json.loads(reqGetResources.text)
        for resource in autoRecycling.recycleResources:
            for item in reqGetResourcesText['profileChanges'][0]['profile']['items']:
                if reqGetResourcesText['profileChanges'][0]['profile']['items'][f'{item}']['templateId'] == resource:
                    recycleResources.append({"itemGuid": item, "templateId": resource, "itemName": getStringList['Item names'][f'{resource}'], "quantity": reqGetResourcesText['profileChanges'][0]['profile']['items'][f'{item}']['quantity']})
        reqRecycleItems = requests.post(links.profileRequest.format(accountId, "RecycleItemBatch", "campaign"), headers=headers, json={"targetItemIds": itemGuidsToRecycle})
        reqRecycleItemsText = json.loads(reqRecycleItems.text)
        if "errorMessage" in reqRecycleItemsText:
            input(f"ERROR: {reqRecycleItemsText['errorMessage']}\n\nPress ENTER to close the program.\n")
            exit()
        print("The following items have been succesfully Recycled/Retired:")
        for item in itemsToRecycle:
            recycledItemsCount += 1
            print(f"{recycledItemsCount}: {item['itemQuantity']}x {item['itemName']}")
        reqGetResources2 = requests.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}")
        reqGetResources2Text = json.loads(reqGetResources2.text)
        print("\nResources received:")
        for resource in recycleResources:
            resourceQuantity = int(reqGetResources2Text['profileChanges'][0]['profile']['items'][resource['itemGuid']]['quantity']) - int(resource['quantity'])
            if resourceQuantity > 0:
                recycleResourcesCount += 1
                print(f"{recycleResourcesCount}: {resourceQuantity}x {resource['itemName']}. Total amount: {reqGetResources2Text['profileChanges'][0]['profile']['items'][resource['itemGuid']]['quantity']}")
        print("") # Extra newline
input("Press ENTER to close the program.\n")
exit()