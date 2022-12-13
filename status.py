###
# Mastostatus, bot administrativo de una instancia. 
# De momento publica el estado, pero está preparado para hacer más acciones a partir de keywords
# Fork (cada vez más lejano) del bot "info" original de @spla@mastodont.cat
# En https://git.mastodont.cat/spla/info
###  

from bundle.mastobot import Mastobot
from bundle.config import Config
from bundle.logger import Logger
from bundle.translator import Translator

import random

BOT_NAME = "Statusbot"

class Bot(Mastobot):

    def __init__(self, botname: str = BOT_NAME) -> None:

        super().__init__(botname = botname)

        self.init_replay_bot()
        self.init_translator()


    def run(self, botname: str = BOT_NAME) -> None:

        notifications = self.mastodon.notifications()

        for notif in notifications:

            action   = self._actions["instance_status"]   
            replay, dismiss = self.process_notif(notif, "mention", action["keyword"])
            if replay:
                self.replay_toot(self.find_text(notif, action), notif)
     
            if dismiss:
                self.mastodon.notifications_dismiss(notif.id)

        super().run(botname = botname)


    def find_text(self, notif, action):        

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

        post_text  = "@" + username + ", " +_text("estado") + " " + self._hostname + ":\n\n"
        post_text += _text("registrados") + ": " + registers + "\n"
        post_text += _text("activos") + ": " + mau + "\n"
        post_text += _text("apuntes") + ": " + posts + "\n"
        post_text += _text("federados") + ": " + posts + "\n"
        post_text += _text("version") + ": " + version + "\n"
        post_text += _text("registro") + ": " + opened + "\n\n"
        post_text += "(" + _text("mencion") + " " + keyword + " " + _text("respuesta") + ")"

        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text

        self._logger.debug ("answer text\n" + post_text)

        return post_text


# main

if __name__ == '__main__':
    Bot().run()
