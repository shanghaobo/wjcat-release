<template>
  <div style="text-align: center">
    fsdf
    sdff
    <br><br><br><br><br>

    <div class="test">
      <el-radio>
        <active-input :text="'选项二'" style="display: inline-block"></active-input>
      </el-radio>

      <!--<el-radio v-model="input"  style="margin: 0">-->
        <!--<el-input :class="{'out':!isInput1}" v-model="radio1" @focus="isInput1=true" @blur="isInput1=false"></el-input>-->
      <!--</el-radio>-->
      <!--<br><br>-->
      <!--<el-radio>-->
        <!--<el-input :class="{'out':!isInput2}" v-model="radio2" @focus="isInput2=true" @blur="isInput2=false"></el-input>-->
      <!--</el-radio>-->
    </div>
  </div>
</template>
<script>
  import activeInput from './activeInput.vue'

  export default{
    components:{
      activeInput
    },
    data(){
      return{
        radio1:'选项1',
        radio2:'选项2',
        isInput1:false,
        isInput2:false,
        input:false,
      }
    },

  }
</script>
<style scoped>
  .test{
    width: 50%;
    height: 500px;
    /*background-color: yellow;*/
    display: inline-block;
    background-color: #fafafa;
  }
  .inputClass{

    margin: 0;
  }
</style>
<style>
  .out .el-input__inner{
    background-color: #fafafa;
    border: none;
  }
  /*.out2 .el-input__inner{*/

  /*}*/
</style>
