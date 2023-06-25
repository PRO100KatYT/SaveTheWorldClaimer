version = "1.12.0"
configVersion = "1.10.1"
print(f"Fortnite Save the World Claimer v{version} by PRO100KatYT\n")

import os
import sys
import subprocess
import json
from configparser import ConfigParser
from datetime import datetime, timedelta
import webbrowser
import time
if os.name == "nt": os.system(f"title Fortnite Save the World Claimer")
try: from requests import Session
except ImportError:
    print(f"The program will now try to install the requests module.\n")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    if os.name == 'posix': os.system('clear')
    else: os.system('cls')
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])


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

# Start a new requests session.
session = Session()

# Default bShowDateTime value.
bShowDateTime = "false"

# Get the current date and time and neatly format it | by Salty-Coder :)
def getDateTimeString():
    dateTimeObj = datetime.now()
    return f"[{dateTimeObj.year:04d}/{dateTimeObj.month:02d}/{dateTimeObj.day:02d} {dateTimeObj.hour:02d}:{dateTimeObj.minute:02d}:{dateTimeObj.second:02d}]"

# Get the next time program is going to run by Salty-Coder
def nextrun(loopMinutes):
    now = datetime.now()
    nextrun = now + timedelta(minutes = loopMinutes)
    return f"{nextrun.year:04d}/{nextrun.month:02d}/{nextrun.day:02d} {nextrun.hour:02d}:{nextrun.minute:02d}:{nextrun.second:02d}"

# Load the stringlist.json file.
stringListPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "stringlist.json")
if not os.path.exists(stringListPath):
    input("ERROR: The stringlist.json file doesn't exist. Get it from this program's repository on GitHub (https://github.com/PRO100KatYT/SaveTheWorldClaimer), add it back and run this program again.\n\nPress ENTER to close the program.\n")
    exit()
try: stringList = json.loads(open(stringListPath, "r", encoding = "utf-8").read())
except:
    input("ERROR: The program is unable to read the stringlist.json file. Delete the stringlist.json file, download it from this program's repository on GitHub (https://github.com/PRO100KatYT/SaveTheWorldClaimer), add it back here and run this program again.\n\nPress ENTER to close the program.\n")
    exit()

# Get a string in currently selected language.
def getString(string):
    try: return stringList['Strings'][language][f'{string}']
    except: return stringList['Strings']['en'][f'{string}']

# Get a correct plural word depending on the int.
def getPluralWord(string, number):
    if number == 1: plural = 'one'
    elif 2 <= number < 5: plural = 'few'
    elif number == 0 or number >= 5: plural = 'many'
    else: plural = 'other'
    try: return stringList['Strings'][language]['words'][string][plural]
    except KeyError: return stringList['Strings']['en']['words'][string][plural]

# Error with a custom message.
def customError(text):
    if bShowDateTime == "true": input(f"{getDateTimeString()} {getString('customerror.message').format(text)}")
    else: input(getString('customerror.message').format(text))
    exit()

# Error for invalid config values.
def configError(key, value, validValues): customError(getString("configerror.message").format(key, value, validValues))

# Input loop until it's one of the correct values.
def validInput(text, values):
    while True:
        response = input(f"{text}\n").lower()
        if values == "digit" and response.replace(",", ".").replace(".", "").isdigit(): break
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
    count = 0
    while True:
        count += 1
        if count > 1: loginLink = altLoginLink
        webbrowser.open_new_tab(loginLink)
        print(getString("reqtoken.message").format(loginLink))
        reqToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": f"basic {authHeader}"}, data={"grant_type": "authorization_code", "code": input(getString("reqtoken.insertcode"))}), False)
        if not "errorMessage" in reqToken: break
        else: input(getString("reqtoken.error").format(reqToken['errorMessage']))
    return reqToken

# Print a message with or without the date and time.
def message(string):
    if bShowDateTime == "true":
        string = string.replace("\n", "\n"+" "*((len(getDateTimeString()))+1))
        print(f"{getDateTimeString()} {string}")
    else: print(string)

