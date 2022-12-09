###
# Mastostatus, bot para publicar el estado de una instancia en Mastodon
# Fork (cada vez más lejano) del bot "info" original de @spla@mastodont.cat
# En https://git.mastodont.cat/spla/info
###  

from bundle.mastobot import Mastobot
from bundle.config import Config
from bundle.logger import Logger
from bundle.translator import Translator

import random

class Runner:
    '''
    Main runner of the app
    '''
    def init(self):
        self._config     = Config()
        self._logger     = Logger(self._config).getLogger()

        self._logger.info("init app")

        self._translator = Translator("es")
        self._bot        = Mastobot(self._config)
        self._keyword    = self._config.get("app.keyword") 

        return self

    def run(self):

        self._logger.debug ("runing app with " + self._keyword)

        notifications = self._bot.mastodon.notifications()

        for notif in notifications:
            if notif.type == 'mention':
                if self._bot.check_keyword_in_nofit(self._bot, notif, self._keyword):
                    text_post = self.replay_text(notif.status.language)
                    self._logger.debug ("answersing with\n" + text_post)

                    if self._config.get("testing.disable_push_answer"):
                        self._logger.info("push answer disabled")                    
                    else:
                        self._logger.info("answering notification id" + str(notif.id))
                        self._bot.replay(notif, text_post)

            if self._config.get("testing.disable_dismis_notification"):
                self._logger.debug("dismis notification disabled")                    
            else:
                self._logger.debug("dismissing notification id" + str(notif.id))
                self._bot.mastodon.notifications_dismiss(notif.id)


        self._logger.info("end app")


    def replay_text(self, language):        
    
        self._logger.debug("notif language: " + language)                    

        self._translator.fix_language (language)
        _text     = self._translator.get_text
        
        mau = self._bot.mastodon.instance_nodeinfo().usage.users.activeMonth
        mau = '{:,}'.format(mau).replace(',','.')

        registers = self._bot.mastodon.instance().stats.user_count
        registers = '{:,}'.format(registers).replace(',','.')

        posts = self._bot.mastodon.instance().stats.status_count
        posts = '{:,}'.format(posts).replace(',','.')

        peers = self._bot.mastodon.instance().stats.domain_count
        peers = '{:,}'.format(peers).replace(',','.')

        version = self._bot.mastodon.instance().version

        if self._bot.mastodon.instance_nodeinfo().openRegistrations:
            opened = _text ("abierto")
        else:
            opened = _text ("cerrado")

        post_text  = ", " +_text("estado") + " " + self._bot._hostname + ":\n\n"
        post_text += _text("registrados") + ": " + registers + "\n"
        post_text += _text("activos") + ": " + mau + "\n"
        post_text += _text("apuntes") + ": " + posts + "\n"
        post_text += _text("federados") + ": " + posts + "\n"
        post_text += _text("version") + ": " + version + "\n"
        post_text += _text("registro") + ": " + opened + "\n\n"
        post_text += "(" + _text("mencion") + " " + self._keyword + " " + _text("respuesta") + ")"

        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text

        self._logger.debug ("answer text\n" + post_text)

        return post_text

# main

if __name__ == '__main__':
    Runner().init().run()
