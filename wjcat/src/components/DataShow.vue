<!--
程序名：数据分析页面
功能：对问卷调查结果的数据进行分析并用图表可视化展示
-->
<template>
  <div
    id="pdfDom"
    class="Count"
    v-loading="loading"
    element-loading-text="生成中..."
  >
    <div v-if="!(detail.length == 0)" class="opera-buttons">
      <el-button
        type="primary"
        size="mini"
        @click.native="analysisExportExcel"
        :loading="exportExcelLoading"
        >导出excel</el-button
      >
      <el-button type="success" size="mini" @click.native="exportPdf"
        >导出PDF</el-button
      >
    </div>
    <div v-if="detail.length == 0">暂时没有数据</div>
    <el-card class="question" v-for="(item, index) in detail">
      <div slot="header" class="clearfix">
        <span>{{ index + 1 + "." + item.title }}</span>
      </div>
      <!--如果数据库中的问题类型为单项选择或者多项选择-->
      <!--则将数据库中的数据以表格、柱状图、饼状图、圆环图、条形图的方式进行展示-->
      <div v-if="item.type == 'radio' || item.type == 'checkbox'">
        <el-table
          size="small"
          :data="item.result"
          style="width: 100%"
          stripe
          class="table"
        >
          <el-table-column prop="option" label="选项"></el-table-column>
          <el-table-column
            prop="count"
            label="数量"
            width="180"
          ></el-table-column>
          <el-table-column
            prop="percent"
            label="占比"
            width="180"
          ></el-table-column>
        </el-table>
        <br />

        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="changeValue(index, 1)"
          >柱状图</el-button
        >
        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="changeValue(index, 2)"
          >饼状图</el-button
        >
        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="changeValue(index, 3)"
          >圆环图</el-button
        >
        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="changeValue(index, 4)"
          >条形图</el-button
        >
        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="changeValue(index, 0)"
          >隐藏图表</el-button
        >

        <div :id="'img' + index" class="img" v-show="visible[index] == 1"></div>
        <div
          :id="'bing' + index"
          class="bing"
          v-show="visible[index] == 2"
        ></div>
        <div
          :id="'ring' + index"
          class="ring"
          v-show="visible[index] == 3"
        ></div>
        <div :id="'tz' + index" class="tz" v-show="visible[index] == 4"></div>
      </div>
      <!--如果数据库中的问题类型为text类型则将数据以弹窗表格的形式进行显示-->
      <div v-if="item.type == 'text'">
        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="lookTextDetail(item.questionId)"
          >详细内容</el-button
        >
        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="answerText2Excel(item.questionId)"
          :loading="item.questionId == answerText2ExcelQeustionId"
          >导出excel</el-button
        >
      </div>
    </el-card>
    <el-dialog title="详细内容" :visible.sync="dialogTableVisible">
      <el-table :data="tableData">
        <el-table-column property="context" label="答案"></el-table-column>
      </el-table>
      <el-pagination
        @size-change="sizeChange"
        @current-change="currentChange"
        :current-page.sync="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size.sync="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </el-dialog>
  </div>
</template>
<script>
import echarts from "echarts";
import { designOpera } from "./api";
import Design from "./Design.vue";
import axios from "axios";

