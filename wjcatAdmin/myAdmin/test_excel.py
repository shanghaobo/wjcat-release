import xlwt

wb=xlwt.Workbook()
ws=wb.add_sheet('test')

ws.write(0,0,"第1列")
ws.write(0,1,"第2列")
ws.write(0,2,"第3列")

wb.save('./test.xls')