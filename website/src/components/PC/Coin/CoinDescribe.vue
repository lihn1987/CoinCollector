<template>
  <div class="main">
    <Header :current=2 />
    <CoinDescribeIntruduce :id="this.$route.params.id" />
    <CoinDepth :id="this.$route.params.id" />
    <CoinDetail :id="this.$route.params.id" />
    <CoinTradeInfo :id="this.$route.params.id" />
    <div class="info clearfix">
      <CoinNewsOnCoin :id="this.$route.params.id" class="left CoinNewsOnCoin"/> 
      <CoinTwitterOnCoin :id="this.$route.params.id" class="left CoinTwitterOnCoin"/>
    </div>
    <Footer />
  </div>
</template>
<script> 
import Vue from 'vue'
import Header from '../Common/Header.vue'
import Footer from '../Common/Footer.vue'
import CoinDescribeIntruduce from './Item/CoinDescribeIntruduce'
import CoinNewsOnCoin from './Item/CoinNewsOnCoin'
import CoinDepth from './Item/CoinDepth'
import CoinDetail from './Item/CoinDetail'
import CoinTradeInfo from './Item/CoinTradeInfo'
import CoinTwitterOnCoin from './Item/CoinTwitterOnCoin'
Vue.component('Header', Header)
Vue.component('CoinDescribeIntruduce', CoinDescribeIntruduce)
Vue.component('CoinNewsOnCoin', CoinNewsOnCoin)
Vue.component('Footer', Footer)
Vue.component('CoinDepth', CoinDepth)
Vue.component('CoinDetail', CoinDetail)
Vue.component('CoinTradeInfo', CoinTradeInfo)
Vue.component('CoinTwitterOnCoin', CoinTwitterOnCoin)



export default {
  name: 'CoinDescrebe',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../style/index.scss";
.main{
  background:rgb(236,236,236);
}
.info{
  width:$content_width;
  margin:0 auto;
}
$news_width:800px;
$margin_left:24px;
.CoinNewsOnCoin{
  background:#ffffff;
  padding:24px;
  width:$news_width;
  box-sizing: border-box;
  border-radius:4px;
}
.CoinTwitterOnCoin{
  background:#ffffff;
  width: $content_width - $news_width - $margin_left;
  margin-left:$margin_left;
  box-sizing: border-box;
  border-radius:4px;
}
</style>
