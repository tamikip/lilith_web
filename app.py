from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import threading
import time
from main import gpt, online_generate_image
import os
from main import get_holiday

app = Flask(__name__)

precomputed_event_content = ""


def precompute_data():
    global precomputed_event_content, precomputed_comment, precomputed_hold_time

    current_time = datetime.now().strftime("%H:%M:%S")
    holiday = get_holiday()
    print(holiday)
    precomputed_event_content = "你做的上一件事情是{precomputed_event_content}" if precomputed_event_content else ""
    prompt = f"现在的时间是{current_time}，{precomputed_event_content},{holiday}"
    print(prompt)
    event = gpt(1, "", prompt)
    event_data = json.loads(event)
    precomputed_event_content = event_data.get("event")
    print("事件:", precomputed_event_content)
    precomputed_hold_time = event_data.get("hold_time")
    # print("持续时间:", precomputed_hold_time)
    # en_event = gpt(2, "翻译下面的内容成英文，只需要保留动作和名词，无需给出人名，用短词格式输出，例如：run,swim,sleep,book",
    #                precomputed_event_content)
    # print("英文prompt:", en_event)
    # online_generate_image(en_event, "pic")
    if "睡" in precomputed_event_content:
        precomputed_comment = "ZZZ~(呼噜声)"
    else:
        precomputed_comment = gpt(2,
                                  "你是一个有些傲娇的二次元女生莉莉丝，现在你正在做一件事情，请你用一句话对周围正在观看你做这件事情的人说一句话。",
                                  precomputed_event_content).replace("哼，", "")


def scheduled_task():
    while True:
        precompute_data()
        time.sleep(int(precomputed_hold_time) * 60)


@app.route('/')
def index():
    return render_template('index.html', event=precomputed_event_content, comment=precomputed_comment,
                           hold_time=precomputed_hold_time)


@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    user_comment = request.json.get('comment')
    if "睡" not in precomputed_event_content:
        gpt_response = gpt(2, f"你是一个有些傲娇的二次元女生莉莉丝，{precomputed_event_content}，现在有人对你进行了评论:",
                           user_comment)
        return jsonify({
            'gpt_response': gpt_response
        })
    else:
        return jsonify({
            'gpt_response': "[自动回复]本公主睡着了，有什么事等我醒了再说吧"
        })


if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        precompute_data()
        task_thread = threading.Thread(target=scheduled_task)
        task_thread.daemon = True
        task_thread.start()

    app.run(debug=True)
