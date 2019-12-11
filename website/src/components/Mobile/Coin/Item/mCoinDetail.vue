<template>
  <div>
    <div class ="title_content clearfix">
      <div class="title left">汇总成交记录</div>
      <div class="show_btn left" v-on:click = "show = !show"> 展开/折叠</div>
    </div>
    <transition name="bounce">
      <div v-if="show" class = "depth clearfix">
        <div class="left depth_item">
          <table class="table_sell">
            <tr>
              <th class="depth_head1">交易时间</th>
              <th class="depth_head2">价格(USDT)</th>
              <th class="depth_head3">数量</th>
              <th class="depth_head4">平台</th>
            </tr>
            <tr v-for="i in 10" v-bind:class="{green:detail_data[i-1][3]==0}">
              <td >{{utc2beijing(detail_data[i-1][0]).toString()}}</td>
              <td >{{(detail_data[i-1][1]).toString().substring(0,10)}}</td>
              <td >{{(detail_data[i-1][2]).toString().substring(0,10)}}</td>
              <td >{{detail_data[i-1][4]}}</td>
            </tr>
          </table>
        </div>
      </div>
    </transition>
  </div>
</template>
<script> 
import Vue from 'vue'

import {server_config,websocket_config} from '../../../../config/server_config.js'
import axios from "axios"
var _this = '';
export default {
  name: 'mCoinDetail',
  props:{
    id: String
  },
  data () {
    return {
      show : false,
      depth_data:[],
      detail_data:[]
    }
  },
  created: function(){
    _this = this
    var detail_count = 10;
    var _depth_data = new Array()
    var _detail_data = new Array()
    for(var market_idx = 0; market_idx < 3; market_idx++){
      _depth_data[market_idx] = new Array()
      for(var detail_idx = 0; detail_idx < detail_count; detail_idx++){
        _depth_data[market_idx][detail_idx] = new Array('-','-','-',0);
      }
    }
    for(var detail_idx = 0; detail_idx < detail_count; detail_idx++){
      _detail_data[detail_idx] = new Array('-','-','-','-','-');
    }
    this.depth_data = _depth_data;
    this.detail_data = _detail_data;
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
    utc2beijing(utc_datetime) {
      if(utc_datetime == '-')return'-';
      var d = new Date(parseInt(utc_datetime));
      return (d.getHours().toString().length == 1?"0":"")+d.getHours().toString()+":"+(d.getMinutes().toString().length == 1?"0":"")+d.getMinutes().toString()+":"+(d.getSeconds().toString().length == 1?"0":"")+d.getSeconds().toString();
  }
  }
}


var coin_order = '';
var ws = null;
var time_id = null;
var disconnected = false;
var ping_time_id = null;
var close_time  = null;
function reset_close_time(){
  if(close_time){
    clearTimeout(close_time);
  }
  close_time = setTimeout(function(){
    if(ws){
      console.log("force close")
      ws.close();
    }
  }, 10000)
}
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
    ws = new WebSocket(websocket_config.detail_url);
    ws.onopen = function(e){
        console.log("连接服务器成功");
        for(var item in sub_obj){
          //ws.send(JSON.stringify(item));
          //console.log(JSON.stringify(sub_obj[item]))
          ws.send(JSON.stringify(sub_obj[item]))
        }
        if(ping_time_id)clearInterval(ping_time_id);
        ping_time_id = setInterval(function(){
          if(ws != null)
            ws.send(JSON.stringify({ping:0}));
          },
        5000);
        reset_close_time();
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
        reset_close_time();
        var json_obj = JSON.parse(e.data)
        if("pong" in json_obj){
          return;
        }
        var json_obj = JSON.parse(e.data)
        if(json_obj.order_coin == coin_order && json_obj.market == 0){
          var tmp_array = [];
          for(var item in json_obj.data){
            tmp_array.push([json_obj.data[item].trade_time, json_obj.data[item].price, json_obj.data[item].amount, json_obj.data[item].dir,"火币"]);
          }
          tmp_array = tmp_array.concat(_this.detail_data);
          _this.detail_data = tmp_array.slice(0,10);
        }else if(json_obj.order_coin == coin_order && json_obj.market == 1){
          var tmp_array = [];
          for(var item in json_obj.data){
            tmp_array.push([json_obj.data[item].trade_time, json_obj.data[item].price, json_obj.data[item].amount, json_obj.data[item].dir,"OK"]);
          }
          tmp_array = tmp_array.concat(_this.detail_data);
          _this.detail_data = tmp_array.slice(0,10);
        }else if(json_obj.order_coin == coin_order && json_obj.market == 2){
          var tmp_array = [];
          for(var item in json_obj.data){
            tmp_array.push([json_obj.data[item].trade_time, json_obj.data[item].price, json_obj.data[item].amount, json_obj.data[item].dir,"币安"]);
          }
          tmp_array = tmp_array.concat(_this.detail_data);
          _this.detail_data = tmp_array.slice(0,10);
        }
    }
}
function reconnect_websocket(){
  if(disconnected)return;
  if(time_id){
    clearTimeout(time_id);
    time_id = null;
  }
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
    time_id = null;
  }
  if(ping_time_id != null){
    clearInterval(ping_time_id);
    ping_time_id = null;
  }
  if(close_time){
    clearTimeout(close_time);
    close_time = null;
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
  width:100vw;
  margin: 24px auto 0 auto;
}
.title {
  font-size:24px;
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
  font-size:14px;
  color:rgb(255,255,255);
  padding:4px 4px;
  border-radius:4px;
  margin-top:3px;
  margin-left:48px;
}
.depth{
  width:$content_width;
  margin:0 auto;
}
$margin_mid:1vw;
$depth_item_width: ( 100vw - ( $margin_mid * 1 ) ) / 2;

.depth_item{
  width:100vw;
}
.depth_item1{
  @extend .depth_item ;
}
.depth_item2{
  @extend .depth_item ;
  margin-left: $margin_mid;
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
  font-size:12px;
  table-layout:fixed;
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
	padding:0;
	background-color:#3F3F3F;
	border:1px solid #3F3F3F;
	color:#fff;
	}

td {
  nowrap:false;
	vertical-align:text-top;
	padding:0,0,0,0;
  border:1px solid #aaa;
  overflow:hidden;
	}

tr:nth-child(odd) {
	background-color:#F5F5F5;
}

tr:nth-child(even) {
	background-color:#fff;
}
.depth_head{
  width:33.3333%;
}
.depth_head1{
  width:25vw;
}
.depth_head2{
  width:30vw;
}
.depth_head3{
  width:33vw;
}
.depth_head4{
  width:12vw;
}
.green {
  color:rgb(86,236,86);
}
.red {
  color:rgb(236,86,86);
}
</style>
