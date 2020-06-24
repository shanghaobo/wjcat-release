<!--
程序名：网站首页
功能：对网站进行介绍
-->
<template>
  <div class="main">
    <el-carousel height="500px">
      <el-carousel-item v-for="(item, index) in topImg" :key="index">
        <!--<div style="background-color: black;width: 100%;height: 100%;">-->
        <img :src="item.url" style="width: 100%;height: 100%;" />
        <div class="cover">
          {{ item.title }}<br />
          <span style="font-size: 35px">{{ item.subTitle }}</span>
        </div>
      </el-carousel-item>
    </el-carousel>
    <!--<el-divider></el-divider>-->

    <code-div><img src="/static/images/demo1.png" class="demoImg"/></code-div>
    <code-div><img src="/static/images/demo2.png" class="demoImg"/></code-div>
    <code-div><img src="/static/images/demo3.png" class="demoImg"/></code-div>
    <!-- <img src="/static/images/demo1.png" class="demoImg" /><br /> -->
    <!-- <img src="/static/images/demo2.png" class="demoImg" /><br />
    <img src="/static/images/demo3.png" class="demoImg" /><br /><br /> -->
    <h3>用户须知</h3>

    <el-divider></el-divider>
    <div style="text-align: left;padding-left: 300px;padding-right: 300px;">
      <p>
        为了规范互联网信息服务活动，促进互联网信息服务健康有序发展，让我们共同打造一个绿色、健康的互联网生态环境，以下内容禁止在本平台发布：
      </p>
      <p class="b">(一)涉及违反宪法所确定的基本原则；</p>
      <p class="b">
        (二)涉及危害国家安全，泄露国家秘密，颠覆国家政权，破坏国家统一；
      </p>
      <p class="b">(三)涉及损害党、国家、政府的荣誉和利益；</p>
      <p class="b">(四)涉及煽动民族仇恨、民族歧视，破坏民族团结；</p>
      <p class="b">(五)涉及破坏国家宗教政策，宣扬邪教和封建迷信；</p>
      <p class="b">(六)散布谣言，扰乱社会秩序，破坏社会稳定；</p>
      <p class="b">(七)散布淫秽、色情、赌博、暴力、凶杀、恐怖或者教唆犯罪；</p>
      <p class="b">(八)侮辱或者诽谤他人，侵害他人合法权益；</p>
      <p class="b">(九)含有法律、行政法规禁止的其他内容；</p>
      <p class="b">(十)特殊调查：涉外调查、社会调查</p>
      <p class="b">
        (十一)强制诱导性分享与关注，请查看朋友圈管理办法：<a
          href="http://kf.qq.com/faq/131117ne2MV7141117JzI32q.html"
          >http://kf.qq.com/faq/131117ne2MV7141117JzI32q.html</a
        >
      </p>
      <p class="b">(十二)广告类：广告、刷单、借贷名义实行诈骗</p>
    </div>
    <el-footer class="bottom">
      <p>Copyright © 2019 WjCat. All rights reserved.</p>
      <p>问卷喵交流群：850804401</p>
      <p>豫ICP备17008007号-2</p>
    </el-footer>
  </div>
</template>
<script>
import CodeDiv from "@/components/CodeDiv";
export default {
  components: {
    CodeDiv
  },
  data() {
    return {
      topImg: [
        {
          title: "免费在线问卷调查系统",
          subTitle: "Free Online Questionnaire System",
          url: "/static/images/4.jpg"
        }
        //          {
        //            'title':'简单的打开方式',
        //            'subTitle':'Simple Opening Method',
        //            'url':'/static/images/6.jpg'
        //          },
        //          {
        //            'title':'多样的数据可视化',
        //            'subTitle':'Diversified data visualization',
        //            'url':'/static/images/11.jpg'
        //          },
      ]
    };
  }
};
</script>
<style scoped>
.main {
  position: relative;
  width: 100%;
  height: 100%;
}
.bottom {
  height: 150px !important;
  background-color: #2e3e4e;
  color: #9b9ea0;
  position: relative;
  padding: 20px;
}
.demoImg {
  width: 100%;
  height: 100%;
  /*border-radius: 5px;*/
}
.cover {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 100;
  left: 0;
  top: 0;
  color: white;
  font-size: 50px;
  line-height: 60px;
  padding-top: 180px;
}
.lj {
}
.b {
  font-weight: 700;
}
</style>
