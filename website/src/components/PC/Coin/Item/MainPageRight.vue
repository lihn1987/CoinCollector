<template>
  <div class="MainPageRight">
    <CoinTwitter></CoinTwitter>
  </div>
</template>
<script> 
import Vue from 'vue'
import axios from "axios"
import CoinTwitter from './CoinTwitter.vue'
Vue.component('CoinTwitter', CoinTwitter)
export default {
  name: 'MainPageRight',
  data () {
    return {
    }
  },
  created: function(){
  },computed: {
    // 计算属性的 getter
    
  },methods:{
  }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../../style/index.scss";
.MainPageRight{
  //background-color:#ff0000;
}
</style>
