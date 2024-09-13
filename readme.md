<div align="center">
<h1>Fortnite Save the World Research Points & free Llama Claimer</h1>
  
This program allows you to claim Research Points, open free Llamas, manage your Daily Quests and even skip the tutorial mission without opening the game.

[![](https://img.shields.io/badge/python-3.9.5+-blue.svg)](https://www.python.org/downloads/)

[Features](#features) •
[Changelog](#changelog) •
[How to use it?](#how-to-use-it) •
[Found a bug?](#found-a-bug)
</div>

---

### Features:
- Multiple account support with two login methods: refresh token and device auth.
  - You can see more info about them and choose the method when adding an account.
- Claiming new Daily Quests and displaying information about them.
  - The program will display their progress and earnable rewards.
- Daily Quest replacing
  - You can access the Daily Quest manager in the Main Menu.
- Claiming and auto spending Research Points.
  - You can choose the method or toggle auto spending via config.
- Tutorial mission skipping (Unlocks the Save the World music pack even if you don't own StW).
- Claiming free Llamas and automatic free Llama loot recycling.
  - You can toggle and adjust these features via config.
- Program Looping.
  - You can set the time (in minutes) after the program will run again in config.
  - The looping is set to 0 (disabled) by default.
- Discord Webhook integration
  - You can set the Webhook URL in config.
- Multi-language support.
  - Currently supported languages the program can be displayed in are: English and Polish.
- 15 languages support for Fortnite item names.

---

### Changelog:
What's new in the 1.13.2 update:
- Fixed the device login method not working.
  - Included backwards compatibility with accounts saved prior to this update.
- Added a confirmation question after selecting an account to remove from the program.
- Added the Eternal Wanderer, Madcap and Mayhem heroes strings to the stringlist.json
- Tweaked the program's code a little bit.

What's new in the 1.13.1 update:
- If enabled, the program will now send Discord Webhooks in a thread so that it won't slow down the whole program anymore.
- When you want to stop the program in the Main Menu, you can now just leave the input blank and press ENTER instead of having to additionally type `4` in the input.
- Added Birthday Llama name strings to stringlist.json
- The program will now display data from responses such as catalog, in the item language specified in the configuration.
- Added a .gitignore file.
---

### How to use it?
- Install `Python 3.9.5` or newer.

- If you didn't do it yet, the program will try to automatically install the `requests` module. If the program fails to do it, install it using the `pip install requests` console command.

- After starting the SaveTheWorldClaimer.py for the first time (or after deleting config.ini) you will be asked if you want to start config setup process (recommended) or use the default config values. If you want to start the setup, type 1, if no, type 2.

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

### Looking for Daily Login Rewards?
Read more [here](https://www.fortnite.com/news/changes-coming-to-fortnite-save-the-worlds-daily-reward-system-in-v25-10).

---

If you want to receive notifications about free llamas, I recommend joining [the r/FORTnITE discord server](https://discord.gg/PjqZaDmV8D "Here is the link :D") and giving yourself the freellamas role on the #role-assignment channel.