# Create and/or read the config.ini file.
config, configPath = [ConfigParser(), os.path.join(os.path.split(os.path.abspath(__file__))[0], "config.ini")]
itemLangValues, langValues, boolValues = [["ar", "de", "en", "es", "es-419", "fr", "it", "ja", "ko", "pl", "pt-BR", "ru", "tr", "zh-CN", "zh-Hant"], ["en", "pl"], ["true", "false"]]
if not os.path.exists(configPath):
    message(getString("config.startgenerating"))
    bStartSetup = validInput(getString("config.bstartsetup"), ["1", "2"])
    if bStartSetup == "1":
        iLanguage = language = validInput(getString("config.setup.language").format(', '.join(langValues)), langValues)
        iItemsLanguage = validInput(getString("config.setup.itemslanguage").format(', '.join(itemLangValues)), itemLangValues)
        iSpend_Research_Points = validInput(getString("config.setup.researchpoints"), ["off", "lowest", "everyten"])
        iOpen_Free_Llamas = validInput(getString("config.setup.freellamas"), boolValues)
        bAutomaticRecycle = validInput(getString("config.setup.brecycle"), boolValues)
        if bAutomaticRecycle == "false": iRecycle_Weapons = iRecycle_Traps = iRetire_Survivors = iRetire_Defenders = iRetire_Heroes = "off"
        else:
            iList = []
            itemTypeJson = {"Recycle_Weapons": {"name": getString("config.setup.recycle.weapon"), "recycleWord": getString("config.setup.recycle.recycleword")}, "Recycle_Traps": {"name": getString("config.setup.recycle.trap"), "recycleWord": getString("config.setup.recycle.recycleword")}, "Recycle_Survivors": {"name": getString("config.setup.recycle.survivor"), "recycleWord": getString("config.setup.recycle.retireword")}, "Recycle_Defenders": {"name": getString("config.setup.recycle.defender"), "recycleWord": getString("config.setup.recycle.retireword")}, "Recycle_Heroes": {"name": getString("config.setup.recycle.hero"), "recycleWord": getString("config.setup.recycle.retireword")}}
            for itemType in itemTypeJson: iList.append(validInput(getString("config.setup.recycle.message").format(itemTypeJson[itemType]['name'], itemTypeJson[itemType]['recycleWord']), ["off", "common", "uncommon", "rare", "epic"]))
            iRecycle_Weapons, iRecycle_Traps, iRetire_Survivors, iRetire_Defenders, iRetire_Heroes = iList  
        iSkip_Tutorial = validInput(getString("config.setup.bskiptutorial"), boolValues)
        iLoop_Time = validInput(getString("config.setup.looptime"), "digit")
        iShow_Date_Time = validInput(getString("config.setup.datetime"), boolValues)
    else: iLanguage, iItemsLanguage, iSpend_Research_Points, iOpen_Free_Llamas, iRecycle_Weapons, iRecycle_Traps, iRetire_Survivors, iRetire_Defenders, iRetire_Heroes, iSkip_Tutorial, iLoop_Time, iShow_Date_Time = ["en", "en", "lowest", "true", "uncommon", "uncommon", "rare", "rare", "uncommon", "false", 0, "false"]           
    with open(configPath, "w") as configFile: configFile.write(getString("config.configfile").format(', '.join(langValues), iLanguage, ', '.join(itemLangValues), iItemsLanguage, iSpend_Research_Points, iOpen_Free_Llamas, iSkip_Tutorial, iRecycle_Weapons, iRecycle_Traps, iRetire_Survivors, iRetire_Defenders, iRetire_Heroes, iLoop_Time, iShow_Date_Time, configVersion))
    print(getString("config.setup.success"))
