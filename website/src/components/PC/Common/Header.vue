<template>
  <div class="Header ">
    <div class="content clearfix">
      <a href="/" class="logo left">{{main_name}}</a>
      <a href="/news" class="item right" :class="{ item_active: current==4 }">{{new_name}}</a>
      <!-- <a href="/stone" class="item right" :class="{ item_active: current==3 }">{{stone_name}}</a> -->
      <a href="/coin" class="item right" :class="{ item_active: current==2 }">{{coin_name}}</a>
      <a href="/" class="item right" :class="{ item_active: current==1 }">{{page_home}}</a>
    </div>
    <div class="content clearfix" >
      <div class="clearfix left price_left" v-bind:class="{price_up:(btc_percent>0),price_down:(btc_percent<0)}">
        <div class="left">BTC:</div>
        <div class="left">{{btc_price}}</div>
        <div class="left">{{btc_dir}}</div>
        <div class="left">{{btc_percent}}</div>
      </div>
      <div class="clearfix left price_mid" v-bind:class="{price_up:(eth_percent>0),price_down:(eth_percent<0)}">
        <div class="left ">ETH:</div>
        <div class="left">{{eth_price}}</div>
        <div class="left">{{eth_dir}}</div>
        <div class="left">{{eth_percent}}</div>
      </div>
      <div class="clearfix left price_mid" v-bind:class="{price_up:(eos_percent>0),price_down:(eos_percent<0)}">
        <div class="left">EOS:</div>
        <div class="left">{{eos_price}}</div>
        <div class="left">{{eos_dir}}</div>
        <div class="left">{{eos_percent}}</div>
      </div>
      <div class="clearfix left price_right" v-bind:class="{price_up:(xrp_percent>0),price_down:(xrp_percent<0)}">
        <div class="left">XRP:</div>
        <div class="left">{{xrp_price}}</div>
        <div class="left">{{xrp_dir}}</div>
        <div class="left">{{xrp_percent}}</div>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import axios from "axios"
import {server_config} from '../../../config/server_config.js'
var _this = null;
var flush_timer = null;
export default {
  name: 'Header',
  props:{
    current: Number
  },
  data () {
    return {
      main_name: '小站',
      page_home: '首页',
      coin_name: '币圈数据分析',
      stone_name: '股票数据分析',
      new_name: '最新动态',
      btc_price:'11111111',
      eth_price:'-2222222',
      eos_price:'3333333',
      xrp_price:'66666666',

      btc_dir:'↑',
      eth_dir:'↑',
      eos_dir:'↑',
      xrp_dir:'↑',

      btc_percent:'80.88%',
      eth_percent:'80.33%',
      eos_percent:'-80.88%',
      xrp_percent:'-80.88%',
      
    }
  },created: function(){
    _this = this;
    flush_timer = setInterval(flush_top, 1000);
    flush_top();
  },destroyed: function(){
    if(flush_timer){
      clearInterval(flush_timer);
      flush_timer = null;
    }
  },
}
function flush_top(){
var url = server_config.url+"/back/getprice.php?symbel=btc_usdt|eth_usdt|eos_usdt|xrp_usdt";
    axios.get(
      url,
      {
      method:'get',
      withCredentials:false,
    })
    .then( (response) => {
      console.log(response.data);
      var json_obj = response.data["data"];
      for(var i = 0; i < json_obj.length; i++){
        switch(json_obj[i]["coin"]){
          case "BTC_USDT":
            _this.btc_price = json_obj[i]["close"].toString().slice(0,8);
            _this.btc_percent = ((json_obj[i]["close"]-json_obj[i]["open"])/json_obj[i]["open"]*100).toString().slice(0,5);
            _this.btc_dir = (json_obj[i]["close"]-json_obj[i]["open"] > 0)?"↑":"↓";
            break;
          case "ETH_USDT":
            _this.eth_price = json_obj[i]["close"].toString().slice(0,8);
            _this.eth_percent = ((json_obj[i]["close"]-json_obj[i]["open"])/json_obj[i]["open"]*100).toString().slice(0,5);
            _this.eth_dir = (json_obj[i]["close"]-json_obj[i]["open"] > 0)?"↑":"↓";
            break;
          case "EOS_USDT":
            _this.eos_price = json_obj[i]["close"].toString().slice(0,8);
            _this.eos_percent = ((json_obj[i]["close"]-json_obj[i]["open"])/json_obj[i]["open"]*100).toString().slice(0,5);
            _this.eos_dir = (json_obj[i]["close"]-json_obj[i]["open"] > 0)?"↑":"↓";
            break;
          case "XRP_USDT":
            _this.xrp_price = json_obj[i]["close"].toString().slice(0,8);
            _this.xrp_percent = ((json_obj[i]["close"]-json_obj[i]["open"])/json_obj[i]["open"]*100).toString().slice(0,5);
            _this.xrp_dir = (json_obj[i]["close"]-json_obj[i]["open"] > 0)?"↑":"↓";
            break;
        }
        console.log(json_obj[i]);
      }
    })
    .catch( (error) => {
      console.log(error)
    });
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss" scoped>
@import "../../../style/index.scss";
$header_height: 76px;
.Header {
  background:#ffffff;
  box-shadow: 0 2px 4px 0px;
  position:relative;
  z-index: 1;
}
.content {
  margin:0 auto;
  width: $content_width ;
}
.logo {
  line-height:$header_height;
  font-size:14px;
  color:rgb(74, 74, 74);
  text-decoration:none;
}
.item {
  line-height:$header_height;
  font-size:14px;
  color:rgb(74, 74, 74);
  margin-left:120px;
  text-decoration:none;
}
.item_active{
  color:rgb(95,188,118);;
}
.price_item{
  font-size:14px;
}
.price_up{
  @extend .price_item ;
  color:$green;
}
.price_down{
  @extend .price_item ;
  color:$red;
}
$margin_mid:1px;
$width: ( $content_width - 4 - ( $margin_mid * 3 ) ) / 4;
.price{
  text-align: center;
  margin:0 90px;
  font-weight: 800;
}
.price_left{
  @extend .price ;
  //margin-left:0px;
}
.price_right{
  @extend .price ;
  //margin-right:0px;
}
.price_mid{
  @extend .price ;
  //margin: 0 $margin_mid;
}
</style> 
