# Info
This code publish information of the Mastodon instance where the bot has its account, if requested.  
Based in the 'info' bot of @spla@mastodont.cat (https://git.mastodont.cat/spla/info)

The bot listen to 'frikistatus' word key:

@bot_username frikistatus

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

3. Run `pip install -r requirements.txt` to install needed libraries.  

4. Run `python3 status.py` manually once to bot setup and get its access token to Mastodon instance.

5. Use your favourite scheduling method to set `status.sh` to run every minute. For example, 
   add  `* * * * * /home/user_name/mastostatus/status.sh 2>&1 | /usr/bin/logger -t MASTOSTATUS` in 
   `crontab -e`. The system and error log will be in `/var/log/syslog`. 
   Don't forgot the execution privilegies `chmod +x info.sh`. 
   Don't forgot update the user_name in `status.sh`  

