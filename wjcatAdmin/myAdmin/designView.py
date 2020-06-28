from django.shortcuts import HttpResponse
import json
from myAdmin.models import *
from django.db import transaction,connection
from django.db.models import Q
from . import handle
from io import BytesIO
import base64


############################################################
#功能：问卷设计者操作主入口
#最后更新：2019-05-23
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
        else:
            opera_type = info.get('opera_type')  # 获取操作类型
            username = request.session.get('username')
            if opera_type:#如果操作类型不为空
                if opera_type == 'login':
                    response = login(info, request)
                elif opera_type == 'logincheck':
                    response = loginCheck(request)
                elif opera_type == 'register':
                    response = register(info)
                elif opera_type == 'resetpass':
                    response = resetpass(info)
                elif username:#需要验证username的方法
                    if opera_type == 'add_wj':  # 添加问卷
                        response = addWj(info,username)
                    elif opera_type == 'get_wj_list':  # 获取问卷列表
                        response = getWjList(info,username)
                    elif opera_type == 'get_temp_wj_list':  # 获取问卷列表
                        response = getTempWjList(info,username)
                    elif opera_type == 'delete_wj':  # 删除问卷
                        response = deleteWj(info,username)
                    elif opera_type == 'get_question_list':  # 获取问题列表
                        response = getQuestionList(info,username)
                    elif opera_type == 'add_question':  # 添加问题
                        response = addQuestion(info,username)
                    elif opera_type == 'delete_question':  # 删除问题
                        response = deleteQuestion(info,username)
                    elif opera_type == 'push_wj':  # 发布问卷（更改问卷状态）
                        response = pushWj(info,username)
                    elif opera_type == 'dataAnalysis':#获取统计数据
                        response = dataAnalysis(info)
                    elif opera_type == 'add_temp':#添加模板
                        response = addTemp(info,username)
                    elif opera_type == 'use_temp':#添加模板
                        response = useTemp(info,username)
                    elif opera_type == 'exit':
                        response = exit(request)
                    elif opera_type=='get_text_answer_detail':
                        response=getTextAnswerDetail(info)
                    elif opera_type=='analysis_export_excel':
                        response=analysisExportExcel(info)
                    elif opera_type=='answer_text_to_excel':
                        response=answerText2Excel(info)
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


def loginCheck(request):
    response = {'code': 0, 'msg': 'success'}
    # 查询django_session中是否有username，查询失败抛出异常
    # 查询成功判断username是否为空，若为空，返回404错误，不为空，返回成功信息
    try:
        username = request.session.get('username')
    except:
        response['code']='-4'
        response['msg']='操作失败'
    else:
        if username:
            response['data']={'user':username}
        else:
            response['code'] = '404'
            response['msg'] = '未登录'
    return response



############################################################
#功能：添加问卷/更新问卷
#最后更新：2019-05-23
#备注：当传入id(问卷id)为空时：添加问卷  不为空时：更新问卷
############################################################
def addWj(info,username):
    response = {'code': 0, 'msg': 'success'}
    title = info.get('title')#问卷标题
    desc=info.get('desc')#问卷描述
    id=info.get('id')#问卷id 可为空
    if username and title:
        try:
            if id:#id不为空 更新问卷
                res=Wj.objects.get(username=username,id=id)
                res.title=title
                res.desc=desc
                res.save()
            else:#否则 添加问卷
                res = Wj.objects.create(username=username, title=title,desc=desc, status=0)
        except:
            response['code'] = '-4'
            response['msg'] = '操作失败'
        else:
            if res.id > 0:
                response['id'] = res.id
            else:
                response['code'] = '-4'
                response['msg'] = '操作失败'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response



