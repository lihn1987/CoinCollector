<template>
  <div>
    <div class="title">分析</div>
    <div class = "depth clearfix">
      <div class="left" v-for="n in 3" v-bind:class="{depth_item1:n==1,depth_item2:n==2,depth_item3:n==3}">
        <div>
          最近10分钟多空情况
        </div>
        <div class="clearfix">
        <div class = "buy left">买入总数:{{min_amount[n-1][0]}}</div>
        <div class = "sell left">卖出总数:{{min_amount[n-1][1]}}</div>
        </div>
        <div class="clearfix">
        <div class = "buyscale left" style="background:#00ff00;"  v-bind:style="{width: min_buy_width[n-1] + '%' }"></div>
        <div class = "sellscale left" style="background:#ff0000;" v-bind:style="{width: 100-min_buy_width[n-1] + '%' }"></div>
        </div>

        <div>
          最近1小时多空情况
        </div>
        <div class="clearfix">
        <div class = "buy left">买入总数:{{hour_amount[n-1][0]}}</div>
        <div class = "sell left">卖出总数:{{hour_amount[n-1][1]}}</div>
        </div>
        <div class="clearfix">
        <div class = "buyscale left" style="background:#00ff00;"  v-bind:style="{width: hour_buy_width[n-1] + '%' }"></div>
        <div class = "sellscale left" style="background:#ff0000;" v-bind:style="{width: 100-hour_buy_width[n-1] + '%' }"></div>
        </div>

        <div>
          最近1天多空情况
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
  </div>
</template>
<script> 
import Vue from 'vue'

import {server_config} from '../../../../config/server_config.js'
import axios from "axios"
var _this = '';
var huobi_timer = null;
var ok_timer = null;
export default {
  name: 'Main',
  props:{
    id: String
  },
  data () {
    return {
      min_amount:[[0,0],[0,0],[0,0]],
      min_buy_width:[100,100,100],
      hour_amount:[[0,0],[0,0],[0,0]],
      hour_buy_width:[100,100,100],
      day_amount:[[0,0],[0,0],[0,0]],
      day_buy_width:[100,100,100],
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
          huobi_timer = setInterval(function(){get_huobi(response.data);},1000);
          ok_timer = setInterval(function(){get_ok(response.data);},1000);
        })
        .catch( (error) => {

        });
        
    }
  },destroyed: function(){
    clearInterval(huobi_timer);
    clearInterval(ok_timer);
  },methods:{
    
  }
}

function get_huobi(order_coin){
    var url = server_config.url+"/back/gettradeinfo.php?market=0&order_coin="+order_coin+"&base_coin=USDT&second=600";
    axios.get(
      url,
      {
      method:'get',
      withCredentials:false,
    })
    .then( (response) => {
      var json_obj = response.data;
      _this.$set(_this.min_amount[0],0,json_obj["buy_count"].slice(0,10));
      _this.$set(_this.min_amount[0],1,json_obj["sell_count"].slice(0,10));
      _this.$set(_this.min_buy_width, 0, parseFloat(json_obj["buy_count"])/(parseFloat(json_obj["buy_count"])+parseFloat(json_obj["sell_count"]))*100);
    })
    .catch( (error) => {

    });
    url = server_config.url+"/back/gettradeinfo.php?market=0&order_coin="+order_coin+"&base_coin=USDT&second=3600";
    axios.get(
      url,
      {
      method:'get',
      withCredentials:false,
    })
    .then( (response) => {
      var json_obj = response.data;
      _this.$set(_this.hour_amount[0],0,json_obj["buy_count"].slice(0,10));
      _this.$set(_this.hour_amount[0],1,json_obj["sell_count"].slice(0,10));
      _this.$set(_this.hour_buy_width, 0, parseFloat(json_obj["buy_count"])/(parseFloat(json_obj["buy_count"])+parseFloat(json_obj["sell_count"]))*100);
    })
    .catch( (error) => {

    });
    url = server_config.url+"/back/gettradeinfo.php?market=0&order_coin="+order_coin+"&base_coin=USDT&second=86400";
    axios.get(
      url,
      {
      method:'get',
      withCredentials:false,
    })
    .then( (response) => {
      var json_obj = response.data;
      _this.$set(_this.day_amount[0],0,json_obj["buy_count"].slice(0,10));
      _this.$set(_this.day_amount[0],1,json_obj["sell_count"].slice(0,10));
      _this.$set(_this.day_buy_width, 0, parseFloat(json_obj["buy_count"])/(parseFloat(json_obj["buy_count"])+parseFloat(json_obj["sell_count"]))*100);
    })
    .catch( (error) => {

    });
}
function get_ok(order_coin){
    var url = server_config.url+"/back/gettradeinfo.php?market=1&order_coin="+order_coin+"&base_coin=USDT&second=600";
    axios.get(
      url,
      {
      method:'get',
      withCredentials:false,
    })
    .then( (response) => {
      var json_obj = response.data;
      _this.$set(_this.min_amount[1],0,json_obj["buy_count"].slice(0,10));
      _this.$set(_this.min_amount[1],1,json_obj["sell_count"].slice(0,10));
      _this.$set(_this.min_buy_width, 1, parseFloat(json_obj["buy_count"])/(parseFloat(json_obj["buy_count"])+parseFloat(json_obj["sell_count"]))*100);
    })
    .catch( (error) => {
    });
    var url = server_config.url+"/back/gettradeinfo.php?market=1&order_coin="+order_coin+"&base_coin=USDT&second=3600";
    axios.get(
      url,
      {
      method:'get',
      withCredentials:false,
    })
    .then( (response) => {
      var json_obj = response.data;
      _this.$set(_this.hour_amount[1],0,json_obj["buy_count"].slice(0,10));
      _this.$set(_this.hour_amount[1],1,json_obj["sell_count"].slice(0,10));
      _this.$set(_this.hour_buy_width, 1, parseFloat(json_obj["buy_count"])/(parseFloat(json_obj["buy_count"])+parseFloat(json_obj["sell_count"]))*100);
    })
    .catch( (error) => {
    });
    var url = server_config.url+"/back/gettradeinfo.php?market=1&order_coin="+order_coin+"&base_coin=USDT&second=86400";
    axios.get(
      url,
      {
      method:'get',
      withCredentials:false,
    })
    .then( (response) => {
      var json_obj = response.data;
      _this.$set(_this.day_amount[1],0,json_obj["buy_count"].slice(0,10));
      _this.$set(_this.day_amount[1],1,json_obj["sell_count"].slice(0,10));
      _this.$set(_this.day_buy_width, 1, parseFloat(json_obj["buy_count"])/(parseFloat(json_obj["buy_count"])+parseFloat(json_obj["sell_count"]))*100);
    })
    .catch( (error) => {
    });
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
</style>
