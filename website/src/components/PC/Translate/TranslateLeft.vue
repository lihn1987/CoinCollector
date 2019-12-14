<template>
  <div class="TranslateLeft">
      <div class="row_title clearfix">
          <div class="col1 left">
            币对
          </div>
          <div class="col2 left">
            当前价
          </div>
          <div class="col3 left">
            涨幅
          </div>
        </div>
      <div v-for="n in pair.length" v-on:click="ClickPair(pair[n-1].order,pair[n-1].base)">
        <div class="row_item clearfix" v-bind:class="{row_active:(current_pair==pair[n-1].order+'/'+pair[n-1].base)}">
          <div class="col1 left">
            {{pair[n-1].order}}/{{pair[n-1].base}}
          </div>
          <div class="col2 left">
            {{pair[n-1].price}}
          </div>
          <div class="col3 left" v-bind:class="{red:pair[n-1].change_persent<0,  green:pair[n-1].change_persent >= 0 }">
            {{pair[n-1].change_persent}}%
          </div>
        </div>
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
import {server_config} from '../../../config/server_config.js'
import axios from "axios"
var _this=null;
var flush_timer = null;
export default {
  name: 'TranslateLeft',
  created: function(){
    _this = this;
    flush_timer = setInterval(flush, 1000);
    flush();
  },destroyed: function(){
    if(flush_timer){
      clearInterval(flush_timer);
      flush_timer = null;
    }
  },methods:{
    ClickPair :function(order, base){
      //console.log(order+base);
      this.bus.$emit('current_coin_change', order+"/"+base);
      this.current_pair = order+"/"+base;
    }
  },
  data () {
    return {
      pair:[
        {"order":"BTC", "base":"USDT","price":"0","change_persent":"+88.88"},
        {"order":"ETH", "base":"USDT","price":"0","change_persent":"-88.88"},
        {"order":"XRP", "base":"USDT","price":"0","change_persent":"+88.88"},
        {"order":"BCH", "base":"USDT","price":"0","change_persent":"-88.88"},
        {"order":"LTC", "base":"USDT","price":"0","change_persent":"+88.88"},
        {"order":"EOS", "base":"USDT","price":"0","change_persent":"-88.88"},
        {"order":"BSV", "base":"USDT","price":"0","change_persent":"+88.88"},
        {"order":"XLM", "base":"USDT","price":"0","change_persent":"-88.88"},
        {"order":"TRX", "base":"USDT","price":"0","change_persent":"+88.88"},
        {"order":"ADA", "base":"USDT","price":"0","change_persent":"-88.88"},
      ],
      current_pair : "BTC/USDT",
      msg: 'Welcome to Your Vue.js App'
    }
  }
}

function flush(){
    try{
      var symbol = "";
      for(var i=0;i<_this.pair.length;i++){
        symbol+=_this.pair[i].order.toLowerCase()+"_"+_this.pair[i].base.toLowerCase()+"|";
      }
      symbol = symbol.slice(0, symbol.length-1);
      var url = server_config.url+"/back/getprice.php?symbel="+symbol;
      axios.get(
        url,
        {
        method:'get',
        withCredentials:false,
      }).then( (response) => {
        var json_obj = response.data["data"];
        for(var i = 0; i < json_obj.length; i++){
          var coin_name = json_obj[i]["coin"];
          var index = -1;
          var coin_name_pair = coin_name.split("_");

          for(var j = 0; j < _this.pair.length; j++){
              if(_this.pair[j].order == coin_name_pair[0] &&
              _this.pair[j].base == coin_name_pair[1]){
                var item = {};
                item.order=_this.pair[j].order;
                item.base=_this.pair[j].base;
                item.price=json_obj[i]["close"];
                item.change_persent=((json_obj[i]["close"]-json_obj[i]["open"])/json_obj[i]["open"]*100).toString().slice(0,5);
                _this.$set(_this.pair, j, item);
                break;
              }
          }
        }
      })
      .catch( (error) => {
        console.log(error)
      });
    }catch(e){}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss" scoped>
@import "../../../style/index.scss";
.TranslateLeft{
  border:1px solid rgb(215,215,215);
  border-radius:8px;
  padding:17px; 
}
.col{
  font-size:13px;
}
.col1{
  @extend .col ;
  width:68px;
  text-align-last: left;
}
.col2{
  @extend .col ;
  width:98px;
  text-align-last: right;
}
.col3{
  @extend .col ;
  width:98px;
  text-align-last: right;
  font-weight: 600;
}
.row_title{

}
.row_item{
  padding:8px 0;
  
}
.row_active{
  border-left:4px solid $green;
  margin-left:-18px;
  padding-left:14px;
  margin-right:-18px;
  background:$gray-back;
}
.green{
  color:$green;
}
.red{
  color:$red;
  
}
</style>
