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

        self._translator = Translator("es")

        super().__init__(botname = botname)


    def init_test_options (self):

        self._dismiss_disable = self._config.get("testing.disable_dismiss")
        self._test_word       = self._config.get("testing.text_word")

        self._logger.debug ("test_word: "   + self._test_word)
        self._logger.debug ("ignore test: " + str(self._config.get("testing.ignore_test_toot")))

        if self._test_word != "" and self._config.get("testing.ignore_test_toot"):
            self._ignore_test = True
        else:
            self._ignore_test = False 

        super().init_test_options()
 

    def run(self, botname: str = BOT_NAME) -> None:

        notifications = self.mastodon.notifications()

        for notif in notifications:

            dismiss = True

            if notif.type == 'mention':

                if self._dismiss_disable:
                    dismiss = False
                    self._logger.debug("dismissing disabled notification id " + str(notif.id))                    
    
                if self._ignore_test and self.check_keyword_in_nofit(notif, self._test_word):
                    dismiss = False
                    self._logger.info("ignoring test notification id " + str(notif.id))
                else: 

                    action = self._actions ["instance_status"]

                    if self.check_keyword_in_nofit(notif, action["keyword"]):
                        text_post = self.find_text(notif.status.language, action["keyword"])

                        if self._push_disable:
                            self._logger.info("pushing answer disabled notification id " + str(notif.id))                     
                        else:
                            self._logger.info("answering notification id " + str(notif.id))
                            self.replay(notif, text_post)

            if dismiss:
                self._logger.debug("dismissing notification id " + str(notif.id))
                self.mastodon.notifications_dismiss(notif.id)

        super().run(botname = botname)


    def find_text(self, language, keyword):        
    
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

        post_text  = ", " +_text("estado") + " " + self._hostname + ":\n\n"
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
