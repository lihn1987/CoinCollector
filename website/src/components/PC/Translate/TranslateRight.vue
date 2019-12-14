<template>
  <div class="TranslateRight">
    <TranslateDepth />
    <TranslateDetail />
  </div>
</template>

<script>

import Vue from 'vue'
import TranslateDepth from './TranslateDepth.vue'
import TranslateDetail from './TranslateDetail.vue'
Vue.component('TranslateDepth', TranslateDepth)
Vue.component('TranslateDetail', TranslateDetail)
var _this = null;
export default {
  name: 'TranslateRight',
  created: function(){
    _this = this;
    this.bus.$on('current_coin_change', function(data) {
      console.log("lalalalaal"+data);
      _this.msg=data  //data就是触发updata事件带过来的数据
    })
  },
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

</style>
