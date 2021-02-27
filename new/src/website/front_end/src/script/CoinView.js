import axios from 'axios'
export default {
  name: 'HelloWorld',
  data () {
    return {
      main_tb_index:"1",
      //历史
      huobi_main:[],
      huobi_main_amount_sum:0,
      huobi_main_profit_sum:0,
      huobi_main_count_sum:0,
      huobi_sub1:[],
      huobi_sub1_amount_sum:0,
      huobi_sub1_profit_sum:0,
      huobi_sub1_count_sum:0,
      //持仓
      huobi_main_now:[],
      huobi_main_now_amount_sum:0,
      huobi_main_now_profit_sum:0,
      huobi_main_now_count_sum:0,
      huobi_sub1_now:[],
      huobi_sub1_now_amount_sum:0,
      huobi_sub1_now_profit_sum:0,
      huobi_sub1_now_count_sum:0
    }
  },
  mounted: function () {
    let that = this
    this.FlushProfit()
    this.FlushProfitNow()
    setInterval(() => {
      that.FlushProfit()
      that.FlushProfitNow()
    }, 5000);
  },
  destroyed: function () {

  },
  methods: {
    FlushProfit(){
      let that = this
      axios.post("/coin_view/get_profit.php").then(function(result){
        that.huobi_main = result.data.huobi_main
        that.huobi_main_amount_sum = 0
        that.huobi_main_profit_sum = 0
        that.huobi_main_count_sum = 0
        that.huobi_sub1_amount_sum = 0
        that.huobi_sub1_profit_sum = 0
        that.huobi_sub1_count_sum = 0
        for(var i = 0; i < that.huobi_main.length; i++){
          that.huobi_main_amount_sum += that.huobi_main[i]["amount"]
          that.huobi_main_profit_sum += that.huobi_main[i]["profit"]
          that.huobi_main_count_sum += that.huobi_main[i]["count"]

          that.huobi_main[i]["amount"] = that.huobi_main[i]["amount"].toFixed(2);
          that.huobi_main[i]["profit"] = that.huobi_main[i]["profit"].toFixed(2);
          that.huobi_main[i]["profit_buy"] = that.huobi_main[i]["profit_buy"].toFixed(2);
          that.huobi_main[i]["profit_sell"] = that.huobi_main[i]["profit_sell"].toFixed(2);
        }
        that.huobi_sub1 = result.data.huobi_sub1
        for(var i = 0; i < that.huobi_sub1.length; i++){
          that.huobi_sub1_amount_sum += that.huobi_sub1[i]["amount"]
          that.huobi_sub1_profit_sum += that.huobi_sub1[i]["profit"]
          that.huobi_sub1_count_sum += that.huobi_sub1[i]["count"]

          that.huobi_sub1[i]["amount"] = that.huobi_sub1[i]["amount"].toFixed(2);
          that.huobi_sub1[i]["profit"] = that.huobi_sub1[i]["profit"].toFixed(2);
          that.huobi_sub1[i]["profit_buy"] = that.huobi_sub1[i]["profit_buy"].toFixed(2);
          that.huobi_sub1[i]["profit_sell"] = that.huobi_sub1[i]["profit_sell"].toFixed(2);
        }

        that.huobi_main_amount_sum = that.huobi_main_amount_sum.toFixed(2)
        that.huobi_main_profit_sum = that.huobi_main_profit_sum.toFixed(2)
        that.huobi_main_count_sum = that.huobi_main_count_sum.toFixed(2)
        that.huobi_sub1_amount_sum = that.huobi_sub1_amount_sum.toFixed(2)
        that.huobi_sub1_profit_sum = that.huobi_sub1_profit_sum.toFixed(2)
        that.huobi_sub1_count_sum = that.huobi_sub1_count_sum.toFixed(2)

      })
    },
    FlushProfitNow(){
      let that = this
      axios.post("/coin_view/get_profit_now.php").then(function(result){
        that.huobi_main_now_amount_sum = 0
        that.huobi_main_now_profit_sum = 0
        that.huobi_main_now_count_sum = 0
        that.huobi_sub1_now_amount_sum = 0
        that.huobi_sub1_now_profit_sum = 0
        that.huobi_sub1_now_count_sum = 0

        that.huobi_main_now = result.data.huobi_main
        for(var i = 0; i < that.huobi_main_now.length; i++){
          that.huobi_main_now_amount_sum += parseFloat(that.huobi_main_now[i]["position_margin"])
          that.huobi_main_now_profit_sum += parseFloat(that.huobi_main_now[i]["profit"])
          that.huobi_main_now[i]["profit_rate"] = that.huobi_main_now[i]["profit_rate"]*100
          that.huobi_main_now[i]["profit_rate"] = that.huobi_main_now[i]["profit_rate"].toFixed(2)
        }
        that.huobi_main_now_amount_sum.toFixed(2)
        that.huobi_main_now_profit_sum.toFixed(2) 

        that.huobi_sub1_now = result.data.huobi_sub1
        for(var i = 0; i < that.huobi_main_now.length; i++){
          that.huobi_sub1_now_amount_sum += parseFloat(that.huobi_sub1_now[i]["position_margin"])
          that.huobi_sub1_now_profit_sum += parseFloat(that.huobi_sub1_now[i]["profit"])
          that.huobi_sub1_now[i]["profit_rate"] = that.huobi_sub1_now[i]["profit_rate"]*100
          that.huobi_sub1_now[i]["profit_rate"] =that.huobi_sub1_now[i]["profit_rate"].toFixed(2)
        }
        that.huobi_sub1_now_amount_sum.toFixed(2)
        that.huobi_sub1_now_profit_sum.toFixed(2) 
        /*that.huobi_sub1 = result.data.huobi_sub1
        for(var i = 0; i < that.huobi_sub1.length; i++){
          that.huobi_sub1_now_amount_sum += that.huobi_sub1_now[i]["amount"]
          that.huobi_sub1_now_profit_sum += that.huobi_sub1_now[i]["profit"]

          that.huobi_sub1_now[i]["amount"] = that.huobi_sub1_now[i]["amount"].toFixed(2);
          that.huobi_sub1_now[i]["profit"] = that.huobi_sub1_now[i]["profit"].toFixed(2);
          that.huobi_sub1_now[i]["profit_buy"] = that.huobi_sub1_now[i]["profit_buy"].toFixed(2);
          that.huobi_sub1_now[i]["profit_sell"] = that.huobi_sub1_now[i]["profit_sell"].toFixed(2);
        }

        that.huobi_main_now_amount_sum = that.huobi_main_now_amount_sum.toFixed(2)
        that.huobi_main_now_profit_sum = that.huobi_main_now_profit_sum.toFixed(2)

        that.huobi_sub1_now_amount_sum = that.huobi_sub1_now_amount_sum.toFixed(2)
        that.huobi_sub1_now_profit_sum = that.huobi_sub1_now_profit_sum.toFixed(2)*/
      })
    }
  }
}