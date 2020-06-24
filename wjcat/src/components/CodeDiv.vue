<template>
  <div class="code-div">
    <div class="code-div-head">
      <div class="round"></div>
      <div class="round"></div>
      <div class="round"></div>
    </div>
    <div class="content">
      <slot></slot>
    </div>
  </div>
</template>
<style scoped>
.code-div {
  width: 800px;
  height: 500px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  overflow: hidden;
  margin-left: 50%;
  margin-bottom: 40px;
  margin-top: 40px;
  transform: translate(-50%);
}
.code-div-head {
  width: 100%;
  height: 40px;
  background-color: #2e3e4e;
  line-height: 40px;
  text-align: left;
  padding-left: 15px;
  box-sizing: border-box;
}
.round {
  width: 12px;
  height: 12px;
  margin: 0 3px;
  background-color: #9db1bb;
  border-radius: 50%;
  display: inline-block;
}
.content {
  width: 100%;
  height: calc(100% - 40px);
}
</style>
