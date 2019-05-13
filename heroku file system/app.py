from flask import Flask
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "your-token"
updater = Updater(token=TOKEN)

memory_of_users = []
count_of_moves = 0

def add_new_user(user_id):
    global memory_of_users
    if(memory_of_users):
        for user in memory_of_users:
            if (user_id == user):
                return False
    memory_of_users.append(user_id)
    return True

def start_function(bot, update):
    if(add_new_user(update.message.chat_id)):
        bot.send_message(chat_id= update.message.chat_id,
                         text= "You'll sub to get notifide about moves")
    else:
        bot.send_message(chat_id= update.message.chat_id,
                         text= "You already subed")
handler = CommandHandler("start", start_function)
updater.dispatcher.add_handler(handler)

def info_function(bot, update):
    global count_of_moves
    info_mess = "From the start of running server was count " + str(count_of_moves) + " moves"
    bot.send_message(chat_id= update.message.chat_id,
                     text= info_mess)
handler = CommandHandler("info", info_function)

updater.dispatcher.add_handler(handler)
updater.start_polling()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/esp')
def send_mess():
    global updater, count_of_moves
    count_of_moves += 1
    if(memory_of_users):
        for user in memory_of_users:
            updater.bot.send_message(chat_id= user, text= "Moves")
    return 'Message Sent! (' + str(count_of_moves) + ')'

@app.route('/<path:path>')
def catch_all(path):
    return 'Error, try just /'

if __name__ == "__main__":
    app.run()
