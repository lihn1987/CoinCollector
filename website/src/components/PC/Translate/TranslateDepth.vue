<template>
  <div class="TranslateDepth">
    <div style="font-size:13px;">深度区域{{current_coin}}</div>

    <div class="clearfix" >
      <div class=" depth_item_left left">价格</div>
      <div class=" depth_item_right right">数量</div>
    </div>
    <div class="clearfix" v-for="n in depth_sell_list.length">
      <div class="sell depth_item_left left">{{depth_sell_list[n-1][0].toString().slice(0,10)}}</div>
      <div class="sell depth_item_right right">{{depth_sell_list[n-1][1].toString().slice(0,10)}}</div>
    </div>
    <div class="clearfix" >
      <div class=" depth_item_left left">价格</div>
      <div class=" depth_item_right right">数量</div>
    </div>
    <div class="clearfix" v-for="n in depth_buy_list.length">
      <div class="buy depth_item_left left">{{depth_buy_list[n-1][0].toString().slice(0,10)}}</div>
      <div class="buy depth_item_right right">{{depth_buy_list[n-1][1].toString().slice(0,10)}}</div>
    </div>
  </div>
</template>

<script>
/*
import Vue from 'vue'
import Header from '../Common/Header.vue'
import Footer from '../Common/Footer.vue'
import Body from '../Common/ErrorBody.vue'
Vue.component('Header', Header)
Vue.component('Footer', Footer)
Vue.component('ErrorBody', Body)*/
import {server_config, websocket_config} from '../../../config/server_config.js'
var _this = null;
export default {
  name: 'TranslateDepth',
  created: function(){
    _this = this;
    this.bus.$on('current_coin_change', function(data) {
      _this.current_coin=data  //data就是触发updata事件带过来的数据
      depth_discnnect_websocket();
      _this.depth_sell_list_item=[[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]],[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]],[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]]];
      _this.depth_buy_list_item=[[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]],[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]],[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]]];
      depth_connect_websocket(_this.current_coin);
    })
    depth_connect_websocket("BTC/USDT");
  },destroyed: function(){
    depth_discnnect_websocket();
  },
  data () {
    return {
      current_coin:"BTC/USDT",
      msg: 'Welcome to Your Vue.js App',
      depth_sell_list:[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]],
      depth_buy_list:[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]],
      depth_sell_list_item:[[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]],[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]],[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]]],
      depth_buy_list_item:[[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]],[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]],[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]]]
    }
  }
}

