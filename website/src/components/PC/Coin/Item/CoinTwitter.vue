<template>
  <div class="CoinTwitter">
    <div class="twitter_module_title"> 最新twitter官方新闻</div>
    <div class="twitter_list">
      <div v-for="n in twitter_list.length">
        <div class="twitter_title">{{twitter_list[n-1]["coin_name"]}}官方</div>
        <a class="twitter_content" v-bind:href="twitter_list[n-1]['src']" target="_blank">{{twitter_list[n-1]["content"]}}</a>
        <div class = "twitter_bottom clearfix">
          <a class="twitter_user left" v-bind:href="'https://twitter.com/'+twitter_list[n-1]['username']" target="_blank">{{twitter_list[n-1]["name"]}}</a>
          <a class="twitter_time right">{{twitter_list[n-1]["time"]}}</a>
        </div>
      </div>
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
  name: 'CoinNews',
  data () {
    return {
      twitter_list:[],
      twitter_count:0
    }
  },
  filters:{
        getTwitterUserHref:function(val){
            return 'https://www.baidu.com/' + val 
        }
    },
  created: function(){
    var size = 5;
      var url = server_config.url+"/back/gettwitters.php?size="+size;;
      axios.get(
        url,
        {
        method:'get',
        withCredentials:false,
      })
      .then( (response) => {
        if(response.data.data.length){
          this.twitter_list = response.data.data;
          for(var i = 0; i < this.twitter_list.length; i++){
            this.twitter_list[i]["time"] = this.transformTime(this.twitter_list[i]["time"]);
            //console.log("??????")
            //console.log(twitter_list[i]["time"])
            //console.log(this.transformTime(twitter_list[i]["time"]))
          }
        }
        this.twitter_count = response.data.data.length;
      })
      .catch( (error) => {
        console.log(error)
      });
  },computed: {
    // 计算属性的 getter
    
  },methods:{
    addZero(m) {
        return m < 10 ? '0' + m : m;
    },
    transformTime(timestamp) {
        var time_now = Date.parse(new Date());
        timestamp/=1;
        if(time_now-timestamp < 60*60*1000){
            return parseInt((time_now-timestamp)/1000/60)+"分钟前"
        }else if(time_now-timestamp < 24*60*60*1000){
            return parseInt((time_now-timestamp)/1000/60/60)+"小时前"
        }
        if (timestamp) {
            var time = new Date(timestamp);
            var y = time.getFullYear();
            var M = time.getMonth() + 1;
            var d = time.getDate();
            var h = time.getHours();
            var m = time.getMinutes();
            var s = time.getSeconds();
            return y + '-' + this.addZero(M) + '-' + this.addZero(d) + ' ' + this.addZero(h) + ':' + this.addZero(m) + ':' + this.addZero(s);
        } else {
            return '';
        }
    }
  }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../../style/index.scss";
.CoinTwitter{
  //background-color:rgb(222,222,0);
}
.twitter_list{
  height:400px;
  overflow-x :hidden;
  overflow-y :auto;
}
.twitter_module_title{
  font-size:24px;
  color:$green;
  font-weight: 600px;
}
.twitter_title{
  margin-top:24px;
  text-decoration:none;
  color:#4a4a4a;
  font-weight:600;
}
.twitter_content{
  margin-top:4px;
  text-decoration:none;
  color:$gray-text;
}
.twitter_bottom{
  margin-top:4px;
  text-decoration:none;
  color:$gray-text;
}
.twitter_user{
  text-decoration:none;
  color:$gray-text;
}
.twitter_time{
  text-decoration:none;
  color:$gray-text;
}

</style>
