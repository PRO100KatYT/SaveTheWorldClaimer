# Fortnite Save the World Daily Reward, Research Points & free Llama Claimer

This program allows you to claim Save the World Daily Reward, Research Points and open free Llamas without opening the game.

---
### Changelog:
What's new in the 1.2.0 update:
- NEW Feature - Free Llama opening!
  - Starting with this update, the program is able to search for free Llamas and open them.
  - This feature is turned on by default, however if you don't want it you can turn it off in the config file.
- Added an error message when one of the imported modules is not installed.
- Changed the itemlist file name to stringlist.
- Added Llama names and Item names to stringlist.
- Changed the config file format from json to ini.
- Tweaked the program's code a little bit.
---

### How to use it?

- After starting the SaveTheWorldClaimer.py for the first time (or after deleting the auth.json file), you will be asked to insert the auth code. To get it, go to the Epic Games website [using this link](https://www.epicgames.com/id/logout?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253D3446cd72694c4a4485d81b77adbb2141%2526responseType%253Dcode "Here is the link :D") and log in.

- After logging in, a page should open with content similar to this:

```json
{"redirectUrl":"com.epicgames.fortnite://fnauth/?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
```
- Copy the code (e.g. 930884289b5852842271e9027376a527), paste it into the program and press enter.

- If all went well, the program will say it has generated the auth.json file successfully.

- Now the program will proceed to claim the rewards, points and search for free Llamas.

- Congratulations! You just claimed your Daily Reward, Research Points and opened free Llamas if they were avaiable!

- Next time you start the program, you will not need to enter a new auth code, because the login credentials have been saved in the auth.json file.