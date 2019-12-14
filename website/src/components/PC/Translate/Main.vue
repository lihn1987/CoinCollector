<template>
  <div class="main">
    <Header :current=3 />
    <div class="content clearfix" >
      <TranslateLeft class = "left"/>
      <TranslateMid class = "left"/>
      <TranslateRight class = "left"/>
    </div>
    <Footer />
  </div>
</template>

<script> 
import Vue from 'vue'
import Header from '../Common/Header.vue'
import Footer from '../Common/Footer.vue'
import Body from '../Common/ErrorBody.vue'
import TranslateLeft from './TranslateLeft'
import TranslateMid from './TranslateMid'
import TranslateRight from './TranslateRight'
Vue.component('Header', Header)
Vue.component('Footer', Footer)
Vue.component('ErrorBody', Body)
Vue.component('TranslateLeft', TranslateLeft)
Vue.component('TranslateMid', TranslateMid)
Vue.component('TranslateRight', TranslateRight)
export default {
  name: 'Translate',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss" scoped>
@import "../../../style/index.scss";
$left_width : 300px;
$right_width : 300px;
$info_height:1040px;
$mid_width :  $content_width - $left_width - $right_width ;
.TranslateLeft{
  margin-top:16px;
  width:$left_width;
  box-sizing: border-box;
}
.TranslateMid{
  margin-top:16px;
  width:$mid_width;
  background:#00ff00;
  box-sizing: border-box;
}
.TranslateRight{
  margin-top:16px;
  height:$info_height;
  width:$right_width;
  box-sizing: border-box;
}
.content{
  width:$content_width;
  margin:0 auto;
}
</style>
