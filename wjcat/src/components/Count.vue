<template>
  <div class="Count">
    <el-card class="question" v-for="(item,index) in detail">
      <div slot="header" class="clearfix">
        <span>{{(index+1)+'.'+item.title}}</span>
        <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>
      </div>
      <div>
        <el-table :data="item.result" style="width: 100%" stripe class="table">
          <el-table-column prop="option" label="选项" width="180"></el-table-column>
          <el-table-column prop="count" label="数量" width="180"></el-table-column>
          <el-table-column prop="percent" label="占比"></el-table-column>
        </el-table>
        <div :id="'img'+(index)" class="img">

        </div>
      </div>
    </el-card>
  </div>
</template>
<script>
  import echarts from 'echarts'
  export default{
    data(){
      return{
        detail:[
          {
            title:'您的性别是？',
            type:'radio',
            result:[
              {
                option:'男',
                count:5,
                percent:50
              },
              {
                option:'女',
                count:5,
                percent:50
              },
            ]
          },
          {
            title:'您平均每月购买日用品的消费是多少？',
            type:'radio',
            result:[
              {
                option:'50以下',
                count:0,
                percent:0
              },
              {
                option:'50-100',
                count:2,
                percent:66.67
              },
              {
                option:'100-150',
                count:1,
                percent:33.33
              },
              {
                option:'150以上',
                count:0,
                percent:0
              },
            ]
          },
        ]
      }
    },
    mounted(){
      this.init();
    },
    methods:{
      init(){
        for(let i=0;i<this.detail.length;i++){
          this.setImg(i);
        }
      },
      setImg(id){
        console.log(id);
        var myChart = echarts.init(document.getElementById('img'+id));
        var option = {
            tooltip: {},
            legend: {
                data:['数量']
            },
            dataset:{
              dimensions: ['option', 'count', 'percent'],
              source: this.detail[id].result,
            },
            xAxis: {
                type:'category'
            },
            yAxis: {},
            series: [
              {
                type: 'bar',
                barWidth:30,

//                label:{
//                    show:true,
//                formatter:'{b}xxx'
//
//                }
              },
            ],
        };
        myChart.setOption(option);
      }
    }
  }
</script>
<style scoped>
  .Count{
    background-color: yellow;
    text-align: center;
    /*width: 80%;*/
  }
  .Count .question{
    /*background-color: red;*/
    max-width: 800px;
    width: 80%;
    display: inline-block;
    margin: 10px;
    text-align: left;
  }
  .Count .table{
    /*width: 100px;*/
  }
  .Count .img{
    width: 100%;
    height: 300px;
    /*background-color: green;*/
  }

</style>
