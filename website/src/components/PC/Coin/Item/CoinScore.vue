<template>
  <div class="CoinScore clearfix">
    <div class="score_item1 clearfix left">
      <div class="left">代码提交总数</div>
      <div class="num right">{{commit_all}}</div>
    </div>
    <div class="score_item2 clearfix left">
      <div class="left">近7日代码提交数</div>
      <div class="num right">{{commit_7d}}</div>
    </div>
    <div class="score_item3 clearfix left">
      <div class="left">近7日媒体报道数</div>
      <div class="num right">{{media_news_count}}</div>
    </div>
    <div class="score_item4 clearfix left">
      <div class="left">近7日官媒发声数</div>
      <div class="num right">{{offical_news_count}}</div>
    </div>
  </div>
</template>
<script> 
import Vue from 'vue'
import axios from "axios"

import {server_config} from '../../../../config/server_config.js'
import Pagination from 'vue-pagination-2'
import { vPage } from 'v-page'
Vue.component('pagination', Pagination)
Vue.component('v-page', vPage)
export default {
  name: 'CoinDescribeIntruduce',
  props:{
    id: String
  },
  data () {
    return {
      commit_all:"0",
      commit_7d:"0",
      media_news_count:"0",
      offical_news_count:"0"
    }
  },
  created: function(){
    var url = server_config.url+"/back/getCommitScore.php?id="+this.$props.id;
    axios.get(
      url,
      {
      method:'get',
      withCredentials:false,
    })
    .then( (response) => {
      //this.discription = response.data;
      //console.log(response)
      this.commit_all = response.data['data']['max'];
      this.commit_7d = response.data['data']['count'];
    })
    .catch( (error) => {
      console.log(error)
      alert(error)
    });
    //http://a.com/back/getNewsScore.php?id=3962

    var url = server_config.url+"/back/getNewsScore.php?id="+this.$props.id;
    axios.get(
      url,
      {
      method:'get',
      withCredentials:false,
    })
    .then( (response) => {
      //this.discription = response.data;
      //console.log(response)
      this.media_news_count = response.data['data']['media_news_count'];
      this.offical_news_count = response.data['data']['offical_news_count'];
    })
    .catch( (error) => {
      console.log(error)
      alert(error)
    });
  },methods:{
    pageChange(pInfo){
      console.log(pInfo);//{pageNumber: 1, pageSize: 10}
    }
  }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../../style/index.scss";
.CoinScore{
  width: $content_width;
  margin:60px auto;
}
$score_item_margin:50px;
$score_item_width:( $content_width - ( $score_item_margin * 3 ) ) / 4;
.num{
  color:$green;
}
.score_item{
  width:$score_item_width;
  box-sizing: border-box;
  background:#ffffff;
  border-radius:4px;
  padding:8px;
}
.score_item1{
  @extend .score_item ;
}
.score_item2{
  @extend .score_item ;
  margin-left:$score_item_margin;
}
.score_item3{
  @extend .score_item ;
  margin:auto $score_item_margin;
}
.score_item4{
  @extend .score_item ;
}

</style>
