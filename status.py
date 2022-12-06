###
# Mastoquote, bot para publicar citas en Mastodon
# Fork (cada vez más lejano) del bot "info" original de @spla@mastodont.cat
# En https://git.mastodont.cat/spla/info
###  

from bundle.mastobot import Mastobot
from bundle.config import Config
from bundle.logger import Logger
import random

class Runner:
    '''
    Main runner of the app
    '''
    def init(self):
        self._config = Config()
        self._logger = Logger(self._config).getLogger()
        self._logger.info("init app")

        return self

    def run(self):
        self._logger.info("run app")
        
        keyword = self._config.get("app.keyword")
        self._logger.info ("starting bot with " + keyword)

        bot = Mastobot(self._config)

        notifications = bot.mastodon.notifications()

        for notif in notifications:
            if notif.type == 'mention':
                mention = bot.get_mention(notif, keyword)

            if mention.reply:
                text_post = self.replay_text(bot, keyword)
                self._logger.debug ("answersing with\n" + text_post)

                if not self._config.get("testing.disable_push_answer"):
                    self._logger.info("answering notification id" + notif.id)
                    bot.replay(mention, text_post)

            if not self._config.get("testing.disable_dismis_notification"):
                self._logger.info("dismissing notification id" + notif.id)
                bot.mastodon.notifications_dismiss(notif.id)

        self._logger.info("end")

    def replay_text(self, bot, keyword):        
    
        mau = bot.mastodon.instance_nodeinfo().usage.users.activeMonth
        mau = '{:,}'.format(mau).replace(',','.')

        registers = bot.mastodon.instance().stats.user_count
        registers = '{:,}'.format(registers).replace(',','.')

        posts = bot.mastodon.instance().stats.status_count
        posts = '{:,}'.format(posts).replace(',','.')

        peers = bot.mastodon.instance().stats.domain_count
        peers = '{:,}'.format(peers).replace(',','.')

        version = bot.mastodon.instance().version

        reg_open = bot.mastodon.instance_nodeinfo().openRegistrations

        if reg_open:
            opened = 'abierto'
        else:
            opened = 'cerrado'

        post_text  = f", estado de {bot.mastodon_hostname}:\n\n"
        post_text += f"Usuarios registrados: {registers}\n"
        post_text += f"Usuarios activos (en el mes): {mau}\n"
        post_text += f"Apuntes: {posts}\n"
        post_text += f"Servidores federados: {peers}\n"
        post_text += f"Versión de Mastodon: v{version}\n"
        post_text += f"Registro: {opened} \n\n"
        post_text += f"(Mencióname con la palabra '{keyword}' y te responderé con estos datos)"
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text

        self._logger.debug ("answer text\n" + post_text)
        return post_text

# main

if __name__ == '__main__':
    Runner().init().run()
