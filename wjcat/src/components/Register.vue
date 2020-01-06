<!--
程序名：网站注册页面
功能：网站注册
-->
<template>
    <div class="register">
      <div class="main-register">
        <div class="title">注 册</div>
        <!-- 注册表单 -->
        <el-row>
          <el-form  :model="registerForm" status-icon :rules="rules" size="medium" ref="registerForm" label-width="100px" class="demo-registeForm">
            <el-form-item prop="username" label="用户名">
              <el-input @keyup.enter.native="Register('registerForm')" v-model="registerForm.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="pass">
              <el-input @keyup.enter.native="Register('registerForm')" v-model="registerForm.pass" autocomplete="off" placeholder="请输入密码(不少于6位)" show-password>
              </el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="checkPass">
              <el-input  @keyup.enter.native="Register('registerForm')" v-model="registerForm.checkPass" autocomplete="off" placeholder="请再次输入密码" show-password>
              </el-input>
            </el-form-item>
            <!-- 注册，重置按钮 -->
            <el-form-item style="margin-left: -25%">
              <el-button type="primary" @click="Register('registerForm')" >注册</el-button>
              <el-button @click="resetForm('registerForm')" style="margin-right: -5%">重置</el-button>
            </el-form-item>
          </el-form>
        </el-row>
        <!-- 登录页面链接 -->
        <div class="link">
        <el-link type="primary" :underline="false" href="/login">已有账号?去登录</el-link>
      </div>
      </div>
    </div>
</template>

<script>
    import { designOpera } from './api';
    export default {
    name: "Register",
    data() {
      // 检查密码
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.registerForm.checkPass !== '') {
            this.$refs.registerForm.validateField('checkPass');
          }
          callback();
        }
      };
      // 确认密码验证
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.registerForm.pass) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      return {
        // 表单数据
        registerForm: {
          username: '', // 用户名
          pass: '', // 密码
          checkPass: '',  // 检查密码
        },
        // 验证规则
        rules: {
          // 用户名验证规则
          username: [
          {required: true,message: '账号不能为空', trigger: 'blur'},
          { max: 20, message: '账号长度最长20位', trigger: 'blur' }
        ],
        // 密码验证规则
        pass: [
          { required: true, validator: validatePass, trigger: 'blur' },
          { min: 6, message: '密码长度最少为6位', trigger: 'blur' },
          {max:16,message:'密码长度不能超过16位',trigger:'blur'}
        ],
        // 检查密码验证规则
        checkPass: [
          { required: true, validator: validatePass2, trigger: 'blur' }
        ],
        },
      };
    },
    // 页面初始化
     mounted() {
       this.logincheck();
    },
    // 方法定义
    methods: {
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
      // 注册
      Register(formName) {
        // 表单验证通过，可进行操作
        this.$refs[formName].validate((valid) => {
          if (valid) {
            designOpera({
              opera_type:'register',  //操作类型
              username:this.registerForm.username,  //用户名
              password:this.$md5(this.registerForm.pass)  //密码md5加密
            })
            .then(data=>{
              console.log(data);
              if(data.code == 0){ //注册成功
                  this.$message({
                  message: '注册成功，请登录!',
                  type: 'success'
                });
                this.$router.push({path:'/login'});
              }
              else{   //注册失败
                this.$message({
                    type: 'error',
                    message: '该用户名已被注册',
                    showClose: true
                  });
              }
            });
          } else {   //表单验证失败，返回false
            console.log('error submit!!');
            return false;
          }
        });
      },
      // 表单重置
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
    }
}
</script>

<style scoped>
  /* 注册页面样式 */
  .register{
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
  /* 注册表单区域样式 */
  .main-register {
    position: absolute;
    left:48%;
    top:40%;
    width:350px;
    height:300px;
    margin:-190px 0 0 -190px;
    padding:40px;
    border-radius: 5px;  /*圆角边框*/
    background: #F2F6FC;
  }
  /* el-form标签样式 */
  .el-form {
    padding-top: 5%;
    padding-right: 10%;
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
    margin-top: -12%;
    text-align: center;
    margin-left: -5%;
  }
  /* el-link标签样式 */
  .el-link{
    margin-left: 8px;
    line-height: 20px;
    font-size: 8px;
  }

</style>
