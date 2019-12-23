<template>
  <div id="app">
    <!-- <img src="./assets/logo.png"> -->
    <!-- <router-link to="/login">登录</router-link> -->
    <router-view/>
    <!-- <router-link to="/brand">品牌</router-link> -->
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style lang="less">
  @import './style/index.less';
  #app {
    height: 100%
  }
</style>
