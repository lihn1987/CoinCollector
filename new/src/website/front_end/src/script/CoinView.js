import axios from 'axios'
export default {
  name: 'HelloWorld',
  data () {
    return {
      coin_list: [],
      current_base_coin:'',
      current_order_coin:'',
      coin_info: {
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
    }, 100);
  },
  destroyed: function () {

  },
  methods: {
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
        console.log(result);
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
    OnSetCoinList(){
      var that = this;
      this.$prompt('请输入币种列表,例如([["BTC","USDT"],["ETH","USDT"]])', '配置币种', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
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
      var coin_pair = selection.coin_pair.split("-");
      this.current_order_coin = coin_pair[0]
      this.current_base_coin = coin_pair[1]
      this.FlushSymbol(coin_pair[0], coin_pair[1])
    },
    FlushSymbol(order_coin, base_coin){
      var that = this;
      axios.get('/coin_view/get_symbol.php?market=huobi&order_coin='+order_coin+'&base_coin='+base_coin).then(function (response) {
        var result = response.data
        //console.log(result)
        if(result.result == true){
          that.coin_info = result.data;
          console.log(that.coin_info)
          console.log(that.coin_info["order_coin"])
        }

      }).catch(function (error) {
        console.log(error)
      })
    }
  }
}