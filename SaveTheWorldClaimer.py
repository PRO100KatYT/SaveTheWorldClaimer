import json
import requests
import os

# Links that will be used in the later part of code.
class links:
    getToken = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    getDeviceAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{0}/deviceAuth"
    profileRequest = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/{1}?profileId={2}"

print("Fortnite StW Daily Reward & Research Points claimer v1.1.0 by PRO100KatYT\n")

# Creating and/or reading the auth.json file.
authPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "auth.json")
if not os.path.exists(authPath):
    print("Starting to generate the auth.json file.\n")
    reqToken = requests.post(links.getToken, headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "authorization_code", "code": input("Insert the auth code:\n")})
    reqTokenText = json.loads(reqToken.text)
    if "errorMessage" in reqTokenText:
        print(f"\nERROR: {reqTokenText['errorMessage']}\n")
        input("Press ENTER to close the program.\n") 
        exit()
    else:
        accessToken = reqTokenText["access_token"]
        accountId = reqTokenText["account_id"]
    reqDeviceAuth = requests.post(links.getDeviceAuth.format(accountId), headers={"Authorization": f"bearer {accessToken}"}, data={})
    reqDeviceAuthText = json.loads(reqDeviceAuth.text)
    if "errorMessage" in reqDeviceAuthText:
        print(f"\nERROR: {reqDeviceAuthText['errorMessage']}\n")
        input("Press ENTER to close the program.\n") 
        exit()
    else:
        deviceId = reqDeviceAuthText["deviceId"]
        secret = reqDeviceAuthText["secret"]
        jsontosave = ("{\"WARNING\": \"Don't show anyone the contents of this file, because it contains information with which the program logs into the account.\", \"deviceId\":\"{deviceId}\", \"accountId\":\"{account_id}\", \"secret\":\"{secret}\"}")
        firstjsonreplace = jsontosave.replace("{deviceId}", deviceId)
        secondjsonreplace = firstjsonreplace.replace("{account_id}", accountId)
        thirdjsonreplace = secondjsonreplace.replace("{secret}", secret)
        json.dump(json.loads(thirdjsonreplace), open(authPath, "w"), indent = 2)
        print("\nThe auth.json file was generated successfully.\n")
try:
    getAuthJson = json.loads(open(authPath, "r").read())
    deviceId = getAuthJson["deviceId"]
    accountId = getAuthJson["accountId"]
    secret = getAuthJson["secret"]
except:
    print("ERROR: The program is unable to read the auth.json file. Delete the auth.json file and run this program again to generate a new one.\n")
    input("Press ENTER to close the program.\n")
    exit()
itemListPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "itemlist.json")
if not os.path.exists(itemListPath):
    print("ERROR: The itemlist.json file doesn't exist. Get it from this program's repository on Github, add it back and run this program again.\n")
    input("Press ENTER to close the program.\n")
    exit()
try: getItemList = json.loads(open(itemListPath, "r").read())
except:
    print("ERROR: The program is unable to read the itemlist.json file. Delete the itemlist.json file, download it from this program's repository on Github, add it back here and run this program again.\n")
    input("Press ENTER to close the program.\n")
    exit()
reqToken = requests.post(links.getToken, headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "device_auth", "device_id": deviceId, "account_id": accountId, "secret": secret, "token_type": "eg1"})
reqTokenText = json.loads(reqToken.text)
if "errorMessage" in reqTokenText:
    print(f"ERROR: At least one variable in the auth.json file is no longer valid. Delete the auth.json file and run this program again to generate a new one.\n")
    input("Press ENTER to close the program.\n") 
    exit()
else:
    accessToken = reqTokenText['access_token']
    displayName = reqTokenText['displayName']
    
print(f"Logged in as {displayName}.\n")
headers = {"Authorization": f"bearer {accessToken}", "Content-Type": "application/json"}