############################################################
#功能：获取问卷列表
#最后更新：2019-05-27
############################################################
def getWjList(info,username):
    response = {'code': 0, 'msg': 'success'}
    if username:
        obj = Wj.objects.filter(username=username).order_by('-id')
        detail=[]
        for item in obj:
            temp={}
            temp['id']=item.id
            temp['title']=item.title
            temp['desc']=item.desc
            temp['status']=item.status
            detail.append(temp)
        response['data']={'detail':detail}

    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response


############################################################
#功能：获取模板库问卷列表
#最后更新：2019-06-16
############################################################
def getTempWjList(info,username):
    response = {'code': 0, 'msg': 'success'}
    page = info.get('page',1)  # 问卷标题
    if username:
        obj = TempWj.objects.all().order_by('id')
        count=obj.count()
        obj=obj[(page - 1) * 5: (page - 1) * 5 + 5]
        detail=[]
        for item in obj:
            temp={}
            temp['tempid']=item.id
            temp['tempname']=item.title
            temp['username'] = item.username
            # temp['desc']=item.desc
            detail.append(temp)
        response['detail']=detail
        response['count']=count

    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response




############################################################
#功能：删除问卷
#最后更新：2019-05-23
############################################################
def deleteWj(info,username):
    response = {'code': 0, 'msg': 'success'}
    id = info.get('id')#问卷id
    if username and id:
        try:
            Wj.objects.filter(username=username, id=id).delete()#删除问卷
            obj=Question.objects.filter(wjId=id)#查询所有关联问题
            for item in obj:
                Options.objects.filter(questionId=item.id).delete()#删除问题关联的选项
            obj.delete()#删除问卷所有关联问题

            Submit.objects.filter(wjId=id).delete()#删除该问卷的提交信息
            Answer.objects.filter(wjId=id).delete()#删除该问题的所有回答
        except:
            response['code'] = '-4'
            response['msg'] = '操作失败'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response




############################################################
#功能：获取问题列表
#最后更新：2019-05-27
############################################################
def getQuestionList(info,username):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')#wjid
    if username:
        res=Wj.objects.filter(id=wjId,username=username)
        if res.exists():#判断该问卷id是否为本人创建
            obj=Question.objects.filter(wjId=wjId)
            detail=[]
            for item in obj:
                temp={}
                temp['title']=item.title
                temp['type']=item.type
                temp['id']=item.id#问题id
                temp['row']=item.row
                temp['must']=item.must
                #获取选项
                temp['options']=[]
                if temp['type'] in ['radio', 'checkbox']:  # 如果是单选或者多选
                    optionItems = Options.objects.filter(questionId=item.id)
                    for optionItem in optionItems:
                        temp['options'].append({'title': optionItem.title, 'id': optionItem.id})
                temp['radioValue']=-1#接收单选框的值
                temp['checkboxValue'] =[]#接收多选框的值
                temp['textValue']=''#接收输入框的值
                detail.append(temp)
            response['detail']=detail
        else:
            response['code'] = '-6'
            response['msg'] = '权限不足'

    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response





