# GETCommunity Tools

This repo is a collection of different tools which can be used to give more insights into the usage of the GET Protocol NFTs. The combination of the different components in this repo can facilitate:

- The GET Protocol Events telegram channel
- The GET Protocol NFT Community Site (In progress, this 1 will replace the current community site)

## Prerequisites
The following prerequisites are necessary:
-	A postgress database. (This can be run inside a container, just start the postgres image (see also the Docker Compose file)
-	An Infura API key ( Get 1 from infura.io and enable Polygon on your account, it’s free)
-	A Polygonscan API key ( Get 1 from polygonscan.com, it’s free)
-	A telegram bot API key ( Get 1 from @botfather at Telegram, it’s free)

## Configuration:
-	Copy sample.env to prod.env and add the API keys
-	Run the Docker-compose file to start the containers (it will also launch a database container, exclude it if you have a locale Postgress database)
-	If you make changes to the code, and want to re-create the docker files, the Docker files in each root folder can be used.

## Code navigation:
All functionalities are divided over multiple containers which have an own function. The following list will provide a brief function of each container:
-	A Postgress database container or local installation (not in this repo) where all collected data is stored)
-	**EventsImporter** contains a program which imports all events fueled by the GET Protocol in the database
-	**NFTImporter** contains a program which import all GET Protocol NFTs in the database
-	**TelegramInput** contains a program which listen to all communication for the configured bot and will register the channel/group where the bots is active in the database.
-	**Reporter** contains a program which runs each day at 9:00 and provides a summery of the sold/scanned tickets of the last day.
-	**UpcomingEvents** contains a program which runs each day at 16:00 and generates a report with upcoming events in the upcoming 30 days including the amount of tickets being sold for these events.
-	**PriceImporter** contains a program which import the GET Protocol price from CoinGecko in the database every 5 minutes.
-	**CommunitySite** contains the GET Protocol NFT communitysite (Django), work in progress.
-	**CommunitySiteProxy** publish the GET Protocol NFT communitysite over https via an NGINX proxy


