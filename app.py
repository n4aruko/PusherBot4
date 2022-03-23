from telegram.ext import *
import telegram
import ftplib
import  os
import json
USER=os.environ.get("USERIDSITE")
PASSWD = os.environ.get("PASSWDSITE")
SERVE = os.environ.get("SERVERIP")
session = ftplib.FTP(SERVE,USER,PASSWD)
def start_command(update, context):
    name = update.message.chat.first_name
    update.message.reply_text("Hello " + name)
    update.message.reply_text("Please share your image")

def image_handler(update, context):
    file = update.message.photo[-1].get_file()
    path = file.download("output.jpg")
    filepic = open("output.jpg","rb")
    session.cwd('/public_html/Paste/')
    session.storbinary('STOR Picture.jpg', filepic)
    filepic.close()



def echo(update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    file = open('test.txt','w')
    file.write(update.message.text)
    file.close()
    file2 = open("test.txt","rb")
    session.cwd('/public_html/Paste/')
    session.storbinary('STOR kitten.txt', file2)
    file.close()
#    session.quit()


def main():
    print("Started")
    TOKEN = os.environ.get("TELEGRAM_CODE")
    updater = Updater(TOKEN, use_context = True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dp.add_handler(MessageHandler(Filters.photo, image_handler))

#    updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",port=os.environ.get("PORT",443),url_path=TOKEN,webhook_url="https://pusherbot4.herokuapp.com/"+TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()
