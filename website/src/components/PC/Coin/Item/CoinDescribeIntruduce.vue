<template>
  <div class="CoinDescribeIntruduce clearfix">
    <div class="discribe">
      {{discription}}
    </div>
    <a class="back" href="/#/coin">
      返回
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
  name: 'CoinDescribeIntruduce',
  props:{
    id: String
  },
  data () {
    return {
      discription:''
    }
  },
  created: function(){
    var url = server_config.url+":"+server_config.port+"/back/getcoinbase.php?method=get_description&id="+this.$props.id;
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
      console.log(pInfo);//{pageNumber: 1, pageSize: 10}
      
    }
  }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../../style/index.scss";
.CoinDescribeIntruduce{
  width: $content_width;
  margin:60px auto;
}

.discribe{
  line-height:36px;
  text-align: left;
  color: $gray-text;
}

.back {
  margin-top:36px;
  background-color:$green;
  color:#ffffff;
  border-radius:10px;
  padding:10px 20px;
  float:right;
  text-decoration:none;
}
</style>