############################################################
#功能：添加问题/更新问题
#最后更新：2019-05-23
#备注：当传入questionId(问题id)为空时：添加问题  不为空时：更新问题
############################################################
#事务处理  当一次插入选项过多时（测试10个选项要5秒以上）很费时间 增加事务处理可大大加快速度（改进后20个选项3秒插入完成）
@transaction.atomic
def addQuestion(info,username):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')#wjid
    q_title=info.get('title')#题目标题
    q_type=info.get('type')#题目类型
    options=info.get('options')#选项
    row=info.get('row')
    must=info.get('must')
    questionId=info.get('questionId')#问题id 可为空
    if wjId and q_title and q_type and must!=None:
        if q_type in ['radio','checkbox','text']:
            if questionId:#问题id存在 更新问题
                newIds=[]
                for temp in options:
                    newIds.append(temp['id'])#将更新后的选项id记录
                allOptions=Options.objects.filter(questionId=questionId)
                #遍历选项 把不在更新后的选项id中的选项删除
                for option in allOptions:
                    if option.id not in newIds:
                        option.delete()
                #更新问题
                Question.objects.filter(wjId=wjId,id=questionId).update(title=q_title,type=q_type,must=must,row=row)
                #更新选项
                for option in options:
                    if option['id']!=0:#选项为已有的 更新
                        Options.objects.filter(questionId=questionId, id=option['id']).update(title=option['title'])
                    else:#选项为新增的 添加
                        Options.objects.create(questionId=questionId,title=option['title'])
            else:#问题id不存在 添加问题
                # 添加问题
                resObj = Question.objects.create(wjId=wjId, title=q_title, type=q_type, row=row,must=must)
                questionId = resObj.id
                response['id'] = questionId
                # 添加选项
                if q_type == 'radio' or q_type == 'checkbox':  # 单选或者多选
                    print(type(options))
                    if options and type(options) == type([]):
                        for item in options:
                            Options.objects.create(questionId=questionId, title=item['title'])
                            # Options(questionId=questionId,title=item)
                    else:  # 传入选项不能为空
                        response['code'] = '-4'
                        response['msg'] = '操作失败'
        else:
            response['code'] = '-5'
            response['msg'] = '传入参数值有误'
            return response
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response


############################################################
#功能：删除问题
#最后更新：2019-05-23
############################################################
@transaction.atomic
def deleteQuestion(info,username):
    response = {'code': 0, 'msg': 'success'}
    questionId=info.get('questionId')
    if questionId and username:
        try:
            s_wjId=Question.objects.get(id=questionId).wjId#该题目所属的问卷id
            s_username=Wj.objects.get(id=s_wjId).username#该题目所属的用户名
            if username==s_username:#该题目是此用户创建的 有权限删除
                Question.objects.filter(id=questionId).delete()#删除问题
                Options.objects.filter(questionId=questionId).delete()#删除关联选项
            else:#该题目不是此用户创建的 无权限删除
                response['code'] = '-6'
                response['msg'] = '权限不足'
        except:
            response['code'] = '-4'
            response['msg'] = '操作失败'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response



############################################################
#功能：发布问卷
#最后更新：2019-05-24
############################################################
def pushWj(info,username):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')
    status=info.get('status')#0暂停问卷 1发布问卷
    print('%s,%s,%s'%(wjId,username,status))
    if wjId and username and (status==0 or status==1):
        res=Wj.objects.filter(id=wjId,username=username)
        if res.exists():  # 该题目是此用户创建的 有权限
            res.update(status=status)
        else:  # 该题目不是此用户创建的 无权限
            response['code'] = '-6'
            response['msg'] = '权限不足'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'

    return response




############################################################
#功能：登录
#最后更新：2019-05-28
############################################################
def login(info,request):
    response = {'code': 0, 'msg': 'success'}
    username = info.get('username')  #用户名
    password = info.get('password')  #密码
    if username and password:
        try:
            # 根据前台传回的用户名查找密码和用户状态
            # 若查询失败，抛出异常错误
            # 若查询成功，判断密码是否正确和用户状态是否正常
            t_password = User.objects.get(username=username).password
            t_status = User.objects.get(username=username).status
        except:
            response['code'] = '-5'
            response['msg'] = '不存在该用户'
        else:
            if password==t_password and 0==t_status:
                request.session["username"]= username
                return response
            else:
                response['code'] = '-4'
                response['msg'] = '操作失败'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response

############################################################
#功能：退出登录
#最后更新：2019-05-28
############################################################
def exit(request):
    response = {'code': 0, 'msg': 'success'}
    # 对django_session中的用户名执行删除操作
    # 若删除成功，返回成功信息
    # 若删除失败，抛出异常操作失败
    try:
        del request.session['username']
    except:
        response['code'] = '-4'
        response['msg'] = '操作失败'
    else:
        return response
    return response



