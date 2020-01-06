<template>
  <div>
     <el-radio v-model="radio" label="1">备选项</el-radio>
    <el-radio v-model="radio" label="2">备选项</el-radio>

    {{radio}}

    <el-button type="primary" @click="test">主要按钮</el-button>
  </div>
</template>
<script>
  export default{
    data(){
      return{
        radio:'1'
      }
    },
    methods:{
      test(){
        console.log(this.radio);
      }
    },
    mounted(){

    },
    computed:{

    },
  }
</script>
<style>

</style>
