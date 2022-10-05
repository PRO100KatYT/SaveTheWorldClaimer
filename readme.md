## [Docker](https://hub.docker.com/repository/docker/probablypablito/savetheworldclaimer)

- Run the setup in the container. `sudo docker run -e "discord_webhook_url=https://discord.com/example" -e "website=http://example.com" -it -v savetheworldclaimer:/app/data --name=SaveTheWorldClaimer --restart="always" probablypablito/savetheworldclaimer`

  - If you dont want Discord notifications omit both -e flags.
  
- Use CTRL+C to exit the container once setup is done
- Done!
