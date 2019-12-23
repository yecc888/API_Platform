<template>
  <el-container>
    <el-form :model="ruleLogin" status-icon :rules="loginRules" ref="ruleLogin" class="demo-ruleForm">
      <el-form-item prop="userName">
        <el-input type="password" v-model="ruleLogin.userName" auto-complete="off" placeholder="请输入账号"></el-input>
      </el-form-item>
      <el-form-item prop="passWord">
        <el-input type="password" v-model="ruleLogin.passWord" auto-complete="off" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleLogin')">登录</el-button>
        <el-button @click="register()">注册</el-button>
      </el-form-item>
    </el-form>
  </el-container>
</template>
<script>
  export default {
    data() {
      var checkName = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('用户名不能为空'));
        }
        callback();
      };
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.ruleLogin.passWord !== '') {
            callback();
          }
        }
      };
      return {
        ruleLogin: {
          userName: '',
          passWord: ''
        },
        loginRules: {
          userName: [{
            validator: checkName,
            trigger: 'blur'
          }],
          passWord: [{
            validator: validatePass,
            trigger: 'blur'
          }]
        }
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      register() {}
    }
  }
</script>
<style scoped lang="less">
  .el-container {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    display: flex;
    display: -webkit-flex;
    align-items: center;
    -webkit-align-items: center;
    justify-content: center;
    -webkit-justify-content: center;
    background-color: #f0f2f5;

    .el-form {
      border-radius: 20px;
      background-color: #fff;
      padding: 40px 30px;

      .el-form-item {
        display: flex;
        display: -webkit-flex;
        align-items: center;
        -webkit-align-items: center;
        justify-content: space-between;

        .el-input {
          flex: 1;
          -webkit-flex: 1;
          width: 260px;
          display: flex;
          display: -webkit-flex;
          align-items: center;
          -webkit-align-items: center;

          input {
            flex: 1;
            -webkit-flex: 1;
          }
        }
      }
    }
  }
</style>
