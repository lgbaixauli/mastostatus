###
# Mastostatus, bot administrativo de una instancia. 
# De momento publica el estado, pero está preparado para hacer más acciones a partir de keywords
# Fork (cada vez más lejano) del bot "info" original de @spla@mastodont.cat
# En https://git.mastodont.cat/spla/info
###  

from pybot.mastobot import Mastobot
from pybot.programmer import Programmer
from pybot.config import Config
from pybot.translator import Translator
from pybot.logger import Logger

import random
import datetime

BOT_NAME = "Statusbot"

class Bot(Mastobot):

    def __init__(self, botname: str = BOT_NAME) -> None:

        super().__init__(botname = botname)

        self.init_replay_bot()
        self.init_publish_bot()
        self.init_translator()
        self.init_programmer()
        self.init_output_file()


    def run(self, botname: str = BOT_NAME) -> None:

        action   = self._actions["write_status"]   
        if self.check_programmer(action["hours"], True):
            self.write_output_file(self.find_row())
            self.post_toot (self.find_text(None, action), "en", 0)
     
        action   = self._actions["replay_status"]   
        notifications = self.mastodon.notifications()
 
        for notif in notifications:

            replay, dismiss = self.process_notif(notif, "mention", action["keyword"])
            if replay:
                self.replay_toot(self.find_text(notif, action), notif)
     
            if dismiss:
                self.mastodon.notifications_dismiss(notif.id)

        super().run(botname = botname)


    def find_text(self, notif, action):        

        if notif == None:
            language = "en" 
            username = ""        
        else:
            language = notif.status.language
            username = notif.account.acct
        
        keyword  = action["keyword"]
        
        self._logger.debug("notif language: " + language)                    
        self._logger.debug("notif kewword : " + keyword) 

        self._translator.fix_language (language)
        _text     = self._translator.get_text
        
        mau = self.mastodon.instance_nodeinfo().usage.users.activeMonth
        mau = '{:,}'.format(mau).replace(',','.')

        registers = self.mastodon.instance().stats.user_count
        registers = '{:,}'.format(registers).replace(',','.')

        posts = self.mastodon.instance().stats.status_count
        posts = '{:,}'.format(posts).replace(',','.')

        peers = self.mastodon.instance().stats.domain_count
        peers = '{:,}'.format(peers).replace(',','.')

        version = self.mastodon.instance().version

        if self.mastodon.instance_nodeinfo().openRegistrations:
            opened = _text ("abierto")
        else:
            opened = _text ("cerrado")

        if username == "":
            post_text  = _text("estado2") + " " + self._hostname + ":\n\n"
        else:
            post_text  = "@" + username + ", " +_text("estado") + " " + self._hostname + ":\n\n"
        
        post_text += _text("registrados") + ": " + registers + "\n"
        post_text += _text("activos") + ": " + mau + "\n"
        post_text += _text("apuntes") + ": " + posts + "\n"
        post_text += _text("federados") + ": " + posts + "\n"
        post_text += _text("version") + ": " + version + "\n"
        post_text += _text("registro") + ": " + opened + "\n\n"
        post_text += "(" + _text("mencion") + " \"" + keyword + "\" " + _text("respuesta") + ")"

        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text

        self._logger.debug ("answer text\n" + post_text)

        return post_text


    def find_row(self):        

        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')

        mau       = str(self.mastodon.instance_nodeinfo().usage.users.activeMonth)
        registers = str(self.mastodon.instance().stats.user_count)
        posts     = str(self.mastodon.instance().stats.status_count)
        peers     = str(self.mastodon.instance().stats.domain_count)
 
        row = [date, time, mau, registers, posts, peers]

        self._logger.debug ("row\n" + str(row))

        return row



# main

if __name__ == '__main__':
    Bot().run()
