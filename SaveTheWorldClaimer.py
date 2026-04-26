versionNum = 43
versionStr = "1.16.0"
configVersion = "1.16.0"
print(f"Save the World Claimer v{versionStr} by PRO100KatYT\n")

# Save the World Claimer
# Copyright (C) 2026 PRO100KatYT
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import subprocess
import json
from configparser import ConfigParser
from datetime import datetime, timedelta, timezone
import webbrowser
import time
import shutil
import argparse
from threading import Thread
if os.name == "nt": os.system("title Save the World Claimer")
else: print("\033]0;Save the World Claimer\007", end='', flush=True) # This is for window title for Linux and macOS.
try: import requests
except ImportError:
    print("The program will now try to install the requests module.\n")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    if os.name == 'posix': os.system('clear')
    else: os.system('cls')
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
    sys.exit(1)

# Default program language value.
language = "en"

# Links that will be used in the later part of code.
class links:
    loginLink1 = "https://www.epicgames.com/id/api/redirect?clientId={0}&responseType=code"
    loginLink2 = "https://www.epicgames.com/id/logout?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253D{0}%2526responseType%253Dcode"
    getOAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/{0}"
    getDeviceAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{0}/deviceAuth"
    getStorefront = "https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/storefront/v2/catalog"
    profileRequest = "https://mcp-gc.live.fngw.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/{1}?profileId={2}"

# Automatic llama loot recycling variables.
class autoRecycling:
    rarities = {"off": "", "common": "common", "uncommon": "common, uncommon", "rare": "common, uncommon, rare", "epic": "common, uncommon, rare, epic"}
    itemRarities = []
    recycleResources = ["AccountResource:peoplexp", "AccountResource:heroxp", "AccountResource:personnelxp", "AccountResource:phoenixxp", "AccountResource:phoenixxp_reward", "AccountResource:reagent_alteration_ele_fire", "AccountResource:reagent_alteration_ele_nature", "AccountResource:reagent_alteration_ele_water", "AccountResource:reagent_alteration_gameplay_generic", "AccountResource:reagent_alteration_generic", "AccountResource:reagent_alteration_upgrade_r", "AccountResource:reagent_alteration_upgrade_sr", "AccountResource:reagent_alteration_upgrade_uc", "AccountResource:reagent_alteration_upgrade_vr", "AccountResource:reagent_c_t01", "AccountResource:reagent_c_t02", "AccountResource:reagent_c_t03", "AccountResource:reagent_c_t04", "AccountResource:reagent_evolverarity_r", "AccountResource:reagent_evolverarity_sr", "AccountResource:reagent_evolverarity_vr", "AccountResource:reagent_people", "AccountResource:reagent_promotion_heroes", "AccountResource:reagent_promotion_survivors", "AccountResource:reagent_promotion_traps", "AccountResource:reagent_promotion_weapons", "AccountResource:reagent_traps", "AccountResource:reagent_weapons", "AccountResource:reagent_schematic", "AccountResource:schematicxp"]

# BR Winterfest event presents related variables.
class winterfest:
    rewardGraphId, nodesClaimingOrder = "", ["ERG.Node.A.3", "ERG.Node.A.4", "ERG.Node.A.5", "ERG.Node.A.6", "ERG.Node.A.7", "ERG.Node.A.8", "ERG.Node.A.9", "ERG.Node.A.2", "ERG.Node.A.10", "ERG.Node.A.11", "ERG.Node.A.12", "ERG.Node.B.1", "ERG.Node.A.13", "ERG.Node.A.1"]

# Get the base path depending on whether the program is compiled or not.
def getBasePath(bGetExePath = True):
    bIsCompiled = hasattr(sys, "frozen") or "__compiled__" in globals()
    if not bIsCompiled or not bGetExePath:  return os.path.dirname(os.path.abspath(__file__))
    if "APPIMAGE" in os.environ: return os.path.dirname(os.environ["APPIMAGE"])
    exePath = sys.executable if hasattr(sys, "frozen") else sys.argv[0]
    if not os.path.isabs(exePath): exePath = shutil.which(exePath) or os.path.abspath(exePath)
    baseDir = os.path.dirname(exePath)
    if sys.platform == "darwin" and "Contents/MacOS" in baseDir:
        baseDir = os.path.abspath(os.path.join(baseDir, "../../.."))
    return baseDir

# Set and get launch arguments.
parser = argparse.ArgumentParser(description="Fortnite STW Claimer for free Llamas, manager for your Daily Quests, Backpack items, and more.", add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help="Shows this help message and exits the program.")
parser.add_argument("-l", "--loop", type=float, default=0.0, metavar="<minutes>", help="Makes the program loop every X minutes.")
parser.add_argument("-sc", "--skip-to-claimer", action="store_true", help="Makes the program skip the Main Menu and go straight to the main program execution.")
parser.add_argument("-si", "--skip-to-invcleaner", action="store_true", help="Makes the program skip the Main Menu and go straight to the Inventory Junk Cleaner execution.")
parser.add_argument("-dssl", "--disable-ssl", action="store_true", help="Turns off SSL certificate verification after an error. Use this option at your own risk and only when really needed!")
args = parser.parse_args()

