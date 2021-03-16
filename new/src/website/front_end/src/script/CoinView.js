import axios from 'axios'
var echarts = require('echarts');
var _this = null;
export default {
  name: 'HelloWorld',
  data () {
    return {
      main_tb_index:"1",
      config:[{
          name:"1",
          lbl:"火币账户1",
          amount_balance:0,
          profit_history:{
            detail:[],
            amount_sum:0,
            profit_sum:0,
            count_sum:0,
          },
          profit_now:{
            detail:[],
            amount_sum:0,
            profit_sum:0,
            count_sum:0,
          },
          statistic:{
            start_time: '',
            statistic_coin:'ALL',
            statistic_type:'1',
          }
        },{
          name:"2",
          lbl:"火币账户2",
          amount_balance:0,
          profit_history:{
            detail:[],
            amount_sum:0,
            profit_sum:0,
            count_sum:0,
          },
          profit_now:{
            detail:[],
            amount_sum:0,
            profit_sum:0,
            count_sum:0,
          },
          statistic:{
            start_time: '',
            statistic_coin:'ALL',
            statistic_type:'1',
          }
        }
      ],
      history:[{
        data_list:[
        ],
        page_size:0,
        page_index:0,
      },{
        data_list:[
        ],
        page_size:0,
        page_index:0,
      }
      ]
    }
  },
  mounted: function () {
    _this = this;
    let that = this
    this.InitStatistic()
    this.FlushProfit()
    this.FlushProfitNow()
    that.FlushHistory()
    that.FlushAmountBalance()
    setInterval(() => {
      that.FlushProfit()
      that.FlushProfitNow()
      that.FlushHistory()
      that.FlushAmountBalance()
    }, 5000);
  },
  destroyed: function () {

  },
  methods: {
    InitStatistic(){
      this.config[0].statistic.start_time = Date.parse(new Date())-1000*60*60*24*7;
      this.config[1].statistic.start_time = Date.parse(new Date())-1000*60*60*24*7;
      this.FlushECharts(1)
      this.FlushECharts(2)
    },
    FlushAmountBalance(){
      axios.post("/coin_view/get_balance_now.php").then(function(result){
        _this.config[0].amount_balance = result.data.data[0]
        _this.config[1].amount_balance = result.data.data[1]
      })
    },
    //刷新今天收益统计
    FlushProfit(){
      let that = this
      axios.post("/coin_view/get_profit.php").then(function(result){
        that.config[0].profit_history.detail = result.data.huobi_main
        that.config[1].profit_history.detail = result.data.huobi_sub1

        for(var i = 0; i < 2; i++){
          that.config[i].profit_history.amount_sum = 0
          that.config[i].profit_history.profit_sum = 0
          that.config[i].profit_history.count_sum = 0
        }
        
        for(var i = 0; i < that.config[0].profit_history.detail.length; i++){
          that.config[0].profit_history.amount_sum += that.config[0].profit_history.detail[i]["amount"]
          that.config[0].profit_history.profit_sum += that.config[0].profit_history.detail[i]["profit"]
          that.config[0].profit_history.count_sum += that.config[0].profit_history.detail[i]["count"]

          that.config[0].profit_history.detail[i]["amount"] = that.config[0].profit_history.detail[i]["amount"].toFixed(2);
          that.config[0].profit_history.detail[i]["profit"] = that.config[0].profit_history.detail[i]["profit"].toFixed(2);
          that.config[0].profit_history.detail[i]["profit_buy"] = that.config[0].profit_history.detail[i]["profit_buy"].toFixed(2);
          that.config[0].profit_history.detail[i]["profit_sell"] = that.config[0].profit_history.detail[i]["profit_sell"].toFixed(2);
        }
        //that.huobi_sub1 = result.data.huobi_sub1
        for(var i = 0; i < that.config[1].profit_history.detail.length; i++){
          that.config[1].profit_history.amount_sum += that.config[1].profit_history.detail[i]["amount"]
          that.config[1].profit_history.profit_sum += that.config[1].profit_history.detail[i]["profit"]
          that.config[1].profit_history.count_sum += that.config[1].profit_history.detail[i]["count"]

          that.config[1].profit_history.detail[i]["amount"] = that.config[1].profit_history.detail[i]["amount"].toFixed(2);
          that.config[1].profit_history.detail[i]["profit"] = that.config[1].profit_history.detail[i]["profit"].toFixed(2);
          that.config[1].profit_history.detail[i]["profit_buy"] = that.config[1].profit_history.detail[i]["profit_buy"].toFixed(2);
          that.config[1].profit_history.detail[i]["profit_sell"] = that.config[1].profit_history.detail[i]["profit_sell"].toFixed(2);
        }
        for(var i = 0; i < 2; i++){
          that.config[i].profit_history.amount_sum = parseFloat(that.config[i].profit_history.amount_sum).toFixed(2)
          that.config[i].profit_history.profit_sum = parseFloat(that.config[i].profit_history.profit_sum).toFixed(2)
          that.config[i].profit_history.count_sum = parseFloat(that.config[i].profit_history.count_sum).toFixed(2)
        }
        //此处开始同步交易进程状态
        for(var i = 0; i < that.config[0].profit_history.detail.length; i++){
          that.config[0].profit_history.detail[i].status="运行"
        }
        for(var i = 0; i < that.config[0].profit_history.detail.length; i++){
          that.config[1].profit_history.detail[i].status="停止"
        }
      })
    },
    //刷新当前持仓
    FlushProfitNow(){
      let that = this
      axios.post("/coin_view/get_profit_now.php").then(function(result){
        for(var i = 0; i < 2; i++){
          that.config[i].profit_now.amount_sum = parseFloat(0)
          that.config[i].profit_now.profit_sum = parseFloat(0)
        }

        that.config[0].profit_now.detail = result.data.huobi_main
        for(var i = 0; i < that.config[0].profit_now.detail.length; i++){
          that.config[0].profit_now.amount_sum += parseFloat(that.config[0].profit_now.detail[i]["position_margin"])
          that.config[0].profit_now.profit_sum += parseFloat(that.config[0].profit_now.detail[i]["profit"])
          that.config[0].profit_now.detail[i]["profit_rate"] = that.config[0].profit_now.detail[i]["profit_rate"]*100
          that.config[0].profit_now.detail[i]["profit_rate"] = that.config[0].profit_now.detail[i]["profit_rate"].toFixed(2)
        }
        that.config[0].profit_now.amount_sum = that.config[0].profit_now.amount_sum.toFixed(2)
        that.config[0].profit_now.profit_sum = that.config[0].profit_now.profit_sum.toFixed(2) 

        that.config[1].profit_now.detail = result.data.huobi_sub1
        for(var i = 0; i < that.config[1].profit_now.detail.length; i++){
          that.config[1].profit_now.amount_sum += parseFloat(that.config[1].profit_now.detail[i]["position_margin"])
          that.config[1].profit_now.profit_sum += parseFloat(that.config[1].profit_now.detail[i]["profit"])
          that.config[1].profit_now.detail[i]["profit_rate"] = that.config[1].profit_now.detail[i]["profit_rate"]*100
          that.config[1].profit_now.detail[i]["profit_rate"] = that.config[1].profit_now.detail[i]["profit_rate"].toFixed(2)
        }
        that.config[1].profit_now.amount_sum = parseFloat(that.config[1].profit_now.amount_sum).toFixed(2)
        that.config[1].profit_now.profit_sum = parseFloat(that.config[1].profit_now.profit_sum).toFixed(2) 
      })
    },
    //刷新历史信息
    FlushHistory(){
      let that = this
      axios.post("/coin_view/get_history.php?tag=huobi_1&page_index="+(this.history[0].page_index-1)).then(function(result){
        that.history[0].data_list = result.data.data
        that.history[0].page_size = parseInt(result.data.page_size)
        for(var i = 0; i < that.history[0].data_list.length; i++){
          switch(that.history[0].data_list[i].dir){
            case "1":that.history[0].data_list[i].dir = "买入开多";break;
            case "2":that.history[0].data_list[i].dir = "卖出开空";break;
            case "3":that.history[0].data_list[i].dir = "买入平空";break;
            case "4":that.history[0].data_list[i].dir = "卖出平多";break;
          }
        }
      })
      axios.post("/coin_view/get_history.php?tag=huobi_2&page_index="+(this.history[1].page_index-1)).then(function(result){
        that.history[1].data_list = result.data.data
        that.history[1].page_size = parseInt(result.data.page_size)
        for(var i = 0; i < that.history[0].data_list.length; i++){
          switch(that.history[0].data_list[i].dir){
            case "1":that.history[0].data_list[i].dir = "买入开多";break;
            case "2":that.history[0].data_list[i].dir = "卖出开空";break;
            case "3":that.history[0].data_list[i].dir = "买入平空";break;
            case "4":that.history[0].data_list[i].dir = "卖出平多";break;
          }
        }
      })
    },
    OnStop(coin_name, index){
      console.log("OnStop", coin_name, index)
    },
    OnLiquidation(coin_name, index){
      console.log("OnLiquidation", coin_name, index)
    },
    OnReset(coin_name, index){
      console.log("OnReset", coin_name, index)
    },
    FlushECharts(n){
      console.log(n)
      let echart_tmp = echarts.init(document.getElementById("echart"+n));
      axios.post("/coin_view/get_statistic_all.php", JSON.stringify(
        {
          data:{
            start_time:_this.config[n-1].statistic.start_time,
            coin_name:_this.config[n-1].statistic.statistic_coin,
            statistic_type:_this.config[n-1].statistic.statistic_type,
            key:"huobi_"+n
          }
        }
      )).then(function(data){
        console.log(data)
        console.log(_this.start_time)
        var result = data.data;
        var x_list = [], y_list = []
        for(var i = 0; i < result.length; i++){
          x_list.push(result[i]["time"])
          switch(_this.config[n-1].statistic.statistic_type){
            case "1":
              y_list.push(result[i]["profit"])
              break;
            case "2":
              y_list.push(result[i]["amount"])
              break;
            case "3":
              y_list.push(result[i]["count"])
              break;
          }
        }
        console.log(x_list)
        console.log(y_list)
        var option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                    type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [
                {
                    type: 'category',
                    data: x_list,
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            yAxis: [
                {
                    type: 'value'
                }
            ],
            series: [
                {
                    name: '值',
                    type: 'bar',
                    barWidth: '60%',
                    data: y_list
                }
            ]
        };
        echart_tmp.setOption(option);
        _this.$nextTick(()=>{
          echart_tmp.resize();
        })
      }).catch(function(){

      });
    }
  }
}