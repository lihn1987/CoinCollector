<template>
  <div>
    <div class ="title_content clearfix">
      <div class="title left">深度行情</div>
      <div class="show_btn left" v-on:click = "show = !show"> 展开/折叠</div>
    </div>
    <transition name="bounce">
    <div v-if="show" class = "depth clearfix">
      <div class="left" v-for="n in 3" v-bind:class="{depth_item1:n==1,depth_item2:n==2,depth_item3:n==3}">
        <div>
          {{depth_item_title[n-1]}}
        </div>
        <table class="table_sell">
          <tr>
            <th class="depth_head1">价格(USDT)</th>
            <th class="depth_head2">数量</th>
          </tr>
          <tr v-for="i in 5" >
            <td >{{depth_data[n-1][0][i-1][0].toString().substring(0,10)}}</td>
            <td >{{depth_data[n-1][0][i-1][1].toString().substring(0,10)}}</td>
          </tr>
        </table>
        <table class = "table_buy">
          <tr>
            <th class="depth_head1">价格(USDT)</th>
            <th class="depth_head2">数量</th>
          </tr>
          <tr v-for="i in 5" >
            <td >{{depth_data[n-1][1][i-1][0].toString().substring(0,10)}}</td>
            <td >{{depth_data[n-1][1][i-1][1].toString().substring(0,10)}}</td>
          </tr>
        </table>
      </div>
    </div>
    </transition>
  </div>
</template>
<script> 
import Vue from 'vue'

import {server_config} from '../../../../config/server_config.js'
import axios from "axios"
var _this = '';
export default {
  name: 'Main',
  props:{
    id: String
  },
  data () {
    return {
      show:false,
      depth_item_title:["火币行情", "OK行情", "币安行情"],
      depth_data:[[[['-','-'],['-','-'],['-','-'],['-','-'],['-','-']],[['-','-'],['-','-'],['-','-'],['-','-'],['-','-']]],
        [[['-','-'],['-','-'],['-','-'],['-','-'],['-','-']],[['-','-'],['-','-'],['-','-'],['-','-'],['-','-']]],
        [[['-','-'],['-','-'],['-','-'],['-','-'],['-','-']],[['-','-'],['-','-'],['-','-'],['-','-'],['-','-']]]]
    }
  },
  created: function(){
    _this = this
    if(window.WebSocket){
        var url = server_config.url+"/back/getcoinbase.php?method=get_coin_name_en&id="+this.$props.id;
        axios.get(
          url,
          {
          method:'get',
          withCredentials:false,
        })
        .then( (response) => {
          connect_websocket(response.data);
        })
        .catch( (error) => {
          console.log(error)
          alert(error)
        });
        
    }
  },destroyed: function(){
    discnnect_websocket();
  },methods:{
    
  }
}


var coin_order = '';
var ws = null;
var time_id = null;
var disconnected = false;
function connect_websocket(coin){
    coin_order = coin;
    var sub_obj = [{
      "method": "sub_depth",
      "param": {
        "market": 0,
        "order_coin": coin_order.toUpperCase(),
        "base_coin": "USDT",
        "depth": 5
      }
    },{
      "method": "sub_depth",
      "param": {
        "market": 1,
        "order_coin": coin_order.toUpperCase(),
        "base_coin": "USDT",
        "depth": 5
      }
    },{
      "method": "sub_depth",
      "param": {
        "market": 2,
        "order_coin": coin_order.toUpperCase(),
        "base_coin": "USDT",
        "depth": 5
      }
    }]
    ws = new WebSocket('ws://localhost:8000');
    ws.onopen = function(e){
        console.log("连接服务器成功");
        //_this.depth_item_title=['a1','b1','c1'];
        
        for(var item in sub_obj){
          //ws.send(JSON.stringify(item));
          console.log(JSON.stringify(sub_obj[item]))
          ws.send(JSON.stringify(sub_obj[item]))
        }
    }
    ws.onclose = function(e){
        console.log("服务器关闭");
        reconnect_websocket();
    }
    ws.onerror = function(){
        console.log("连接出错");
        //reconnect_websocket();
    }
    ws.onmessage = function(e){
        //mess.innerHTML = "连接成功";
        //console.log(e.data);
        var json_obj = JSON.parse(e.data)
        if(json_obj.order_coin == coin_order && json_obj.market == 0){
          _this.$set(_this.depth_data[0],0,json_obj.forsell.slice(0,5).reverse());
          _this.$set(_this.depth_data[0],1,json_obj.forbuy.slice(0,5));
          //console.log(json_obj.forsell.slice(json_obj.forsell.length-5,json_obj.forsell.length))
        }else if(json_obj.order_coin == coin_order && json_obj.market == 1){
          _this.$set(_this.depth_data[1],0,json_obj.forsell.slice(0,5).reverse());
          _this.$set(_this.depth_data[1],1,json_obj.forbuy.slice(0,5));
          //console.log(json_obj.forsell.slice(json_obj.forsell.length-5,json_obj.forsell.length))
        }else if(json_obj.order_coin == coin_order && json_obj.market == 2){
          _this.$set(_this.depth_data[2],0,json_obj.forsell.slice(0,5).reverse());
          _this.$set(_this.depth_data[2],1,json_obj.forbuy.slice(0,5));
          //console.log(json_obj.forsell.slice(json_obj.forsell.length-5,json_obj.forsell.length))
        }
    }
}
function reconnect_websocket(){
  if(disconnected)return;
  time_id = setTimeout(function () {
　　　　// f1的任务代码
　　　　connect_websocket(coin_order);
　　  }, 5000);
}
function discnnect_websocket(){
  console.log("关闭连接");
  disconnected = true;
  if(time_id != null){
    clearTimeout(time_id)
  }
  if(ws != null){
    ws.close();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../../style/index.scss";
.title_content{
  width:$content_width;
  margin: 36px auto 0 auto;
}
.title {
  font-size:36px;
  color:$green;
}
.bounce-enter-active {
  animation: bounce-in .3s;
}
.bounce-leave-active {
  animation: bounce-in .3s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}

.show_btn{
  background:rgb(255,106,25);
  font-size:18px;
  color:rgb(255,255,255);
  padding:4px 4px;
  border-radius:4px;
  margin-top:8px;
  margin-left:48px;
}
.depth{
  width:$content_width;
  margin:0 auto;
}
$margin_mid:60px;
$depth_item_width: ( $content_width - ( $margin_mid * 2 ) ) / 3;

.depth_item{
  width:$depth_item_width;
}
.depth_item1{
  @extend .depth_item ;
}
.depth_item2{
  @extend .depth_item ;
  margin: 0 $margin_mid;
}
.depth_item3{
  @extend .depth_item ;
}
table {
	margin-top:15px;
	border-collapse:collapse;
	border:1px solid #aaa;
  color:rgb(255,0,0);
	width:100%;
	}
.table_sell {
  color:rgb(236,86,86);
  font-weight: 600;
}
.table_buy{
  color:rgb(86,236,86);
  font-weight: 600;
}
th {
	vertical-align:baseline;
	padding:5px 15px 5px 6px;
	background-color:#3F3F3F;
	border:1px solid #3F3F3F;
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
.depth_head{
  width:50%;
}
.depth_head1{
  @extend .depth_head ;
}
.depth_head2{
  @extend .depth_head ;
}
</style>