config.read(configPath)
try: configVer = config['Config_Version']['Version']
except: customError(getString("config.readerror"))
if configVer != f"STWC_{configVersion}": customError(getString("config.versionerror"))
try:
    language, itemsLang, spendAutoResearch, bOpenFreeLlamas, bSkipTutorial, loopMinutes, bShowDateTime, bSkipMainMenu = [config['StW_Claimer_Config']['Language'].lower(), config['StW_Claimer_Config']['ItemsLanguage'].lower(), config['StW_Claimer_Config']['Spend_Research_Points'].lower(), config['StW_Claimer_Config']['Open_Free_Llamas'].lower(), config['StW_Claimer_Config']['Skip_Tutorial'].lower(), config['Loop']['Loop_Minutes'], config['Misc']['Show_Date_Time'].lower(), config['Misc']['Skip_Main_Menu'].lower()]
    autoRecycling.itemRarities = {"weapon": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Recycle_Weapons'].lower()].split(", "), "trap": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Recycle_Traps'].lower()].split(", "), "survivor": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Retire_Survivors'].lower()].split(", "), "defender": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Retire_Defenders'].lower()].split(", "), "hero": autoRecycling.rarities[config['Automatic_Recycle/Retire']['Retire_Heroes'].lower()].split(", ")}
except: customError(getString("config.readerror"))
checkValuesJson = {"Language": {"value": language, "validValues": langValues}, "ItemsLanguage": {"value": itemsLang, "validValues": itemLangValues}, "Spend_Research_Points": {"value": spendAutoResearch, "validValues": ["off", "lowest", "everyten"]}, "Open_Free_Llamas": {"value": bOpenFreeLlamas, "validValues": boolValues}, "Skip_Tutorial": {"value": bSkipTutorial, "validValues": boolValues}, "Show_Date_Time": {"value": bShowDateTime, "validValues": boolValues}, "Skip_Main_Menu": {"value": bSkipMainMenu, "validValues": boolValues}}
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
except: configError("Loop_Minutes", loopMinutes, getString("config.error.number"))

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
        if authType == "token":
            reqRefreshToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "refresh_token", "refresh_token": refreshToken}), False)
            if "errorMessage" in reqRefreshToken: customError(getString("main.login.token.error").format(displayName))
            account['refreshToken'], account['refresh_expires_at'] = reqRefreshToken["refresh_token"], reqRefreshToken["refresh_expires_at"]
            with open(authPath, "w", encoding="utf-8") as saveAuthFile: json.dump(authJson, saveAuthFile, indent=2, ensure_ascii=False)
            reqExchange = requestText(session.get(links.getOAuth.format("exchange"), headers={"Authorization": f"bearer {reqRefreshToken['access_token']}"}, data={"grant_type": "authorization_code"}), True)
            reqToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "exchange_code", "exchange_code": reqExchange["code"], "token_type": "eg1"}), True)
        elif authType == "device": reqToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "device_auth", "device_id": deviceId, "account_id": accountId, "secret": secret, "token_type": "eg1"}), True)
        accessToken, displayName = reqToken['access_token'], reqToken['displayName']
        message(getString("main.login.success"))

        # Headers for MCP requests.
        headers = {"User-Agent": "Fortnite/++Fortnite+Release-19.40-CL-19215531 Windows/10.0.19043.1.768.64bit", "Authorization": f"bearer {accessToken}", "Content-Type": "application/json"}

        # Check whether the account has the campaign access token and is able to receive V-Bucks.
        # The receivemtxcurrency token is not required, but if it's not in the profile, the account will receive X-Ray Tickets instead of V-Bucks.
        reqQueryProfiles = [json.dumps(requestText(session.post(links.profileRequest.format(accountId, "QueryProfile", "common_core"), headers=headers, data="{}"), False)), json.dumps(requestText(session.post(links.profileRequest.format(accountId, "ClientQuestLogin", "campaign"), headers=headers, data="{}"), False))]
        campaignProfile = json.loads(reqQueryProfiles[1])['profileChanges'][0]['profile']
        bReceiveMtx = False
        if "Token:receivemtxcurrency" in reqQueryProfiles[1]: bReceiveMtx = True

        self.headers, self.accountId, self.displayName, self.campaignProfile, self.bReceiveMtx = headers, accountId, displayName, campaignProfile, bReceiveMtx

