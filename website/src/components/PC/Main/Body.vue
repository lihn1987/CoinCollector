<template>
  <div class="Body">
    <div class="body_content">
      <CoinNews></CoinNews>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import CoinNews from '../Coin/Item/CoinNews.vue'
Vue.component('CoinNews', CoinNews)
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
  background-color:rgb(216,216,216);
}
.body_content {
  //padding-top:180px;
  width:$content_width;
  background-color:rgb(255,255,255);
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

</style>
