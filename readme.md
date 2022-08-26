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
- 15 languages support for Fortnite item names.
- Discord Webhook notification on token expiration 
---
### Changelog:
What's new in the 1.9.4 update:
- If enabled, the date and time in front of the messages now have a leading 0 next to a digit, making it look nicer.
- Removed the `Skipping Research Points claiming because {displayName} doesn't have access to the Research Lab.` message.
- Added Gia and Fennix heroes to the stringlist.
- Tweaked the program's code a little bit.
---

### How to use it?

## [Docker](https://hub.docker.com/repository/docker/probablypablito/savetheworldclaimer)

- Create a volume. `sudo docker volume create savetheworldclaimer`

- Run the setup in the container. `sudo docker run -it -v savetheworldclaimer:/app/data --name=SaveTheWorldClaimer --restart="always" probablypablito/savetheworldclaimer`

  - You may optionally add a Discord Webhook URL by adding `-e "discord_webhook_url=<url here>"` between `run` and `-it`. 
  
  - For help with setup, refer to the without Docker instructions.

- Use CTRL+C to exit the container once setup is done.

- Stop the container. `sudo docker stop SaveTheWorldClaimer`

- Run the container. `sudo docker start SaveTheWorldClaimer`

## Without Docker

- Install `Python 3.9.5` or newer.

- If you didn't do it yet, install the `requests` module. You can do it using the `pip install requests` console command.

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

- Next time you launch the program, to start claiming rewards, type 1 and press ENTER. You will not need to enter a new auth code because the login credentials have been saved in the auth.json file.
---

### Found a bug?
Feel free to [open an issue](https://github.com/PRO100KatYT/SaveTheWorldClaimer/issues/new "Click here if you want to open an issue.") if you encounter any bugs or just have a question.

---

If you want to receive notifications about free llamas, I recommend joining [the r/FORTnITE discord server](https://discord.gg/PjqZaDmV8D "Here is the link :D") and giving yourself the freellamas role on the #role-assignment channel.