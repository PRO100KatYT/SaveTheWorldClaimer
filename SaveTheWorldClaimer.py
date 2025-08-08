versionNum = 34
versionStr = "1.14.0"
configVersion = "1.14.0"
print(f"Fortnite Save the World Claimer v{versionStr} by PRO100KatYT\n")

import os
import sys
import subprocess
import json
from configparser import ConfigParser
from datetime import datetime, timedelta, timezone
import webbrowser
import time
from threading import Thread
if os.name == "nt": os.system(f"title Fortnite Save the World Claimer")
try: from requests import Session
except ImportError:
    print(f"The program will now try to install the requests module.\n")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    if os.name == 'posix': os.system('clear')
    else: os.system('cls')
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
    exit()

# Default program language value.
language = "en"

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

# Basic headers for logging in. (For backwards compatibility with accounts saved prior to the 1.13.2 Update)
class basicHeaders:
    inUse = ""
    ios = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE"
    android = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU"

# Start a new requests session.
session = Session()

# Send requests and retry if something goes wrong.
sendRequestErrorMsg = "An error occured when trying to send a \"{0}\" request to {1}.{2} Make sure you have a stable internet connection.\nRetrying in {3}s...\n" # It will later be overriden by the one from stringlist.json
def request(method, url, headers=None, data=None, json=None):
    global sendRequestErrorMsg
    retries, secondsToWait = [0, 5]
    while True:
        try:
            if method == "get": req = session.get(url, headers=headers, data=data, json=json)
            elif method == "post": req = session.post(url, headers=headers, data=data, json=json)
        except Exception as e:
            secondsToWait = 10 if (retries in [2, 3]) else (30 if (retries in [4, 5]) else (60 if retries >= 6 else 5))
            print(sendRequestErrorMsg.format(method, url, (" ({0}).".format(e) if retries >= 6 else ""), secondsToWait))
            time.sleep(secondsToWait)
            retries += 1
            continue
        return req

# Default bShowDateTime value.
bShowDateTime = False

# Get the current date and time and neatly format it | by Salty-Coder :)
def getDateTimeString(): return datetime.now().strftime("[%Y/%m/%d %H:%M:%S]")

# Get the next time program is going to run by Salty-Coder
def nextrun(loopSeconds):
    nextrun = datetime.now() + timedelta(seconds=loopSeconds)
    return nextrun.strftime("%Y/%m/%d %H:%M:%S")

# Load and/or download the stringlist.json file.
stringListPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "stringlist.json")
def downloadAndSaveStringlistFile():
    global stringListPath
    content = request("get", "https://raw.githubusercontent.com/PRO100KatYT/SaveTheWorldClaimer/refs/heads/main/stringlist.json").content
    with open(stringListPath, "wb") as file: file.write(content)
if not os.path.exists(stringListPath): downloadAndSaveStringlistFile()
try: stringList = json.loads(open(stringListPath, "r", encoding = "utf-8").read())
except:
    downloadAndSaveStringlistFile()
    try: stringList = json.loads(open(stringListPath, "r", encoding = "utf-8").read())
    except:
        input("ERROR: The program still can't read the newly downloaded stringlist.json file. Weird...")
        exit()

# Get a string in currently selected language.
def getString(string): return stringList["Strings"].get(language, stringList["Strings"]["en"]).get(string, string)

# Get a correct plural word depending on the int.
def getPluralWord(string, number):
    global language
    if language == "pl":
        if number == 1: plural = "one"
        elif number % 10 in [2, 3, 4] and not (12 <= (number % 100) <= 14): plural = "few"
        else: plural = "many"
    elif language == "en": plural = "one" if number == 1 else "other"
    else: plural = "other"
    return stringList["Strings"].get(language, stringList["Strings"]["en"])["words"][string].get(plural, stringList["Strings"]["en"]["words"][string]["other"])

# Error with a custom message.
def customError(text):
    if bShowDateTime == "true": input(f"{getDateTimeString()} {getString('customerror.message').format(text)}")
    else: input(getString('customerror.message').format(text))
    exit()

# Error for invalid config values.
def configError(key, value, validValues): customError(getString("configerror.message").format(key, value, validValues))

# Input loop until it's one of the correct values.
def validInput(text, values):
    values = [i.lower() if isinstance(i, str) else i for i in values] if isinstance(values, list) else values
    while True:
        response = input(f"{text}\n").lower()
        if values == "digit" and response.replace(",", ".").replace(".", "").replace("-", "").isdigit(): break
        elif response in values: break
        text = getString("validinput.message")
    return response

# Get the text from a request and check for errors.
def requestText(request, bCheckForErrors):
    requestText = json.loads(request.text)
    if (bCheckForErrors and ("errorMessage" in requestText)): customError(requestText['errorMessage'])
    return requestText

# Send token request.
def reqTokenText(loginLink, altLoginLink, authHeader):
    while True:
        webbrowser.open_new_tab(loginLink)
        print(getString("reqtoken.message").format(loginLink))
        reqToken = requestText(request("post", links.getOAuth.format("token"), headers={"Authorization": f"basic {authHeader}"}, data={"grant_type": "authorization_code", "code": input(getString("reqtoken.insertcode"))}), False)
        if "errorMessage" not in reqToken: return reqToken
        else: input(getString("reqtoken.error").format(reqToken['errorMessage']))
        loginLink = altLoginLink

# Print a message with or without the date and time.
webhookUrl = "" # A value will be assigned in the config part of the program.
webhookMessagesToSend = []
def message(string):
    global webhookUrl
    if bShowDateTime:
        lines = [f"{getDateTimeString()} {line}" if line.strip() else line for line in string.split("\n")]
        string = "\n".join(lines)
    print(string)
    if not webhookUrl: return
    webhookMessagesToSend.append(string)

# Send webhook messages to a Discord channel if the webhook url is specified in config.ini.
def webhookLoop():
    global webhookUrl
    while True:
        try:
            if webhookUrl and webhookMessagesToSend:
                webhookMessagesToSend2 = "".join(mess if mess.endswith('\n') else mess+'\n' for mess in webhookMessagesToSend)
                webhookMessagesToSend.clear()
                request("post", webhookUrl, data=json.dumps({"content": webhookMessagesToSend2}), headers={"Content-Type": "application/json"})
            else: time.sleep(0.25)
        except Exception as e: webhookMessagesToSend.clear()