# Start a new requests session.
session = requests.Session()

# Send requests and retry if something goes wrong.
sendRequestErrorMsg = "An error occured when trying to send a \"{0}\" request to {1}.{2} Make sure you have a stable internet connection.\nRetrying in {3}s...\n" # It will later be overriden by the one from stringlist.json
bDisableSSLAfterError = args.disable_ssl
def request(method, url, headers=None, data=None, json=None):
    global sendRequestErrorMsg, bDisableSSLAfterError
    retries, secondsToWait = [0, 5]
    while True:
        try:
            if method == "get": req = session.get(url, headers=headers, data=data, json=json)
            elif method == "post": req = session.post(url, headers=headers, data=data, json=json)
        except requests.exceptions.SSLError:
            if bDisableSSLAfterError: # This option is skipped in the config setup and is not advised to be turned on for a longer period of time. This was made primarly for users who are running a packet sniffer in the background.
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                session.verify = False
                print("Turning off SSL certificate verification for this session due to an SSL error. The program should function normally.\n")
            continue
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
stringListPath = os.path.join(getBasePath(False), "stringlist.json")
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
        sys.exit(1)

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

# Return the power level of a weapon/trap.
def getItemPowerLevel(templateId, level):
    templateId = templateId.lower().replace("_crystal", "").replace("_ore", "")
    strToCheck = "_" + "_".join(templateId.lower().split("_")[-2:]).upper()
    if not strToCheck in stringList["Item Power Levels"]: return -1
    return stringList["Item Power Levels"][strToCheck][f"{level}"]

# Error with a custom message.
def customError(text):
    if bShowDateTime == "true": input(f"{getDateTimeString()} {getString('customerror.message').format(text)}")
    else: input(getString('customerror.message').format(text))
    sys.exit(1)

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

# Check if a newer version of this program is available.
def checkUpdate():
    try:
        getJson = (request("get", "https://raw.githubusercontent.com/PRO100KatYT/SaveTheWorldClaimer/main/SaveTheWorldClaimer.py").text).splitlines()[0:2]
        latestVerNum = int(getJson[0].split("=")[1].strip())
        latestVerStr = getJson[1].split("=")[1].strip().strip('"')
        if latestVerNum > versionNum: message(getString("updatechecker.message").format(latestVerStr))
    except: pass # If for some reason the program cannot check it then do nothing else

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
config, configPath = [ConfigParser(), os.path.join(getBasePath(), "config.ini")]
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
        configFileContent += f"# {getString('config.availableoptions').format(', '.join(str(item) for item in setting['validValues']).lower() if isinstance(setting['validValues'], list) else getString(setting['validValues']))}\n{setting['settingName']} = {str(value).lower() if setting['settingType'] in ['bool', 'string'] else value}\n\n"
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

# Check if the user config file exists. If not, then create it. And read the file.
userConfigPath = os.path.join(getBasePath(), "userConfig.json")
if not os.path.exists(userConfigPath):
    with open(userConfigPath, "w") as userConfigJson: userConfigJson.write("{}")
try: 
    with open(userConfigPath, "r", encoding="utf-8") as f: userConfigJson = json.loads(f.read())
except: customError(getString("userconfig.readerror"))

class perAccountConfig:
    def readOption(accountId, path):
        global userConfigJson
        obj = userConfigJson[accountId] if accountId in userConfigJson else None
        for key in path:
            try: obj = obj[key]
            except: return None
        return obj

    def setOption(accountId, path, value):
        global userConfigJson
        if not accountId in userConfigJson: userConfigJson[accountId] = {}
        obj = userConfigJson[accountId]
        for key in path[:-1]:
            try: obj = obj.setdefault(key, {})
            except: return False
        try:
            obj[path[-1]] = value
            return True
        except: return False

    def saveFile():
        global userConfigJson
        try:
            with open(userConfigPath, "w", encoding="utf-8") as saveConfigFile: json.dump(userConfigJson, saveConfigFile, indent=2, ensure_ascii=False)
            return True
        except: return False

    def readInput(typeToCheckFor):
        userInput = input().lower()
        if typeToCheckFor == "bool":
            if userInput == "y": return True
            if userInput == "n": return False
            return None
        elif typeToCheckFor == "int":
            try: return int(userInput)
            except ValueError: return None
        elif typeToCheckFor == "float":
            try: return float(userInput)
            except ValueError: return None
        return None
    
    def bHasAllConfigOptionsSet(accountId, configOptionsList):
        for option in configOptionsList:
            if perAccountConfig.readOption(accountId, option["optionPath"]) == None:
                return False
        return True

    def askSetupQuestionsAndSaveFile(accountId, configOptionsList):
        for option in configOptionsList:
            print(getString(option["question"]))
            userInput = perAccountConfig.readInput(option["settingType"])
            if userInput == None:
                userInput = option["defaultValue"]
                print(getString('userconifg.usingdefault'))
            while userInput not in option["validValues"]:
                if not option["validValues"]: break
                print(getString('userconfig.invalidinput'))
                userInput = perAccountConfig.readInput(option["settingType"])
            perAccountConfig.setOption(accountId, option["optionPath"], userInput)
        perAccountConfig.saveFile()