var depth_coin = '';
var depth_ws = null;
var depth_time_id = null;
var depth_ping_time_id = null;
var depth_close_time = null;
var depth_disconnected = false;
function depth_reset_close_time(){
  if(depth_close_time){
    clearTimeout(depth_close_time);
  }
  depth_close_time = setTimeout(function(){
    if(depth_ws){
      console.log("force close")
      depth_ws.close();
      depth_connect_websocket(depth_coin);
    }
  }, 10000)
}
function depth_connect_websocket(coin){
    depth_coin = coin;
    var depth_coin_order = coin.split("/")[0];
    var depth_coin_base = coin.split("/")[1];
    var sub_obj = [{
      "method": "sub_depth",
      "param": {
        "market": 0,
        "order_coin": depth_coin_order.toUpperCase(),
        "base_coin": depth_coin_base.toUpperCase(),
        "depth": 5
      }
    },{
      "method": "sub_depth",
      "param": {
        "market": 1,
        "order_coin": depth_coin_order.toUpperCase(),
        "base_coin": depth_coin_base.toUpperCase(),
        "depth": 5
      }
    },{
      "method": "sub_depth",
      "param": {
        "market": 2,
        "order_coin": depth_coin_order.toUpperCase(),
        "base_coin": depth_coin_base.toUpperCase(),
        "depth": 5
      }
    }]
    depth_ws = new WebSocket(websocket_config.depth_url);
    depth_ws.onopen = function(e){
        console.log("连接服务器成功");
        
        for(var item in sub_obj){
          depth_ws.send(JSON.stringify(sub_obj[item]))
        }
        if(depth_ping_time_id)clearInterval(depth_ping_time_id);
        depth_ping_time_id = setInterval(function(){
          if(depth_ws != null)
            depth_ws.send(JSON.stringify({ping:0}));
          },
        5000);
        depth_reset_close_time();
    }
    depth_ws.onclose = function(e){
        console.log("服务器关闭");
        depth_reconnect_websocket();
    }
    depth_ws.onerror = function(){
        console.log("连接出错");
        //reconnect_websocket();
    }
    depth_ws.onmessage = function(e){
        depth_reset_close_time();
        var json_obj = JSON.parse(e.data);
        //console.log(json_obj)
        if("pong" in json_obj){
          return;
        }
        _this.depth_sell_list_item[json_obj.market]=json_obj.forsell.slice(0,7).reverse();
        for(var i = 0; i < _this.depth_sell_list_item[json_obj.market].length;i++){
          _this.depth_sell_list_item[json_obj.market][i][0] = _this.depth_sell_list_item[json_obj.market][i][0].toString();
          _this.depth_sell_list_item[json_obj.market][i][1] = _this.depth_sell_list_item[json_obj.market][i][1].toString();
        }
        _this.depth_buy_list_item[json_obj.market]=json_obj.forbuy.slice(0,7).reverse();
        var depth_all=[];
        let tmp_depth_sell_list=[];
        
        
        //卖部分
        for(var market_idx = 0; market_idx < 3; market_idx++){
          for(var i = 0; i < _this.depth_sell_list_item[market_idx].length; i++){
            var finded = false;
            for(var j = 0; j < tmp_depth_sell_list.length; j++){
              if(parseFloat(_this.depth_sell_list_item[market_idx][i][0]) == parseFloat(tmp_depth_sell_list[j][0])){
                finded = true;
                tmp_depth_sell_list[j][1] = (parseFloat(tmp_depth_sell_list[j][1])+parseFloat(_this.depth_sell_list_item[market_idx][i][1])).toString().slice(0,10);
                break;
              }
            }
            if(!finded){
              tmp_depth_sell_list.push([_this.depth_sell_list_item[market_idx][i][0],_this.depth_sell_list_item[market_idx][i][1]]);
            }
          }
        }
        tmp_depth_sell_list=tmp_depth_sell_list.sort(function(a,b){
            return parseFloat(a[0])-parseFloat(b[0]);
        }).reverse();
        //console.log(tmp_depth_sell_list);
        while(tmp_depth_sell_list[tmp_depth_sell_list.length-1][0] == 0){
          //console.log("===========");
          tmp_depth_sell_list.pop();
        }
          
        tmp_depth_sell_list = tmp_depth_sell_list.reverse().slice(0,7).reverse();
        _this.depth_sell_list = tmp_depth_sell_list

        //买部分
        
        _this.depth_buy_list=[];
        for(var market_idx = 0; market_idx < 3; market_idx++){
          for(var i = 0; i < _this.depth_buy_list_item[market_idx].length; i++){
            var finded = false;
            for(var j = 0; j < _this.depth_buy_list.length; j++){
              if(_this.depth_buy_list_item[market_idx][i][0] == _this.depth_buy_list[j][0]){
                finded = true;
                
                _this.depth_buy_list[j][1]=parseFloat(_this.depth_buy_list[j][1])+parseFloat(_this.depth_buy_list_item[market_idx][i][1]);
                break;
              }
            }
            if(!finded){
              _this.depth_buy_list.push([_this.depth_buy_list_item[market_idx][i][0],_this.depth_buy_list_item[market_idx][i][1]]);
            }
          }
        }

        _this.depth_buy_list=_this.depth_buy_list.sort(function(a,b){
            return parseFloat(b[0])-parseFloat(a[0]);
        }).slice(0,7);
        //console.log(_this.depth_sell_list)
        
        //depth_buy_list_item
        
    }
}
function depth_reconnect_websocket(){
  if(depth_disconnected)return;
  if(depth_time_id){
    clearTimeout(depth_time_id);
    depth_time_id = null;
  }
  depth_time_id = setTimeout(function () {
　　　　// f1的任务代码
　　　　depth_connect_websocket(depth_coin);
　　  }, 5000);
}
function depth_discnnect_websocket(){
  console.log("关闭连接");
  depth_disconnected = true;
  if(depth_time_id != null){
    clearTimeout(depth_time_id)
    depth_time_id = null;
  }
  if(depth_ping_time_id != null){
    clearInterval(depth_ping_time_id);
    depth_ping_time_id = null;
  }
  if(depth_close_time){
    clearTimeout(depth_close_time);
    depth_close_time = null;
  }
  if(depth_ws != null){
    depth_ws.close();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss" scoped>
@import "../../../style/index.scss";
.TranslateDepth{
  border:1px solid rgb(215,215,215);
  border-radius:8px;
  padding:17px; 
}
.buy{
  
  color:$green;
} 
.sell{
  
  color:$red;
}
.depth_item_left{
  font-size:13px;
  text-align:left;
}
.depth_item_right{
  font-size:13px;
  text-align:right;
}
</style>