export default {
  data() {
    return {
      dialogTableVisible: false,
      visible: [],
      loading: false,
      detail: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      tableData: [],
      questionId: 0,
      wjId: 0,
      exportExcelLoading: false,
      answerText2ExcelQeustionId: 0
    };
  },
  mounted() {
    //      this.dataAnalysis()
    //      console.log(this.visible);
  },
  methods: {
    answerText2Excel(questionId) {
      this.answerText2ExcelQeustionId = questionId;
      designOpera({
        opera_type: "answer_text_to_excel",
        questionId: questionId
      }).then(data => {
        this.doDownload(data.b64data, data.filename, "excel");
        this.answerText2ExcelQeustionId = 0;
      });
    },
    // 导出pdf
    exportPdf() {
      this.$alert("正在开发...", "提示");
    },
    // 导出excel
    analysisExportExcel() {
      this.exportExcelLoading = true;
      designOpera({
        opera_type: "analysis_export_excel",
        wjId: this.wjId
      }).then(data => {
        this.doDownload(data.b64data, data.filename, "excel");
        this.exportExcelLoading = false;
      });
    },
    doDownload(data, filename, type) {
      var b64data = data; //base64数据
      // b64data = b64data.replace("data:" + type + ";base64,", "");
      var bdata = this.dataURLtoBlob(b64data);
      if (!b64data) {
        return;
      }
      let url = window.URL.createObjectURL(new Blob([bdata]));
      let link = document.createElement("a");
      link.style.display = "none";
      link.href = url;
      //        link.download = 'ea7c0cf24153e0cd62bc8b64841fd84d.jpg'; //下载后文件名
      link.setAttribute("download", filename);

      document.body.appendChild(link);
      link.click();
    },
    dataURLtoBlob(dataurl) {
      //          dataurl=dataurl.replace('data:application/json;base64,','')
      console.log(dataurl);
      var bstr = atob(dataurl),
        n = bstr.length,
        u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return u8arr;
    },
    // 获取表格数据
    getTableData() {
      designOpera({
        opera_type: "get_text_answer_detail",
        questionId: this.questionId,
        currentPage: this.currentPage,
        pageSize: this.pageSize
      }).then(data => {
        console.log(data);
        this.tableData = data.detail;
        this.total = data.total;
      });
    },
    sizeChange() {
      this.getTableData();
    },
    currentChange() {
      this.getTableData();
    },
    //查看文本回答详情
    lookTextDetail(questionId) {
      this.tableData = [];
      this.pageSize = 10;
      this.total = 0;
      this.currentPage = 1;
      this.dialogTableVisible = true;
      this.questionId = questionId;
      this.getTableData();
    },
    //切换图表
    changeValue(num, value) {
      this.$set(this.visible, num, value);
      console.log("num=" + num);
      console.log("value=" + value);
      if (value == 1) {
        this.setImg(num);
      } else if (value == 2) {
        this.setPar(num);
      } else if (value == 3) {
        this.setRing(num);
      } else if (value == 4) {
        this.setTz(num);
      }
    },
    //      请求后端数据
    dataAnalysis(id) {
      this.loading = true;
      this.detail = [];
      console.log("wjid===");
      console.log(this.wjId);
      this.wjId = id;
      designOpera({
        opera_type: "dataAnalysis",
        username: "test",
        wjId: id
      }).then(data => {
        console.log(data);
        console.log(data.detail);
        this.detail = data.detail;
        this.visible = [];
        this.loading = false;
      });

      this.dialogShow = false;
    },
    test() {
      console.log(this.visible);
    },

    //柱状图
    setImg(id) {
      console.log(id);
      console.log(this.detail[id].result);
      let myChart = echarts.init(document.getElementById("img" + id));
      var option = {
        tooltip: {},
        legend: {
          data: ["数量"]
        },
        dataset: {
          dimensions: ["option", "count", "percent"],
          source: this.detail[id].result
        },
        xAxis: {
          type: "category"
        },
        yAxis: {},
        series: [
          {
            name: "数量：",
            type: "bar",
            barWidth: 30,
            color: "deepskyblue"
          }
        ]
      };
      myChart.setOption(option);
    },
    // 饼状图
    setPar(id) {
      let myChart = echarts.init(document.getElementById("bing" + id));
      var option = {
        tooltip: {},

        color: ["#409EFF", "#FFB54D", "#FF7466", "#44DB5E"],
        legend: {
          data: ["数量"]
        },
        dataset: {
          dimensions: ["option", "count", "percent"],
          source: this.detail[id].result
        },
        series: [
          {
            name: "统计结果：",
            type: "pie",
            radius: "55%",
            center: ["50%", "50%"],
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            }
          }
        ]
      };
      myChart.setOption(option);
    },
    // 圆环图
    setRing(id) {
      //console.log(id);
      let myChart = echarts.init(document.getElementById("ring" + id));
      var option = {
        tooltip: {},
        legend: {},
        color: ["#409EFF", "#FFB54D", "#FF7466", "#44DB5E"],
        dataset: {
          dimensions: ["option", "count", "percent"],
          source: this.detail[id].result
        },
        series: [
          {
            name: "数量：",
            type: "pie",
            radius: ["50%", "70%"],
            avoidLabelOverlap: false,
            label: {
              normal: {
                show: false,
                position: "center"
              },
              emphasis: {
                show: true,
                textStyle: {
                  fontSize: "30",
                  fontWeight: "bold"
                }
              }
            },
            labelLine: {
              normal: {
                show: false
              }
            }
          }
        ]
      };
      myChart.setOption(option);
    },
    //圆环图
    setTz(id) {
      //console.log(id);
      let myChart = echarts.init(document.getElementById("tz" + id));
      var option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow"
          }
        },
        dataset: {
          dimensions: ["option", "count", "percent"],
          source: this.detail[id].result
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true
        },
        xAxis: {
          type: "value",
          boundaryGap: [0, 0.01]
        },
        yAxis: {
          type: "category"
        },
        series: [
          {
            name: "数量：",
            type: "bar",
            barWidth: 30,
            color: "#409EFF"
          }
        ]
      };
      myChart.setOption(option);
    },
    //文本内容
    setText(id) {
      return {
        resule: this.detail[id].result
      };
    }
  }
};
</script>
<style scoped>
.Count {
}
.Count .question {
  max-width: 800px;
  width: 80%;
  display: inline-block;
  margin: 5px;
  text-align: left;
}
.Count .table {
}
.Count .img {
  width: 500px;
  height: 300px;
}
.Count .bing {
  width: 500px;
  height: 300px;
}
.Count .ring {
  width: 500px;
  height: 300px;
}
.Count .tz {
  width: 500px;
  height: 300px;
}
.opera-buttons {
  padding: 10px;
}
</style>
