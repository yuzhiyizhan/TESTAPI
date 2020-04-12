# from loguru import logger
# from Testapi.config.config import LOG_NAME
#
# # logger.add(
# #     LOG_NAME, level='INFO', rotation="10 MB", retention="7 days", backtrace=True, diagnose=True,
# #     enqueue=True,
# #     serialize=False)
# logger.add('runtime.log', format="{time} {level} {message}", filter="my_module", level="INFO")
# logger.info("That's it, beautiful and simple logging!")
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return '{hello:1}'


@app.route('/debug', methods=['GET', 'POST'])
def hello_world():
    r = request.args.get('info', '请用info传参')

    return r


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555, debug=True)
