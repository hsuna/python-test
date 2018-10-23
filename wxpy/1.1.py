from wxpy import *
# 初始化机器人，扫码登陆
bot = Bot(cache_path=False, console_qr=True)

#try:
    # 发送消息给自己
bot.file_helper.send('Hello from wxpy!')
#except ResponseError as e:
    # 若群员还不是好友，将抛出 ResponseError 错误
 #   print('error', e.err_code, e.err_msg) # 查看错误号和错误消息