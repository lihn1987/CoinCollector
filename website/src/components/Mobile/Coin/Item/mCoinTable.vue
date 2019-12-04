<template>
  <div class="table">
    <div class="title">代币列表</div>
    <table class="content">
      <tr>
        <th text-align="center">排名</th>
        <th text-align="center">简称</th>
        <th text-align="center">中文名</th>
        <th text-align="center">官网</th>
        <th text-align="center">描述</th>
      </tr>
      <tr v-for="n in row_list.length" >
        <td class="item1 ">{{row_list[n-1].index}}</td>
        <td class="item2 ">{{row_list[n-1].name_en}}</td>
        <td class="item3 ">{{row_list[n-1].name_cn}}</td>
        <td class="item4 "><a class="coinbase_describe" v-bind:href="row_list[n-1].official_website">访问</a></td>
        <td class="item5 "><a class="coinbase_describe" :href="'/coin/describe/'+row_list[n-1].id">详情</a></td>
      </tr>
    </table>
    <div class= "btn_content clearfix">
      <div class="btn left" v-bind:class="{disable:left_btn_disable}" v-on:click="on_page_change(-1)">上一页</div>
      <div class="btn right" v-on:click="on_page_change(1)">下一页</div>
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
  name: 'mCoinTable',
  data () {
    return {
      left_btn_disable: false,
      now_index: 0,
      totalRow : 0,
      row_list :[]
    }
  },
  created: function(){
    this.on_page_change(0);
  },methods:{
    on_page_change(n){
      console.log(n);
      this.now_index += n;
      if(this.now_index < 0){
        this.now_index = 0;
        return;
      }else if (this.now_index == 0){
        this.left_btn_disable = true;
      }
      var url = server_config.url+"/back/getcoinbase.php?method=get_all&page_idx="+((this.now_index)*10)+"&page_size="+10;
      axios.get(
        url,
        {
        method:'get',
        withCredentials:false,
      })
      .then( (response) => {
        let res_obj = response.data;
        this.totalRow=Number(response.data.count);
        this.row_list=response.data.list;
      })
      .catch( (error) => {
        alert(error)
      });
    }
  }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../../style/index.scss";
.title {
  font-size:24px;
  margin-top:36px;
  color:$green;
}
table {
	margin-top:15px;
	border-collapse:collapse;
	border:1px solid #aaa;
	width:100%;
	}

th {
	vertical-align:baseline;
	padding:5px 15px 5px 6px;
	background-color:#3F3F3F;
	border:1px solid #3F3F3F;
	text-align:left;
	color:#fff;
	}

td {
	vertical-align:text-top;
	padding:6px 15px 6px 6px;
	border:1px solid #aaa;
	}

tr:nth-child(odd) {
	background-color:#F5F5F5;
}

tr:nth-child(even) {
	background-color:#fff;
}


.content {
  margin:24px auto 0 auto;
  width: 100vw;
  font-size:12px;
}
.item{
  color:#000000;
  min-height:1px;
}
.item1{
  @extend .item ;
  width:20%;
}
.item2{
  @extend .item ;
  width:20%;
}
.item3{
  @extend .item ;
  width:30%;
}
.item4{
  @extend .item ;
  width:15%;
}
.item5{
  @extend .item ;
  width:15%;
}
.btn {
  box-sizing:border-box;
  background-color:$green;
  color:#ffffff;
  border-radius:10px;
  padding:2vw 5vw;
  text-decoration:none;
  display:block;
}
.disable
{
  background-color:rgb(74,74,74);
}
.btn_content{
  margin:10vw 10vw;
}
.coinbase_describe {
  text-decoration:none;
  color:rgb(95,188,118);;
}
.v-page{
  margin-top:24px;
  margin-bottom:36px;
}
</style>
