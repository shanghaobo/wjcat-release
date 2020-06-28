import xlwt
import json


#回答数据导出excel
def analysisExportExcel(data,title='问卷统计'):
    tran_dict={
        'radio':'单选题',
        'checkbox':'多选题',
        'text':'问答题'
    }
    wb = xlwt.Workbook()
    ws = wb.add_sheet('数据统计')
    i=0
    j=0
    # 标题
    ws.write(i, j, title)
    i+=2
    for index,question in enumerate(data):
        print(i, j, question['title'])
        # 题目
        ws.write(i, j, '%s.[%s]%s'%(index+1,tran_dict[question['type']],question['title']))
        i+=1
        if question['type']=='text':
            ws.write(i, j, '问答题请通过下载详情数据获取')
            i+=2
            continue
        ws.write(i, j, '选项')
        ws.write(i, j+1, '数量')
        ws.write(i, j+2, '占比')
        i += 1
        # 选项
        for option in question['result']:
            ws.write(i,j,option['option'])
            ws.write(i,j+1,option['count'])
            ws.write(i,j+2,option['percent'])
            i+=1
        ws.write(i, j, '总计')
        ws.write(i, j + 1, sum(map(lambda x:x['count'],question['result'])))
        ws.write(i, j + 2, '100%')
        i += 1
        i+=1
    # wb.save('./%s.xls'%title)
    return wb


def answerText2Excel(data):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('回答详情')
    i=0
    j=0
    # print('data=',data)
    for item in data:
        ws.write(i,j,item)
        i+=1
    return wb



if __name__=="__main__":
    pass
    # data=json.loads(data)
    # analysisExportExcel(data['detail'])

