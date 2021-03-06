import axios from 'axios'
export default {
  name: 'HelloWorld',
  data () {
    return {
      main_tb_index:"1",
      config:[{
          name:"1",
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
          }
        },{
          name:"2",
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
          }
        }
      ],
      history:[{
        data_list:[
          /*
        "coin_order"
        "coin_base"
        "dir"
        "profit"
        "amount"
        "timestamp"
          */
        ],
        page_size:0,
        page_index:0,
      },{
        data_list:[
          /*
        "coin_order"
        "coin_base"
        "dir"
        "profit"
        "amount"
        "timestamp"
          */
        ],
        page_size:0,
        page_index:0,
      }
      ]
    }
  },
  mounted: function () {
    let that = this
    this.FlushProfit()
    this.FlushProfitNow()
    that.FlushHistory()
    setInterval(() => {
      that.FlushProfit()
      that.FlushProfitNow()
      that.FlushHistory()
    }, 5000);
  },
  destroyed: function () {

  },
  methods: {
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
      })
    },
    //刷新当前持仓
    FlushProfitNow(){
      let that = this
      axios.post("/coin_view/get_profit_now.php").then(function(result){
        for(var i = 0; i < 2; i++){
          that.config[0].profit_now.amount_sum = parseFloat(0)
          that.config[0].profit_now.profit_sum = parseFloat(0)
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
      axios.post("/coin_view/get_history.php?tag=huobi_1&page_index="+this.history[0].page_index).then(function(result){
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
      axios.post("/coin_view/get_history.php?tag=huobi_2&page_index="+this.history[1].page_index).then(function(result){
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
    }
  }
}