############################################################
#功能：注册
#最后更新：2019-05-29
############################################################
def register(info):
    response = {'code': 0, 'msg': 'success'}
    t_username = info.get('username') #用户名
    t_password = info.get('password') #密码
    if t_username and t_password:  #用户名和密码不为空时，执行操作
        #将用户名和密码，以及初始状态status=0插入数据库中
        #若插入失败，抛出异常操作失败
        #若插入成功，返回成功信息
        try:
            User.objects.create(username=t_username,password=t_password)
        except:
            response['code'] = '-4'
            response['msg'] = '操作失败'
        else:
            return response
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response

############################################################
#功能：重置密码
#最后更新：2019-05-28
############################################################
def resetpass(info):
    response = {'code': 0, 'msg': 'success'}
    username = info.get('username') #用户名
    email = info.get('email') #邮箱
    if username and email:#用户名和邮箱不为空，执行操作
        #根据用户名查询对应邮箱是否正确
        #若正确，返回成功信息，若不正确，抛出异常
        try:
            t_email = User.objects.get(username=username).email
        except:
            response['code'] = '-5'
            response['msg'] = '不存在该用户'
        else:
            if email==t_email:
                return response
            else:
                response['code'] = '-10'
                response['msg'] = '未绑定邮箱'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response


############################################################
#功能：数据分析
#最后更新：2019-05-28
############################################################
def dataAnalysis(info):
    response = {'code': 0, 'msg': 'success'}
    try:
        wjId=info.get('wjId')#获取问卷id
    except:
        response['code'] = '-4'
        response['msg'] = '操作失败'
    else:
        if wjId:  # 如果问卷id 存在
            detail = []
            questions = Question.objects.filter(wjId=wjId)
            for question in questions:
                questionTitle = question.title
                questionType = question.type
                questionId=question.id
                if questionType == "radio" or questionType == "checkbox":
                    result = getQuestionAnalysis(question.id)
                    print(result)
                else:
                    # result = getQuestionText(question.id)
                    result=''

                detail.append({
                    "title": questionTitle,
                    "type": questionType,
                    "result": result,
                    "questionId":questionId
                })
            response['detail'] = detail
        else:
            response['code'] = '-3'
            response['msg'] = '确少必要参数'
    return response


#根据问题id获取统计情况
def getQuestionAnalysis(questionId):
    # options=Options.objects.filter(questionId=questionId)   #获取问题的选项
    # answer = Answer.objects.filter(questionId=questionId)  # 获取问题id的答案
    # total = answer.count()  # 获取答案的总数
    # result=[]
    # for option in options:
    #     optionTitle=option.title#获取问题选项
    #     optionCount=Answer.objects.filter(questionId=questionId,answer=option.id).count()#获取每个选项数量
    #     if total==0:
    #         percent=0
    #     else:
    #         percent=int((optionCount/total)*10000)/100#获取每个选项的占比
    #     result.append({
    #         "option":optionTitle,
    #         "count":optionCount,
    #         "percent":str(percent)+'%'
    #     })
    # return result

    result=[]
    cursor=connection.cursor()
    cursor.execute('select A.id,count(B.submitId),A.title from (select * from myAdmin_options where questionId=%s) A left join myAdmin_answer B on A.id=B.answer group by A.id'%questionId)
    rows=cursor.fetchall()
    total=0
    for id,count,title in rows:
        total+=count
    for id,count,title in rows:
        if total==0:
            percent=0
        else:
            percent=int((count/total)*10000)/100
        result.append({
            'option':title,
            'count':count,
            'percent':str(percent)+'%'
        })
    print('questionId=',questionId)
    print('result=',result)
    return result

#获取文本内容
def getQuestionText(questionId):
    answer = Answer.objects.filter(questionId=questionId)# 获取问题id的答案
    result=[]
    for item in answer:
        if(item.answerText):
            result.append({'context': item.answerText})
    return result


