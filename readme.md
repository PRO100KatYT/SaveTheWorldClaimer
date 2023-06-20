# Fortnite Save the World Research Points & free Llama Claimer

This program allows you to claim Research Points, open free Llamas and even skip the tutorial mission without opening the game.

NOTE: Due to Epic Games removing the Daily Reward system from Fortnite, the program is no longer able to claim these rewards. Read more [here](https://www.fortnite.com/news/changes-coming-to-fortnite-save-the-worlds-daily-reward-system-in-v25-10).

[![](https://img.shields.io/badge/python-3.9.5+-blue.svg)](https://www.python.org/downloads/)
---
### Features:
- Multiple account support with two login methods: refresh token and device auth.
  - You can see more info about them and choose the method when adding an account.
- New Daily Quest getting and displaying information about them.
  - The program will display their progress and earnable rewards.
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
What's new in the 1.11.0 update:
- 🫡 Removed the Daily Rewards claiming due to Epic Games removing them from Fortnite.
- Rewritten some parts of the code. If you encounter any new issues, please report them [here](https://github.com/PRO100KatYT/SaveTheWorldClaimer/issues/new "Click here if you want to open an issue.").

What's new in the 1.11.1 update:
- New feature: The program will now get today's daily quest for you & list all your current active ones with their progress and earnable rewards.
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

- Now the program will proceed to work.

- Congratulations! You just got your today's Daily Quest, claimed Research Points and opened free Llamas if they were available!

- Next time you launch the program, to start claiming rewards, type 1 and press ENTER. You will not need to enter a new auth code because the login credentials have been saved in the auth.json file.
---

### Found a bug?
Feel free to [open an issue](https://github.com/PRO100KatYT/SaveTheWorldClaimer/issues/new "Click here if you want to open an issue.") if you encounter any bugs or just have a question.

---

If you want to receive notifications about free llamas, I recommend joining [the r/FORTnITE discord server](https://discord.gg/PjqZaDmV8D "Here is the link :D") and giving yourself the freellamas role on the #role-assignment channel.