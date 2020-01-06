<template>
  <div>
    <el-input :class="{'out':!isInput,'myInput':!isInput}" v-model="text" @focus="isInput=true" @blur="isInput=false"></el-input>
  </div>
</template>
<script>
  export default{
    props:['text'],
    data(){
      return{
        isInput:false,
      }
    }
  }
</script>
<style>
  .out .el-input__inner{
    background-color: #fafafa;
    border: none;
  }
  .myInput :hover{
    border: 1px dashed black;
    cursor:pointer
  }
</style>
