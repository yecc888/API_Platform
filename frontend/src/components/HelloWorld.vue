-->
<template>
  <div>
    <span class="test33"><i class="el-icon-user"></i>
      <el-input v-if="flag" size="small" style="width: 200px;"></el-input>
    </span>
    <p>
      <!-- <el-button type="primary" icon="el-icon-search">搜索</el-button> -->
    </p>
    <div style="display: flex; margin-top: 20px; height: 100px;">
      <transition name="el-fade-in-linear">
        <div v-show="show" class="transition-box">哈哈 </div>
      </transition>
      <transition name="el-fade-in">
        <div v-show="show" class="transition-box">你好啊</div>
      </transition>
    </div>
  </div>
</template>

<script>
  export default {
    data: () => ({
      show: true,
      flag: true
    })
  }
</script>

<style lang="less" scoped>
  // .transition-box
  .test33{
    margin-top: 10px;
    width: 200px;
    height: 100px;
    border-radius: 4px;
    background-color: #409EFF;
    text-align: center;
    color: #fff;
    padding: 40px 20px;
  }
</style>