# Create and load the auth.json file.
authPath = os.path.join(getBasePath(), "auth.json")
if not os.path.exists(authPath):
    with open(authPath, "w") as authJson: authJson.write("[]")
try: 
    with open(authPath, "r", encoding="utf-8") as f: authJson = json.loads(f.read())
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
            reqRefreshToken = requestText(request("post", links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "refresh_token", "refresh_token": refreshToken}), False)
            if "errorMessage" in reqRefreshToken: customError(getString("main.login.token.error").format(displayName))
            account['refreshToken'], account['refresh_expires_at'] = reqRefreshToken["refresh_token"], reqRefreshToken["refresh_expires_at"]
            with open(authPath, "w", encoding="utf-8") as saveAuthFile: json.dump(authJson, saveAuthFile, indent=2, ensure_ascii=False)
            reqExchange = requestText(request("get", links.getOAuth.format("exchange"), headers={"Authorization": f"bearer {reqRefreshToken['access_token']}"}, data={"grant_type": "authorization_code"}), True)
            reqToken = requestText(request("post", links.getOAuth.format("token"), headers={"Authorization": "basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU"}, data={"grant_type": "exchange_code", "exchange_code": reqExchange["code"], "token_type": "eg1"}), True)
        elif authType == "device": reqToken = requestText(request("post", links.getOAuth.format("token"), headers={"Authorization": "basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU"}, data={"grant_type": "device_auth", "device_id": deviceId, "account_id": accountId, "secret": secret, "token_type": "eg1"}), True)
        accessToken, displayName = reqToken['access_token'], reqToken['displayName']
        message(getString("main.login.success"))

        # Headers for MCP requests.
        headers = {"User-Agent": "Fortnite/++Fortnite+Release-39.40-CL-50341043 Windows/10.0.26100.1.256.64bit", "Authorization": f"bearer {accessToken}", "Content-Type": "application/json", "X-EpicGames-Language": getConfig('Items_Language'), "Accept-Language": getConfig('Items_Language')}

        # Check whether the account has the campaign access token and if it's able to receive V-Bucks.
        reqQueryProfiles = [json.dumps(requestText(request("post", links.profileRequest.format(accountId, "QueryProfile", "common_core"), headers=headers, data="{}"), False)), json.dumps(requestText(request("post", links.profileRequest.format(accountId, "ClientQuestLogin", "campaign"), headers=headers, data="{}"), False)), json.dumps(requestText(request("post", links.profileRequest.format(accountId, "ClientQuestLogin", "athena"), headers=headers, data="{}"), False))]
        commonCoreProfile, campaignProfile, athenaProfile = json.loads(reqQueryProfiles[0])["profileChanges"][0]["profile"], json.loads(reqQueryProfiles[1])["profileChanges"][0]["profile"], json.loads(reqQueryProfiles[2])["profileChanges"][0]["profile"]
        bReceiveMTX = "Token:receivemtxcurrency" in reqQueryProfiles[1]

        ssd3QuestGUID, bRecyclingUnlocked = "", False
        for id in campaignProfile["items"]:
            templateId = campaignProfile["items"][id]["templateId"].lower()
            if templateId == "quest:outpostquest_t1_l3": ssd3QuestGUID = id
            elif templateId == "homebasenode:questreward_recyclecollection": bRecyclingUnlocked = True

        # Check whether the account is able to get Daily Quests
        bDailyQuestsUnlocked = False
        if ssd3QuestGUID:
            if "completion_complete_outpost_1_3" in campaignProfile["items"][ssd3QuestGUID]["attributes"]:
                if (campaignProfile["items"][ssd3QuestGUID]["attributes"]["completion_complete_outpost_1_3"] == 1
                    and campaignProfile["items"][ssd3QuestGUID]["attributes"]["quest_state"].lower() == "claimed"):
                    bDailyQuestsUnlocked = True

        # Check whether the account has the BR Winterfest Reward Graph item.
        winterfestRewardGraphID = next((id for id in athenaProfile["items"] if athenaProfile["items"][id]["templateId"].lower() == winterfest.rewardGraphId.lower()), "")

        self.headers, self.accountId, self.displayName, self.commonCoreProfile, self.campaignProfile, self.athenaProfile, self.bReceiveMTX, self.bDailyQuestsUnlocked, self.bRecyclingUnlocked, self.winterfestRewardGraphID = headers, accountId, displayName, commonCoreProfile, campaignProfile, athenaProfile, bReceiveMTX, bDailyQuestsUnlocked, bRecyclingUnlocked, winterfestRewardGraphID

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
                    if auth.bReceiveMTX == True: rewardsMsg += f" {rewardQuantity}x {rewardName['PassedConditionItem']},"
                    rewardName = rewardName['FailedConditionItem']
                rewardsMsg += f" {rewardQuantity}x {rewardName},"
            rewardsMsg = rewardsMsg[:-1]
            questNumber += 1
            questData[item] = {"templateId": templateId, "questNumber": questNumber, "questName": questName, "progress": progressMsg, "rewards": rewardsMsg}
    return questData

