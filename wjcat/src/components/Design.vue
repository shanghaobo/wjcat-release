<!--
程序名：问题设计页面
功能：对问卷中问题的添加、编辑、删除
-->
<template>
  <div class="Design" v-loading="loading" element-loading-text="加载中...">
    <h3>{{title}}</h3>
      <div class="top" v-if="desc!=''">
        {{desc}}
      </div>
    <el-card class="box-card" v-for="(item,index) in detail" style="margin: 10px;">
        <div slot="header" class="clearfix">
          <div class="questionTitle">
            <!--显示必填标识-->
            <span style="color: #F56C6C;">
              <span v-if="item.must">*</span>
              <span v-else>&nbsp;</span>
            </span>
            <span style="color: black;margin-right: 3px;">{{(index+1)+'.'}}</span>
            {{item.title}}
          </div>
          <div style="float: right;">
            <el-button style="padding: 2px" type="text" @click="editorQuestion(item)">编辑</el-button>
            <el-button style="padding: 2px;color: #F56C6C" type="text" @click="deleteQuestion(index)">删除</el-button>
          </div>
        </div>

        <!--单选题展示-->
        <div class="text item" v-if="item.type=='radio'" v-for="(option,index) in item.options">
          <el-radio v-model="item.radioValue" :label="index" style="margin: 5px;">{{ option.title }}</el-radio>
        </div>

        <!--多选题展示-->
        <el-checkbox-group v-if="item.type=='checkbox'" v-model="item.checkboxValue">
          <div class="text item"  v-for="(option,index) in item.options">
            <el-checkbox :label="index" style="margin: 5px;">{{ option.title }}</el-checkbox>
          </div>
        </el-checkbox-group>

        <!--填空题展示-->
        <el-input
          v-if="item.type=='text'"
          type="textarea"
          :rows="item.row"
          resize="none"
          v-model="item.textValue">
        </el-input>

      </el-card>

      <el-button  icon="el-icon-circle-plus" @click="addQuestion" style="margin-top: 10px;">添加题目</el-button>

