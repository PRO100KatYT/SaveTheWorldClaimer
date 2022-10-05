# SaveTheWorldClaimer
This fork does the following things differently:
  - Only allows for token auth
  - Removes all terminal input, except for setup
  - Runs in Docker
  - Runs a webserver
  - Sends a Discord webhook
When your auth token expires, it will send you a message on Discord via a webhook. You can then go to a URL that points to a port on the container, which will allow you to input your auth token again without having to mess with anything else

## [Docker](https://hub.docker.com/repository/docker/probablypablito/savetheworldclaimer)

- Run the setup in the container. `sudo docker run -p 8080:8000-e "discord_webhook_url=https://discord.com/example" -e "website=http://example.com" -it -v savetheworldclaimer:/app/data --name=SaveTheWorldClaimer --restart="always" probablypablito/savetheworldclaimer`

- If you dont want Discord notifications omit the respective -e flags.

- Set up the config how you want it to be by inputting the values. There are 1440 minutes in a day.

- Once done, press CTRL+C to exit out of the interactive session.

- Restart the container. `sudo docker restart SaveTheWorldClaimer`

- This will map your hosts port 8080 to the website. If you want to listen on a different port, change the (first) port.

You can now navigate to your website and submit your auth token!
