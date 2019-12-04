<template>
  <div class="Body">
    <div class="body_content">
      <h1>最后更新时间</h1>
      <p>2019年12月3日</p>
      <h1>已完成的工作</h1>
      <h2>网页抓取部分</h2>
      <p>已抓取的新闻网站:金色财经,巴比特,区势传媒,链向财经,链闻,陀螺财经</p>
      <p>已分析的内容：通过分词，将新闻归类的各个币种中</p>
      <h2>交易所信息采集</h2>
      <h3>火币</h3>
      <p>已采集币种:("BTC", "USDT"),("ETH", "USDT"),("XRP", "USDT"),("BCH", "USDT"),("LTC", "USDT"),("EOS", "USDT"),("BSV", "USDT"),("XLM", "USDT"),("TRX", "USDT"),("ADA", "USDT")</p>
      <p>已采集内容:交易详情，深度信息</p>
      <p>已分析的内容:按照分钟，小时，天统计多空比</p>
      <h3>OK</h3>
      <p>已采集币种:("BTC", "USDT"),("ETH", "USDT"),("XRP", "USDT"),("BCH", "USDT"),("LTC", "USDT"),("EOS", "USDT"),("BSV", "USDT"),("XLM", "USDT"),("TRX", "USDT"),("ADA", "USDT")</p>
      <p>已采集内容:交易详情，深度信息</p>
      <p>已分析的内容:按照分钟，小时，天统计多空比</p>
      <h3>币安</h3>
      <p>已采集币种:("BTC", "USDT"),("ETH", "USDT"),("XRP", "USDT"),("BCH", "USDT"),("LTC", "USDT"),("EOS", "USDT"),("BSV", "USDT"),("XLM", "USDT"),("TRX", "USDT"),("ADA", "USDT")</p>
      <p>已采集内容:交易详情，深度信息</p>
      <p>已分析的内容:按照分钟，小时，天统计多空比</p>
      <h1>更新日志</h1>
      <h2>2019年12月4日</h2>
      <p>增加了陀螺财经新闻的抓取</p>
      <h2>2019年12月4日</h2>
      <p>增加稳定性:解决服务端websocket服务器内存爆炸的问题，以及客户端websocket重连机制的问题，去除了vue的#</p>
      <h2>2019年12月3日</h2>
      <p>最最基础的简陋到丑陋的版本上线，包括手机版</p>
    </div>
  </div>
</template>

<script>

export default {
  name: 'ErrorBody',
  data () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../style/index.scss";
.Body{
  width:$content-width;
  margin:0 auto;
}
h1,h2,h3,h4,p{
  text-align:left;
}
</style>
