
from flask import Flask, request
from telegram import Bot , Update
from telegram.ext import Dispatcher , CommandHandler
import threading

TOKEN = ''
WEBHOOK_URL = ''
WEBHOOK_PATH = ''


app = Flask(__name__)
bot = Bot(token=TOKEN) 
dispatcher = Dispatcher(bot , None , use_context = True)

# write in data base these two functions amir !! add_score & get_score
def get_score(user_id):
    return 0

def add_score(user_id , user_name , score):
    return 0

def start(update , context):
    update.message.reply_text(" Hello , For see Your Score Enter /score ")
    
def score(update , context):
    user = update.message.from_user
    u_score = get_score(user.id)
    update.message.reply_text(f'{user.first_name},Your Score : {u_score}')
    
def attend(update , context):
    user = update.message.from_user
    new_score = add_score(user.id , user.first_name , 3)
    update.message.reply_text(f'{user.first_name} , +3 score for attending to this session')
    
def translate(update,context):
    user = update.message.from_user
    new_score = add_score(user_id , user.first_name , 10)
    update.message.reply_text(f'{user.first_name} , +10 score for translating book')
    
def message_handler(update,context):
    message_text = update.message.text.lower()
    user = update.message.from_user
    user_id = user.id
    user_name = user.first_name
    
    positive_keywords = ['خیلی ممنون' , 'عالی' , 'فوق العاده' , 'خوب','مرسی']
    if any( word in message_text for word in positive_keywords):
        new_score = add_score(user_id , user_name , 1)
        update.message.reply_text(f'{user_name} , +1 score add :)    Your total score until now :{new_score}')
        
#handler
dispatcher.add_handler(CommandHandler("start",start))
dispatcher.add_handler(CommandHandler("score",score))
dispatcher.add_handler(CommandHandler("attend",attend))
dispatcher.add_handler(CommandHandler("translate",translate))

def handle_update(update_json):
    update = Update.de_json(update_json , bot)
    dispatcher.process_update(update)
    
@app.route(WEBHOOK_PATH , methods = ['POST'])
def webhook():
    update_json = request.get_json(force=True)
    threading.Thread(target=handle_update , args=(update_json , )).start()
    return 'OK'

if __name__ == '__main__':
    bot.set_webhook(WEBHOOK_URL)
    
ssl_cert = ''
ssl_key = ''

#app.run(host='0.0.0.0' , port=443 , ssl_context=(ssl_cert , ssl_key))
    
    