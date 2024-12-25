import requests
import random
import json
import time
from lunarcalendar.festival import festivals
import datetime


def get_holiday():
    today = datetime.date.today()
    for fest in festivals:
        if today == fest(2024):
            return "今天是" + fest.get_lang('zh')
    return None



images_directory = "static/images"
online_draw_key = "0d2977d8d84048f5a8102fdd5c7ddd1d"

url = "https://cn.tensorart.net/v1/jobs"
online_draw_headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "Authorization": f"Bearer {online_draw_key}"
}


def online_generate(prompt):
    print("云端启动绘画")
    requests_id = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    width = 1152
    height = 768
    prompt2 = "1girl, solo, long hair, looking at viewer, pink hair,msterpiece,detailed,yellow eyes,long hair" + prompt
    model = "793993089154004222"

    data = {
        "request_id": str(requests_id),
        "stages": [
            {
                "type": "INPUT_INITIALIZE",
                "inputInitialize": {
                    "seed": -1,
                    "count": 1
                }
            },
            {
                "type": "DIFFUSION",
                "diffusion": {
                    "width": width,
                    "height": height,
                    "prompts": [{"text": prompt2}],
                    "steps": 25,
                    "sdVae": "Automatic",
                    "negativePrompts": [{
                        "text": "nude,naked,picture frame,cropped,out of frame,(worst quality, low quality:1.4),deformed iris,deformed pupils,(deformed, distorted, disfigured:1.3),poorly drawn,bad anatomy,wrong anatomy,extra limb,missing limb,floating limbs,cloned face,(mutated hands and fingers:1.4),disconnected limbs,extra legs,fused fingers,too many fingers,long neck,mutation,mutated,ugly,disgusting,amputation,blurry,jpeg artifacts,(watermark, watermarked, text, Signature:1.3),sketch,bad-artist-anime,EasyNegative,GhostMix-V2.0-fp16-BakedVAE,verybadimagenegative_v1.3,"}],
                    "sd_model": model,
                    "clip_skip": 1,
                    "cfg_scale": 6,
                    "sampler": "Euler a",
                    "lora": {
                        "items": [
                            {
                                "loraModel": "802540623828833319",
                                "weight": 0.7
                            },
                            {
                                "loraModel": "763943054114628494",
                                "weight": 0.3
                            },
                            {
                                "loraModel": "800370016076841484",
                                "weight": 0.6
                            }
                        ]
                    }

                }
            },
            {
                "type": "IMAGE_TO_UPSCALER",
                "image_to_upscaler": {
                    "hr_upscaler": "R-ESRGAN 4x+ Anime6B",
                    "hr_scale": 2,
                    "hr_second_pass_steps": 10,
                    "denoising_strength": 0.3
                }
            }
        ]
    }
    response = requests.post(url, headers=online_draw_headers, data=json.dumps(data))

    if response.status_code == 200:
        id = json.loads(response.text)['job']['id']
        return id
    else:
        print(f"请求失败，状态码：{response.status_code}，请检查是否正确填写了key")
        return "error"


def get_result(job_id, image_name):
    while True:
        time.sleep(1)
        response = requests.get(f"{url}/{job_id}", headers=online_draw_headers)
        get_job_response_data = json.loads(response.text)
        if 'job' in get_job_response_data:
            job_dict = get_job_response_data['job']
            job_status = job_dict.get('status')
            if job_status == 'SUCCESS':
                url2 = job_dict["successInfo"]["images"][0]["url"]
                response = requests.get(url2)
                with open(fr'{images_directory}\{image_name}.png', 'wb') as f:
                    f.write(response.content)
                break
            elif job_status == 'FAILED':
                print(job_dict)
                break


def online_generate_image(prompt, image_name):
    task_id = online_generate(prompt)
    get_result(task_id, image_name)


def gpt(mode, system, prompt):
    gpt_key = "sk-Lf7dN6r59Dv9KvHM4b353a777a6247F7Bd4729C6B0E87a28"
    gpt_url = "https://api.bltcy.ai/v1/chat/completions"
    if mode == 1:
        payload = json.dumps({
            "model": "gpt-4o",
            "temperature": 0.8,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "user",
                    "content": "莉莉丝是一个可爱女生，请你随机生成一个她现在可能会做的事件（在适合的时间会睡觉和吃饭,如果是晚上睡觉，一般要睡到第二天7-9点左右，请计算好时间),"
                               "并且给出他的持续时间，单位为分钟,用json返回，"
                               + '{"event": "莉莉丝正在xxx", "hold_time": ""}' + prompt
                }
            ]
        })
    else:
        payload = json.dumps({
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {gpt_key}',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", gpt_url, headers=headers, data=payload)
    content = json.loads(response.text)['choices'][0]['message']['content']
    return content
