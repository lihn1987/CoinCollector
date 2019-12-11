<template>
  <div class="Body">
    <div class="body_content">
      <div class="clearfix">
        <CoinNews class="left coin_news"></CoinNews>
        <MainPageRight class="right main_page_right"></MainPageRight>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import CoinNews from '../Coin/Item/CoinNews.vue'
import MainPageRight from '../Coin/Item/MainPageRight.vue'
Vue.component('CoinNews', CoinNews)
Vue.component('MainPageRight', MainPageRight)
export default {
  name: 'HeaBodyder',
  data () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../style/index.scss";

.Body{
  background-color:rgb(236,236,236);
}
.body_content {
  //padding-top:180px;
  width:$content_width;
  //background-color:rgb(255,255,255);
  margin:0 auto;
}
.line_item1{
  font-size:52px;
  color:rgb(95,188,118);
}
.line_item2{
  font-size:52px;
  color:rgb(95,188,118);
}
$left-width:800px;
$right-width:400px;
$margin-width:20px;
$right-width: $content_width - $left-width - $margin-width;
.coin_news{
  width: $left-width;
  margin-top:12px;
  background-color:#ffffff;
  border-radius:4px;
  padding:24px;
  box-sizing:border-box;
}

.main_page_right{
  margin-top:12px;
  padding:24px;
  width:$right-width;
  margin-left:$margin-width;
  background-color:#ffffff;
  border-radius:4px;
  box-sizing:border-box;
}
</style>
