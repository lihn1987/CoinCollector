<template>
  <div class="table">
    <div class="title">最新新闻列表</div>
    <div class="news_list" v-for="n in new_list.length">
      <a class="news_title" v-bind:href="new_list[n-1].source_addr" target="_blank">{{new_list[n-1].title}}</a>
      <div class="news_desc">{{new_list[n-1].desc}}</div>
      <div class="bottom clearfix">
        <a class="news_media left" v-bind:href="computeSource(new_list[n-1].source_media)" target="_blank">来源:{{new_list[n-1].source_media}}</a>
        <div class="news_author left">作者:{{new_list[n-1].author}}</div>
        <div class="news_time right">发布时间:{{new_list[n-1].time_utc}}</div>
      </div>
    </div>

    <a class="btn_next" v-on:click="GetPage(page_idx)">下一页</a>

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
      new_list:[],
      page_idx:0
    }
  },
  created: function(){
    this.GetPage(0);
  },computed: {
    // 计算属性的 getter
    
  },methods:{
    GetPage(page_idx){
      var size = 10;
      var url = server_config.url+":"+server_config.port+"/back/getnews.php?&offset="+(page_idx*size)+"&size="+size;;
      axios.get(
        url,
        {
        method:'get',
        withCredentials:false,
      })
      .then( (response) => {
        for(var i = 0; i < response.data.list.length; i++){
          response.data.list[i].time_utc = this.transformTime(response.data.list[i].time_utc);
        }
        this.new_list = this.new_list.concat(response.data.list);
        this.page_idx+=1;
        console.log(this.new_list)
      })
      .catch( (error) => {
        console.log(error)
        alert(error)
      });
    },
    addZero(m) {
        return m < 10 ? '0' + m : m;
    },
    transformTime(timestamp) {
        var time_now = Date.parse(new Date());
        timestamp*=1000
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
    },
    computeSource(media_name){
      switch(media_name){
        case '8比特':
          return "https://www.8btc.com/";
        case '金色财金':
          return "https://www.jinse.com/";
        case '链闻chainnews':
          return 'https://www.chainnews.com/';
        case '区势传媒':
          return 'https://www.55coin.com/';
        case '链向财经':
          return 'https://www.chainfor.com/';
      }
    }
  }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../../style/index.scss";
.title {
  font-size:36px;
  margin-top:36px;
  color:$green;
}
.news_list{
  width:600px;
  margin:36px auto;
}
.news_title{
  text-align: left;
  font-size:24px;
  text-decoration:none;
  color:$gray-text;
}
.news_desc{
  text-align: left;
}
.news_media{
  text-align: left;
  font-size:14px;
  text-decoration:none;
  color:$gray-text;
} 
.news_author{
  text-align: left;
  font-size:14px;
  margin-left:24px;
}
.news_time{
  text-align: left;
  font-size:14px;
}
.bottom {
  margin-top:12px;
}
.btn_next {
  box-sizing:border-box;
  background-color:$green;
  color:#ffffff;
  border-radius:10px;
  padding:10px 20px;
  text-decoration:none;
  display:block;
  width:100px;
  margin:0 auto 36px auto;
}
</style>
