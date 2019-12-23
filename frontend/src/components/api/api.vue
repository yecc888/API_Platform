<template>
  <div class="editable-input titl-name">
    <el-input placeholder="请输入接口名称" v-model="input" clearable></el-input>
  </div>
</template>

<script>
    export default {
      data() {
        return {
          input: ''
        }
      }
    }
</script>

<style lang="less" scoped>

</style>
