import webbrowser
import json
import requests
import os

# Links that will be used in the later part of code.
class links:
    getToken = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    getDeviceAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{0}/deviceAuth"
    claimDailyReward = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/ClaimLoginReward?profileId=campaign"
    claimCollectedResources = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/ClaimCollectedResources?profileId=campaign"
    getProfile = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/QueryProfile?profileId={1}"

print("Fortnite StW Daily Reward & Research Points claimer v1.0.0 by PRO100KatYT\n")

# Creating the auth.json file.
path = os.path.join(os.path.split(os.path.abspath(__file__))[0], "auth.json")
if not os.path.exists(path):
    print("Starting to generate the auth.json file.\n")
    reqToken = requests.post(links.getToken, headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "authorization_code", "code": input("Insert the auth code:\n")})
    reqTokenText = json.loads(reqToken.text)
    if "errorMessage" in reqTokenText:
        print(f"\nERROR: {reqTokenText['errorMessage']}")
        input("\nPress ENTER to close the program.\n") 
        exit()
    else:
        access_token = reqTokenText["access_token"]
        account_id = reqTokenText["account_id"]
    reqDeviceAuth = requests.post(links.getDeviceAuth.format(account_id), headers={"Authorization": f"bearer {access_token}"}, data={})
    reqDeviceAuthText = json.loads(reqDeviceAuth.text)
    if "errorMessage" in reqDeviceAuthText:
        print(f"\nERROR: {reqDeviceAuthText['errorMessage']}")
        input("\nPress ENTER to close the program.\n") 
        exit()
    else:
        deviceId = reqDeviceAuthText["deviceId"]
        secret = reqDeviceAuthText["secret"]
        jsontosave = ("{\"WARNING\": \"Don't show anyone the contents of this file, because it contains information with which the program logs into the account.\", \"deviceId\":\"{deviceId}\", \"accountId\":\"{account_id}\", \"secret\":\"{secret}\"}")
        firstjsonreplace = jsontosave.replace("{deviceId}", deviceId)
        secondjsonreplace = firstjsonreplace.replace("{account_id}", account_id)
        thirdjsonreplace = secondjsonreplace.replace("{secret}", secret)
        json.dump(json.loads(thirdjsonreplace), open(path, "w"), indent = 2)
        print("\nThe auth.json file was generated successfully.\n")
try:
    getAuthJson = json.loads(open(path, "r").read())
    deviceId2 = getAuthJson["deviceId"]
    accountId2 = getAuthJson["accountId"]
    secret2 = getAuthJson["secret"]
except:
    print("ERROR: The program is unable to read the auth.json file. Delete the auth.json file and run this program again to generate a new one.\n")
    input("Press ENTER to close the program.\n")
    exit()
itemListPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "itemlist.json")
if not os.path.exists(itemListPath):
    print("ERROR: The itemlist.json file doesn't exist. Get it from this program's repository on Github, add it back and run this program again.\n")
    input("Press ENTER to close the program.\n")
    exit()
try:
    getItemList = json.loads(open(itemListPath, "r").read())
except:
    print("ERROR: The program is unable to read the itemlist.json file. Delete the itemlist.json file, download it from this program's repository on Github, add it back here and run this program again.\n")
    input("Press ENTER to close the program.\n")
    exit()
reqToken2 = requests.post(links.getToken, headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "device_auth", "device_id": deviceId2, "account_id": accountId2, "secret": secret2, "token_type": "eg1"})
reqToken2Text = json.loads(reqToken2.text)
if "errorMessage" in reqToken2Text:
    print(f"ERROR: At least one variable in the auth.json file is no longer valid. Delete the auth.json file and run this program again to generate a new one.")
    input("\nPress ENTER to close the program.\n") 
    exit()
else:
    access_token2 = reqToken2Text['access_token']
    display_name2 = reqToken2Text['displayName']
    
print(f"Logged in as {display_name2}.\n")
headers = {"Authorization": f"bearer {access_token2}", "Content-Type": "application/json"}