t = Thread(target=webhookLoop)
t.daemon = True # End the thread when program stops.
t.start()

# Check if there is a newer version of this program available.
def checkUpdate():
    try:
        getJson = (request("get", "https://raw.githubusercontent.com/PRO100KatYT/SaveTheWorldClaimer/main/SaveTheWorldClaimer.py").text).splitlines()[0:2]
        latestVerNum = int(getJson[0].split("=")[1].strip())
        latestVerStr = getJson[1].split("=")[1].strip().strip('"')
        if latestVerNum > versionNum: message(getString("updatechecker.message").format(latestVerStr))
    except: pass

# Check whether the type matches the value and return it.
def isCorrectValue(value, type, validValues = []):
    if validValues and isinstance(validValues, list):
        for option in validValues:
            if str(value).lower() == str(option).lower(): return [True, option]
        return [False, ""]
    if type == "string": return [True, str(value)]
    if type in ["int", "float"]:
        try:
            conv = int if type == "int" else float
            return [True, conv(value)]
        except: return [False, ""]
    return [False, ""]

# Create and/or read the config.ini file.
config, configPath = [ConfigParser(), os.path.join(os.path.split(os.path.abspath(__file__))[0], "config.ini")]
if not os.path.exists(configPath):
    configFileContent = "[Config]\n\n"
    configJson = {}
    bStartSetup = validInput(getString("config.bstartsetup"), ["1", "2"])
    message(getString("config.startgenerating"))
    for setting in stringList["Config"]["Settings"]:
        value = isCorrectValue(setting["defaultValue"], setting["settingType"], setting["validValues"])[1]
        bSkipSetup = setting["bSkipInSetup"] or (bStartSetup != "1")
        if setting["skipInSetupIf"]:
            for key in setting["skipInSetupIf"]:
                if key in configJson:
                    setting2 = next(setting2 for setting2 in stringList["Config"]["Settings"] if setting2["settingName"] == key) # Get the properties of the setting
                    val1 = isCorrectValue(configJson[key], setting2["settingType"], setting2["validValues"])[1]
                    val2 = isCorrectValue(setting["skipInSetupIf"][key], setting2["settingType"], setting2["validValues"])[1]
                    if val1 == val2:
                        bSkipSetup = True
                        break
        if not bSkipSetup:
            for comment in setting["settingComments"]: print(getString(comment))
            print(getString("config.availableoptions").format(', '.join(str(item) for item in setting['validValues']).lower() if isinstance(setting['validValues'], list) else getString(setting['validValues'])))
            value = input()
            isCorrect = isCorrectValue(value, setting["settingType"], setting["validValues"])
            value = isCorrect[1]
            while not isCorrect[0]:
                print(getString("validinput.message"))
                value = input()
                isCorrect = isCorrectValue(value, setting["settingType"], setting["validValues"])
            print()
        configJson[setting["settingName"]] = value
        if setting["settingName"] == "Language": language = value # Scuffed but yeah
        for comment in setting["extraComments"] + setting["settingComments"]:
            configFileContent += f"# {getString(comment)}\n" if comment else "\n" # if comment is empty then just do newline
        configFileContent += f"# {getString('config.availableoptions').format(', '.join(str(item) for item in setting['validValues']).lower() if isinstance(setting['validValues'], list) else getString(setting['validValues']))}\n{setting['settingName']} = {str(value).lower() if setting['settingType'] in ["bool", "string"] else value}\n\n"
    configFileContent += f"# {getString('config.setup.dontchange')}\n[Config_Version]\n\nVersion = STWC_{configVersion}\n"
    with open(configPath, "w", encoding="utf-8") as file:
        file.write(configFileContent)
    message(getString("config.setup.success"))
config.read(configPath)
try: configVer = config['Config_Version']['Version']
except: customError(getString("config.readerror"))
if configVer != f"STWC_{configVersion}": customError(getString("config.versionerror"))

# Get a setting value from the config file.
def getConfig(settingName):
    try:
        setting = next(i for i in stringList["Config"]["Settings"] if i["settingName"] == settingName)
        rawValue = config.get("Config", settingName)
        if setting["settingType"] == "bool": return config.getboolean("Config", settingName)
        elif setting["settingType"] == "int": return config.getint("Config", settingName)
        elif setting["settingType"] == "float": return config.getfloat("Config", settingName)
        return rawValue
    except Exception as e: customError(getString("config.getconfigerror").format(settingName, e))

bShowDateTime, webhookUrl, language = [getConfig('Show_Date_Time'), getConfig('Discord_Webhook_URL'), getConfig('Language')]
try: autoRecycling.itemRarities = {"weapon": autoRecycling.rarities[getConfig('Recycle_Weapons').lower()].split(", "), "trap": autoRecycling.rarities[getConfig('Recycle_Traps').lower()].split(", "), "survivor": autoRecycling.rarities[getConfig('Retire_Survivors').lower()].split(", "), "defender": autoRecycling.rarities[getConfig('Retire_Defenders').lower()].split(", "), "hero": autoRecycling.rarities[getConfig('Retire_Heroes').lower()].split(", ")}
except: customError(getString("config.readerror"))
bRecycle = False
for key in ["Recycle_Weapons", "Recycle_Traps", "Retire_Survivors", "Retire_Defenders", "Retire_Heroes"]:
    if getConfig(key).lower() != "off": bRecycle = True
sendRequestErrorMsg = getString('request.error')

# Create and load the auth.json file.
authPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "auth.json")
if not os.path.exists(authPath):
    with open(authPath, "w") as authJson: authJson.write("[]")
try: authJson = json.loads(open(authPath, "r", encoding = "utf-8").read())
except: customError(getString("authjson.readerror"))
if not isinstance(authJson, list): customError(getString("authjson.oldformat"))

