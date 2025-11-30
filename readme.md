<div align="center">

<h1>Fortnite Save the World Claimer</h1>

This program allows you to open free Llamas, claim and replace your Daily Quests, and much more — all without opening the game.

[![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

📜 [Features](#-features) •
🔄 [Changelog](#-changelog) •
🚀 [How to use it?](#-how-to-use-it) •
🐛 [Found a bug?](#-found-a-bug)
</div>

---

### 📜 Features:
- 👥 **Multiple account support** with two login methods: refresh token and device auth.
  - You can see more info about them and choose the method when adding an account.
- 🗓️ **Daily Quests**: claiming new quests and displaying their progress and rewards.
- ♻️ **Daily Quest replacing** via the Daily Quest manager in the Main Menu.
- 🦙 **Claiming free Llamas** and automatic Llama loot recycling.
  - You can toggle and adjust these features via the config file.
- 🎓 **Tutorial mission skipping**: unlock the Save the World music pack even if you don't own StW.
- 🧹 **Inventory Junk Cleaner**: destroy/recycle unwanted backpack resources, weapons, etc.
  - You can find out more about this configurable feature in the Menu.
- 💬 **Discord Webhook integration**.
  - You can set the Webhook URL in the config file.
- 🌐 **Multi-language support** for the program interface (English & Polish).
- 🌍 **18 languages support** for Fortnite item and quest names.
- 🔁 **Program Looping**.
  - You can set the time (in minutes) after which the main program will run again in the config.
  - The looping is set to 0 (disabled) by default.

---

### 🔄 Changelog:
**What's new in the `1.14.2` update:**
- ⛔ Removed the Research Points related program functionality due to Epic Games removing the Research system from the game.
- 🎨 Tweaked the program's code a little bit.

---

### 🚀 How to use it?
1.  Install **Python 3.9.5** or a newer version.

2.  The program will try to automatically install the `requests` module. If it fails, open your console/terminal and install it manually using the command: `pip install requests`.

3.  When you start `SaveTheWorldClaimer.py` for the first time (or after deleting `config.ini`), you will be asked to start the config setup. It's recommended to do so.

4.  Next, the program will ask if you are logged into your Epic account in your default web browser.

5.  An Epic Games website will open. Log in if you haven't already.

6.  A page should then open with content similar to this:
    ```json
    {"redirectUrl":"https://localhost/launcher/authorized?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
    ```
    or this:
    ```json
    {"redirectUrl":"com.epicgames.fortnite://fnauth/?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
    ```

7.  ➡️ Copy the `authorizationCode` (e.g., `930884289b5852842271e9027376a527`), paste it into the program, and press ENTER.

8.  ✅ If everything went well, the program will confirm that the `auth.json` file was generated successfully. The program will then proceed to the Main Menu.

9.  🎉 Congratulations! You can now get your daily quest, open free llamas (if available), and much more!

10. The next time you launch the program, you won't need a new authorization code, as your login credentials are saved in `auth.json`.

---

### 🐛 Found a bug?
Feel free to [open an issue](https://github.com/PRO100KatYT/SaveTheWorldClaimer/issues/new "Click here to open an issue.") if you encounter any bugs or just have a question.

---

### 🎁 Looking for Daily Login Rewards?
Daily Login Rewards were removed from the game in June 2023. Read more [here](https://www.fortnite.com/news/changes-coming-to-fortnite-save-the-worlds-daily-reward-system-in-v25-10 "Daily Login Rewards removal info").
### 🧪 Looking for Research Points?
Research system was removed from the game in November 2025. Read more [here](https://www.reddit.com/r/FORTnITE/comments/1pa4vz8/save_the_world_v3900_update_notes "Research system removal info").

---

### 🔔 Want notifications for free llamas?
I recommend joining [the r/FORTnITE discord server](https://discord.gg/PjqZaDmV8D "Here is the link :D") and assigning yourself the `freellamas` role on the `#role-assignment` channel.