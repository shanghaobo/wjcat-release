from django.shortcuts import render,HttpResponse,redirect
# from botAdmin import models
import json
from .models import *
from datetime import datetime, timedelta
import time
from django.views.generic import TemplateView

# Create your views here.

def index(request):

    # return TemplateView.as_view(template_name="index.html")
    username = request.session.get('username')
    if not username:
        return redirect('/login')
        # return TemplateView.as_view(template_name="index.html")
    else:
        return render(request, 'index.html')
        # pass
        # return TemplateView.as_view(template_name="index.html")




#检查登录是否过期
def check(func):
    def wrapper(request):
        username=request.session.get('username')
        print('username=%s'%username)
        if username:
            return func(request,username)
        return HttpResponse(json.dumps({'code': '-1', 'errormsg': '登录过期！'}))
    return wrapper

#检查群号是否有误
def checkGroup(func):
    def wrapper(request,username):
        reqInfo = json.loads(str(request.body, encoding='utf-8'))
        group=reqInfo.get('group')
        if group:
            obj=GroupConfig.objects.filter(username=username,group=group)
            if obj.exists():
                return func(request,username,group)
            else:
                return HttpResponse(json.dumps({'code': '-5', 'errormsg': '群号有误！'}))
        else:
            return HttpResponse(json.dumps({'code': '-5', 'errormsg': '群号有误！'}))
    return wrapper


#登录
def login(request):
    response = {'code': '0', 'success': 'false', 'errormsg': ''}
    reqInfo = json.loads(str(request.body, encoding='utf-8'))
    if request.method=='POST':
        username = reqInfo.get('username', None)
        password = reqInfo.get('password', None)
        if username and password:
            try:
                user =User.objects.get(username=username)
                if user.password == password:
                    response['success'] = 'true'
                    request.session['username']=username
                else:
                    response['success'] = 'false'
                    response['errormsg'] = '账号或密码错误'
            except User.DoesNotExist:
                response['errormsg'] = '账号或密码错误'
        else:
            response['code'] = '-6'
            response['errormsg']='用户名或密码不存在'
        return HttpResponse(json.dumps(response))

# 注册
def register(request):
    response = {'code': '0', 'errormsg': ''}
    reqInfo = json.loads(str(request.body, encoding='utf-8'))
    if request.method == 'POST':
        username = reqInfo.get('username', None)
        password = reqInfo.get('password', None)
        visited = reqInfo.get('visited', None)
        if username and password:
            obj=BotConfig.objects.filter(username=visited)
            if obj.exists():
                user = User.objects.filter(username=username)
                if user.exists():
                    response['code'] = '-7'
                    response['errormsg'] = '用户名已存在'
                else:
                    User.objects.create(username=username, password=password, visited=visited)
            else:
                response['code'] = '-6'
                response['errormsg'] = '邀请码不存在'
        else:
            response['code'] = '-6'
            response['errormsg'] = '用户名或密码不存在'
        return HttpResponse(json.dumps(response))

#登出
@check
def logout(request,username):
    response = {'code': '0', 'errormsg': ''}
    reqInfo = json.loads(str(request.body, encoding='utf-8'))
    if request.method == 'POST':
        del request.session['username']
        return HttpResponse(json.dumps(response))



#检测登录是否过期
@check
def loginCheck(request,username):
    response = {'code': '0', 'errormsg': ''}
    return HttpResponse(json.dumps(response))

#设置进群欢迎
@check
@checkGroup
def setWelcome(request,username,group):
    response = {'code': '0', 'errormsg': ''}
    reqInfo = json.loads(str(request.body, encoding='utf-8'))
    if request.method == 'POST':
        content = reqInfo.get('content',None)
        # print('set:group=%s,content=%s'%(group,content))
        obj=Welcome.objects.filter(group=group)
        if not obj.exists():
            Welcome.objects.create(group=group, content=content)
        else:
            obj.update(content=content)

        return HttpResponse(json.dumps(response))

#获取进群欢迎
@check
@checkGroup
def getWelcome(request,username,group):
    response = {'code': '0', 'errormsg': ''}
    # reqInfo=json.loads(str(request.body,encoding='utf-8'))
    if request.method == 'POST':
        obj = Welcome.objects.filter(group=group)
        if not obj.exists():
            response['detail']=''
        else:
            response['detail'] =obj[0].content
        return HttpResponse(json.dumps(response))

#获取关键词禁言
@check
@checkGroup
def getKeyStop(request,username,group):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        # reqInfo = json.loads(str(request.body, encoding='utf-8'))
        obj=KeyStop.objects.filter(group=group)
        if obj.exists():
            keyword=obj[0].keyword
            tempList=keyword.split(',')
            response['detail'] = tempList
        else:
            response['detail']=[]
        time=KeyStop.objects.filter(group=group)
        if time.exists():
            response['time']=time[0].time
        else:
            response['time']=0

        return HttpResponse(json.dumps(response))

