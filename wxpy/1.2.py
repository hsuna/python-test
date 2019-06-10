# 导入模块
from wxpy import *
# 初始化机器人，扫码登陆
bot = Bot(cache_path=True, console_qr=True)

# 调用图灵机器人API
tuling = Tuling(api_key='')

# 查找到要使用机器人来聊天的好友
my_friend = ensure_one(bot.search('巽蓝'))

@bot.register()
def auto_reply(msg):
    tuling.do_reply(msg)

@bot.register(my_friend)
def reply_my_friend(msg):
    tuling.do_reply(msg)

embed()