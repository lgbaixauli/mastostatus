from mastobot import Mastobot

# main

if __name__ == '__main__':

    keyword = "frikistatus"

    def replay_text ():

        mau = bot.mastodon.instance_nodeinfo().usage.users.activeMonth
        mau = '{:,}'.format(mau).replace(',','.')

        registers = bot.mastodon.instance().stats.user_count
        registers = '{:,}'.format(registers).replace(',','.')

        posts = bot.mastodon.instance().stats.status_count
        posts = '{:,}'.format(posts).replace(',','.')

        peers = bot.mastodon.instance().stats.domain_count
        peers = '{:,}'.format(peers).replace(',','.')

        version = bot.mastodon.instance().version

        reg_open =  bot.mastodon.instance_nodeinfo().openRegistrations

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

        return post_text

    bot = Mastobot()

    notifications = bot.mastodon.notifications()

    for notif in notifications:

        if notif.type != 'mention':

            print(f"Dismissing notification id {notif.id}")

            bot.mastodon.notifications_dismiss(notif.id)

        else:

            mention = bot.get_mention(notif, keyword)

            if mention.reply:

                print(f"Answering notification id {notif.id}")

                text_post = replay_text()

                bot.replay(mention, text_post)

            else:

                print(f"Dismissing notification id {notif.id}")

                bot.mastodon.notifications_dismiss(notif.id)
