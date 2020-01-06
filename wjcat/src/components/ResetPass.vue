<template>
    <div class="rpw">
      <div class="main-rpw">
        <div class="title">重 置 密 码</div>
        <el-row>
          <!-- 重置密码表单 -->
          <el-form :model="rpwForm" status-icon :rules="rules" ref="rpwForm" label-width="100px" class="demo-rpwForm">
            <el-form-item prop="username" label="用户名">
              <el-input @keyup.enter.native="rpw('rpwForm')" v-model="rpwForm.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item prop="email" label="邮  箱">
              <el-input @keyup.enter.native="rpw('rpwForm')" v-model="rpwForm.email" placeholder="请输入邮箱"></el-input>
            </el-form-item>
            <el-form-item>
              <!-- 提示信息 -->
              <p style="margin:-5% 0 0 -32%;font-size:5px;">重置后的密码会发送至该邮箱</p>
            </el-form-item>
            <el-form-item style="margin:-5% 0 0 -12%;">
              <!-- 重置密码提交按钮 -->
              <el-button type="primary" @click="rpw('rpwForm')" style="text-align: center;width: 225px">提交</el-button>
            </el-form-item>
          </el-form>
        </el-row>
        <div class="link">
          <!-- 跳转登录页面链接 -->
        <el-link type="primary" :underline="false" href="/login">想起密码了?去登录</el-link>
      </div>
      </div>
    </div>
</template>

<script>
  import { designOpera } from './api';
    export default {
    name:'ResetPass',
      data() {
        return {
          // 表单数据
          rpwForm: {
            username:'',  //用户名
            email: '',  //邮箱
          },
          // 验证规则
          rules: {
            // 用户名验证规则
            username: [
            {required: true,message: '账号不能为空', trigger: 'blur'},
            { max: 20, message: '账号长度最长20位', trigger: 'blur' }
          ],
          // 邮箱验证规则
            email:[
            { required: true, message: '请输入邮箱地址', trigger: 'blur' },
            { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
          ],
          }
     };
  },
      // 页面初始化
      mounted() {
        this.logincheck();
      },
      // 方法定义
      methods:{
        //检查登录是否过期
        logincheck(){
            designOpera({
            opera_type:'logincheck',
          })
          .then(data=>{
            console.log(data);
            if(data.code==404){
              return false
            }
            else if(data.data!=null){
              console.log(data)
              sessionStorage.setItem('username',data.data.user) //将后端传的username存入session
              this.$router.push({path:'/home'})
            }
          })
        },
        // 重置密码
        rpw(formName) {
          // 表单验证通过，可进行操作
            this.$refs[formName].validate((valid) => {
              if (valid) {
                // 确认操作
                this.$confirm('此操作将重置绑定该邮箱的账户密码, 是否继续?', '提示', {
                      confirmButtonText: '确定',
                      cancelButtonText: '取消',
                      type: 'warning'
                    })
                    .then(() => {  //确定时执行操作
                      designOpera({
                        opera_type:'resetpass',
                        username:this.rpwForm.username,
                        email:this.rpwForm.email
                      })
                      .then(data=>{
                        if(data.code==0){
                            this.$notify({
                            title: '重置密码成功',
                            message: '新密码已发送至您的邮箱，请注意查收!',
                            type: 'success'
                          });
                          this.$router.push({path:'/login'})
                        }else{
                          if(data.code==-5){
                              this.$message({
                              type: 'error',
                              message: '您还未注册账户，请注册',
                              showClose: true
                            });
                          }
                          else if(data.code==-10){
                            this.$message({
                              type: 'error',
                              message: '您还未绑定邮箱',
                              showClose: true
                            });
                          }
                          else{
                            this.$message({
                              type: 'error',
                              message: '用户名或邮箱错误',
                              showClose: true
                            });
                          }
                        }
                      })
                    }).catch(() => { //取消操作
                      this.$message({
                        type: 'info',
                        message: '已取消密码重置'
                      });
                    });
              } else { // 表单验证错误，返回false
              console.log('error submit!!');
              return false;
            }
        });
      },
      }
    }
</script>

<style scoped>
  /* 页面样式 */
  .rpw{
    position: absolute;
    width:100%;
    height:100%;
    background-color: #E4E7ED;
  }
  /* 标题样式 */
  .title {
    font-size: large;
    font-weight: bolder;
    text-align: center;
    color:black;
  }
  /* 表单区域样式 */
  .main-rpw {
    position: absolute;
    left:48%;
    top:40%;
    width:320px;
    height:270px;
    margin:-190px 0 0 -190px;
    padding:40px;
    border-radius: 5px; /* 圆角边框 */
    background: #F2F6FC;
  }
  /* el-form标签样式 */
  .el-form {
    padding-top: 5%;
    padding-left: 0;
    padding-right: 10%;
    width:300px
  }
  /* el-form-item标签样式 */
  .el-form-item{
    margin-left: -10%;
  }
  /* el-row标签样式 */
  .el-row {
    height: 100%;
    width: 100%;
  }
  /* link标签样式 */
  .link{
    margin-top: -10%;
    text-align: center;
    margin-left: 5%;
  }
  /* el-link标签样式 */
  .el-link{
    margin-left: 8px;
    line-height: 20px;
    font-size: 8px;
  }

</style>
