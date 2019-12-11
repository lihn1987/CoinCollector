<template>
  <div class="CoinDescribeIntruduce clearfix">
    <div v-bind:class="{discribe:!show, discribe_all:show}">
      {{discription}}
    </div>
    <a class="back" v-on:click = "show = !show">
      展开详情/收起详情
    </a>
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
  name: 'mCoinDescribeIntruduce',
  props:{
    id: String
  },
  data () {
    return {
      show : false,
      discription:''
    }
  },
  created: function(){
    var url = server_config.url+"/back/getcoinbase.php?method=get_description&id="+this.$props.id;
      axios.get(
        url,
        {
        method:'get',
        withCredentials:false,
      })
      .then( (response) => {
        this.discription = response.data;
      })
      .catch( (error) => {
        console.log(error)
        alert(error)
      });
  },methods:{
    pageChange(pInfo){
    },
  }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../../style/index.scss";
.CoinDescribeIntruduce{
  width: 100vw;
  margin:60px auto;
}

.discribe{
  line-height:36px;
  text-align: left;
  color: $gray-text;
  text-overflow: -o-ellipsis-lastline;
overflow: hidden;
text-overflow: ellipsis;
display: -webkit-box;
-webkit-line-clamp: 2;
-webkit-box-orient: vertical;
}
.discribe_all{
  line-height:36px;
  text-align: left;
  color: $gray-text;
}

.back {
  background:rgb(255,106,25);
  font-size:14px;
  color:rgb(255,255,255);
  padding:4px 4px;
  border-radius:4px;
  margin-top:24px;
  float:right;
  text-decoration:none;
}
</style>