# Log into an account.
class login:
    def __init__(self, account):
        # Read the auth.json file.
        try:
            authType, accountId = account['authType'], account["accountId"]
            displayName = account.get('displayName', getString("startup.listaccounts.noname"))
            if authType == "token":
                expirationDate, refreshToken = account["refresh_expires_at"], account["refreshToken"]
                if expirationDate < datetime.now().isoformat(): customError(getString("main.auth.tokenexpired").format(displayName))
            elif authType == "device": deviceId, secret = account["deviceId"], account["secret"]
        except: customError(getString("main.auth.readerror").format(displayName))

        # Log in.
        message(getString("main.login.start").format(displayName))
        if not "addedInVersionNum" in account: basicHeaders.inUse = basicHeaders.ios
        else: basicHeaders.inUse = basicHeaders.android
        if authType == "token":
            reqRefreshToken = requestText(request("post", links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "refresh_token", "refresh_token": refreshToken}), False)
            if "errorMessage" in reqRefreshToken: customError(getString("main.login.token.error").format(displayName))
            account['refreshToken'], account['refresh_expires_at'] = reqRefreshToken["refresh_token"], reqRefreshToken["refresh_expires_at"]
            with open(authPath, "w", encoding="utf-8") as saveAuthFile: json.dump(authJson, saveAuthFile, indent=2, ensure_ascii=False)
            reqExchange = requestText(request("get", links.getOAuth.format("exchange"), headers={"Authorization": f"bearer {reqRefreshToken['access_token']}"}, data={"grant_type": "authorization_code"}), True)
            reqToken = requestText(request("post", links.getOAuth.format("token"), headers={"Authorization": f"basic {basicHeaders.inUse}"}, data={"grant_type": "exchange_code", "exchange_code": reqExchange["code"], "token_type": "eg1"}), True)
        elif authType == "device": reqToken = requestText(request("post", links.getOAuth.format("token"), headers={"Authorization": f"basic {basicHeaders.inUse}"}, data={"grant_type": "device_auth", "device_id": deviceId, "account_id": accountId, "secret": secret, "token_type": "eg1"}), True)
        accessToken, displayName = reqToken['access_token'], reqToken['displayName']
        message(getString("main.login.success"))

        # Headers for MCP requests.
        headers = {"User-Agent": "Fortnite/++Fortnite+Release-19.40-CL-19215531 Windows/10.0.19043.1.768.64bit", "Authorization": f"bearer {accessToken}", "Content-Type": "application/json", "X-EpicGames-Language": getConfig('Items_Language'), "Accept-Language": getConfig('Items_Language')}

        # Check whether the account has the campaign access token and if it's able to receive V-Bucks.
        reqQueryProfiles = [json.dumps(requestText(request("post", links.profileRequest.format(accountId, "QueryProfile", "common_core"), headers=headers, data="{}"), False)), json.dumps(requestText(request("post", links.profileRequest.format(accountId, "ClientQuestLogin", "campaign"), headers=headers, data="{}"), False))]
        campaignProfile = json.loads(reqQueryProfiles[1])['profileChanges'][0]['profile']
        bReceiveMtx = False
        bHasCampaignAccess = False
        if "Token:receivemtxcurrency" in reqQueryProfiles[1]: bReceiveMtx = True
        if "Token:campaignaccess" in reqQueryProfiles[0]: bHasCampaignAccess = True

        # Check whether the account is able to get Daily Quests
        bDailyQuestsUnlocked = False
        ssd3QuestGUID = next((id for id in campaignProfile["items"] if campaignProfile["items"][id]["templateId"].lower() == "quest:outpostquest_t1_l3"), "")
        if ssd3QuestGUID:
            if "completion_complete_outpost_1_3" in campaignProfile["items"][ssd3QuestGUID]["attributes"]:
                if (campaignProfile["items"][ssd3QuestGUID]["attributes"]["completion_complete_outpost_1_3"] == 1
                    and campaignProfile["items"][ssd3QuestGUID]["attributes"]["quest_state"].lower() == "claimed"):
                    bDailyQuestsUnlocked = True

        # Check whether the account is able to get Research Points
        bRecyclingUnlocked = any(campaignProfile["items"][id]["templateId"].lower() == "homebasenode:questreward_recyclecollection" for id in campaignProfile["items"])

        self.headers, self.accountId, self.displayName, self.campaignProfile, self.bHasCampaignAccess, self.bReceiveMtx, self.bDailyQuestsUnlocked, self.bRecyclingUnlocked = headers, accountId, displayName, campaignProfile, bHasCampaignAccess, bReceiveMtx, bDailyQuestsUnlocked, bRecyclingUnlocked

# Get an account's Daily Quests
def getDailyQuests(auth):
    questNumber = 0
    questData = {}
    for item in auth.campaignProfile['items']:
        itemData = auth.campaignProfile['items'][item]
        if itemData['templateId'].lower().startswith("quest:daily_") and itemData['attributes']['quest_state'].lower() == "active":
            templateId = itemData['templateId']
            questName = stringList['Items'][templateId]['name'][getConfig('Items_Language')]
            objectives = stringList['Items'][templateId]['objectives']
            progressMsg = ""
            for objective in objectives:
                objData = objectives[objective]
                objName, objCount = objData['name'][getConfig('Items_Language')], objData['count']
                completionCount = itemData['attributes'].get(f'completion_{objective}', 0)
                progressMsg += f" {completionCount}/{objCount} {objName},"
            progressMsg = progressMsg[:-1]
            rewards = stringList['Items'][templateId]['rewards']
            rewardsMsg = ""
            for reward in rewards:
                rewardQuantity, rewardName = [rewards[reward], stringList['Items'][reward]['name'][getConfig('Items_Language')]]
                if reward.startswith("ConditionalResource:"):
                    if auth.bReceiveMtx == True: rewardsMsg += f" {rewardQuantity}x {rewardName['PassedConditionItem']},"
                    rewardName = rewardName['FailedConditionItem']
                rewardsMsg += f" {rewardQuantity}x {rewardName},"
            rewardsMsg = rewardsMsg[:-1]
            questNumber += 1
            questData[item] = {"templateId": templateId, "questNumber": questNumber, "questName": questName, "progress": progressMsg, "rewards": rewardsMsg}
    return questData