# Creating and/or reading the config.json file.
configPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "config.json")
if not os.path.exists(configPath):
    print("Starting to generate the config.json file.\n")
    jsontosave = ("{\"Automatically spend Research Points when you'll have the maximum number of accumulated Research Points at once\": \"false\"}")
    json.dump(json.loads(jsontosave), open(configPath, "w"), indent = 2)
    print("The config.json file was generated successfully.\n")
try:
    getConfigJson = json.loads(open(configPath, "r").read())
    bSpendAutoResearch = getConfigJson["Automatically spend Research Points when you'll have the maximum number of accumulated Research Points at once"]
except:
    print("ERROR: The program is unable to read the config.json file. Delete the config.json file and run this program again to generate a new one.\n")
    input("Press ENTER to close the program.\n")
    exit()
if not (bSpendAutoResearch == "true" or bSpendAutoResearch == "false"):
    print(f"ERROR: You set the wrong value in config.json ({bSpendAutoResearch}). Valid values: true, false. Change it and run this program again.\n")
    input("Press ENTER to close the program.\n")
    exit()

# Checking whether the account has the campaign access token and founder's token. The founder's token is not required, but instead of V-Bucks the account will recieve X-Ray Tickets.
reqCommonCoreProfileCheck = requests.post(links.profileRequest.format(accountId, "QueryProfile", "common_core"), headers=headers, data="{}")
bCampaignAccess = 0
bFounder = 0
if "Token:campaignaccess" in reqCommonCoreProfileCheck.text: bCampaignAccess = 1
if "Token:founderspack" in reqCommonCoreProfileCheck.text: bFounder = 1
if bCampaignAccess == 0:
    print(f"ERROR: {displayName} doesn't have access to Save the World.\n")
    input("Press ENTER to close the program.\n")
    exit()

# Claiming the Daily Reward.
print("Claiming the Daily Reward...\n")
reqClaimDailyReward = requests.post(links.profileRequest.format(accountId, "ClaimLoginReward", "campaign"), headers=headers, data="{}")
reqClaimDailyRewardText = json.loads(reqClaimDailyReward.text)
if "errorMessage" in reqClaimDailyRewardText:
    print(f"ERROR: {reqClaimDailyRewardText['errorMessage']}\n")
    input("Press ENTER to close the program.\n")
    exit()
cdrItems = reqClaimDailyRewardText['notifications'][0]['items']
cdrDaysLoggedIn = reqClaimDailyRewardText['notifications'][0]['daysLoggedIn']
cdrDaysModified = int(cdrDaysLoggedIn) % 336 # Credit to dippyshere for this and the next line of code.
if cdrDaysModified == 0: cdrDaysModified = 336
if not cdrItems:
    print(f"The daily reward for {displayName} has been already claimed today!")
else: print(f"Today's daily reward for {displayName} has been successfully claimed!")
getReward = getItemList[f'{cdrDaysModified}']
if "V-Bucks" in getReward:
    if bFounder == 0: reward = getReward.replace("V-Bucks", "X-Ray Tickets")
    else: reward = getReward
else: reward = getReward
print(f"Day: {cdrDaysLoggedIn}\nReward: {reward}\n")

# Claiming and automatic spending the Research Points
reqCampaignProfileCheck = requests.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}")
reqCampaignProfileCheckText = json.loads(reqCampaignProfileCheck.text)
reqCampaignProfileCheckResearchLevels = reqCampaignProfileCheckText['profileChanges'][0]['profile']['stats']['attributes']['research_levels']
if (reqCampaignProfileCheckResearchLevels['fortitude'] == 120 and reqCampaignProfileCheckResearchLevels['offense'] == 120 and reqCampaignProfileCheckResearchLevels['resistance'] == 120 and reqCampaignProfileCheckResearchLevels['technology'] == 120):
    print(f"Skipping claiming Research Points because {displayName} has max F.O.R.T. stats.\n")
    input("Press ENTER to close the program.\n")
    exit()
