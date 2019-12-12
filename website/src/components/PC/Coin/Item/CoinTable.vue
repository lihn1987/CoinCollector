<template>
  <div class="table">
    <div class="title">代币列表</div>
    <table class="content">
      <tr>
        <th>排名</th>
        <th>名称</th>
        <th>简称</th>
        <th>中文名</th>
        <th>官网</th>
        <th>项目评分</th>
        <th>详细描述</th>
      </tr>
      <tr v-for="n in row_list.length" >
        <td class="item1 ">{{row_list[n-1].index}}</td>
        <td class="item2 ">{{row_list[n-1].name}}</td>
        <td class="item3 ">{{row_list[n-1].name_en}}</td>
        <td class="item4 ">{{row_list[n-1].name_cn}}</td>
        <td class="item5 ">{{row_list[n-1].official_website}}</td>
        <td class="item7 ">{{row_list[n-1].score_all.slice(0,5)}}</td>
        <td class="item6 "><a class="coinbase_describe" :href="'/coin/describe/'+row_list[n-1].id">详情以及相关新闻指数</a></td>
      </tr>
    </table>
    <v-page  :totalRow="totalRow" :pageSizeMenu="[10, 20, 50]"  @page-change="pageChange" class="v-pagination--center v-page"></v-page>
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
  name: 'Main',
  data () {
    return {
      totalRow : 0,
      row_list :[]
    }
  },
  created: function(){
    
  },methods:{
    pageChange(pInfo){
      
      var url = server_config.url+"/back/getcoinbase.php?method=get_all&page_idx="+((pInfo.pageNumber-1)*pInfo.pageSize)+"&page_size="+pInfo.pageSize;
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
        console.log(this.row_list);
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
  font-size:36px;
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
  text-align:left;
}

tr:nth-child(odd) {
	background-color:#F5F5F5;
}

tr:nth-child(even) {
	background-color:#fff;
}


.content {
  margin:24px auto 0 auto;
  width: $content_width;
}
.item{
  color:#000000;
  min-height:1px;
}
.item1{
  @extend .item ;
  width:5%;
}
.item2{
  @extend .item ;
  width:15%;
}
.item3{
  @extend .item ;
  width:7%;
}
.item4{
  @extend .item ;
  width:15%;
}
.item5{
  @extend .item ;
  width:30%;
}
.item6{
  @extend .item ;
  width:18%;
}
.item7{
  @extend .item ;
  width:10%;
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
