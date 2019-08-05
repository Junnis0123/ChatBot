import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
import ParsingMail
from time import sleep
import threading, time

token = ''
chat_id = ''

# start
def start(bot, update) :
    global chat_id
    chat_id = update.message.chat.id
    update.message.reply_text('start to read mail.' )
        
    t = threading.Thread(target=Check_mail)
    t.daemon = True
    t.start()


# change from people
def chnage_from_people(bot, update) :
    name = update.message.text.split()
    if len(name) == 1:
        update.message.reply_text('Command is /change newName')
        return
    ParsingMail.change_from_name(name[1])
    update.message.reply_text('{}{}{}'.format('from person is  changed by ', name[1], ' ))


# print from people
def print_from_people(bot, update) :
    update.message.reply_text('{}{}{}'.format('To person is ', ParsingMail.get_name(), ' ))


#check Mail
def Check_mail():
    while True:
        count, data = ParsingMail.ConnectMailSvr()
        if count == 0:
            sleep(20)
            continue
        else:
            bot = telegram.Bot(token = token)
            bot.sendMessage(chat_id = chat_id, text='unseen mail is {}, new is {}'.format(count, len(data)))

            for mail in data:
                bot.sendMessage(chat_id = chat_id, text='subject : {}\ncontext : {}'.format(mail[0],mail[1]))
            sleep(60)
            

if __name__ == "__main__":

    updater = Updater(token)

    print_handler = CommandHandler('print', print_from_people)
    updater.dispatcher.add_handler(print_handler)

    change_handler = CommandHandler('change', chnage_from_people)
    updater.dispatcher.add_handler(change_handler)

    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    updater.start_polling(timeout=3, clean=True)
    updater.idle()