print("Claiming the Research Points...\n")
reqCampaignProfileCheckItems = reqCampaignProfileCheckText['profileChanges'][0]['profile']['items']
for key in reqCampaignProfileCheckItems: # Credit to Lawin for helping me figuring out how to write this and the next line of code.
    if reqCampaignProfileCheckItems[f'{key}']['templateId'] == "CollectedResource:Token_collectionresource_nodegatetoken01": tokenToClaim = key
reqClaimCollectedResources = requests.post(links.profileRequest.format(accountId, "ClaimCollectedResources", "campaign"), headers=headers, json={"collectorsToClaim": [f"{tokenToClaim}"]})
reqClaimCollectedResourcesText = json.loads(reqClaimCollectedResources.text)
if "errorMessage" in reqClaimCollectedResourcesText:
    print(f"\nERROR: {reqClaimCollectedResourcesText['errorMessage']}\n")
    input("Press ENTER to close the program.\n")
    exit()
try: reqClaimCollectedResourcesText['notifications']
except:
    for key in reqCampaignProfileCheckItems:
        if reqCampaignProfileCheckItems[f'{key}']['templateId'] == "Token:collectionresource_nodegatetoken01": totalItemGuid = key
    rpToClaim = reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{tokenToClaim}']['attributes']['stored_value']
    rpStored = reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity']
    if int(rpToClaim) < 1: input(f"ERROR: Failed to claim {rpToClaim} Research Point because in order to collect it, at least 1 point must be available for claiming.\n\nPress ENTER to close the program.\n")
    else:
        if bSpendAutoResearch == "false": print(f"Failed to claim {rpToClaim} Research Points because you have the maximum number of accumulated Research Points at once ({rpStored}).\nIn this situation if you want to automatically spend them, change the value in config.json from false to true and run this program again.\n")
        else:
            print(f"You have the maximum number of accumulated Research Points at once ({rpStored}).\nStarting to automatically spend Research Points...\n")
            while True:
                reqFORTLevelsCheck = requests.post(links.profileRequest.format(accountId, "QueryProfile", "campaign"), headers=headers, data="{}")
                reqFORTLevelsCheckText = json.loads(reqCampaignProfileCheck.text)['profileChanges'][0]['profile']['stats']['attributes']['research_levels']
                levelsList = [int(reqFORTLevelsCheckText['fortitude']), int(reqFORTLevelsCheckText['offense']), int(reqFORTLevelsCheckText['resistance']), int(reqFORTLevelsCheckText['technology'])]
                lowestLevel = min(levelsList)
                for key in reqFORTLevelsCheckText:
                    if reqFORTLevelsCheckText[f'{key}'] == int(lowestLevel): statToClaim = key
                reqPurchaseResearchStatUpgrade = requests.post(links.profileRequest.format(accountId, "PurchaseResearchStatUpgrade", "campaign"), headers=headers, json={"statId": f'{statToClaim}'})
                reqPurchaseResearchStatUpgradeText = json.loads(reqPurchaseResearchStatUpgrade.text)
                if "errorMessage" in reqPurchaseResearchStatUpgradeText: break
                else: print(f"Bought 1 {statToClaim.capitalize()} level. New level: {reqPurchaseResearchStatUpgradeText['profileChanges'][0]['profile']['stats']['attributes']['research_levels'][f'{statToClaim}']}.")
            print("\nCannot buy more F.O.R.T. levels. Claiming the Research Points...\n")
            reqClaimCollectedResources = requests.post(links.profileRequest.format(accountId, "ClaimCollectedResources", "campaign"), headers=headers, json={"collectorsToClaim": [f"{tokenToClaim}"]})
            reqClaimCollectedResourcesText = json.loads(reqClaimCollectedResources.text)
            totalItemGuid = reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['itemGuid']
            print(f"Claimed {reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['quantity']} Research Points. Total Research Points: {reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity']}\n")
        input("Press ENTER to close the program.\n")
        exit()
totalItemGuid = reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['itemGuid']
print(f"Claimed {reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['quantity']} Research Points. Total Research Points: {reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity']}\n")
input("Press ENTER to close the program.\n")
exit()