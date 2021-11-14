# Fortnite Save the World Daily Reward & Research Points Claimer

This program allows you to claim Save the World Daily Reward and Research Points without opening the game.

---
### Changelog:
The new 1.1.0 update introduces:
- The ability to automatically spend points on purchasing F.O.R.T. stats when the maximum amount is accumulated.
  - To enable it, change the value in config.json from false to true.
- Tweaked the item list and the program's code a little bit.
---

### How to use it?

- After starting the SaveTheWorldClaimer.py for the first time (or after deleting the auth.json file), you will be asked to insert the auth code. To get it, go to the Epic Games website [using this link](https://www.epicgames.com/id/logout?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253D3446cd72694c4a4485d81b77adbb2141%2526responseType%253Dcode "Here is the link :D") and log in.

- After logging in, a page should open with content similar to this:

```json
{"redirectUrl":"com.epicgames.fortnite://fnauth/?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
```
- Copy the code (e.g. 930884289b5852842271e9027376a527), paste it into the program and press enter.

- If all went well, the program will say it has generated the auth.json file successfully.

- Now the program will proceed to claim the rewards & points.

- Congratulations! You just claimed your Daily Reward and Research Points!

- Next time you start the program, you will not need to enter a new auth code, because the login credentials have been saved in the auth.json file.