# Checking whether the account has the campaign access token and founder's token. The founder's token is not required, but instead of V-Bucks the account will recieve X-Ray Tickets.
reqCommonCoreProfileCheck = requests.post(links.getProfile.format(accountId2, "common_core"), headers=headers, data="{}")
bCampaignAccess = 0
bFounder = 0
if "Token:campaignaccess" in reqCommonCoreProfileCheck.text:
    bCampaignAccess = 1
if "Token:founderspack" in reqCommonCoreProfileCheck.text:
    bFounder = 1
if bCampaignAccess == 0:
    print(f"\nERROR: {display_name2} doesn't have access to Save the World.")
    input("\nPress ENTER to close the program.\n")
    exit()

# Claiming the Daily Reward.
print("Claiming the Daily Reward...\n")
reqClaimDailyReward = requests.post(links.claimDailyReward.format(accountId2), headers=headers, data="{}")
reqClaimDailyRewardText = json.loads(reqClaimDailyReward.text)
if "errorMessage" in reqClaimDailyRewardText:
    print(f"\nERROR: {reqClaimDailyRewardText['errorMessage']}")
    input("\nPress ENTER to close the program.\n")
    exit()
cdrItems = reqClaimDailyRewardText['notifications'][0]['items']
cdrDaysLoggedIn = reqClaimDailyRewardText['notifications'][0]['daysLoggedIn']
cdrDaysModified = int(cdrDaysLoggedIn) % 336 # Credit to dippyshere for this and the next two lines of code.
if cdrDaysModified == 0:
    cdrDaysModified = 336
if not cdrItems:
    print(f"The daily reward for {display_name2} has been already claimed today!")
else:
    print(f"Today's daily reward for {display_name2} has been successfully claimed!")
getReward = getItemList[f'{cdrDaysModified}']
if "V-Bucks" in getReward:
    if bFounder == 0:
        reward = getReward.replace("V-Bucks", "X-Ray Tickets")
    else:
        reward = getReward
else:
    reward = getReward
print(f"Day: {cdrDaysLoggedIn}\nReward: {reward}\n")

# Claiming the Research Points
print("Claiming the Research Points...\n")
reqCampaignProfileCheck = requests.post(links.getProfile.format(accountId2, "campaign"), headers=headers, data="{}")
reqCampaignProfileCheckItems = json.loads(reqCampaignProfileCheck.text)['profileChanges'][0]['profile']['items']
for key in reqCampaignProfileCheckItems: # Credit to Lawin for helping me figuring out how to write this and the next two lines of code.
    if reqCampaignProfileCheckItems[f'{key}']['templateId'] == "CollectedResource:Token_collectionresource_nodegatetoken01":
        tokenToClaim = key
reqClaimCollectedResources = requests.post(links.claimCollectedResources.format(accountId2), headers=headers, json={"collectorsToClaim": [f"{tokenToClaim}"]})
reqClaimCollectedResourcesText = json.loads(reqClaimCollectedResources.text)
if "errorMessage" in reqClaimCollectedResourcesText:
    print(f"\nERROR: {reqClaimCollectedResourcesText['errorMessage']}")
    input("\nPress ENTER to close the program.\n")
    exit()
try:
    reqClaimCollectedResourcesText['notifications']
except:
    for key in reqCampaignProfileCheckItems:
        if reqCampaignProfileCheckItems[f'{key}']['templateId'] == "Token:collectionresource_nodegatetoken01":
            totalItemGuid = key
    print(f"ERROR: Failed to claim {reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{tokenToClaim}']['attributes']['stored_value']} Research Points because you have the maximum number of accumulated Research Points at once ({reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity']})\n")
    input("Press ENTER to close the program.\n")
    exit()
totalItemGuid = reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['itemGuid']
print(f"Claimed {reqClaimCollectedResourcesText['notifications'][0]['loot']['items'][0]['quantity']} Research Points. Total Research Points: {reqClaimCollectedResourcesText['profileChanges'][0]['profile']['items'][f'{totalItemGuid}']['quantity']}\n")
input("Press ENTER to close the program.\n")
exit()