#获取文本回答详情
def getTextAnswerDetail(info):
    response = {'code': 0, 'msg': 'success'}
    questionId=info.get('questionId')
    pageSize=info.get('pageSize',10)
    currentPage=info.get('currentPage',1)
    if not questionId:
        response['code'] = '-4'
        response['msg'] = '操作失败'
        return response
    answer=Answer.objects.filter(~Q(answerText=''),questionId=questionId,answerText__isnull=False)
    total=answer.count()
    answer=answer[(currentPage-1)*pageSize:currentPage*pageSize]
    result = []
    for item in answer:

        result.append({'context': item.answerText})
    response['detail']=result
    response['total']=total
    return response



############################################################
#功能：添加模板（临时）
#说明：根据wjId，将现有的问卷添加到模板库
#最后更新：2019-06-16
############################################################
def addTemp(info,username):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')
    if wjId:
        try:
            wjItem=Wj.objects.get(id=wjId)
            # 添加问卷信息
            wjRes=TempWj.objects.create(
                title=wjItem.title,
                username=wjItem.username,
                desc=wjItem.desc
            )
            #添加问题信息
            questions=Question.objects.filter(wjId=wjId)
            for q in questions:
                qRes=TempQuestion.objects.create(
                    title=q.title,
                    type=q.type,
                    wjId=wjRes.id,
                    row=q.row,
                    must=q.must
                )
                #添加选项
                options=Options.objects.filter(questionId=q.id)
                for o in options:
                    TempOptions.objects.create(
                        questionId=qRes.id,
                        title=o.title
                    )

        except:
            response['code'] = '-4'
            response['msg'] = '操作失败'

    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'

    return response



############################################################
#功能：使用模板
#说明：根据模板wjId，将模板库问卷添加到用户问卷
#最后更新：2019-06-16
############################################################
def useTemp(info,username):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')
    if wjId:
        try:
            wjItem=TempWj.objects.get(id=wjId)
            # 添加问卷信息
            wjRes=Wj.objects.create(
                title=wjItem.title,
                username=username,
                desc=wjItem.desc,
                status=0
            )
            #添加问题信息
            questions=TempQuestion.objects.filter(wjId=wjId)
            for q in questions:
                qRes=Question.objects.create(
                    title=q.title,
                    type=q.type,
                    wjId=wjRes.id,
                    row=q.row,
                    must=q.must
                )
                #添加选项
                options=TempOptions.objects.filter(questionId=q.id)
                for o in options:
                    Options.objects.create(
                        questionId=qRes.id,
                        title=o.title
                    )

        except:
            response['code'] = '-4'
            response['msg'] = '操作失败'

    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'

    return response


# 导出excel
def analysisExportExcel(info):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')
    if not wjId:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
        return response
    wj=Wj.objects.get(id=wjId)
    title=wj.title
    data=dataAnalysis(info)
    if data['code']==0:
        detail=data['detail']
        wb=handle.analysisExportExcel(detail,title)
        bio = BytesIO()
        wb.save(bio)
        bio.seek(0)
        response['filename']='%s.xls'%title
        response['b64data']=base64.b64encode(bio.getvalue()).decode()
        return response
    else:
        return response

#回答文本导出excel
def answerText2Excel(info):
    response = {'code': 0, 'msg': 'success'}
    questionId=info.get('questionId')
    if not questionId:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
        return response
    try:
        q = Question.objects.get(id=questionId)
    except:
        response['code']='-4'
        response['code']='操作失败'
        return response
    else:
        title=q.title
    answer = Answer.objects.filter(~Q(answerText=''), questionId=questionId, answerText__isnull=False)
    data=[]
    for item in answer:
        data.append(item.answerText)
    wb=handle.answerText2Excel(data)
    bio = BytesIO()
    wb.save(bio)
    bio.seek(0)
    response['filename'] = '%s.xls' % title
    response['b64data'] = base64.b64encode(bio.getvalue()).decode()
    return response