#设置关键词禁言
@check
@checkGroup
def setKeyStop(request,username,group):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        reqInfo = json.loads(str(request.body, encoding='utf-8'))
        keyList=reqInfo.get('keyList',None)
        time=reqInfo.get('time',None)
        if type(time)==str and time.isdigit():
            time=int(time)
        if keyList!=None and time!=None and type(time)==int:
            keyword=','.join(keyList)
            obj = KeyStop.objects.filter(group=group)
            if obj.exists():
                obj.update(keyword=keyword,time=time)
            else:
                KeyStop.objects.create(group=group,keyword=keyword,time=time)
        else:
            response['code'] = '-2'
            response['errormsg'] = '传入数据有误'
    return HttpResponse(json.dumps(response))

#获取关键词回复
@check
@checkGroup
def getKeyReply(request,username,group):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        obj=KeyReply.objects.filter(group=group)
        detail = []
        for item in obj:
            temp = {}
            temp['keyword'] = item.keyword
            temp['reply'] = item.reply
            detail.append(temp)
        response['detail']=detail
        return HttpResponse(json.dumps(response))

#设置关键词回复
@check
@checkGroup
def setKeyReply(request,username,group):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        reqInfo = json.loads(str(request.body, encoding='utf-8'))
        oldkey = reqInfo.get('oldkey', None)
        keyword=reqInfo.get('keyword',None)
        reply=reqInfo.get('reply',None)
        if oldkey!=None and keyword and reply:
            if oldkey!='':
                obj=KeyReply.objects.filter(group=group,keyword=oldkey).update(keyword=keyword,reply=reply)
            else:
                KeyReply.objects.create(group=group,keyword=keyword,reply=reply)
        else:
            response['code']=-2
            response['errormsg']='传入数据有误'
    return HttpResponse(json.dumps(response))

#删除关键词回复
@check
@checkGroup
def delKeyReply(request,username,group):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        reqInfo = json.loads(str(request.body, encoding='utf-8'))
        keyword=reqInfo.get('keyword',None)
        if keyword:
            obj = KeyReply.objects.filter(group=group,keyword=keyword)
            if obj.exists():
                obj.delete()
        else:
            response['code']=-2
            response['errormsg']='传入数据有误'
        return HttpResponse(json.dumps(response))

#机器人开关
@check
@checkGroup
def openBot(request, username,group):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        reqInfo = json.loads(str(request.body, encoding='utf-8'))
        status=reqInfo.get('status',None)
        if status!=None and type(status)==bool:
            obj=GroupConfig.objects.filter(username=username,group=group)
            if obj.exists():
                obj.update(status=status)
            else:
                response['code'] = -5
                response['errormsg'] = '群不存在'
        else:
            response['code'] = -2
            response['errormsg'] = '传入数据有误'
        return HttpResponse(json.dumps(response))

#初始化我的页面
@check
@checkGroup
def initMine(request, username,group):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        obj = GroupConfig.objects.filter(username=username, group=group)
        if obj.exists():
            response['status'] = obj[0].status
            # response['group'] = obj[0].group
        else:
            response['status'] = False
        response['username']=username
        response['botqq'] = GroupConfig.objects.filter(group=group)[0].botqq
        return HttpResponse(json.dumps(response))


#获取管理员口令
@check
def getAdminKey(request, username):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        obj=AdminKey.objects.all()
        detail=[]
        for item in obj:
            temp={}
            temp['name']=item.name
            temp['way']=item.way
            detail.append(temp)
        response['detail']=detail
        return HttpResponse(json.dumps(response))

# 获取黑名单
@check
@checkGroup
def getBlackName(request, username,group):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        obj = BlackName.objects.filter(group=group)
        detail = []
        for item in obj:
            detail.append(item.qq)
        response['detail'] = detail
        return HttpResponse(json.dumps(response))

# 移除黑名单
@check
@checkGroup
def removeBlackName(request, username, group):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        reqInfo = json.loads(str(request.body, encoding='utf-8'))
        qq = reqInfo.get('qq', None)
        if qq:
            obj = BlackName.objects.filter(group=group,qq=qq)
            if obj.exists():
                obj.delete()
            else:
                response['code'] = -2
                response['errormsg'] = '传入数据有误'
        else:
            response['code'] = -2
            response['errormsg'] = '传入数据有误'

        return HttpResponse(json.dumps(response))

# 获取邀请记录
@check
@checkGroup
def getInviteDetail(request, username,group):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        inObj = InGroupDetail.objects.filter(group=group)
        outObj=OutGroupDetail.objects.filter(group=group)
        inCount={}
        outCount={}
        detail=[]
        for item in inObj:
            inCount[item.inviteQQ]=inCount.get(item.inviteQQ,0)+1
        for item in outObj:
            outCount[item.inviteQQ]=outCount.get(item.inviteQQ,0)+1
        for key,value in inCount.items():
            if key=='' or key==None:
                continue
            detail.append({
                'qq':key,
                'inCount':value,
                'outCount':outCount.get(key,0),
                'trueCount':value-outCount.get(key,0)
            })
        response['detail'] = detail
        return HttpResponse(json.dumps(response))


