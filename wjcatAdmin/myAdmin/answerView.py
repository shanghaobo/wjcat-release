"""
程序名：回答问卷请求接口
功能：回答问卷后台处理函数
"""
from django.shortcuts import HttpResponse
import json
from myAdmin.models import *
from django.db import transaction
import datetime


############################################################
#功能：问卷回答者操作主入口
#最后更新：2019-05-24
############################################################
def opera(request):
    response={'code':0,'msg':'success'}
    if request.method=='POST':
        body=str(request.body,encoding='utf-8')
        print(body)
        try:
            info = json.loads(body)#解析json报文
        except:
            response['code'] = '-2'
            response['msg'] = '请求格式有误'
        opera_type=info.get('opera_type')#获取操作类型
        if opera_type:
            if opera_type=='get_info':#获取问卷信息
                response=getInfo(info,request)
            elif opera_type=='get_temp_info':#获取问卷信息
                response=getTempInfo(info,request)
            elif opera_type=='submit_wj':#提交问卷
                response=submitWj(info,request)
            else:
                response['code'] = '-7'
                response['msg'] = '请求类型有误'
        else:
            response['code'] = '-3'
            response['msg'] = '确少必要参数'
    else:
        response['code']='-1'
        response['msg']='请求方式有误'

    return HttpResponse(json.dumps(response))


############################################################
#功能：获取问卷信息
#最后更新：2019-05-24
############################################################
def getInfo(info,request):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')
    username = request.session.get('username')
    if wjId:
        try:#判断问卷id是否存在
            res=Wj.objects.get(id=wjId)#查询id为wjId
            response['title']=res.title
            response['desc']=res.desc
        except:
            response['code'] = '-10'
            response['msg'] = '问卷不存在'
        else:
            if res.username==username or res.status==1:#只有问卷发布者或者此问卷为已发布才能查看
                obj = Question.objects.filter(wjId=wjId)
                detail = []
                for item in obj:
                    temp = {}
                    temp['title'] = item.title
                    temp['type'] = item.type
                    temp['id'] = item.id  # 问题id
                    temp['row'] = item.row
                    temp['must'] = item.must
                    # 获取选项
                    temp['options'] = []
                    if temp['type'] in ['radio', 'checkbox']:  # 如果是单选或者多选
                        optionItems = Options.objects.filter(questionId=item.id)
                        for optionItem in optionItems:
                            temp['options'].append({'title':optionItem.title,'id':optionItem.id})
                    temp['radioValue'] = -1  # 接收单选框的值
                    temp['checkboxValue'] = []  # 接收多选框的值
                    temp['textValue'] = ''  # 接收输入框的值
                    detail.append(temp)
                response['detail'] = detail
            else:
                response['code'] = '-10'
                response['msg'] = '问卷尚未发布'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response




############################################################
#功能：获取模板问卷信息
#最后更新：2019-06-16
############################################################
def getTempInfo(info,request):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')
    username = request.session.get('username')
    if wjId:
        try:#判断问卷id是否存在
            res=TempWj.objects.get(id=wjId)#查询id为wjId
            response['title']=res.title
            response['desc']='问卷描述'
        except:
            response['code'] = '-10'
            response['msg'] = '模板不存在'
        else:
            obj = TempQuestion.objects.filter(wjId=wjId)
            detail = []
            for item in obj:
                temp = {}
                temp['title'] = item.title
                temp['type'] = item.type
                temp['id'] = item.id  # 问题id
                temp['row'] = item.row
                temp['must'] = item.must
                # 获取选项
                temp['options'] = []
                if temp['type'] in ['radio', 'checkbox']:  # 如果是单选或者多选
                    optionItems = TempOptions.objects.filter(questionId=item.id)
                    for optionItem in optionItems:
                        temp['options'].append({'title':optionItem.title,'id':optionItem.id})
                temp['radioValue'] = -1  # 接收单选框的值
                temp['checkboxValue'] = []  # 接收多选框的值
                temp['textValue'] = ''  # 接收输入框的值
                detail.append(temp)
            response['detail'] = detail
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response



############################################################
#功能：提交问卷
#最后更新：2019-06-08
############################################################
@transaction.atomic
def submitWj(info,request):
    response = {'code': 0, 'msg': 'success'}
    wjId = info.get('wjId')
    useTime=info.get('useTime')
    detail=info.get('detail')
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
    else:
        ip = request.META.get('REMOTE_ADDR')

    s1 = transaction.savepoint()#设置事务保存点 回滚使用
    if wjId:

        try:  # 判断问卷id是否存在
            res = Wj.objects.get(id=wjId)  # 查询id为wjId
            response['title'] = res.title
            response['desc'] = res.desc
        except:
            response['code'] = '-10'
            response['msg'] = '问卷不存在'
            return response
        if res.status==0:#当问卷状态为1(已发布)时才可回答
            response['code'] = '-10'
            response['msg'] = '问卷尚未发布'
            return response

        #记录提交信息
        submitInfo=Submit.objects.create(
            wjId=wjId,
            submitTime=datetime.datetime.now(),
            submitIp=ip,
            useTime=useTime
        )
        qItems=Question.objects.filter(wjId=wjId,must=True)#查询所有必填题目
        musts=[]
        for qItem in qItems:
            musts.append(qItem.id)#记录所有必填题目的题目id
        #记录答案
        for item in detail:
            # print(item)
            if item['type']=='radio':#单选题
                if item['id'] in musts and item['radioValue']==-1:#此必填选项未填 回滚
                    print('开始回滚')
                    transaction.savepoint_rollback(s1)
                    print('已回滚')
                    response['code'] = '-11'
                    response['msg'] = '有必答题目未回答'
                    break
                Answer.objects.create(
                    questionId=item['id'],
                    submitId=submitInfo.id,
                    wjId=wjId,
                    type=item['type'],
                    answer=item['radioValue']
                )
            elif item['type']=='checkbox':#多选题
                if item['id'] in musts and len(item['checkboxValue'])==0:#此必填选项未填 回滚
                    print('开始回滚')
                    transaction.savepoint_rollback(s1)
                    print('已回滚')
                    response['code'] = '-11'
                    response['msg'] = '有必答题目未回答'
                    break
                for value in item['checkboxValue']:
                    Answer.objects.create(
                        questionId=item['id'],
                        submitId=submitInfo.id,
                        wjId=wjId,
                        type=item['type'],
                        answer=value
                    )
            elif item['type']=='text':#填空题
                if item['id'] in musts and item['textValue']=='':#此必填选项未填 回滚
                    print('开始回滚')
                    transaction.savepoint_rollback(s1)
                    print('已回滚')
                    response['code'] = '-11'
                    response['msg'] = '有必答题目未回答 '
                    break
                Answer.objects.create(
                    questionId=item['id'],
                    submitId=submitInfo.id,
                    wjId=wjId,
                    type=item['type'],
                    answerText=item['textValue']
                )
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'

    return response
