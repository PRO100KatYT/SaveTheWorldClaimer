<div align="center">

<img src="https://raw.githubusercontent.com/PRO100KatYT/SaveTheWorldClaimer/main/icons/penny.png" alt="Penny Logo" width="130"/><br>
<img width="500" alt="Save the World Claimer banner" src="https://raw.githubusercontent.com/PRO100KatYT/SaveTheWorldClaimer/main/icons/banner.png" />
<br>
This Fortnite: Save the World tool allows you to open free Llamas, claim and replace your Daily Quests, manage your Backpack items, auto-buy items from the Weekly & Event Store, and much more - all without launching the game.

[![](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

📜 [Features](#-features) •
🔄 [Changelog](#-changelog) •
🚀 [How to install and use?](#-how-to-install-and-use) •
❓ [FAQ](#-faq) •
🐛 [Found a bug?](#-found-a-bug)
</div>

---

### 📜 Features:
- 🗓️ **Daily Quests Management** - claim new quests, display progress, and replace them.
- 🦙 **Free Llamas Claiming** - open free llamas and automatically recycle their loot (configurable).
- 🛒 **STW Item Shop Purchaser** - auto-buy chosen items from the Event and Weekly store for Gold.
- 🧹 **Inventory Junk Cleaner** - automatically destroy or recycle unwanted backpack items after missions.
- 🎓 **Tutorial Mission Skipping** - unlock the Save the World music pack even if you don't own STW.
- 🎁 **Winterfest Presents** - claim available presents during the BR Winterfest event.
- 👥 **Multiple account support** - log in with refresh token or device auth.
- 💬 **Discord Webhook Integration** - receive program's messages directly on your Discord server channel.
- 🌐 **Multi-language Support** - program interface in English & Polish, with 18 languages supported for Fortnite items.
- 🔁 **Program Looping** - run the program in the background at set intervals.

---

### 🔄 Changelog:
You can view the latest release changelog [here](https://github.com/PRO100KatYT/SaveTheWorldClaimer/releases/latest).

---

### 🚀 How to install and use?

<details>
<summary><b>Click to expand the step-by-step installation and use guide</b></summary>
<br>

#### Option 1: Pre-compiled Release
1. Go to the [Releases](https://github.com/PRO100KatYT/SaveTheWorldClaimer/releases/latest) page on this GitHub repository.
2. Download the correct file for your operating system:
   - **Windows:** Download and run `SaveTheWorldClaimer_Setup_x64.exe`. It will install the app and create shortcuts.
   - **Linux / macOS:** Download the respective binary file, grant it execution permissions, and run it directly in your terminal.
3. Launch the program and proceed to the **First-time Setup** below.
<br>

#### Option 2: Python Script from Source
1. Install **Python 3.9** or newer.
2. Run the script.
3. The program will try to automatically install the `requests` module. If it fails, open your console/terminal and install it manually using the command: `pip install requests`.
4. Proceed to the **First-time Setup** below.
<br>

#### First-time Setup & Login
1. When you start the program for the first time (or after deleting `config.ini`), you will be asked to start the config setup. It's recommended to do so.
2. Next, the program will ask if you are logged into your Epic account in your default web browser.
3. An Epic Games website will open. Log in if you haven't already.
4. A page should then open with content similar to this:
   ```json
   {"redirectUrl":"https://localhost/launcher/authorized?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
   ```
   or this:
   ```json
   {"redirectUrl":"com.epicgames.fortnite://fnauth/?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
   ```
5. ➡️ Copy the `authorizationCode` (e.g., `930884289b5852842271e9027376a527`), paste it into the program, and press **ENTER**.
6. ✅ If everything went well, the program will confirm that the `auth.json` file was generated successfully. The program will then proceed to the Main Menu.
7. 🎉 Congratulations! You can now get your daily quest, open free llamas (if available), and much more!
8. The next time you launch the program, you won't need a new authorization code, as your login credentials are saved in `auth.json`.

</details>

---

### ❓ FAQ

<details>
<summary><b>Click to expand the answers to frequently asked questions</b></summary>
<br>

**🔒 Will my accounts be safe?**  
Yes! This program is open-source so anyone can read and verify the whole code. It runs only on your device and your login data is saved locally. Unlike Discord bots, your info is never sent to any third-party servers.

**❓ Can I get banned for using this?**  
No one has ever been banned for using this tool since I released the first version of it in 2021. The program safely interacts directly with the Epic Games API, acting just like the real game client. But like with any unofficial third-party software, use it at your own risk.

**🎁 What happened to Daily Login Rewards?**  
Daily Login Rewards were removed from the game in June 2023. Read more [here](https://www.fortnite.com/news/changes-coming-to-fortnite-save-the-worlds-daily-reward-system-in-v25-10 "Daily Login Rewards removal info").

**🧪 What happened to Research Points?**  
Research system was removed from the game in November 2025. Read more [here](https://www.reddit.com/r/FORTnITE/comments/1pa4vz8/save_the_world_v3900_update_notes "Research system removal info").

**🔔 How can I get notifications for free llamas?**  
You can set the program to loop every 60 minutes to ensure you won't miss them when they appear in the llama shop. Alternatively, I recommend joining [the r/FORTnITE discord server](https://discord.gg/PjqZaDmV8D "Here is the link :D") and assigning yourself the `freellamas` role so that you'll get pinged whenever they are available.

</details>

---

### 🐛 Found a bug?
Feel free to [open an issue](https://github.com/PRO100KatYT/SaveTheWorldClaimer/issues/new "Click here to open an issue.") if you encounter any bugs or just have a question.

---

### ⭐ Star History

<details>
<summary><b>Thanks to all stargazers! Click to expand the Star History Chart.</b></summary>
<br>

<a href="https://www.star-history.com/?repos=PRO100KatYT%2FSaveTheWorldClaimer&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=PRO100KatYT/SaveTheWorldClaimer&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=PRO100KatYT/SaveTheWorldClaimer&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/image?repos=PRO100KatYT/SaveTheWorldClaimer&type=date&legend=top-left" />
 </picture>
</a>

</details>

---

Portions of the materials used are trademarks and/or copyrighted works of Epic Games, Inc. All rights reserved by Epic. This material is not official and is not endorsed by Epic.

This tool is a fan-made, non-commercial Fortnite: Save the World project created for educational and utility purposes.
