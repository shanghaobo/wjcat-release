<template>
  <div class="home">

    <!--左侧导航栏-->
    <el-menu
      :default-active="defaultActive"
      class="menu">

      <el-menu-item v-for="(item,index) in wjList" :index="(index+1).toString()">
        <i class="el-icon-tickets"></i>

        <span slot="title">{{item.title}}</span>

      </el-menu-item>

      <el-menu-item @click="dialogShow=true">
        <i class="el-icon-plus"></i>
        <span slot="title">添加问卷</span>
      </el-menu-item>
    </el-menu>



    <!--添加问卷弹窗-->
    <el-dialog title="添加问卷" :visible.sync="dialogShow" :close-on-click-modal="false" class="dialog">
      <el-form ref="form" :model="willAddWj" label-width="80px">
        <el-form-item label="问卷标题" style="width: 100%;">
          <el-input v-model="willAddWj.title" placeholder="请输入问卷标题" ></el-input>
        </el-form-item>
      </el-form>
      <div style="width: 100%;text-align: right">
        <el-button type="primary" style="margin-left: 10px;" @click="addWj">确定</el-button>
      </div>
    </el-dialog>


    <!--内容区域-->
    <div class="content">
      <design ref="design"></design>
    </div>

    <!--右侧操作栏-->
    <div class="right">
      <el-button type="success"  icon="el-icon-upload" style="margin: 5px;">发布问卷</el-button><br>
      <el-button type="primary"  icon="el-icon-view" style="margin: 5px;">预览问卷</el-button><br>
      <el-button type="danger"  icon="el-icon-delete" style="margin: 5px;">删除问卷</el-button>

      <div>
        状态：未发布<br>
        提交：3<br>
        浏览：28<br>
      </div>

    </div>
  </div>
</template>
<script>
  import Design from './Design.vue'
  export default{
    components:{
      Design,
    },
    data(){
      return{
        defaultActive:'1',//当前激活菜单
        wjList:[
          {
            title:'关于问卷系统的需求分析调查',
            flag:0,//0未发布 1已发布
          },
        ],
        dialogShow:false,
        willAddWj:{
          title:'',
          flag:0
        }
      }
    },
    methods:{
      addWj(){
        this.wjList.push(this.willAddWj);
//        this.$refs.design.detail=[];
        this.dialogShow=false;
      }
    }
  }
</script>
<style scoped>
  .home{
    position: absolute;
    width: 100%;
    height: calc(100vh - 100px);
    text-align: left;

  }
  .home .badgeItem{
    margin-top: 40px;
  }
  .content{
    /*background-color: yellow;*/
    /*float: left;*/
    padding: 20px;
    width: 60%;
    height: 100%;
    text-align: center;
    display: inline-block;
    position: absolute;
    left: 20%;
    overflow-y: scroll;
    overflow-x: hidden;
  }
  .menu{
    /*float: left;*/
    width: 20%;
    background-color: white;
    height: calc(100vh - 60px);
    position: absolute;
    left: 0;
  }

  .home .right{
    background-color: yellow;
    position: absolute;
    left: 80%;
    margin-left: 40px;
    top:0;
    padding-top: 30px;
    padding-left: 30px;
  }
</style>
