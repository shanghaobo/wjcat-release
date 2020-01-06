<!--
程序名：Vue页面主入口
功能：Vue页面主入口
-->
<template>
  <div id="app">
    <router-view/>
  </div>
</template>
<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
  html,body{
    padding: 0;
    margin: 0;
      background-color: #fafafa;
  }
</style>
