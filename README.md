# Info
This code publish information of the Mastodon instance where the bot has its account, if requested.  
Based in the info bot of @spla@mastodont.cat (https://git.mastodont.cat/spla/info)

The bot listen to 'frikistatus' word key:

@bot_username info  

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

1. Run `pip install -r requirements.txt` to install needed libraries.  

2. Run `python info.py` manually once to bot setup and get its access token to Mastodon instance.

3. Use your favourite scheduling method to set `python info.py` to run every minute.   

