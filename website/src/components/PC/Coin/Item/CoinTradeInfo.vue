<template>
  <div>
    <div class ="title_content clearfix">
      <div class="title left">分析</div>
      <div class="show_btn left" v-on:click = "show = !show"> 展开/折叠</div>
    </div>
    <transition name="bounce">
      <div v-if="show">
        <div  class = "title_content clearfix">
          <div class="left" v-for="n in 3" v-bind:class="{depth_item1:n==1,depth_item2:n==2,depth_item3:n==3}">
            <div>
              当日多空情况
            </div>
            <div class="clearfix">
            <div class = "buy left">买入总数:{{day_amount[n-1][0]}}</div>
            <div class = "sell left">卖出总数:{{day_amount[n-1][1]}}</div>
            </div>
            <div class="clearfix">
            <div class = "buyscale left" style="background:#00ff00;"  v-bind:style="{width: day_buy_width[n-1] + '%' }"></div>
            <div class = "sellscale left" style="background:#ff0000;" v-bind:style="{width: 100-day_buy_width[n-1] + '%' }"></div>
            </div>
          </div>
        </div>
        <div class="amount_title">
              汇总
        </div>
        <div class="clearfix amount_count" style="width:600px">
          <div class = "buy left">买入总数:{{all_amount[0]}}</div>
          <div class = "sell left">卖出总数:{{all_amount[1]}}</div>
          </div>
          <div class="clearfix amount_line">
          <div class = "buyscale left" style="background:#00ff00;"  v-bind:style="{width: all_buy_width + '%' }"></div>
          <div class = "sellscale left" style="background:#ff0000;" v-bind:style="{width: 100-all_buy_width + '%' }"></div>
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
var timer = [null, null, null];
export default {
  name: 'Main',
  props:{
    id: String
  },
  data () {
    return {
      show:false,
      day_amount:[[0,0],[0,0],[0,0]],
      day_buy_width:[100,100,100],
      all_amount:[0,0],
      all_buy_width:100
    }
  },
  created: function(){
    var time_now = new Date();
    console.log(time_now.getTime())
    time_now.setHours(0)
    time_now.setMinutes(0)
    time_now.setSeconds(0)
    time_now.setMilliseconds(0)

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
          console.log("lalalaalalalal"+response.data)
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
      "method": "sub_analyse",
      "param": {
        "market": 0,
        "order_coin": coin_order.toUpperCase(),
        "base_coin": "USDT",
        "watch_type": ["min", "hour", "day"]
      }
    },{
      "method": "sub_analyse",
      "param": {
        "market": 1,
        "order_coin": coin_order.toUpperCase(),
        "base_coin": "USDT",
        "watch_type": ["min", "hour", "day"]
      }
    },{
      "method": "sub_analyse",
      "param": {
        "market": 2,
        "order_coin": coin_order.toUpperCase(),
        "base_coin": "USDT",
        "watch_type": ["min", "hour", "day"]
      }
    }]
    ws = new WebSocket(websocket_config.analyse_url);
    ws.onopen = function(e){
        console.log("连接服务器成功");
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
        console.log(e.data)
        var json_obj = JSON.parse(e.data)
        var key_list = json_obj["type"].split("_");
        if(key_list[0] == "day" && json_obj["data"].length != 0){
          _this.$set(_this.day_amount[key_list[1]],0,json_obj["data"][0]["buy"].toString().slice(0,10));
          _this.$set(_this.day_amount[key_list[1]],1,json_obj["data"][0]["sell"].toString().slice(0,10));
          _this.$set(_this.day_buy_width, key_list[1], parseFloat(json_obj["data"][0]["buy"])/(parseFloat(json_obj["data"][0]["buy"])+parseFloat(json_obj["data"][0]["sell"]))*100);
          var all_buy = 0;
          var all_sell = 0;
          for(var i = 0; i < 3; i++){
            all_buy += parseFloat(_this.day_amount[i][0]);
            all_sell += parseFloat(_this.day_amount[i][1]);
          }
          _this.all_amount = [all_buy.toString().slice(0,10), all_sell.toString().slice(0,10)];
          _this.all_buy_width = all_buy*100/(all_buy+all_sell);
        }
        return;
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
.buy{
  min-height: 1px;
  width:50%;
}
.sell{
  min-height: 1px;
  width:50%;
}
.buyscale{
  min-height: 5px;
  width:50%;
}
.sellscale{
  min-height: 5px;
  width:50%;
}

.amount_title{
  margin-top:24px;
}
.amount_count{
  width:600px;
  margin:0 auto;
}
.amount_line{
  width:$content_width;
  margin:0 auto;
}
</style>
