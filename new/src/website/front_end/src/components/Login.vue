<template>
  <div class="app" style = "min-width:1280px">
    <el-card class="login_card">
      <div style="display:flex; flex-direction:row;justify-content:space-between">
        <div style="width:90px;line-height:40px;text-align: justify;">用户名</div>
        <el-input v-model="username" style="width:360px"></el-input>
      </div>
      <div style="display:flex; flex-direction:row;justify-content:space-between;margin-top:24px;">
        <div style="width:90px;line-height:40px;text-align: justify;">密码</div>
        <el-input v-model="password" style="width:360px" show-password></el-input>
      </div>
      <el-button type="primary" style="margin-top:24px;" @click="login">登  录</el-button>
    </el-card>
  </div>
</template>
<script src="../script/Login.js"></script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
  @import '../scss/common.scss';
  .login_card{
    position: absolute;
    width: 480px;
    height: 200px;
    top: 40%;
    left: 50%;
    transform: translateX(-50%) translateY(-50%);
    display:flex;
    flex-direction:column;
    justify-content:space-between;
  }
</style>
