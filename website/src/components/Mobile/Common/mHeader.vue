<template>
  <div class="Header">
    <div class="content clearfix">
      <a href="/#/" class="logo left">{{main_name}}</a>
      <a href="/#/news" class="item right" :class="{ item_active: current==4 }">{{new_name}}</a>
      <!-- <a href="/#/stone" class="item right" :class="{ item_active: current==3 }">{{stone_name}}</a> -->
      <a href="/#/coin" class="item right" :class="{ item_active: current==2 }">{{coin_name}}</a>
      <a href="/#/" class="item right" :class="{ item_active: current==1 }">{{page_home}}</a>
    </div>
  </div>
</template>

<script>

export default {
  name: 'mHeader',
  props:{
    current: Number
  },
  data () {
    return {
      main_name: '小站',
      page_home: '首页',
      coin_name: '币圈数据分析',
      stone_name: '股票数据分析',
      new_name: '最新动态'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss" scoped>
@import "../../../style/index.scss";
$header_height: 36px;
.Header {
  
  height:$header_height;
  background:#ffffff;
  box-shadow: 0 2px 4px 0px;
  position:relative;
  z-index: 1;
}
.content {
  padding:0 0vw;
  width: 100vw;
}
.logo {
  line-height:$header_height;
  font-size:14px;
  color:rgb(74, 74, 74);
  text-decoration:none;
  margin-left:5vw;
}
.item {
  line-height:$header_height;
  font-size:14px;
  color:rgb(74, 74, 74);
  margin:0 5vw;
  text-decoration:none;
}
.item_active{
  color:rgb(95,188,118);;
}
</style> 
