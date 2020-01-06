import requests as r
import json

api='http://127.0.0.1:8000/api/design'

#创建问卷
def opera_addWj():
    data={
        'username':'test',
        'opera_type':'add_wj',
        'title':'测试问卷',

    }
    res=r.post(api,data=json.dumps(data))
    print(res.text)
    print(res.json())


#删除问卷
def opera_deleteWj():
    data={
        'username':'test',
        'opera_type':'delete_wj',
        'id':'3',

    }
    res=r.post(api,data=json.dumps(data))
    print(res.text)
    print(res.json())

#添加单选题
def addRadioQuestion():
    data={
        'username':'test',
        'opera_type':'add_question',
        'wjId':'4',
        'title':'您的性别是？',
        'type':'radio',
        'options':['男','女']
    }
    res = r.post(api + '/opera', data=json.dumps(data))
    print(res.text)
    print(res.json())

#添加多选题
def addCheckboxQuestion():
    data={
        'username':'test',
        'opera_type':'add_question',
        'wjId':'4',
        'title':'您的爱好有？',
        'type':'checkbox',
        'options':['唱','跳','rap','篮球']
    }
    res = r.post(api + '/opera', data=json.dumps(data))
    print(res.text)
    print(res.json())


#添加填空题
def addInputQuestion():
    data={
        'username':'test',
        'opera_type':'add_question',
        'wjId':'4',
        'title':'您的联系方式是？',
        'type':'text',
        'row':1,
    }
    res = r.post(api + '/opera', data=json.dumps(data))
    print(res.text)
    print(res.json())

#删除题目
def deleteQuestion():
    data={
        'username':'test',
        'opera_type':'delete_question',
        'questionId':'9',
    }
    res = r.post(api + '/opera', data=json.dumps(data))
    print(res.text)
    print(res.json())




opera_addWj()
# opera_deleteWj()
# addRadioQuestion()
# addCheckboxQuestion()
# addInputQuestion()

# deleteQuestion()