<template>
  <div>
    <div class="title">火币行情</div>
    
  </div>
</template>
<script> 
import Vue from 'vue'

import {server_config} from '../../../../config/server_config.js'
export default {
  name: 'Main',
  data () {
    return {
    }
  },
  created: function(){
    if(window.WebSocket){
            var ws = new WebSocket('wss://api.huobi.pro/ws');
            ws.onopen = function(e){
                console.log("连接服务器成功");
                ws.send("game1");
            }
            ws.onclose = function(e){
                console.log("服务器关闭");
            }
            ws.onerror = function(){
                console.log("连接出错");
            }
            ws.onmessage = function(e){
                mess.innerHTML = "连接成功";
                console.log(e.data);
                /*document.querySelector(".kuang").onclick = function(e){
                    var time = new Date();
                    ws.send(time + "  game1点击了“" + e.target.innerHTML+"”");
                }*/
            }
        }
  },methods:{
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

</style>
