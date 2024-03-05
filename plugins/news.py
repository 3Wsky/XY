import aiohttp
import pywxdll
import yaml
from loguru import logger

from plugin_interface import PluginInterface


class News(PluginInterface):
    def __init__(self):
        config_path = 'plugins/news.yml'
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f.read())

        self.api_url = config['api_url']
        self.response_format = config['response_format']
        self.api_key = config['api_key']

        main_config_path = 'main_config.yml'
        with open(main_config_path, 'r', encoding='utf-8') as f:
            main_config = yaml.safe_load(f.read())

        self.ip = main_config['ip']
        self.port = main_config['port']
        self.bot = pywxdll.Pywxdll(self.ip, self.port)

    async def run(self, recv):
        try:
            imageurl = 'https://example.com/image.jpg'  # 替换为实际的图片 URL
            datetime = '2024-03-05'  # 替换为实际的日期时间
            text = 'This is a news article.'  # 替换为实际的新闻文本

            params = {
                'imageurl': imageurl,
                'datetime': datetime,
                'text': text
            }

            headers = {
                'Authorization': self.api_key
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url, params=params, headers=headers) as response:
                    if response.status == 200:
                        if self.response_format == 'json':
                            json_data = await response.json()
                            # 处理返回的 JSON 数据
                            # ...
                        else:
                            # 处理其他返回格式的数据
                            # ...
                    else:
                        logger.error('Request failed with status code: {status_code}', status_code=response.status)

            out_message = '处理返回的数据，生成消息内容'
            logger.info('[发送信息]{out_message}| [发送到] {wxid}', out_message=out_message, wxid=recv['wxid'])
            self.bot.send_txt_msg(recv['wxid'], out_message)

        except Exception as error:
            out_message = '出现错误！⚠️{error}'.format(error=error)
            logger.info('[发送信息]{out_message}| [发送到] {wxid}'.format(out_message=out_message, wxid=recv['wxid']))
            self.bot.send_txt_msg(recv['wxid'], out_message)