# Get an account's Daily Quests
def getDailyQuests(auth):
    questNumber = 0
    questData = {}
    for item in auth.campaignProfile['items']:
        itemData = auth.campaignProfile['items'][item]
        if itemData['templateId'].lower().startswith("quest:daily_") and itemData['attributes']['quest_state'].lower() == "active":
            templateId = itemData['templateId']
            questName = stringList['Items'][templateId]['name'][itemsLang]
            objectives = stringList['Items'][templateId]['objectives']
            progressMess = ""
            for objective in objectives:
                objData = objectives[objective]
                objName, objCount = objData['name'][itemsLang], objData['count']
                completionCount = itemData['attributes'].get(f'completion_{objective}', 0)
                progressMess += f" {completionCount}/{objCount} {objName},"
            progressMess = progressMess[:-1]
            rewards = stringList['Items'][templateId]['rewards']
            rewardsMess = ""
            for reward in rewards:
                rewardQuantity, rewardName = [rewards[reward], stringList['Items'][reward]['name'][itemsLang]]
                if reward.startswith("ConditionalResource:"):
                    if auth.bReceiveMtx == True: rewardsMess += f" {rewardQuantity}x {rewardName['PassedConditionItem']},"
                    rewardName = rewardName['FailedConditionItem']
                rewardsMess += f" {rewardQuantity}x {rewardName},"
            rewardsMess = rewardsMess[:-1]
            questNumber += 1
            questData[item] = {"templateId": templateId, "questNumber": questNumber, "questName": questName, "progress": progressMess, "rewards": rewardsMess}
    return questData

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
            jsonToAppend = {getString("authjson.warning.header"): getString("authjson.warning.text"), "authType": "token", "refreshToken": refreshToken, "accountId": accountId, "displayName": displayName, "refresh_expires_at": expirationDate}
        else:
            reqToken = reqTokenText(loginLink.format("3446cd72694c4a4485d81b77adbb2141"), links.loginLink1.format("3446cd72694c4a4485d81b77adbb2141"), "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=")
            accessToken, accountId, displayName = [reqToken["access_token"], reqToken["account_id"], reqToken["displayName"]]
            reqDeviceAuth = requestText(session.post(links.getDeviceAuth.format(accountId), headers={"Authorization": f"bearer {accessToken}"}, data={}), True)
            deviceId, secret = [reqDeviceAuth["deviceId"], reqDeviceAuth["secret"]]
            jsonToAppend = {getString("authjson.warning.header"): getString("authjson.warning.text"), "authType": "device",  "deviceId": deviceId, "accountId": accountId, "displayName": displayName, "secret": secret}
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
                    for quest in questData: print(getString("startup.managedailyquests.info").format(questData[quest]['questNumber'], questData[quest]['questName'], questData[quest]['progress'], questData[quest]['rewards']))
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
                            reqRerollQuest = requestText(session.post(links.profileRequest.format(auth.accountId, "FortRerollDailyQuest", "campaign"), headers=auth.headers, json={"questId": questToReplace}), True)
                            newQuestTemplateId = reqRerollQuest.get("notifications", [{}])[0].get("newQuestId")
                            if newQuestTemplateId:
                                newQuestName = stringList['Items'].get(newQuestTemplateId, {}).get('name', {}).get(itemsLang, newQuestTemplateId)
                                print(getString("startup.managedailyquests.success").format(questData[questToReplace]['questName'], newQuestName))
                                input(getString("startup.managedailyquests.pressenter"))

    while True:
        if not authJson: addAccount(False)
        bStartClaimer = validInput(getString("mainmenu.message"), ["1", "2", "3", "4"])
        if bStartClaimer == "1": break
        elif bStartClaimer == "2": manageDailyQuests()
        elif bStartClaimer == "3":
            while True:
                whatToDo = validInput(getString("accountmanager.message"), ["1", "2", "3", "4"])
                if whatToDo == "1": addAccount()
                elif whatToDo == "2": removeAccount()
                elif whatToDo == "3":
                    listAccounts()
                    input(getString("accountmanager.pressenter"))
                else: break
        else: exit()

