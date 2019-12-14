<template>
  <div class="TranslateDetail">
    <div>成交明细{{current_coin}}</div>
    <div class = "clearfix" >
      <div class = "col1 left">时间</div>
      <div class = "col2 left">价格</div>
      <div class = "col3 left">数量</div>
    </div>
    <div v-for="n in detail_list.length" class = "clearfix" v-bind:class="{green:detail_list[n-1][3]==0,red:detail_list[n-1][3]==1}">
      <div class = "col1 left">{{ detail_list[n-1][0] }}</div>
      <div class = "col2 left">{{ detail_list[n-1][1] }}</div>
      <div class = "col3 left">{{ detail_list[n-1][2] }}</div>
    </div>
  </div>
</template>

<script>

import Vue from 'vue'
import {server_config, websocket_config} from '../../../config/server_config.js'
var _this = null;
export default {
  name: 'TranslateDetail',
  created: function(){
    _this = this;
    connect_websocket(_this.current_coin);
    this.bus.$on('current_coin_change', function(data) {
      _this.current_coin=data  //data就是触发updata事件带过来的数据
      _this.detail_list=[]
      discnnect_websocket()
      connect_websocket(_this.current_coin);
    })
  },destroyed: function(){
    discnnect_websocket();
  },
  data () {
    return {
      current_coin:"BTC/USDT",
      detail_list : []
    }
  }
}

function addZero(m) {
    return m < 10 ? '0' + m : m;
}
function transformTime(timestamp) {
    var time_now = Date.parse(new Date());
    timestamp*=1
    /*if(time_now-timestamp < 60*60*1000){
        return parseInt((time_now-timestamp)/1000/60)+"分钟前"
    }else if(time_now-timestamp < 24*60*60*1000){
        return parseInt((time_now-timestamp)/1000/60/60)+"小时前"
    }*/
    if (timestamp) {
        var time = new Date(timestamp);
        var y = time.getFullYear();
        var M = time.getMonth() + 1;
        var d = time.getDate();
        var h = time.getHours();
        var m = time.getMinutes();
        var s = time.getSeconds();
        return addZero(h) + ':' + addZero(m) + ':' + addZero(s);
    } else {
        return '';
    }
}



var coin_order = '';
var ws = null;
var time_id = null;
var ping_time_id = null;
var disconnected = false;
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
    var order = coin.split("/")[0]
    var base = coin.split("/")[1]
    var sub_obj = [{
      "method": "sub_depth",
      "param": {
        "market": 0,
        "order_coin": order.toUpperCase(),
        "base_coin": base.toUpperCase(),
        "depth": 5
      }
    },{
      "method": "sub_depth",
      "param": {
        "market": 1,
        "order_coin": order.toUpperCase(),
        "base_coin": base.toUpperCase(),
        "depth": 5
      }
    },{
      "method": "sub_depth",
      "param": {
        "market": 2,
        "order_coin": coin_order.toUpperCase(),
        "base_coin": base.toUpperCase(),
        "depth": 5
      }
    }]
    ws = new WebSocket(websocket_config.detail_url);
    ws.onopen = function(e){
        console.log("连接服务器成功");
        for(var item in sub_obj){
          //ws.send(JSON.stringify(item));
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
        console.log(json_obj);
        for(var item in json_obj.data){
            _this.detail_list.unshift([transformTime(json_obj.data[item].trade_time), json_obj.data[item].price.toString().slice(0,10), json_obj.data[item].amount.toString().slice(0,10), json_obj.data[item].dir]);
        }
        _this.detail_list = _this.detail_list.slice(0,33)
        
        /*if(json_obj.order_coin == coin_order && json_obj.market == 0){
          var tmp_array = [];
          for(var item in json_obj.data){
            tmp_array.push([json_obj.data[item].trade_time, json_obj.data[item].price, json_obj.data[item].amount, json_obj.data[item].dir]);
          }
          tmp_array = tmp_array.concat(_this.depth_data[0]);
          _this.$set(_this.depth_data,0,tmp_array.slice(0,10));
        }else if(json_obj.order_coin == coin_order && json_obj.market == 1){
          var tmp_array = [];
          for(var item in json_obj.data){
            tmp_array.push([json_obj.data[item].trade_time, json_obj.data[item].price, json_obj.data[item].amount, json_obj.data[item].dir]);
          }
          tmp_array = tmp_array.reverse();
          tmp_array = tmp_array.concat(_this.depth_data[1]);
          _this.$set(_this.depth_data,1,tmp_array.slice(0,10));
        }else if(json_obj.order_coin == coin_order && json_obj.market == 2){
          var tmp_array = [];
          for(var item in json_obj.data){
            tmp_array.push([json_obj.data[item].trade_time, json_obj.data[item].price, json_obj.data[item].amount, json_obj.data[item].dir]);
          }
          tmp_array = tmp_array.reverse();
          tmp_array = tmp_array.concat(_this.depth_data[2]);
          _this.$set(_this.depth_data,2,tmp_array.slice(0,10));
        }*/
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
<style  lang="scss" scoped>
@import "../../../style/index.scss";

.TranslateDetail{
  margin-top:12px;
  border:1px solid rgb(215,215,215);
  border-radius:8px;
  padding:17px; 
  font-size:13px;
  height:683px;
  box-sizing: border-box;
}
.col1{
  width: 33.3%;
  text-align:left;
}
.col2{
  width: 33.3%;
  text-align:right;
}
.col3{
  width: 33.3%;
  text-align:right;
}
.green{
  color:$green;
}
.red{
  color:$red;
}
</style>