class invJunkCleaner:
    tiers = {1: ["t01"], 2: ["t01", "t02"], 3: ["t01", "t02", "t03"], 4: ["t01", "t02", "t03", "t04"], 5: ["t01", "t02", "t03", "t04", "t05"], "t06": ["t01", "t02", "t03", "t04", "t05", "t06"]};
    TIDsToExclude = ["Trap:tid_floor_defender", "Trap:tid_floor_player_jump_pad", "Trap:tid_floor_player_jump_pad_free_direction", "Trap:tid_floor_launchpad_r_t01", "Trap:tid_floor_hoverboard_speed_curve_r_t01", "Trap:tid_floor_hoverboard_speed_r_t01", "Trap:tid_wall_spikes_r_t01", "Trap:ob_trap_floor_spikes"]

    def isProfileLocked(theater0):
        if not "profileLockExpiration" in theater0: return False
        lockExpirationDate = lockExpirationDate = datetime.fromisoformat(theater0["profileLockExpiration"].replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
        nowDate = datetime.now(timezone.utc)
        secondsDiff = (lockExpirationDate - nowDate).total_seconds()
        return [lockExpirationDate.date() >= nowDate.date(), secondsDiff]
    
    def findItems(theater0):
        itemGUIDsToRecycle, itemGUIDsToDestroy = [[], []]
        for key in theater0["items"]:
            templateId, attributes, quantity = [theater0["items"][key]["templateId"], theater0["items"][key]["attributes"], theater0["items"][key]["quantity"]]
            if templateId.lower().startswith("ingredient:"):
                if templateId in stringList["Items"] and "tier" in stringList["Items"][templateId]:
                    if stringList["Items"][templateId]["tier"].lower() in invJunkCleaner.tiers[getConfig('Inventory_Junk_Cleaner')]:
                        itemGUIDsToDestroy.append(key)
            elif templateId.lower().startswith("trap:"):
                if (("alterationDefinitions" not in attributes or not attributes["alterationDefinitions"]
                or "itemSource" in attributes
                and attributes["itemSource"] in ["EFortPickupSourceTypeFlag::Container", "EFortPickupSourceTypeFlag::AI"])
                and templateId not in invJunkCleaner.TIDsToExclude):
                    trapTier = templateId.split("_")[-1].lower()
                    if trapTier in invJunkCleaner.tiers[getConfig('Inventory_Junk_Cleaner')]: itemGUIDsToDestroy.append(key)
                    else: itemGUIDsToRecycle.append({"itemId": key, "quantity": quantity})
            elif templateId.lower().startswith("weapon:"):
                if "itemSource" in attributes and attributes["itemSource"] in ["EFortPickupSourceTypeFlag::Container", "EFortPickupSourceTypeFlag::AI"]:
                    weaponTier = templateId.split("_")[-1].lower()
                    if weaponTier in invJunkCleaner.tiers[getConfig('Inventory_Junk_Cleaner')]: itemGUIDsToDestroy.append(key)
                    else: itemGUIDsToRecycle.append({"itemId": key, "quantity": quantity})
        return [itemGUIDsToRecycle, itemGUIDsToDestroy]

    def recycleAndDestroy(auth, itemGUIDsToRecycle, itemGUIDsToDestroy):
        if (not itemGUIDsToRecycle) and (not itemGUIDsToDestroy):
            message(getString("junkcleaner.nothingfound"))
        if itemGUIDsToRecycle:
            message(getString("junkcleaner.recycling").format(len(itemGUIDsToRecycle), getPluralWord('items', len(itemGUIDsToRecycle))))
            requestText(request("post", links.profileRequest.format(auth.accountId, "DisassembleWorldItems", "theater0"), headers=auth.headers, json={"targetItemIdAndQuantityPairs": itemGUIDsToRecycle}), True)
        if itemGUIDsToDestroy:
            message(getString("junkcleaner.destroying").format(len(itemGUIDsToDestroy), getPluralWord('items', len(itemGUIDsToRecycle))))
            requestText(request("post", links.profileRequest.format(auth.accountId, "DestroyWorldItems", "theater0"), headers=auth.headers, json={"itemIds": itemGUIDsToDestroy}), True)

# Menu (Account & Daily Quest Manager)
def menu():
    def addAccount(bGoBack=True):
        isLoggedIn = validInput(getString("startup.addaccount.isloggedin1" if bGoBack else "startup.addaccount.isloggedin2"), ["1", "2", "3"])
        if isLoggedIn == "3": return
        authType = validInput(getString("startup.addaccount.authtype"), ["token", "device"])
        input(getString("startup.addaccount.openwebsiteinfo"))
        loginLink = links.loginLink1 if isLoggedIn == "1" else links.loginLink2
        if authType == "token": # Shoutout to BayGamerYT for telling me about this login method.
            reqToken = reqTokenText(loginLink.format("34a02cf8f4414e29b15921876da36f9a"), links.loginLink1.format("34a02cf8f4414e29b15921876da36f9a"), "MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y=")
            refreshToken, accountId, displayName, expirationDate = [reqToken["refresh_token"], reqToken["account_id"], reqToken["displayName"], reqToken["refresh_expires_at"]]
            jsonToAppend = {getString("authjson.warning.header"): getString("authjson.warning.text"), "authType": "token", "refreshToken": refreshToken, "accountId": accountId, "displayName": displayName, "refresh_expires_at": expirationDate, "addedInVersionNum": versionNum}
        else:
            reqToken = reqTokenText(loginLink.format("3f69e56c7649492c8cc29f1af08a8a12"), links.loginLink1.format("3f69e56c7649492c8cc29f1af08a8a12"), "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU=")
            accessToken, accountId, displayName = [reqToken["access_token"], reqToken["account_id"], reqToken["displayName"]]
            reqDeviceAuth = requestText(request("post", links.getDeviceAuth.format(accountId), headers={"Authorization": f"bearer {accessToken}"}, data={}), True)
            deviceId, secret = [reqDeviceAuth["deviceId"], reqDeviceAuth["secret"]]
            jsonToAppend = {getString("authjson.warning.header"): getString("authjson.warning.text"), "authType": "device",  "deviceId": deviceId, "accountId": accountId, "displayName": displayName, "secret": secret, "addedInVersionNum": versionNum}
        bAlreadyLoggedIn = any(account['accountId'] == accountId for account in authJson)
        if bAlreadyLoggedIn: print(getString("startup.addaccount.alreadyadded").format(displayName))
        else:
            authJson.append(jsonToAppend)
            with open(authPath, "w", encoding="utf-8") as authFile: json.dump(authJson, authFile, indent=2, ensure_ascii=False)
            print(getString("startup.addaccount.success").format(displayName))

    def listAccounts():
        print(getString("startup.listaccounts.header"))
        if not authJson: print(getString("startup.listaccounts.empty"))
        else:
            for account in authJson:
                try: print(f"{authJson.index(account) + 1}: {account['displayName']}")
                except KeyError: print(f"{authJson.index(account) + 1}: {getString('startup.listaccounts.noname')}")

    def removeAccount():
        listAccounts()
        if not authJson: return
        print(getString("startup.removeaccount.message"))
        accountCountList = [str(i) for i in range(len(authJson))]
        accountToRemove = int(validInput("", accountCountList + [str(int(accountCountList[-1]) + 1)]))
        if accountToRemove != 0:
            areYouSure = int(validInput(getString("startup.removeaccount.areyousure").format(authJson[accountToRemove - 1]['displayName']), ["1", "2"]))
            if areYouSure == 1:
                print(getString("startup.removeaccount.success").format(authJson[accountToRemove - 1]['displayName']))
                authJson.pop(accountToRemove - 1)
                with open(authPath, "w", encoding="utf-8") as authFile: json.dump(authJson, authFile, indent=2, ensure_ascii=False)

    def manageDailyQuests():
        while authJson:
            listAccounts()
            print(getString("startup.managedailyquests.message"))
            accountCountList = list(map(str, range(len(authJson))))
            accountIndex = int(validInput("", accountCountList + [str(int(accountCountList[-1]) + 1)]))
            if accountIndex == 0: break
            accountToManage = authJson[accountIndex - 1]
            while True:
                auth = login(accountToManage)
                print(getString("startup.managedailyquests.searching"))
                questData = getDailyQuests(auth)
                if not questData:
                    print(getString("startup.managedailyquests.notfound"))
                    input(getString("startup.managedailyquests.pressenter"))
                    break
                else:
                    for quest in questData: message(getString("startup.managedailyquests.info").format(questData[quest]['questNumber'], questData[quest]['questName'], questData[quest]['progress'], questData[quest]['rewards']))
                    dailyQuestRerolls = auth.campaignProfile["stats"]["attributes"].get("quest_manager", 0).get("dailyQuestRerolls", 0)
                    if dailyQuestRerolls <= 0:
                        print(getString("startup.managedailyquests.norerolls"))
                        input(getString("startup.managedailyquests.pressenter"))
                        break
                    else:
                        print(getString("startup.managedailyquests.choosequest").format(auth.displayName))
                        questCountList = list(map(str, range(len(questData))))
                        questIndex = int(validInput("", questCountList + [str(int(questCountList[-1]) + 1)]))
                        if questIndex == 0: break
                        questToReplace = list(questData.keys())[questIndex - 1]
                        confirmReroll = validInput(getString("startup.managedailyquests.confirm").format(questData[questToReplace]['questName']), ["1", "2"])
                        if confirmReroll == "1":
                            reqRerollQuest = requestText(request("post", links.profileRequest.format(auth.accountId, "FortRerollDailyQuest", "campaign"), headers=auth.headers, json={"questId": questToReplace}), True)
                            newQuestTemplateId = reqRerollQuest.get("notifications", [{}])[0].get("newQuestId")
                            if newQuestTemplateId:
                                newQuestName = stringList['Items'].get(newQuestTemplateId, {}).get('name', {}).get(getConfig('Items_Language'), newQuestTemplateId)
                                print(getString("startup.managedailyquests.success").format(questData[questToReplace]['questName'], newQuestName))
                                input(getString("startup.managedailyquests.pressenter"))            
    
    def junkCleaner():
        while authJson:
            print(getString("junkcleaner.message").format(getConfig('Inventory_Junk_Cleaner')))
            selectedAccounts = []
            whatToDo2 = validInput(getString("junkcleaner.whattodo"), ["1", "2", "3"])
            if whatToDo2 == "1":
                listAccounts()
                print(getString("junkcleaner.selectaccount"))
                accountCountList = list(map(str, range(len(authJson))))
                accountIndex = int(validInput("", accountCountList + [str(int(accountCountList[-1]) + 1)]))
                if accountIndex == 0: return
                selectedAccounts = [authJson[accountIndex - 1]]
            elif whatToDo2 == "2": selectedAccounts = authJson.copy()
            else: break
            loopMinutes = float(validInput(getString("junkcleaner.loopinput"), "digit"))
            loopMinutes = int(loopMinutes) if str(loopMinutes).endswith(".0") else float(loopMinutes)
            if len(selectedAccounts) > 1:
                selectedNicknames = [i["displayName"] for i in selectedAccounts]
                confirmation = validInput(getString("junkcleaner.confirmation").format(', '.join(selectedNicknames), getConfig('Inventory_Junk_Cleaner')), ["1", "2"])
                if confirmation == "2": break
            while True:
                t1 = datetime.now()
                for account in selectedAccounts:
                    print()
                    auth = login(account)
                    message(getString("junkcleaner.gettinginfo"))
                    reqGetTheater0 = requestText(request("post", links.profileRequest.format(auth.accountId, "QueryProfile", "theater0"), headers=auth.headers, data="{}"), True)['profileChanges'][0]['profile']
                    isLocked = invJunkCleaner.isProfileLocked(reqGetTheater0)
                    if isLocked[0]: message(getString("junkcleaner.profilelocked").format(auth.displayName))
                    else:
                        itemGUIDsToRecycle, itemGUIDsToDestroy = invJunkCleaner.findItems(reqGetTheater0)
                        invJunkCleaner.recycleAndDestroy(auth, itemGUIDsToRecycle, itemGUIDsToDestroy)
                t2 = datetime.now()
                message(getString("junkcleaner.done"))
                if loopMinutes <= 0: break
                else:
                    minutesWord = getPluralWord("minutes", loopMinutes)
                    totalSecondsToSleep = max(1, loopMinutes * 60 - (t2 - t1).total_seconds())
                    message(getString("junkcleaner.loopmessage").format(loopMinutes, minutesWord, nextrun(totalSecondsToSleep)))
                    time.sleep(totalSecondsToSleep)
            input(getString("junkcleaner.pressenter"))
            break
    
    while True:
        if not authJson: addAccount(False)
        whatToDo1 = validInput(getString("mainmenu.message"), ["1", "2", "3", "4", ""])
        if whatToDo1 == "1": break
        elif whatToDo1 == "2": manageDailyQuests()
        elif whatToDo1 == "3": junkCleaner()
        elif whatToDo1 == "4":
            while True:
                whatToDo3 = validInput(getString("accountmanager.message"), ["1", "2", "3", "4"])
                if whatToDo3 == "1": addAccount()
                elif whatToDo3 == "2": removeAccount()
                elif whatToDo3 == "3":
                    listAccounts()
                    input(getString("accountmanager.pressenter"))
                else: break
        else: exit()

# The main part of the program that can be looped.
def main():
    for account in authJson:
        auth = login(account)
        
        # Skip the StW tutorial if it hasn't been completed yet. Works for accounts that don't own StW too. It will get the account the StW music pack.
        if getConfig('Skip_Tutorial'):
            for item in auth.campaignProfile['items']:
                if auth.campaignProfile['items'][item]['templateId'].lower() != "quest:homebaseonboarding": continue
                if auth.campaignProfile['items'][item]['attributes']['quest_state'].lower() == "claimed": break
                message(getString("main.skiptutorial.start").format(auth.displayName))
                request("post", links.profileRequest.format(auth.accountId, "SkipTutorial", "campaign"), headers=auth.headers, data="{}")
                reqUpdateObjectives = requestText(request("post", links.profileRequest.format(auth.accountId, "UpdateQuestClientObjectives", "campaign"), headers=auth.headers, json={"advance": [{"statName": "hbonboarding_watchsatellitecine", "count": 1, "timestampOffset": 0}, {"statName": "hbonboarding_namehomebase", "count": 1, "timestampOffset": 0}]}), True)
                if reqUpdateObjectives['profileChanges'][0]['profile']['items'][item]['attributes']['quest_state'].lower() == "claimed": message(getString("main.skiptutorial.success").format(auth.displayName))
                else: message(getString("main.skiptutorial.error").format(auth.displayName))
                break

        # Display current daily challenges, their rewards and progress if there is any.
        if auth.bDailyQuestsUnlocked:
            message(getString("main.dailies.searching"))
            questData = getDailyQuests(auth)
            if not questData: message(getString("main.dailies.notfound"))
            for quest in questData: message(getString("main.dailies.info").format(questData[quest]['questNumber'], questData[quest]['questName'], questData[quest]['progress'], questData[quest]['rewards']))
        else: message(getString("main.dailies.unavailable"))

        # Claim and automatically spend the Research Points.
        reqCampaignProfileCheck = requestText(request("post", links.profileRequest.format(auth.accountId, "QueryProfile", "campaign"), headers=auth.headers, data="{}"), True)
        try:
            reqCampaignProfileCheckResearchLevels = reqCampaignProfileCheck['profileChanges'][0]['profile']['stats']['attributes']['research_levels']
            bTryToClaimRP = True
            tokenToClaim = []
        except: bTryToClaimRP = False
        try:
            if (reqCampaignProfileCheckResearchLevels['fortitude'] == reqCampaignProfileCheckResearchLevels['offense'] == reqCampaignProfileCheckResearchLevels['resistance'] == reqCampaignProfileCheckResearchLevels['technology'] == 120): bTryToClaimRP = False
        except: pass
        if bTryToClaimRP:
            reqCampaignProfileCheckItems = reqCampaignProfileCheck['profileChanges'][0]['profile']['items']
            for key in reqCampaignProfileCheckItems: # Shoutout to Lawin for helping me figuring out how to write this and the next line of code.
                if reqCampaignProfileCheckItems[key]['templateId'] == "CollectedResource:Token_collectionresource_nodegatetoken01":
                    tokenToClaim = key
                    break
            if tokenToClaim:
                reqClaimCollectedResources = requestText(request("post", links.profileRequest.format(auth.accountId, "ClaimCollectedResources", "campaign"), headers=auth.headers, json={"collectorsToClaim": [tokenToClaim]}), False)
                if "errorMessage" in reqClaimCollectedResources: message(getString("main.research.error").format(reqClaimCollectedResources['errorMessage'])) # Error without exit()
                else:
                    storedMaxPoints = False
                    try:
                        totalItemGuid, rpToClaim = [reqClaimCollectedResources['notifications'][0]['loot']['items'][0]['itemGuid'], reqClaimCollectedResources['profileChanges'][0]['profile']['items'][tokenToClaim]['attributes']['stored_value']]
                        rpStored, rpClaimedQuantity = [reqClaimCollectedResources['profileChanges'][0]['profile']['items'][totalItemGuid]['quantity'], int(reqClaimCollectedResources['notifications'][0]['loot']['items'][0]['quantity'])]
                        if float(rpToClaim) >= 1: storedMaxPoints = True
                        researchPointsWord = getPluralWord("researchPoints", rpClaimedQuantity)
                        message(getString("main.research.success").format(rpClaimedQuantity, researchPointsWord, reqClaimCollectedResources['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity']))
                    except:
                        for key in reqCampaignProfileCheckItems:
                            if reqCampaignProfileCheckItems[key]['templateId'] == "Token:collectionresource_nodegatetoken01":
                                totalItemGuid = key
                                break
                        rpToClaim, rpStored, storedMaxPoints = [reqClaimCollectedResources['profileChanges'][0]['profile']['items'][f'{tokenToClaim}']['attributes']['stored_value'], reqClaimCollectedResources['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity'], True]
                        if int(rpToClaim) < 1:
                            storedMaxPoints = False
                            message(getString("main.research.notenough").format(round(rpToClaim, 2)))

                    if storedMaxPoints:
                        if getConfig('Spend_Research_Points') == "off": message(getString("main.research.max.off").format(round(rpToClaim, 2), rpStored))
                        else:
                            message(getString("main.research.max.on").format(rpStored))
                            while True:
                                reqFORTLevelsCheck = {**{"fortitude": 0, "offense": 0, "resistance": 0, "technology": 0}, **requestText(request("post", links.profileRequest.format(auth.accountId, "QueryProfile", "campaign"), headers=auth.headers, data="{}"), True)['profileChanges'][0]['profile']['stats']['attributes']['research_levels']}
                                if getConfig('Spend_Research_Points') == "lowest":
                                    levelsList = [int(reqFORTLevelsCheck['fortitude']), int(reqFORTLevelsCheck['offense']), int(reqFORTLevelsCheck['resistance']), int(reqFORTLevelsCheck['technology'])]
                                    level = min(levelsList)
                                elif getConfig('Spend_Research_Points') == "everyten":
                                    levelsList, levelsJson = [[int(reqFORTLevelsCheck['fortitude']) % 10, int(reqFORTLevelsCheck['offense']) % 10, int(reqFORTLevelsCheck['resistance']) % 10, int(reqFORTLevelsCheck['technology']) % 10], {int(reqFORTLevelsCheck['fortitude']) % 10: int(reqFORTLevelsCheck['fortitude']), int(reqFORTLevelsCheck['offense']) % 10: int(reqFORTLevelsCheck['offense']), int(reqFORTLevelsCheck['resistance']) % 10: int(reqFORTLevelsCheck['resistance']), int(reqFORTLevelsCheck['technology']) % 10: int(reqFORTLevelsCheck['technology'])}]
                                    level = levelsJson[max(levelsList)]
                                for key in reqFORTLevelsCheck:
                                    if reqFORTLevelsCheck[key] == int(level):
                                        statToClaim = key
                                        break
                                reqPurchaseResearchStatUpgrade = requestText(request("post", links.profileRequest.format(auth.accountId, "PurchaseResearchStatUpgrade", "campaign"), headers=auth.headers, json={"statId": f'{statToClaim}'}), False)
                                statName = stringList['Strings'][getConfig('Language')]['researchStats'][f'{statToClaim}']
                                if "errorMessage" in reqPurchaseResearchStatUpgrade: break # Error without exit()
                                else: message(getString("main.research.spend.success").format(statName, reqPurchaseResearchStatUpgrade['profileChanges'][0]['profile']['stats']['attributes']['research_levels'][statToClaim]))
                            message(getString("main.research.spend.end"))
                            reqClaimCollectedResources = requestText(request("post", links.profileRequest.format(auth.accountId, "ClaimCollectedResources", "campaign"), headers=auth.headers, json={"collectorsToClaim": [tokenToClaim]}), True)
                            try:
                                totalItemGuid = reqClaimCollectedResources['notifications'][0]['loot']['items'][0]['itemGuid']
                                message(getString("main.research.success").format(reqClaimCollectedResources['notifications'][0]['loot']['items'][0]['quantity'], reqClaimCollectedResources['profileChanges'][0]['profile']['items'][totalItemGuid]['quantity']))
                            except: pass

        # Search for free Llamas and open them if they're available.
        alreadyOpenedFreeLlamas, freeLlamasCount, cpspStorefront = [0, 0, []]
        if getConfig('Open_Free_Llamas'):
            reqGetStorefront = requestText(request("get", links.getStorefront, headers=auth.headers, data={}), True)['storefronts']
            for key in reqGetStorefront:
                if key['name'] == "CardPackStorePreroll":
                    cpspStorefront = key['catalogEntries']
                    break
            if not cpspStorefront: customError(getString("main.freellamas.noshop"))
            else:
                freeLlamas = [key for key in cpspStorefront if (not "always" in key['devName'].lower()) and (key['prices'][0]['finalPrice'] == 0)]
                freeLlamasCount = len(freeLlamas)
                if not freeLlamas: message(getString("main.freellamas.nollamas"))
                else:
                    message(getString("main.freellamas.yesllamas"))
                    itemsfromLlamas, openedLlamas = [[], 0]
                    for llama in freeLlamas:
                        llamaToClaimOfferId, llamaToClaimName = [llama['offerId'], []]
                        try: llamaToClaimTitle = llama['title']
                        except: llamaToClaimTitle = []
                        llamaToClaimCPId = llama['itemGrants'][0]['templateId']
                        try: llamaToClaimName = stringList['Items'][llamaToClaimCPId]['name'][getConfig('Items_Language')]
                        except:
                            if llamaToClaimTitle: llamaToClaimName = llamaToClaimTitle
                        if not llamaToClaimName: llamaToClaimName = llamaToClaimCPId
                        while True:
                            reqPopulateLlamas = requestText(request("post", links.profileRequest.format(auth.accountId, "PopulatePrerolledOffers", "campaign"), headers=auth.headers, data="{}"), True)
                            for key in reqPopulateLlamas['profileChanges'][0]['profile']['items']:
                                if (reqPopulateLlamas['profileChanges'][0]['profile']['items'][key]['templateId'].lower().startswith("prerolldata") and reqPopulateLlamas['profileChanges'][0]['profile']['items'][key]['attributes']['offerId'] == llamaToClaimOfferId):
                                    try: llamaTier = reqPopulateLlamas['profileChanges'][0]['profile']['items'][key]['attributes']['highest_rarity']
                                    except: llamaTier = 0
                                    llamaTier = stringList['Llama tiers'][f'{llamaTier}'][getConfig('Language')]
                            reqBuyFreeLlama = requestText(request("post", links.profileRequest.format(auth.accountId, "PurchaseCatalogEntry", "common_core"), headers=auth.headers, json={"offerId": llamaToClaimOfferId, "purchaseQuantity": 1, "currency": "GameItem", "currencySubType": "AccountResource:currency_xrayllama", "expectedTotalPrice": 0, "gameContext": "Frontend.None"}), False)
                            if "errorMessage" in reqBuyFreeLlama:
                                if "limit of" in reqBuyFreeLlama['errorMessage']:
                                    if openedLlamas == 0: alreadyOpenedFreeLlamas += 1
                                if "because fulfillment" in reqBuyFreeLlama['errorMessage']: message(getString("main.freellamas.cantclaim").format(auth.displayName, llamaToClaimTitle))
                                break
                            else:
                                message(getString("main.freellamas.start").format(llamaToClaimName, llamaTier))
                                llamaLoot, llamaLootCount = [reqBuyFreeLlama['notifications'][0]['lootResult']['items'], 0]
                                openedLlamas += 1
                                for key in llamaLoot:
                                    templateId, itemGuid, itemQuantity = [key['itemType'], key['itemGuid'], key['quantity']]
                                    try: itemName = stringList['Items'][templateId]['name'][getConfig('Items_Language')]
                                    except: itemName = templateId
                                    try: itemRarity, itemType = [stringList['Items'][templateId]['rarity'], stringList['Items'][templateId]['type']]
                                    except: itemRarity, itemType = ["Unknown rarity", "Unknown type"]
                                    llamaLootCount += 1
                                    if itemRarity in ("common", "uncommon", "rare", "epic"): itemsfromLlamas.append({"itemName": itemName, "itemType": itemType, "templateId": templateId, "itemGuid": itemGuid, "itemRarity": itemRarity, "itemQuantity": itemQuantity})
                                    try: message(f"{llamaLootCount}: {stringList['Item Rarities'][stringList['Items'][templateId]['rarity']][getConfig('Items_Language')]} | {stringList['Item Types'][stringList['Items'][templateId]['type']][getConfig('Items_Language')]}: {itemQuantity}x {itemName}")
                                    except: message(f"{llamaLootCount}: {itemRarity} | {itemType}: {itemQuantity}x {itemName}")
                    if int(alreadyOpenedFreeLlamas) == freeLlamasCount: message(getString("main.freellamas.alreadyclaimed"))
                    else:
                        freeLlamasWord = getPluralWord("freeLlamas", int(openedLlamas))
                        if openedLlamas > 0: message(getString("main.freellamas.success").format(openedLlamas, freeLlamasWord))

        # Automatically recycle selected llama loot.
        if bRecycle and int(alreadyOpenedFreeLlamas) != freeLlamasCount:
            itemsToRecycle = [item for item in itemsfromLlamas if item['itemRarity'] in autoRecycling.itemRarities.get(item['itemType'], [])]
            itemGuidsToRecycle = [item['itemGuid'] for item in itemsToRecycle]
            recycleResources, recycledItemsCount, recycleResourcesCount = [[], 0, 0]
            if not auth.bRecyclingUnlocked: message(getString("main.recycle.unavailable"))
            elif len(itemGuidsToRecycle) != 0:
                freeLlamasWord = getPluralWord("freeLlamasRecycle", openedLlamas)
                message(getString("main.recycle.start").format(openedLlamas, freeLlamasWord))
                reqGetResources = requestText(request("post", links.profileRequest.format(auth.accountId, "QueryProfile", "campaign"), headers=auth.headers, data="{}"), True)
                for resource in autoRecycling.recycleResources:
                    for item in reqGetResources['profileChanges'][0]['profile']['items']:
                        if reqGetResources['profileChanges'][0]['profile']['items'][item]['templateId'] == resource: recycleResources.append({"itemGuid": item, "templateId": resource, "itemName": stringList['Items'][resource]['name'][getConfig('Items_Language')], "quantity": reqGetResources['profileChanges'][0]['profile']['items'][item]['quantity']})
                requestText(request("post", links.profileRequest.format(auth.accountId, "RecycleItemBatch", "campaign"), headers=auth.headers, json={"targetItemIds": itemGuidsToRecycle}), True)
                recycleMessage = getString("main.recycle.message")
                for item in itemsToRecycle:
                    recycledItemsCount += 1
                    recycleMessage += f"{recycledItemsCount}: {stringList['Item Rarities'][item['itemRarity']][getConfig('Items_Language')]} | {stringList['Item Types'][item['itemType']][getConfig('Items_Language')]}: {item['itemQuantity']}x {item['itemName']}\n"
                message(f"{recycleMessage}")
                reqGetResources2 = requestText(request("post", links.profileRequest.format(auth.accountId, "QueryProfile", "campaign"), headers=auth.headers, data="{}"), True)
                resourcesMessage = getString("main.recycle.resources")
                for resource in recycleResources:
                    resourceQuantity = int(reqGetResources2['profileChanges'][0]['profile']['items'][resource['itemGuid']]['quantity']) - int(resource['quantity'])
                    if resourceQuantity > 0:
                        recycleResourcesCount += 1
                        resourcesMessage += f"{recycleResourcesCount}: {resourceQuantity}x {resource['itemName']}. {getString('main.recycle.totalamount').format(reqGetResources2['profileChanges'][0]['profile']['items'][resource['itemGuid']]['quantity'])}\n"
                message(f"{resourcesMessage}")

# Start the program.
if getConfig('Check_For_Updates'): checkUpdate()
if not getConfig('Skip_Main_Menu'): menu()
while True:
    t1 = datetime.now()
    main()
    t2 = datetime.now()
    if getConfig('Loop_Minutes') > 0:
        loopMinutes = int(getConfig('Loop_Minutes')) if str(getConfig('Loop_Minutes')).endswith(".0") else getConfig('Loop_Minutes')
        minutesWord = getPluralWord("minutes", loopMinutes)
        totalSecondsToSleep = max(1, loopMinutes * 60 - (t2 - t1).total_seconds())
        print(getString("loop.message").format(loopMinutes, minutesWord, nextrun(totalSecondsToSleep)))
        time.sleep(totalSecondsToSleep)
    else:
        if getConfig('Skip_Main_Menu'): break
        whatToDo = validInput(getString("noloop.input"), ["0", ""])
        if not whatToDo: break
        menu()

exit()
