# itchat

[![Gitter](https://badges.gitter.im/littlecodersh/ItChat.svg)](https://gitter.im/littlecodersh/ItChat?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge) ![python](https://img.shields.io/badge/python-2.7-ff69b4.svg) ![python](https://img.shields.io/badge/python-3.5-red.svg) [English version](https://github.com/littlecodersh/ItChat/blob/master/README_EN.md)

itchat是一个开源的微信个人号接口，使用他你可以轻松的通过命令行使用个人微信号。

使用不到三十行的代码，你就可以完成一个能够处理所有信息的微信机器人。

如今微信已经成为了个人社交的很大一部分，希望这个项目能够帮助你扩展你的个人的微信号、方便自己的生活。


## Documents

你可以在[这里](https://itchat.readthedocs.org/zh/latest/)获取api的使用帮助。

## Installation

可以通过本命令安装itchat：

```python
pip install itchat
```

## Simple uses

通过如下代码，微信已经可以就日常的各种信息进行获取与回复。

```python
#coding=utf8
import itchat, time

@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
def text_reply(msg):
    itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'))

@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

@itchat.msg_register('Text', isGroupChat = True)
def text_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])

itchat.auto_login(True)
itchat.run()
```

## Advanced uses

### 命令行二维码

通过以下命令可以在登陆的时候使用命令行显示二维码：

```python
itchat.auto_login(enableCmdQR = True)
```

部分系统可能字幅宽度有出入，可以通过将enableCmdQR赋值为特定的倍数进行调整：

```python
# 如部分的linux系统，块字符的宽度为一个字符（正常应为两字符），故赋值为2
itchat.auto_login(enableCmdQR = 2)
```

默认控制台背景色为暗色（黑色），若背景色为浅色（白色），可以将enableCmdQR赋值为负值：

```python
itchat.auto_login(enableCmdQR = -1)
```

### 退出程序后暂存登陆状态

通过如下命令登陆，即使程序关闭，一定时间内重新开启也可以不用重新扫码。

```python
itchat.auto_login(hotReload = True)
```

### 用户搜索

使用`get_friends`方法可以搜索用户，有四种搜索方式：
1. 仅获取自己的用户信息
2. 获取特定`UserName`的用户信息
3. 获取备注、微信号、昵称中的任何一项等于`name`键值的用户
4. 获取备注、微信号、昵称分别等于相应键值的用户

其中三、四项可以一同使用，下面是示例程序：

```python
# 获取自己的用户信息，返回自己的属性字典
itchat.get_friends()
# 获取特定UserName的用户信息
itchat.get_friends(userName = '@abcdefg1234567')
# 获取任何一项等于name键值的用户
itchat.get_friends(name = 'littlecodersh')
# 获取分别对应相应键值的用户
itchat.get_friends(wechatAccount = 'littlecodersh')
# 三、四项功能可以一同使用
itchat.get_friends(name = 'LittleCoder机器人', wechatAccount = 'littlecodersh')
```

### 附件的下载与发送

itchat的附件下载方法存储在msg的Text键中。

发送的文件的文件名（图片给出的默认文件名）都存储在msg的FileName键中。

下载方法接受一个可用的位置参数（包括文件名），并将文件相应的存储。

```python
@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    msg['Text'](msg['FileName'])
    itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']), msg['FromUserName'])
    return '%s received'%msg['Type']
```

## Have a try

这是一个基于这一项目的[开源小机器人](https://github.com/littlecodersh/ItChat/tree/robot)，百闻不如一见，有兴趣可以尝试一下。

![QRCode](http://7xrip4.com1.z0.glb.clouddn.com/ItChat%2FQRCode2.jpg?imageView/2/w/400/)

## Screenshots

![file_autoreply](http://7xrip4.com1.z0.glb.clouddn.com/ItChat%2FScreenshots%2F%E5%BE%AE%E4%BF%A1%E8%8E%B7%E5%8F%96%E6%96%87%E4%BB%B6%E5%9B%BE%E7%89%87.png?imageView/2/w/300/) ![login_page](http://7xrip4.com1.z0.glb.clouddn.com/ItChat%2FScreenshots%2F%E7%99%BB%E5%BD%95%E7%95%8C%E9%9D%A2%E6%88%AA%E5%9B%BE.jpg?imageView/2/w/450/)

## FAQ

Q: 为什么中文的文件没有办法上传？

A: 这是由于`requests`的编码问题导致的。若需要支持中文文件传输，将[fields.py](https://github.com/littlecodersh/ItChat/blob/robot/plugin/config/fields.py)文件放入requests包的packages/urllib3下即可

Q: 为什么我在设定了`itchat.auto_login()`的`enableCmdQR`为`True`后还是没有办法在命令行显示二维码？

A: 这是由于没有安装可选的包`pillow`，可以使用右边的命令安装：`pip install pillow`

Q: 如何通过这个包将自己的微信号变为控制器？

A: 有两种方式：发送、接受自己UserName的消息；发送接收文件传输助手（filehelper）的消息

## Author

[LittleCoder](https://github.com/littlecodersh): 整体构架及完成Python2版本。

[Chyroc](https://github.com/Chyroc): 完成Python3版本。

## See also

[liuwons/wxBot](https://github.com/liuwons/wxBot): 类似的基于Python的微信机器人

[zixia/wechaty](https://github.com/zixia/wechaty): 基于Javascript(ES6)的微信个人账号机器人NodeJS框架/库

## Comments

如果有什么问题或者建议都可以在这个[Issue](https://github.com/littlecodersh/ItChat/issues/1)和我讨论

或者也可以在gitter上交流：[![Gitter](https://badges.gitter.im/littlecodersh/ItChat.svg)](https://gitter.im/littlecodersh/ItChat?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
