# coding=utf-8
import time
import itchat
import os
import requests
import urllib

MIMA_URL = 'http://gerenhao.mima.fetqf.com/mima/json'

def qixi_reply():
    @itchat.msg_register
    def get_pic(msg):
        #print itchat.get_userinfo()
        if msg.get('Type', '') == 'Text':
            txt = msg['Text']
            # is_birthday = (txt.isdigit() and len(txt)==8)
            is_at = False;
            if txt[0] =="@":
                is_at = True;
                txt = txt[1:];
            if( is_at and len(txt)>=4 and len(txt)<=24 ):
                img = http_get_mima_img( txt );
                # print img;
                if os.path.exists( img ):
                    itchat.send(u'哈哈,你的密语图片生成了,发给你的朋友让他猜猜看', msg['FromUserName']);
                    return '@img@'+img;
                else:
                    itchat.send(u'有点忙,请稍候在试试', msg['FromUserName']);
            elif txt == '1':
                itchat.send(u'视线15°斜看密语图片,你会发现密码', msg['FromUserName']);
            else:
                itchat.send(u'请输入你的七夕密语,以@开头,如:\n\n@静静我爱你\n\n最少4个字,至多24字\n\n回复『 1 』,获取密语答案', msg['FromUserName']);

    @itchat.msg_register('Friends')
    def add_friend(msg):
        itchat.add_friend(**msg['Text']);
        itchat.get_contract();
        itchat.send(u'亲\n\n请输入你的七夕密语,以@开头,如:\n\n@静静我爱你\n\n最少4个字,至多24字\n\n回复『 1 』,获取密语答案', msg['RecommendInfo']['UserName']);

    itchat.run()

def http_get_mima_img( miyu ):
    payload = {'miyu': miyu };
    url = MIMA_URL;
    rs = requests.get( url=url ,timeout=3, params=payload);
    ret = rs.json();

    img_url = ret['data']['img'];
    # print img_url

    (filepath, tempfilename) = os.path.split(img_url);
    (shotname, extension) = os.path.splitext(tempfilename);

    path = os.path.abspath(os.curdir);
    img_name = path +'/miyu/'+ str(time.time())+extension;
    urllib.urlretrieve(img_url,img_name);
    return img_name;

if __name__ == '__main__':
    itchat.auto_login( enableCmdQR = True )
    qixi_reply()