def loopSleep(t1, t2):
    loopMinutes = int(args.loop) if str(args.loop).endswith(".0") else args.loop
    minutesWord = getPluralWord("minutes", loopMinutes)
    totalSecondsToSleep = max(1, loopMinutes * 60 - (t2 - t1).total_seconds())
    print(getString("loop.message").format(loopMinutes, minutesWord, nextrun(totalSecondsToSleep)))
    time.sleep(totalSecondsToSleep)

class invJunkCleaner:
    tiers = {1: [], 2: ["t01"], 3: ["t01", "t02"], 4: ["t01", "t02", "t03"], 5: ["t01", "t02", "t03", "t04"], 6: ["t01", "t02", "t03", "t04", "t05"]};

    def isProfileLocked(theater0):
        if not "profileLockExpiration" in theater0: return [False, 0]
        lockExpirationDate = lockExpirationDate = datetime.fromisoformat(theater0["profileLockExpiration"].replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
        nowDate = datetime.now(timezone.utc)
        secondsDiff = (lockExpirationDate - nowDate).total_seconds()
        return [lockExpirationDate.date() >= nowDate.date(), secondsDiff]
    
    def makeBackpackSnapshot(theater0):
        existingItemGUIDS = ",".join([key for key in theater0["items"] if theater0["items"][key]["templateId"].lower().split(":")[0] in ["weapon", "trap"]])
        perAccountConfig.setOption(theater0["accountId"], ["invJunkCleaner", "backpackSnapshot"], existingItemGUIDS)
        perAccountConfig.saveFile()
        print(getString('junkcleaner.snapshot.success'))
    
    def findItems(theater0):
        itemGUIDsToRecycle, itemGUIDsToDestroy = [[], []]
        tierConfig = perAccountConfig.readOption(theater0["accountId"], ["invJunkCleaner", "tier"])
        powerLevelConfig = perAccountConfig.readOption(theater0["accountId"], ["invJunkCleaner", "powerLevel"])
        backpackSnapshot = perAccountConfig.readOption(theater0["accountId"], ["invJunkCleaner", "backpackSnapshot"]).split(",")
        for key in theater0["items"]:
            templateId, attributes, quantity = [theater0["items"][key]["templateId"], theater0["items"][key]["attributes"], theater0["items"][key]["quantity"]]
            itemType = templateId.lower().split(":")[0]
            if itemType == "ingredient":
                if templateId in stringList["Items"] and "tier" in stringList["Items"][templateId]:
                    if stringList["Items"][templateId]["tier"].lower() in invJunkCleaner.tiers[tierConfig]:
                        itemGUIDsToDestroy.append(key)
            elif (itemType in ["weapon", "trap"] and key not in backpackSnapshot and "level" in attributes):
                powerLevel = getItemPowerLevel(templateId, attributes["level"])
                if powerLevel < powerLevelConfig: itemGUIDsToRecycle.append({"itemId": key, "quantity": quantity})
        return [itemGUIDsToRecycle, itemGUIDsToDestroy]

    def recycleAndDestroy(auth, itemGUIDsToRecycle, itemGUIDsToDestroy):
        if (not itemGUIDsToRecycle) and (not itemGUIDsToDestroy):
            message(getString("junkcleaner.nothingfound"))
        if itemGUIDsToRecycle:
            message(getString("junkcleaner.recycling").format(len(itemGUIDsToRecycle), getPluralWord('items', len(itemGUIDsToRecycle))))
            reqRecycle = requestText(request("post", links.profileRequest.format(auth.accountId, "DisassembleWorldItems", "theater0"), headers=auth.headers, json={"targetItemIdAndQuantityPairs": itemGUIDsToRecycle}), False)
            if "errorCode" in reqRecycle:
                message(getString("junkcleaner.recycleerror").format(reqRecycle['errorMessage']))
                for item in itemGUIDsToRecycle: itemGUIDsToDestroy.append(item['itemId'])
        if itemGUIDsToDestroy:
            message(getString("junkcleaner.destroying").format(len(itemGUIDsToDestroy), getPluralWord('items', len(itemGUIDsToRecycle))))
            requestText(request("post", links.profileRequest.format(auth.accountId, "DestroyWorldItems", "theater0"), headers=auth.headers, json={"itemIds": itemGUIDsToDestroy}), True)
    
    def main(selectedAccounts):
        while True:
            t1 = datetime.now()
            for account in selectedAccounts:
                if not perAccountConfig.bHasAllConfigOptionsSet(account["accountId"], stringList["Config"]["perUserSettings"]["invJunkCleaner"]): continue
                print()
                auth = login(account)
                message(getString("junkcleaner.gettinginfo"))
                reqGetTheater0 = requestText(request("post", links.profileRequest.format(auth.accountId, "QueryProfile", "theater0"), headers=auth.headers, data="{}"), True)['profileChanges'][0]['profile']
                if not perAccountConfig.readOption(auth.accountId, ["invJunkCleaner", "backpackSnapshot"]):
                    invJunkCleaner.makeBackpackSnapshot(reqGetTheater0)
                isLocked = invJunkCleaner.isProfileLocked(reqGetTheater0)
                if isLocked[0]: message(getString("junkcleaner.profilelocked").format(auth.displayName))
                else:
                    itemGUIDsToRecycle, itemGUIDsToDestroy = invJunkCleaner.findItems(reqGetTheater0)
                    invJunkCleaner.recycleAndDestroy(auth, itemGUIDsToRecycle, itemGUIDsToDestroy)
            t2 = datetime.now()
            message(getString("junkcleaner.done"))
            if args.loop > 0: loopSleep(t1, t2)
            else: break

class itemShop:
    def getOffersPurchasesQuantities(auth, catalogEntries):
        countJson = {}
        for catalogEntry in catalogEntries: countJson[catalogEntry["offerId"]] = 0
        for key in auth.commonCoreProfile["items"]:
            if not auth.commonCoreProfile["items"][key]["templateId"].lower() == "eventpurchasetracker:generic_instance": continue
            attributes = auth.commonCoreProfile["items"][key]["attributes"]
            if not "event_purchases" in attributes: continue
            for offerId2 in attributes["event_purchases"]:
                if offerId2 in countJson: countJson[offerId2] += attributes["event_purchases"][offerId2]
        profileAttributes = auth.commonCoreProfile["stats"]["attributes"]
        for limitType in ["daily", "weekly", "monthly"]:
            if not f"{limitType}_purchases" in profileAttributes: continue
            if not "purchaseList" in profileAttributes[f"{limitType}_purchases"]: continue
            for offerId2 in profileAttributes[f"{limitType}_purchases"]["purchaseList"]:
                if offerId2 in countJson: countJson[offerId2] += profileAttributes[f"{limitType}_purchases"]["purchaseList"][offerId2]
        return countJson
    
    def getOffersPurchasesLimit(auth, catalogEntries):
        countJson = {}
        for catalogEntry in catalogEntries:
            offerId = catalogEntry["offerId"]
            countJson[offerId] = 0
            if "EventLimit" in catalogEntry["meta"]:
                countJson[offerId] += int(catalogEntry["meta"]["EventLimit"])
            for limitType in ["dailyLimit", "weeklyLimit", "monthlyLimit"]:
                if not limitType in catalogEntry: continue
                if catalogEntry[limitType] <= 0: continue
                countJson[offerId] += catalogEntry[limitType]
        return countJson
    
    def getAvailableCurrencyQuantity(auth, currency, currencySubType):
        count = 0
        if currency.lower() == "mtxcurrency":
            for key in auth.commonCoreProfile["items"]:
                if not auth.commonCoreProfile["items"][key]["templateId"].lower().startswith("currency:mtx"): continue
                count += auth.commonCoreProfile["items"][key]["quantity"]
        elif currencySubType:
            for key in auth.campaignProfile["items"]:
                if auth.campaignProfile["items"][key]["templateId"].lower() == currencySubType.lower():
                    count += auth.campaignProfile["items"][key]["quantity"]
        return count
    
    def bCanAffordThisPurchase(auth, purchaseReqBody):
        return itemShop.getAvailableCurrencyQuantity(auth, purchaseReqBody["currency"], purchaseReqBody["currencySubType"]) >= purchaseReqBody["expectedTotalPrice"]

    def denyOnOwnershipNumLeft(auth, catalogEntry):
        templateIdsToCheck = {}
        for requirement in catalogEntry["requirements"]:
            if requirement["requirementType"].lower() == "denyonitemownership":
                templateIdsToCheck[requirement["requiredId"].lower()] = requirement["minQuantity"]
        profileItemsCombined = {k: v for p in [auth.campaignProfile, auth.commonCoreProfile, auth.athenaProfile] for k, v in p["items"].items()}
        for key in profileItemsCombined:
            if profileItemsCombined[key]["templateId"].lower() in templateIdsToCheck.keys():
                templateIdsToCheck[profileItemsCombined[key]["templateId"].lower()] -= profileItemsCombined[key]["quantity"]
        return templateIdsToCheck

    def getCatalogEntriesToPurchase(auth):
        def bIsEligible(catalogEntry):
            for option in stringList["Config"]["perUserSettings"]["itemShop"]:
                if option["settingType"] != "bool": continue # Skip the gold config option
                optionValue = perAccountConfig.readOption(auth.accountId, option["optionPath"])
                if not optionValue: continue
                eligibleShopItems = option["eligibleShopItems"]
                for item in catalogEntry["itemGrants"]:
                    numCriteriaMet, templateId = [0, item["templateId"].lower()]
                    if "templateIds" in eligibleShopItems:
                        if templateId in [i.lower() for i in eligibleShopItems["templateIds"]]:
                            numCriteriaMet += 1
                    if "startsWith" in eligibleShopItems:
                        if any(templateId.startswith(criterion.lower()) for criterion in eligibleShopItems["startsWith"]):
                            numCriteriaMet += 1
                    if "endsWith" in eligibleShopItems:
                        if any(templateId.endswith(criterion.lower()) for criterion in eligibleShopItems["endsWith"]):
                            numCriteriaMet += 1
                    if "contains" in eligibleShopItems:
                        if any(criterion.lower() in templateId for criterion in eligibleShopItems["contains"]):
                            numCriteriaMet += 1
                    if numCriteriaMet == len(eligibleShopItems):
                        return True
            return False
        catalogEntries = []
        reqGetStorefront = requestText(request("get", links.getStorefront, headers=auth.headers, data={}), True)['storefronts']
        for key in reqGetStorefront:
            for catalogEntry in key["catalogEntries"]:
                if bIsEligible(catalogEntry): catalogEntries.append(catalogEntry)
        return catalogEntries
    
    def purchaseCatalogEntries(auth):
        catalogEntries = itemShop.getCatalogEntriesToPurchase(auth)
        purchasedQuantities = itemShop.getOffersPurchasesQuantities(auth, catalogEntries)
        offerPurchaseLimits = itemShop.getOffersPurchasesLimit(auth, catalogEntries)
        bPurchasedSomething = False
        for catalogEntry in catalogEntries:
            offerId = catalogEntry["offerId"]
            purchaseReqBody = {"offerId": offerId, "currency": catalogEntry["prices"][0]["currencyType"], "currencySubType": catalogEntry["prices"][0]["currencySubType"], "gameContext": "fn"}
            purchaseReqBody["purchaseQuantity"] = offerPurchaseLimits[offerId] - purchasedQuantities[offerId]
            if purchaseReqBody["purchaseQuantity"] <= 0: continue
            dontSpendBelowGoldAmount = perAccountConfig.readOption(auth.accountId, ["itemShop", "gold", "dontSpendBelow"])
            if itemShop.getAvailableCurrencyQuantity(auth, purchaseReqBody["currency"], purchaseReqBody["currencySubType"]) < dontSpendBelowGoldAmount:
                continue
            denyOnOwnershipNumLeft = itemShop.denyOnOwnershipNumLeft(auth, catalogEntry)
            for templateId in denyOnOwnershipNumLeft:
                if denyOnOwnershipNumLeft[templateId] < purchaseReqBody["purchaseQuantity"]:
                    purchaseReqBody["purchaseQuantity"] = denyOnOwnershipNumLeft[templateId]
            if purchaseReqBody["purchaseQuantity"] <= 0: continue
            purchaseReqBody["expectedTotalPrice"] = catalogEntry["prices"][0]["finalPrice"] * purchaseReqBody["purchaseQuantity"]
            if not itemShop.bCanAffordThisPurchase(auth, purchaseReqBody): continue
            if purchaseReqBody["purchaseQuantity"] <= 0: continue
            reqPurchase = requestText(request("post", links.profileRequest.format(auth.accountId, "PurchaseCatalogEntry", "common_core"), headers=auth.headers, json=purchaseReqBody), True)
            bPurchasedSomething = True
            for item in catalogEntry["itemGrants"]:
                templateId = item["templateId"]
                itemQuantity = purchaseReqBody['purchaseQuantity'] * item['quantity']
                itemData = stringList.get('Items', {}).get(templateId, {})
                itemName = itemData.get('name', {}).get(getConfig('Items_Language'), templateId)
                itemRarity = itemData.get('rarity', "Unknown rarity")
                itemType = itemData.get('type', "Unknown type")
                try:
                    itemRarityStr = stringList['Item Rarities'][itemRarity][getConfig('Items_Language')]
                    itemTypeStr = stringList['Item Types'][itemType][getConfig('Items_Language')]
                except: itemRarityStr, itemTypeStr = [itemRarity, itemType]
                message(getString('itemshop.purchased').format(itemRarityStr, itemTypeStr, itemQuantity, itemName))
        if bPurchasedSomething: print()

# Menu (Account & Daily Quest Manager)
def menu():
    def addAccount(bGoBack=True):
        isLoggedIn = validInput(getString("startup.addaccount.isloggedin1" if bGoBack else "startup.addaccount.isloggedin2"), ["", "1", "2"])
        if not isLoggedIn: return
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
            for account in authJson: print(f"{authJson.index(account) + 1}: {account.get('displayName', getString('startup.listaccounts.noname'))}")

    def removeAccount():
        listAccounts()
        if not authJson: return
        print(getString("startup.removeaccount.message"))
        accountCountList = [str(i) for i in range(1, len(authJson) + 1)]
        accountToRemove = validInput("", accountCountList + [""])
        if accountToRemove:
            accountToRemove = int(accountToRemove)
            areYouSure = int(validInput(getString("startup.removeaccount.areyousure").format(authJson[accountToRemove - 1]['displayName']), ["1", "2"]))
            if areYouSure == 1:
                print(getString("startup.removeaccount.success").format(authJson[accountToRemove - 1]['displayName']))
                authJson.pop(accountToRemove - 1)
                with open(authPath, "w", encoding="utf-8") as authFile: json.dump(authJson, authFile, indent=2, ensure_ascii=False)

    def manageDailyQuests():
        while authJson:
            accountToManage = []
            if len(authJson) == 1: accountToManage = authJson[0]
            else:
                listAccounts()
                print(getString("startup.managedailyquests.message"))
                accountCountList = list(map(str, range(1, len(authJson) + 1)))
                accountIndex = validInput("", accountCountList + [""])
                if not accountIndex: break
                accountToManage = authJson[int(accountIndex) - 1]
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
                        questCountList = list(map(str, range(1, len(questData) + 1)))
                        questIndex = validInput("", questCountList + [""])
                        if not questIndex: break
                        questToReplace = list(questData.keys())[int(questIndex) - 1]
                        confirmReroll = validInput(getString("startup.managedailyquests.confirm").format(questData[questToReplace]['questName']), ["1", "2"])
                        if confirmReroll == "1":
                            reqRerollQuest = requestText(request("post", links.profileRequest.format(auth.accountId, "FortRerollDailyQuest", "campaign"), headers=auth.headers, json={"questId": questToReplace}), True)
                            newQuestTemplateId = reqRerollQuest.get("notifications", [{}])[0].get("newQuestId")
                            if newQuestTemplateId:
                                newQuestName = stringList['Items'].get(newQuestTemplateId, {}).get('name', {}).get(getConfig('Items_Language'), newQuestTemplateId)
                                print(getString("startup.managedailyquests.success").format(questData[questToReplace]['questName'], newQuestName))
                                input(getString("startup.managedailyquests.pressenter"))
            if len(authJson) == 1: break

    def perUserConfigurator(strPrefix, configName):
        while authJson:
            print(getString(f'{strPrefix}.config.accountlist'))
            if not authJson: print(getString(f"{configName}.config.noaccounts"))
            else:
                for account in authJson: print(f"{authJson.index(account) + 1}: {account.get('displayName', getString('startup.listaccounts.noname'))} | {getString(f'{strPrefix}.config.set') if (account['accountId'] in userConfigJson and perAccountConfig.bHasAllConfigOptionsSet(account['accountId'], stringList['Config']['perUserSettings'][configName])) else (getString(f'{strPrefix}.config.missing') if (account['accountId'] in userConfigJson and configName in userConfigJson[account['accountId']]) else getString(f'{strPrefix}.config.notset'))}")
            print(getString(f'{strPrefix}.config.select'))
            accountCountList = [str(i) for i in range(1, len(authJson) + 1)]
            selectedAccountIndex = validInput("", accountCountList + [""])
            if not selectedAccountIndex: break
            setupInfoStr = getString(f'{strPrefix}.config.setup.info')
            if setupInfoStr: print(setupInfoStr)
            perAccountConfig.askSetupQuestionsAndSaveFile(authJson[int(selectedAccountIndex) - 1]["accountId"], stringList["Config"]["perUserSettings"][configName])
    
    def junkCleaner():
        while authJson:
            print(getString("junkcleaner.message"))
            selectedAccounts = []
            whatToDo2 = validInput(getString("junkcleaner.whattodo"), ["", "1", "2"])
            if whatToDo2 == "1":
                selectedAccounts = authJson.copy()
                invJunkCleaner.main(selectedAccounts)
                input(getString("junkcleaner.pressenter"))
                break
            elif whatToDo2 == "2": perUserConfigurator("junkcleaner", "invJunkCleaner")
            else: break

    def getSeasonalGreeting():
        now = datetime.now()
        month, day = now.month, now.day
        if month == 12 and 24 <= day and day <= 26: return getString('mainmenu.merrychristmas')
        elif (month == 12 and day == 31) or (month == 1 and day == 1): return getString('mainmenu.happynewyear')
        return ""
    
    while True:
        if not authJson: addAccount(False)
        seasonalGreeting = getSeasonalGreeting()
        if seasonalGreeting: message(seasonalGreeting)
        whatToDo1 = validInput(getString("mainmenu.message"), ["1", "2", "3", "4", "5", ""])
        if whatToDo1 == "1": break
        elif whatToDo1 == "2": manageDailyQuests()
        elif whatToDo1 == "3": junkCleaner()
        elif whatToDo1 == "4":
            while True:
                whatToDo3 = validInput(getString("accountmanager.message"), ["1", "2", "3", ""])
                if whatToDo3 == "1": addAccount()
                elif whatToDo3 == "2": removeAccount()
                elif whatToDo3 == "3":
                    listAccounts()
                    input(getString("accountmanager.pressenter"))
                else: break
        elif whatToDo1 == "5": perUserConfigurator("itemshop", "itemShop")
        else: sys.exit()

# The main part of the program that can be looped.
def main():
    for account in authJson:
        auth = login(account)
        
        # Claim a BR Winterfest event present if available.
        if auth.winterfestRewardGraphID and getConfig('Claim_Winterfest_Presents'):
            rewardGraphItem = auth.athenaProfile["items"][auth.winterfestRewardGraphID]["attributes"]
            nodeToUnlock = next((node for node in winterfest.nodesClaimingOrder if node not in rewardGraphItem["reward_nodes_claimed"]), "")
            unlockKeysLeft = 0
            for id in auth.athenaProfile["items"]:
                if auth.athenaProfile["items"][id]["templateId"].lower() == rewardGraphItem["reward_keys"][0]["static_key_template_id"].lower(): unlockKeysLeft += auth.athenaProfile["items"][id]["quantity"]
            if nodeToUnlock and unlockKeysLeft > 0:
                auth.athenaProfile = requestText(request("post", links.profileRequest.format(auth.accountId, "UnlockRewardNode", "athena"), headers=auth.headers, json={"nodeId":nodeToUnlock,"rewardGraphId":auth.winterfestRewardGraphID,"rewardCfg":""}), True)["profileChanges"][0]["profile"]
                rewardGraphItem = auth.athenaProfile["items"][auth.winterfestRewardGraphID]["attributes"]
                message(getString("main.winterfest.claimed").format(rewardGraphItem["reward_keys"][0]["unlock_keys_used"], len(stringList["winterfestRewards"].keys())))
                for templateId in stringList["winterfestRewards"][nodeToUnlock]:
                    message(f"{stringList['Item Types'][stringList['Items'][templateId]['type']][getConfig('Items_Language')]} | {stringList['Items'][templateId]['name'][getConfig('Items_Language')]}")
                print()

        # Display current daily challenges, their rewards and progress.
        if auth.bDailyQuestsUnlocked:
            message(getString("main.dailies.searching"))
            questData = getDailyQuests(auth)
            if not questData: message(getString("main.dailies.notfound"))
            for quest in questData: message(getString("main.dailies.info").format(questData[quest]['questNumber'], questData[quest]['questName'], questData[quest]['progress'], questData[quest]['rewards']))
        else: message(getString("main.dailies.unavailable"))

        # Search for eligible STW Item Shop offers and buy them for gold.
        if auth.accountId in userConfigJson and "itemShop" in userConfigJson[auth.accountId] and perAccountConfig.bHasAllConfigOptionsSet(auth.accountId, stringList["Config"]["perUserSettings"]["itemShop"]):
            itemShop.purchaseCatalogEntries(auth)

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
                            reqBuyFreeLlama = requestText(request("post", links.profileRequest.format(auth.accountId, "PurchaseCatalogEntry", "common_core"), headers=auth.headers, json={"offerId": llamaToClaimOfferId, "purchaseQuantity": 1, "currency": "GameItem", "currencySubType": "AccountResource:currency_xrayllama", "expectedTotalPrice": 0, "gameContext": "fn"}), False)
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
                                    templateId = key['itemType']
                                    itemGuid = key['itemGuid']
                                    itemQuantity = key['quantity']
                                    itemData = stringList.get('Items', {}).get(templateId, {})
                                    itemName = itemData.get('name', {}).get(getConfig('Items_Language'), templateId)
                                    itemRarity = itemData.get('rarity', "Unknown rarity")
                                    itemType = itemData.get('type', "Unknown type")
                                    llamaLootCount += 1
                                    if itemRarity in ("common", "uncommon", "rare", "epic"): itemsfromLlamas.append({"itemName": itemName, "itemType": itemType, "templateId": templateId, "itemGuid": itemGuid, "itemRarity": itemRarity, "itemQuantity": itemQuantity})
                                    try:
                                        itemRarityStr = stringList['Item Rarities'][itemRarity][getConfig('Items_Language')]
                                        itemTypeStr = stringList['Item Types'][itemType][getConfig('Items_Language')]
                                    except: itemRarityStr, itemTypeStr = [itemRarity, itemType]
                                    message(f"{llamaLootCount}: {itemRarityStr} | {itemTypeStr}: {itemQuantity}x {itemName}")

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
if not args.skip_to_claimer and not args.skip_to_invcleaner: menu()
if not args.skip_to_invcleaner:
    while True:
        t1 = datetime.now()
        main()
        t2 = datetime.now()
        if args.loop > 0: loopSleep(t1, t2)
        else:
            if args.skip_to_claimer: break
            whatToDo = input(getString("noloop.input"))
            if not whatToDo: break
            menu()
else:
    message(getString("junkcleaner.title"))
    invJunkCleaner.main(authJson.copy())

sys.exit()
