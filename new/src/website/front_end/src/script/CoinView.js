import axios from 'axios'
export default {
  name: 'HelloWorld',
  data () {
    return {
      coin_list: [],                    //币种列表
      current_base_coin:'',             //当前展示的基础币种
      current_order_coin:'',            //当前展示的交易币种
      coin_info: {                      //当前币种信息
        order_coin:'aaaa',
        price_precision:'',
        amount_precision:'',
        symbol_partition:'',
        symbol:'',
        state:'',
        value_precision:'',
        limit_order_min_order_amt:'',
        limit_order_max_order_amt:'',
        sell_market_min_order_amt:'',
        sell_market_max_order_amt:'',
        buy_market_max_order_value:'',
        min_order_value:'',
        max_order_value:'',
      },
      now_balance:0,                  //当前币种持仓
      pre_profit:[],
      active_right_pan:'first',
      buy_depth:[["0","0"],["1","0"],["2","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]],
      sell_depth:[["0","0"],["1","0"],["2","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]],
    }
  },
  mounted: function () {
    let that = this
    this.FlushCoinList()
    setInterval(() => {
      that.FlushDepth();
      that.FlushPreProfit()
      that.FlushCurrentBalance()
    }, 1000);
  },
  destroyed: function () {

  },
  methods: {
    FlushCurrentBalance(){
      var that = this;
      console.log("FlushCurrentBalance")
      axios.get('/coin_view/get_balance.php?market=huobi&coin='+this.current_order_coin, {
      }).then(function (response) {
        var result = response.data
        console.log(result)
        that.now_balance = result["data"]
      }).catch(function (error) {
        console.log(error)
      })
    },
    FlushCoinList(){
      var that = this;
      axios.get('/coin_view/get_coin_list.php?market=huobi', {
        method: 'get_overview'
      }).then(function (response) {
        var result = response.data
        var coin_list = []

        for(var i = 0; i < result.data.length; i++){
          coin_list.push({
            coin_pair: result.data[i][0]+"-"+result.data[i][1],
            coin_price: '000'
          })
        }
        coin_list = coin_list.sort(function(a,b){return a.coin_pair.localeCompare(b.coin_pair)})
        that.coin_list = coin_list;
        that.$nextTick(()=>{
          that.$refs.coin_list_table.setCurrentRow(that.coin_list[0]);
          
        })
      }).catch(function (error) {
        console.log(error)
      })
    },
    FlushDepth(){
      var that = this
      axios.get('/coin_view/get_depth.php?market=huobi&order_coin='+this.current_order_coin+'&base_coin='+this.current_base_coin, {
        method: 'get_overview'
      }).then(function (response) {
        var result = response.data
        if(result && result["result"] == true){
          //刷新币种列表
          for(var i = 0; i < that.buy_depth.length; i++){
            that.$set(that.buy_depth, i, result.data.forbuy[i]) 
          }
          for(var i = 0; i < that.sell_depth.length; i++){
            that.$set(that.sell_depth, i, result.data.forsell[i]) 
          }
        }else{
          console.log("深度获取失败")
        }

      }).catch(function (error) {
        console.log("深度获取异常")
      })
    },
    FlushPreProfit(){
      var that = this
      axios.get('/coin_view/get_quantitative_haigui.php?market=huobi&order_coin='+this.current_order_coin+'&base_coin='+this.current_base_coin, {
        method: 'get_quantitative_haigui'
      }).then(function (response) {
        var result = response.data
        if(result && result["result"] == true){
          //刷新币种列表
          that.pre_profit = []
          for(var key in  result["data"]){
            result["data"][key]["kline_type"] = key
            result["data"][key]["max_profit"] = parseFloat(result["data"][key]["max_profit"]).toFixed(2)
            result["data"][key]["best_buy_point"] = parseFloat(result["data"][key]["best_buy_point"]).toFixed(2)
            result["data"][key]["best_sell_point_low"] = parseFloat(result["data"][key]["best_sell_point_low"]).toFixed(2)
            result["data"][key]["best_sell_point_hight"] = parseFloat(result["data"][key]["best_sell_point_hight"]).toFixed(2)
            result["data"][key]["normal_profit"] = (parseFloat(result["data"][key]["normal_profit"])*100+100).toFixed(2)
            that.pre_profit.push(
              result["data"][key]
            )
          }
          
        }else{
          console.log("深度获取失败")
        }

      }).catch(function (error) {
        console.log("深度获取异常")
      })
    },
    OnSetCoinList(){
      var that = this;
      this.$prompt('请输入币种列表,例如([["BTC","USDT"],["ETH","USDT"]])', '配置币种', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputValue:'[["BTC","USDT"],["ETH","USDT"]]'
      }).then(({ value }) => {
        axios.get('/coin_view/set_coin_list.php?market=huobi&coin_list='+value, {
          method: 'get_overview'
        }).then(function (response) {
          var result = response.data
          if(result && result["result"] == true){
            //刷新币种列表
            that.$nextTick(() => {
              that.FlushCoinList()
              
            })
          }else{
            this.$alert('币种设置失败，请检查格式', '错误', {
              confirmButtonText: '确定'
            });
          }
  
        }).catch(function (error) {
          console.log(error)
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消输入'
        });       
      });
    },
    OnCoinListSelectChange(selection){
      console.log("OnCoinListSelectChange")
      if(selection != null){
        var coin_pair = selection.coin_pair.split("-");
        this.current_order_coin = coin_pair[0]
        this.current_base_coin = coin_pair[1]
        this.FlushSymbol(coin_pair[0], coin_pair[1])
      }
    },
    FlushSymbol(order_coin, base_coin){
      var that = this;
      axios.get('/coin_view/get_symbol.php?market=huobi&order_coin='+order_coin+'&base_coin='+base_coin).then(function (response) {
        var result = response.data
        //console.log(result)
        if(result.result == true){
          that.coin_info = result.data;
        }

      }).catch(function (error) {
        console.log(error)
      })
    }
  }
}