<br><br><br><br><br>

    <!--添加题目弹窗-->
    <el-dialog :title="dialogTitle" :visible.sync="dialogShow" :close-on-click-modal="false" class="dialog">
      <el-form ref="form" :model="willAddQuestion" label-width="80px">
        <el-form-item label="题目类型" style="width: 100%;">
          <el-select v-model="willAddQuestion.type" placeholder="请选择题目类型" @change="typeChange">
          <el-option
            v-for="item in allType"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        </el-form-item>
        <el-form-item label="是否必填" style="width: 100%;">
          <el-checkbox v-model="willAddQuestion.must">必填</el-checkbox>
        </el-form-item>
        <el-form-item label="题目标题" style="width: 100%;">
          <el-input v-model="willAddQuestion.title" placeholder="请输入标题" ></el-input>
        </el-form-item>

        <template v-if="willAddQuestion.type=='radio'||willAddQuestion.type=='checkbox'">
          <el-form-item :label="'选项'+(index+1)" v-for="(item,index) in willAddQuestion.options" >
            <el-row>
              <el-col :span="16">
                <el-input  v-model="item.title" placeholder="请输入选项名" style="width: 90%;"></el-input>
              </el-col>
            <el-col :span="8">
              <el-button type="danger" plain class="" @click="deleteOption(index)" >删除选项</el-button>
            </el-col>
            </el-row>

          </el-form-item>
          <el-button type="primary" plain class="addOptionButton" @click="addOption">新增选项</el-button>
        </template>
        <template v-if="willAddQuestion.type=='text'">
          <el-form-item label="填空">
            <el-input type="textarea"
  :rows="willAddQuestion.row" style="width: 80%" resize="none"></el-input>
          </el-form-item>
          <el-form-item label="行数">
            <el-input-number v-model="willAddQuestion.row" :min="1" :max="10" label="描述文字"></el-input-number>
          </el-form-item>

        </template>
      </el-form>
      <br>
      <div style="width: 100%;text-align: right">
        <el-button style="margin-left: 10px;" @click="dialogShow=false">取消</el-button>
        <el-button type="primary" style="margin-left: 10px;" @click="checkAddQuestion">完成</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
  import {designOpera} from './api'
  export default{
    data(){
      return{
        loading:false,//页面加载中
        dialogShow:false,
        dialogTitle:'',
        detail:[],
        wjId:0,
        title:'',
        desc:'',
        willAddQuestion:{
          id:0,
          type:'',
          title:'',
          options:[
            {
              title:'',//选项标题
              id:0//选项id
            }
          ],
          row:1,
          must:false,//是否必填
        },
        allType:[
          {
            value:'radio',
            label:'单选题',
          },
          {
            value:'checkbox',
            label:'多选题',
          },
          {
            value:'text',
            label:'填空题',
          },
        ],
      }
    },
    methods:{
      //初始化问卷所有问题
      init(wjId,title,desc){
        this.wjId=wjId;
        this.title=title;
        this.desc=desc;
        this.getQuestionList();
      },
      //获取问题列表(问卷内容)
      getQuestionList(){
        this.detail=[];
        this.loading=true;
        designOpera({
          opera_type:'get_question_list',
          username:'test',
          wjId:this.wjId,
        })
          .then(data=>{
            console.log(data);
            this.detail=data.detail;
            this.loading=false;
          })
      },
      //点击添加问题按钮
      addQuestion(){
        if(this.wjId==0||this.wjId==null){
          this.$message({
            type: 'error',
            message: '清先创建问卷!'
          });
          return;
        }
        this.dialogTitle='添加题目';
        this.willAddQuestion={
          id:0,
          type:'',
          title:'',
          options:[
            {
              title:'',//选项标题
              id:0//选项id
            }
          ],
          row:1,
          must:false,//是否必填
        };
        this.dialogShow=true;
      },
      //删除问题
      deleteQuestion(index){
        this.$confirm('确定删除此题目?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          designOpera({
            opera_type:'delete_question',
            username:'test',
            questionId:this.detail[index].id,
          })
            .then(data=>{
              console.log(data);
              if(data.code==0){
                this.detail.splice(index,1);
                this.$message({
                  type: 'success',
                  message: '删除成功!'
                });
              }
              else{
                this.$message({
                  type: 'error',
                  message: data.msg
                });
              }
            })
        });

      },
      //确认添加/保存题目
      checkAddQuestion(){
        //添加保存问题
        let newItem={};//新添加的问题对象
        newItem={
          type:this.willAddQuestion.type,
          title:this.willAddQuestion.title,
          options:this.willAddQuestion.options,
          row:this.willAddQuestion.row,
          must:this.willAddQuestion.must,
        };
        newItem.radioValue=-1;
        newItem.checkboxValue=[];
        newItem.textValue='';
        designOpera({
          opera_type:'add_question',
          username:'test',
          wjId:this.wjId,
          questionId:this.willAddQuestion.id,
          title:this.willAddQuestion.title,
          type:this.willAddQuestion.type,
          options:this.willAddQuestion.options,
          row:this.willAddQuestion.row,
          must:this.willAddQuestion.must,

        })
          .then(data=>{
            console.log(data);
            newItem.id=data.id;
            if(data.code==0){
              this.dialogShow=false;
              this.$message({
                type: 'success',
                message: '保存成功!'
              });
              this.getQuestionList();
            }
            else{
              this.dialogShow=false;
              this.$message({
                type: 'error',
                message: data.msg
              });
            }
            this.willAddQuestion={
              id:0,
              type:'',
              title:'',
              options:[''],
              row:1,
              must:false,
            };
          });
      },
      //点击编辑问题按钮
      editorQuestion(item){
        this.willAddQuestion.title=item.title;
        this.willAddQuestion.type=item.type;
        this.willAddQuestion.options=JSON.parse(JSON.stringify(item.options));
        this.willAddQuestion.text=item.text;
        this.willAddQuestion.row=item.row;
        this.willAddQuestion.must=item.must;
        this.willAddQuestion.id=item.id;
        this.dialogTitle='编辑问题';
        this.dialogShow=true;
      },
      //添加选项
      addOption(){
        this.willAddQuestion.options.push({
          title:'',
          id:0,
        });
      },
      //删除选项
      deleteOption(index){
        this.willAddQuestion.options.splice(index,1);
      },
      //切换问题类型
      typeChange(value){
        console.log(value);
        this.willAddQuestion.type=value;
        this.willAddQuestion.text='';
        this.row=1;
      },
    }
  }
</script>
<style scoped>
  .Design{

  }
  .Design .dialog{
    text-align: left;
  }
  .Design .questionTitle{
    display: inline-block;
    width: 80%;
    font-size: 16px;
    color: #303133;
  }
  .Design .addOptionButton{
    display: inline-block;
    margin-left: 80px;
  }
  .box-card{
    width: 100%;
    text-align: left;
  }
  .Design .top{
    color: #606266;
    margin-left: 20px;
    padding: 0 10px 10px 10px;
    border-bottom: 3px solid #409EFF;
    font-size: 15px;
    line-height: 22px;
    text-align: left;
  }
</style>