# 获取邀请记录
@check
@checkGroup
def getInviteSeven(request, username,group):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        inObj = InGroupDetail.objects.filter(group=group,status=True)
        outObj = OutGroupDetail.objects.filter(group=group)
        inCount = {}
        outCount = {}
        detail = []
        for item in inObj:
            inCount[item.inviteQQ] = inCount.get(item.inviteQQ, 0) + 1
        for item in outObj:
            outCount[item.inviteQQ] = outCount.get(item.inviteQQ, 0) + 1
        for key, value in inCount.items():
            if key == '' or key == None:
                continue
            detail.append({
                'qq': key,
                'inCount': value,
                'outCount': outCount.get(key, 0),
                'trueCount': value - outCount.get(key, 0)
            })
        response['detail'] = detail

        return HttpResponse(json.dumps(response))

# 获取邀请记录七天数据
@check
@checkGroup
def getInviteSeven(request, username,group):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        allTime=[]
        allInCount=[]
        allOutCount=[]
        allTrueCount=[]

        for i in range(1, 8):
            day = str(datetime.today().date() - timedelta(days=(7 - i)))
            timestamp = int(time.mktime(time.strptime(day, '%Y-%m-%d')))
            inObj = InGroupDetail.objects.filter(group=group,timestamp__gte=timestamp,timestamp__lt=timestamp+86400)
            allInCount.append(inObj.count())
            outObj = OutGroupDetail.objects.filter(group=group, timestamp__gte=timestamp,timestamp__lt=timestamp + 86400)
            allOutCount.append(outObj.count())
            allTrueCount.append(inObj.count()-outObj.count())
            allTime.append(day[-5:])

            # print(day[-5:], timestamp)
        response['detail']={
            'allTime':allTime,
            'allInCount':allInCount,
            'allOutCount':allOutCount,
            'allTrueCount':allTrueCount,
        }
        return HttpResponse(json.dumps(response))

# 获取群列表
@check
def getGroupList(request, username):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        obj=GroupConfig.objects.filter(username=username)
        groupList=[]
        for item in obj:
            groupList.append(item.group)
        response['detail']=groupList
        return HttpResponse(json.dumps(response))

# 添加群
@check
def addGroup(request, username):
    # print(request.META)
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        reqInfo = json.loads(str(request.body, encoding='utf-8'))
        group = reqInfo.get('group', None)
        if group:
            obj = GroupConfig.objects.filter(username=username,group=group)
            if obj.exists():
                response['code'] = -3
                response['errormsg'] = '群号已存在'
            else:
                visited=User.objects.filter(username=username)[0].visited
                botqq=BotConfig.objects.filter(username=visited)[0].botqq
                GroupConfig.objects.create(username=username,group=group,status=True,botqq=botqq)
        else:
            response['code'] = -2
            response['errormsg'] = '传入数据有误'
        return HttpResponse(json.dumps(response))

# 删除群
@check
def deleteGroup(request, username):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        reqInfo = json.loads(str(request.body, encoding='utf-8'))
        group = reqInfo.get('group', None)
        if group:
            obj = GroupConfig.objects.filter(username=username, group=group)
            if obj.exists():
               obj.delete()
            else:
                response['code'] = -4
                response['errormsg'] = '群号不存在'
        else:
            response['code'] = -2
            response['errormsg'] = '传入数据有误'
        return HttpResponse(json.dumps(response))


# 群设置克隆
@check
def copySetting(request, username):
    response = {'code': '0', 'errormsg': ''}
    if request.method == 'POST':
        reqInfo = json.loads(str(request.body, encoding='utf-8'))
        group = reqInfo.get('group', None)#当前群号
        copyGroup=reqInfo.get('copyGroup')
        types = reqInfo.get('types')

        if group and copyGroup:
            try:
                groupItem = GroupConfig.objects.get(group=group)
                copyGroupItem = GroupConfig.objects.get(group=copyGroup)
                if copyGroupItem.username==username and groupItem.username==username:#要克隆的群必须是自己群才可以克隆
                    #克隆进群欢迎
                    if 'jqhy' in types:
                        newItems = Welcome.objects.filter(group=copyGroup)  # 要克隆的内容
                        Welcome.objects.filter(group=group).delete()
                        if newItems.exists():
                            Welcome.objects.create(content=newItems[0].content, group=group)

                    #克隆关键词禁言
                    if 'gjcjy' in types:
                        newItems = KeyStop.objects.filter(group=copyGroup)
                        KeyStop.objects.filter(group=group).delete()
                        if newItems.exists():
                            KeyStop.objects.create(keyword=newItems[0].keyword, time=newItems[0].time, group=group)

                    #克隆关键词回复
                    if 'gjchf' in types:
                        newItems = KeyReply.objects.filter(group=copyGroup)
                        KeyReply.objects.filter(group=group).delete()
                        if newItems.exists():
                            for item in newItems:
                                KeyReply.objects.create(keyword=item.keyword, reply=item.reply, group=group)

                else:
                    response['code'] = -8
                    response['errormsg'] = '权限不足'
            except:
                response['code'] = -9
                response['errormsg'] = '操作失败'
        else:
            response['code'] = -2
            response['errormsg'] = '传入数据有误'
        return HttpResponse(json.dumps(response))