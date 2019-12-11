<template>
  <div class="main">
    <Header :current=2 />
    
    <CoinTable />
    <div class="Info clearfix">
      <CoinNews class="CoinNews left"/>
      <CoinTwitter class="CoinTwitter left"/>
    </div>
    <Footer />
  </div>
</template>
<script> 
import Vue from 'vue'
import Header from '../Common/Header.vue'
import Footer from '../Common/Footer.vue'
import CoinTable from './Item/CoinTable.vue'
import CoinNews from './Item/CoinNews.vue'
import CoinTwitter from "./Item/CoinTwitter.vue"

Vue.component('Header', Header)
Vue.component('CoinTable', CoinTable)
Vue.component('CoinNews', CoinNews)
Vue.component('CoinTwitter', CoinTwitter)
Vue.component()
export default {
  name: 'Main',
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
  background-color:rgb(236,236,236);
}
.Info{
  width:$content_width;
  margin: 0 auto;
}
$coin_news_width: 800px;
$margin-left: 24px;
.CoinNews{
  background-color:#ffffff;
  border-radius:4px;
  padding:24px;
  width: $coin_news_width;
  margin:0 auto;
  box-sizing:border-box;
}

.CoinTwitter{
  background-color:#ffffff;
  margin-left: $margin-left;
  padding:24px;
  width: $content_width - $coin_news_width - $margin-left;
  box-sizing:border-box;
}
</style>
