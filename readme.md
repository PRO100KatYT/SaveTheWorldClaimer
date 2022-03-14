# Fortnite Save the World Daily Reward, Research Points & free Llama Claimer

This program allows you to claim Save the World Daily Reward, Research Points and open free Llamas without opening the game.

---
### Features:
- Two login methods: refresh token and device auth.
  - You can see more info about them and choose the method via the config.ini file.
- Daily reward claiming.
- Research Points claiming.
- Automatic Research Points spending.
  - You can choose the method or disable this feature via the config.ini file.
- Claiming free Llamas.
  - You can disable this feature via the config.ini file.
- Automatic free Llama loot recycling.
  - You can enable this feature via the config.ini file.
- Program Looping.
  - You can set the time (in minutes) after the program will run again in the config file.
  - The looping is set to 0 (disabled) by default.
---
### Changelog:
What's new in the 1.8.0 update:
- The program can now display Fortnite item names in Arabic, German, English, Spanish, Latin American Spanish, French, Italian, Japanese, Korean, Polish, Brazilian Portugese, Russian, Turkish, Simplified Chinese and Traditional Chinese.
  - You change the language by changing the Language value in the config file.
- After logging in, the program now sends a ClientQuestLogin request instead of a QueryProfile one.
  - In other words, the program will now get you a new daily quest, event quests, etc.
- Tweaked the program's code a little bit.
---

### How to use it?

- After starting the SaveTheWorldClaimer.py for the first time (or after deleting the config.ini file) you will be asked if you want to start the config setup process or use the default config values. If you want to start the setup, type 1, if no, type 2.

- Next, you will be asked if you are logged into your Epic account in your browser. If yes, type 1, if no, type 2.

- After you'll press ENTER, an Epic Games website will open. From there, login if you are not already logged into your Epic account.

- Then a page should open with content similar to this:

```json
{"redirectUrl":"https://localhost/launcher/authorized?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
```
or this:
```json
{"redirectUrl":"com.epicgames.fortnite://fnauth/?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
```

- Copy the code (e.g. 930884289b5852842271e9027376a527), paste it into the program and press enter.

- If all went well, the program will say it has generated the auth.json file successfully.

- Now the program will proceed to claim the rewards, points and search for free Llamas.

- Congratulations! You just claimed your Daily Reward, Research Points and opened free Llamas if they were available!

- Next time you start the program, you will not need to enter a new auth code, because the login credentials have been saved in the auth.json file.
---

### Found a bug?
Feel free to [open an issue](https://github.com/PRO100KatYT/SaveTheWorldClaimer/issues/new "Click here if you want to open an issue.") if you encounter any bugs or just have a question.

---

If you want to receive notifications about free llamas, I recommend joining [the r/FORTnITE discord server](https://discord.gg/PjqZaDmV8D "Here is the link :D") and giving yourself the freellamas role on the #role-assignment channel.