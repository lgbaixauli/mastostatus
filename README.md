# Mastostatus

This code publish information of the Mastodon instance where the bot has its account, if requested.  
Based in the 'info' bot of @spla@mastodont.cat (https://git.mastodont.cat/spla/info)

The bot listen to a keyword:

@bot_username keyword

and then reply following information:  

Registered users  
Active users (MAU)  
LocalPosts  
Instance's peers  
Mastodon's version  
Registration Opened/Closed

### Dependencies

-   **Python 3**
-   Mastodon account

### Usage:

Within Python Virtual Environment:

1. Optionally, create a new user for running the bot: `adduser --disabled-login user_name`

2. Clone the repository `git clone https://github.com/lgbaixauli/mastostatus.git` 

3. Crate a virtual environment `python3 -m venv .venv` and activate it `source .venv/bin/activate`

4. Run `pip install -r requirements.txt` to install needed libraries.  

5. Modify options in the `config.yaml` file. For exemple, the keyword the access type or directory and file names.

6. It's possible to fill in the config yaml the cliend id, cliend secret and access token of an application created in the Mastodon web (with de "development" opction). Also, it's possilbe to indicate credentials access and run `python3 quote.py` manually once to setup and get its access token to Mastodon instance.

7. Use your favourite scheduling method to set `status.sh` to run every minute. For example,  add  `* * * * * /home/user_name/mastostatus/status.sh 2>&1 | /usr/bin/logger -t MASTOSTATUS` in `crontab -e`. The system and error log will be in `/var/log/syslog`. 

   Don't forgot the execution privilegies `chmod +x status.sh`. 
   Don't forgot update the user_name in `status.sh`
