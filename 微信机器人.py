import ntchat
import requests
import re
wechat = ntchat.WeChat()
# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)
#发送信息给指定的人
def sentmessage(name,content):
    wechat.send_text(to_wxid=str(name), content=str(content[0])+"\n(此消息为机器人发送)")
#调取api
def out_message(message,name):
    url = f'http://api.qingyunke.com/api.php?key=free&appid=0&msg={message}'
    repq = requests.get(url)
    repq0=repq.content.decode()
    print(repq0)
    repq1=re.findall('"content":"(.*?)"',repq0)#取出回答的问题
    sentmessage(name,repq1)#调用发信息的函数
# 注册监听所有消息回调
@wechat.msg_register(ntchat.MT_ALL)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    if(message["data"]["room_wxid"]==""and message["data"]["from_wxid"]!="wxid_rwzzppa76r2f22"):#判断是不是群发包括不给自己发
        name=message["data"]["from_wxid"]#取出要发送信息的微信号
        out_message(message["data"]["msg"],name)#
# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
while True:
    pass