# The main part of the program that can be looped.
def main():
    for account in authJson:
        auth = login(account)
        
        # Skip the StW tutorial if it hasn't been completed yet. Works for accounts that don't own StW too. It will get the account the StW music pack.
        if bSkipTutorial == "true":
            for item in auth.campaignProfile['items']:
                if auth.campaignProfile['items'][item]['templateId'].lower() != "quest:homebaseonboarding": continue
                if auth.campaignProfile['items'][item]['attributes']['quest_state'].lower() == "claimed": break
                message(getString("main.skiptutorial.start").format(auth.displayName))
                session.post(links.profileRequest.format(auth.accountId, "SkipTutorial", "campaign"), headers=auth.headers, data="{}")
                reqUpdateObjectives = requestText(session.post(links.profileRequest.format(auth.accountId, "UpdateQuestClientObjectives", "campaign"), headers=auth.headers, json={"advance": [{"statName": "hbonboarding_watchsatellitecine", "count": 1, "timestampOffset": 0}, {"statName": "hbonboarding_namehomebase", "count": 1, "timestampOffset": 0}]}), True)
                if reqUpdateObjectives['profileChanges'][0]['profile']['items'][item]['attributes']['quest_state'].lower() == "claimed": message(getString("main.skiptutorial.success").format(auth.displayName))
                else: message(getString("main.skiptutorial.error").format(auth.displayName))
                break

        # Display current daily challenges, their rewards and progress if there is any.
        message(getString("main.dailies.searching"))
        questData = getDailyQuests(auth)
        if not questData: message(getString("main.dailies.notfound"))
        for quest in questData: message(getString("main.dailies.info").format(questData[quest]['questNumber'], questData[quest]['questName'], questData[quest]['progress'], questData[quest]['rewards']))

        # Claim and automatically spend the Research Points.
        reqCampaignProfileCheck = requestText(session.post(links.profileRequest.format(auth.accountId, "QueryProfile", "campaign"), headers=auth.headers, data="{}"), True)
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
                reqClaimCollectedResources = requestText(session.post(links.profileRequest.format(auth.accountId, "ClaimCollectedResources", "campaign"), headers=auth.headers, json={"collectorsToClaim": [tokenToClaim]}), False)
                if "errorMessage" in reqClaimCollectedResources: message(getString("main.research.error").format(reqClaimCollectedResources['errorMessage'])) # Error without exit()
                else:
                    storedMaxPoints = False
                    try:
                        totalItemGuid, rpToClaim = [reqClaimCollectedResources['notifications'][0]['loot']['items'][0]['itemGuid'], reqClaimCollectedResources['profileChanges'][0]['profile']['items'][tokenToClaim]['attributes']['stored_value']]
                        rpStored, rpClaimedQuantity = [reqClaimCollectedResources['profileChanges'][0]['profile']['items'][totalItemGuid]['quantity'], int(reqClaimCollectedResources['notifications'][0]['loot']['items'][0]['quantity'])]
                        if float(rpToClaim) >= 1:
                            storedMaxPoints = True
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

                    if storedMaxPoints == True:
                        if spendAutoResearch == "off": message(getString("main.research.max.off").format(round(rpToClaim, 2), rpStored))
                        else:
                            message(getString("main.research.max.on").format(rpStored))
                            while True:
                                reqFORTLevelsCheck = {**{"fortitude": 0, "offense": 0, "resistance": 0, "technology": 0}, **requestText(session.post(links.profileRequest.format(auth.accountId, "QueryProfile", "campaign"), headers=auth.headers, data="{}"), True)['profileChanges'][0]['profile']['stats']['attributes']['research_levels']}
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
                                reqPurchaseResearchStatUpgrade = requestText(session.post(links.profileRequest.format(auth.accountId, "PurchaseResearchStatUpgrade", "campaign"), headers=auth.headers, json={"statId": f'{statToClaim}'}), False)
                                statName = stringList['Strings'][language]['researchStats'][f'{statToClaim}']
                                if "errorMessage" in reqPurchaseResearchStatUpgrade: break # Error without exit()
                                else: message(getString("main.research.spend.success").format(statName, reqPurchaseResearchStatUpgrade['profileChanges'][0]['profile']['stats']['attributes']['research_levels'][statToClaim]))
                            message(getString("main.research.spend.end"))
                            reqClaimCollectedResources = requestText(session.post(links.profileRequest.format(auth.accountId, "ClaimCollectedResources", "campaign"), headers=auth.headers, json={"collectorsToClaim": [tokenToClaim]}), True)
                            try:
                                totalItemGuid = reqClaimCollectedResources['notifications'][0]['loot']['items'][0]['itemGuid']
                                message(getString("main.research.success").format(reqClaimCollectedResources['notifications'][0]['loot']['items'][0]['quantity'], reqClaimCollectedResources['profileChanges'][0]['profile']['items'][totalItemGuid]['quantity']))
                            except: pass

        # Search for free Llamas and open them if they're available.
        alreadyOpenedFreeLlamas, freeLlamasCount, cpspStorefront = [0, 0, []]
        if bOpenFreeLlamas == "true":
            reqGetStorefront = requestText(session.get(links.getStorefront, headers=auth.headers, data={}), True)['storefronts']
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
                        try: llamaToClaimName = stringList['Items'][llamaToClaimCPId]['name'][itemsLang]
                        except:
                            if llamaToClaimTitle: llamaToClaimName = llamaToClaimTitle
                        if not llamaToClaimName: llamaToClaimName = llamaToClaimCPId
                        while True:
                            reqPopulateLlamas = requestText(session.post(links.profileRequest.format(auth.accountId, "PopulatePrerolledOffers", "campaign"), headers=auth.headers, data="{}"), True)
                            for key in reqPopulateLlamas['profileChanges'][0]['profile']['items']:
                                if (reqPopulateLlamas['profileChanges'][0]['profile']['items'][key]['templateId'].lower().startswith("prerolldata") and reqPopulateLlamas['profileChanges'][0]['profile']['items'][key]['attributes']['offerId'] == llamaToClaimOfferId):
                                    try: llamaTier = reqPopulateLlamas['profileChanges'][0]['profile']['items'][key]['attributes']['highest_rarity']
                                    except: llamaTier = 0
                                    llamaTier = stringList['Llama tiers'][f'{llamaTier}'][language]
                            reqBuyFreeLlama = requestText(session.post(links.profileRequest.format(auth.accountId, "PurchaseCatalogEntry", "common_core"), headers=auth.headers, json={"offerId": llamaToClaimOfferId, "purchaseQuantity": 1, "currency": "GameItem", "currencySubType": "AccountResource:currency_xrayllama", "expectedTotalPrice": 0, "gameContext": "Frontend.None"}), False)
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
                                    try: itemName = stringList['Items'][templateId]['name'][itemsLang]
                                    except: itemName = templateId
                                    try: itemRarity, itemType = [stringList['Items'][templateId]['rarity'], stringList['Items'][templateId]['type']]
                                    except: itemRarity, itemType = ["Unknown rarity", "Unknown type"]
                                    llamaLootCount += 1
                                    if itemRarity in ("common", "uncommon", "rare", "epic"): itemsfromLlamas.append({"itemName": itemName, "itemType": itemType, "templateId": templateId, "itemGuid": itemGuid, "itemRarity": itemRarity, "itemQuantity": itemQuantity})
                                    try: message(f"{llamaLootCount}: {stringList['Item Rarities'][stringList['Items'][templateId]['rarity']][itemsLang]} | {stringList['Item Types'][stringList['Items'][templateId]['type']][itemsLang]}: {itemQuantity}x {itemName}")
                                    except: message(f"{llamaLootCount}: {itemRarity} | {itemType}: {itemQuantity}x {itemName}")
                    if int(alreadyOpenedFreeLlamas) == freeLlamasCount: message(getString("main.freellamas.alreadyclaimed"))
                    else:
                        freeLlamasWord = getPluralWord("freeLlamas", int(openedLlamas))
                        if openedLlamas > 0: message(getString("main.freellamas.success").format(openedLlamas, freeLlamasWord))

        # Automatically recycle selected llama loot.
        if (recycleOn) and (int(alreadyOpenedFreeLlamas) != freeLlamasCount):
            itemsToRecycle = [item for item in itemsfromLlamas if item['itemRarity'] in autoRecycling.itemRarities.get(item['itemType'], [])]
            itemGuidsToRecycle = [item['itemGuid'] for item in itemsToRecycle]
            recycleResources, recycledItemsCount, recycleResourcesCount = [[], 0, 0]
            if len(itemGuidsToRecycle) != 0:
                freeLlamasWord = getPluralWord("freeLlamasRecycle", openedLlamas)
                message(getString("main.recycle.start").format(openedLlamas, freeLlamasWord))
                reqGetResources = requestText(session.post(links.profileRequest.format(auth.accountId, "QueryProfile", "campaign"), headers=auth.headers, data="{}"), True)
                for resource in autoRecycling.recycleResources:
                    for item in reqGetResources['profileChanges'][0]['profile']['items']:
                        if reqGetResources['profileChanges'][0]['profile']['items'][item]['templateId'] == resource: recycleResources.append({"itemGuid": item, "templateId": resource, "itemName": stringList['Items'][resource]['name'][itemsLang], "quantity": reqGetResources['profileChanges'][0]['profile']['items'][item]['quantity']})
                requestText(session.post(links.profileRequest.format(auth.accountId, "RecycleItemBatch", "campaign"), headers=auth.headers, json={"targetItemIds": itemGuidsToRecycle}), True)
                recycleMessage = getString("main.recycle.message")
                for item in itemsToRecycle:
                    recycledItemsCount += 1
                    recycleMessage += f"{recycledItemsCount}: {stringList['Item Rarities'][item['itemRarity']][itemsLang]} | {stringList['Item Types'][item['itemType']][itemsLang]}: {item['itemQuantity']}x {item['itemName']}\n"
                message(f"{recycleMessage}")
                reqGetResources2 = requestText(session.post(links.profileRequest.format(auth.accountId, "QueryProfile", "campaign"), headers=auth.headers, data="{}"), True)
                resourcesMessage = getString("main.recycle.resources")
                for resource in recycleResources:
                    resourceQuantity = int(reqGetResources2['profileChanges'][0]['profile']['items'][resource['itemGuid']]['quantity']) - int(resource['quantity'])
                    if resourceQuantity > 0:
                        recycleResourcesCount += 1
                        resourcesMessage += f"{recycleResourcesCount}: {resourceQuantity}x {resource['itemName']}. {getString('main.recycle.totalamount').format(reqGetResources2['profileChanges'][0]['profile']['items'][resource['itemGuid']]['quantity'])}\n"
                message(f"{resourcesMessage}")

# Start the program.
if bSkipMainMenu == "false": menu()
if loopMinutes > 0:
    while True:
        main()
        if str(loopMinutes).endswith(".0"): loopMinutes = int(str(loopMinutes).split(".")[0])
        minutesWord = getPluralWord("minutes", loopMinutes)
        print(getString("loop.message").format(loopMinutes, minutesWord, nextrun(loopMinutes)))
        time.sleep(loopMinutes * 60)
else: main()

input(getString("exit.pressenter"))
exit()
