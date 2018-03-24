import threading
from flask import Flask
from dreamfarm.bot import bot
from dreamfarm.web.controllers import web
from dreamfarm.web.api import api

lock = threading.Lock()
bot_thread = threading.Thread()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(web, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    global bot_thread
    bot_thread = threading.Thread(target=bot.run)
    bot_thread.start()

    return app

app = create_app()
