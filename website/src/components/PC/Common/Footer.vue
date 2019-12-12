<template>
  <div class="Footer">
    <div class = "container clearfix">
      <div class = "left ">
        <div class="title">特别鸣谢</div>
        <div class="clearfix">
          <a href="https://www.jinse.com" target="_blank" class="left">金色财经</a>
          <a href="https://www.8btc.com" target="_blank" class="left">巴比特</a>
          <a href="https://www.55coin.com" target="_blank" class="left">区势传媒</a>
          <a href="http://www.lianxiang.cc" target="_blank" class="left">链向财经</a>
          <a href="https://www.chainnews.com" target="_blank" class="left">链闻</a>
          <a href="https://www.tuoluocaijing.cn" target="_blank" class="left">陀螺财经</a>
        </div>
        <div class="title ">网站全部源码</div>
        <div class="clearfix">
          <a href="https://github.com/lihn1987/CoinCollector" target="_blank" class="left">https://github.com/lihn1987/CoinCollector</a>
        </div>
      </div>
      <div class = "right">
        <div class="title">联系我</div>
        <div class="clearfix">
          <a class="left">邮件:lihn1011@163.com</a>
        </div>
        <div class="clearfix">
          <a class="left">QQ:253233383</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Footer',
  data () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss" scoped>
@import "../../../style/index.scss";
  .Footer {
    background-color:rgb(49,45,55);
  }
  .container {
    margin: 0 auto;
    padding:24px;
    width:$content_width;
    box-sizing: border-box;
  }
  .title {
    text-align: left;
    color:#ffffff;
    padding:8px;
  }
  a{
    text-align: left;
    text-decoration:none;
    color:$green;
    margin:8px;
  }
</style>
