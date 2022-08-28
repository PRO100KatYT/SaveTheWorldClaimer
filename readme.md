# Fortnite Save the World Daily Reward, Research Points & free Llama Claimer

This program allows you to claim Save the World Daily Reward, Research Points, open free Llamas and even skip the tutorial mission without opening the game.

[![](https://img.shields.io/badge/python-3.9.5+-blue.svg)](https://www.python.org/downloads/)
---
### Features:
- Multiple account support with two login methods: refresh token and device auth.
  - You can see more info about them and choose the method when adding an account.
- Daily reward claiming.
- Research Points claiming.
- Tutorial mission skipping (Unlocks the Save the World music pack even if you don't own StW).
- Automatic Research Points spending.
  - You can choose the method or toggle this feature via the config.ini file.
- Claiming free Llamas.
  - You can toggle this feature via the config.ini file.
- Automatic free Llama loot recycling.
  - You can toggle this feature via the config.ini file.
- Program Looping.
  - You can set the time (in minutes) after the program will run again in the config file.
  - The looping is set to 0 (disabled) by default.
- Multi-language support.
  - Currently supported languages the program can be displayed in are: English and Polish.
- 15 languages support for Fortnite item names.
---
### Changelog:
What's new in the 1.10.0 update:
- Multi-language support!
  - You can now select Polish as language the program be displayed in.
  - Note: this is a seperate config option from the Fortnite item names one.
- Auto installing the `requests` module added by [Playeereq](https://github.com/Playeereq).
- Showing next loop run time added by [Salty-Coder](https://github.com/Salty-Coder).
- Added an option to skip the Main Menu to the reward claiming stage. Suggested by [probablypablito](https://github.com/probablypablito)
  - You can toggle this via the config.ini file only. Set to false by default.
- Fixed being unable to input a float when setting the Loop_Minutes value via the config setup.
- Tweaked the program's code a little bit.
---

### How to use it?
- Install `Python 3.9.5` or newer.

- If you didn't do it yet, the program will try to automatically install the `requests` module. If the program fails to do it, install it using the `pip install requests` console command.

- After starting the SaveTheWorldClaimer.py for the first time (or after deleting the config.ini file) you will be asked if you want to start the config setup process (recommended) or use the default config values. If you want to start the setup, type 1, if no, type 2.

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

- Next time you launch the program, to start claiming rewards, type 1 and press ENTER. You will not need to enter a new auth code because the login credentials have been saved in the auth.json file.
---

### Found a bug?
Feel free to [open an issue](https://github.com/PRO100KatYT/SaveTheWorldClaimer/issues/new "Click here if you want to open an issue.") if you encounter any bugs or just have a question.

---

If you want to receive notifications about free llamas, I recommend joining [the r/FORTnITE discord server](https://discord.gg/PjqZaDmV8D "Here is the link :D") and giving yourself the freellamas role on the #role-assignment channel.