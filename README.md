# 问卷调查网站

> 使用vue和django开发的问卷调查网站。
[在线演示](https://wjcat.com)（账号密码：shanghaobo）


## 示例

![demo](demo.gif)

## 功能
- 问卷设计
    - 问卷设计
    - 创建问卷
    - 编辑问卷
    - 发布问卷
    - 删除问卷
    - 分享问卷
- 结果分析
    - 回答统计
    - 数据可视化
- 后台管理
    - 封禁用户
    - 删除问卷


## 结构设计

- 层次方框图

![问卷调查系统层次方框图](问卷调查系统层次方框图.png)

- ER图

![问卷调查系统ER图](问卷调查系统ER图.png)

- DFD图

![问卷调查系统DFD图](问卷调查系统DFD图.png)

## 环境

- Node.js：v10.15.1
- Vue.js：2.0
- Python：3.7.0
- Django：2.1.2

## 运行说明

1. 在wjcatAdmin里的seetting.py配置数据库信息并迁移。
2. 进入wjcat目录下，在当前目录打开cmd控制台，输入npm run dev启动前端项目。
3. 进入wjcatAdmin目录下，在当前目录打开cmd控制台，输入python manage runserver启动后端项目。
4. 打开浏览器，输入http://127.0.0.1:8080即可访问本系统。
5. 也可直接在浏览器输入http://www.wjcat.com访问部署后的本系统。