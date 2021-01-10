import axios from 'axios'
export default {
  name: 'HelloWorld',
  data () {
    return {
      coin_list: [],
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
      }
    }
  },
  mounted: function () {
    let that = this
    this.FlushCoinList()
    setInterval(function () {
      that.Flush()
    }, 1000)
  },
  destroyed: function () {

  },
  methods: {
    Flush: function () {
      //alert(111)
      // var that = this
      /* axios.post('/coin_view/overview.php', {
        method: 'get_overview'
      }).then(function (response) {
        var result = response.data
        that.table_data = []
        for (let i = 0; i < result.length; i++) {
          that.table_data.push({
            coin_pair: result[i].order_coin + '-' + result[i].base_coin,
            huobi_lowest_sell: result[i].forsell_HUOBI,
            huobi_highest_buy: result[i].forbuy_HUOBI,
            ok_lowest_sell: result[i].forsell_OK,
            ok_highest_buy: result[i].forbuy_OK,
            huobi_buy_profit: ((result[i].forbuy_HUOBI - result[i].forsell_OK) * 100 / result[i].forbuy_HUOBI).toFixed(2),
            ok_buy_profit: ((result[i].forbuy_OK - result[i].forsell_HUOBI) * 100 / result[i].forbuy_OK).toFixed(2),
            huobi_delay: result[i].delay_HUOBI.toFixed(0),
            ok_delay: result[i].delay_OK.toFixed(0)
          })
        }
        // 计算top10利润
        that.huobi_top = []
        that.ok_top = []
        for (let i = 0; i < that.table_data.length; i++) {
          that.huobi_top.push({
            coin_pair: that.table_data[i].coin_pair,
            profit: that.table_data[i].huobi_buy_profit
          })
          that.ok_top.push({
            coin_pair: that.table_data[i].coin_pair,
            profit: that.table_data[i].ok_buy_profit
          })
        }
        that.huobi_top.sort(function (a, b) {
          return b.profit - a.profit
        })
        that.huobi_top = that.huobi_top.slice(0, 10)

        that.ok_top.sort(function (a, b) {
          return b.profit - a.profit
        })
        that.ok_top = that.ok_top.slice(0, 10)

      }).catch(function (error) {
        console.log(error)
      }) */
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
        console.log(result);
        that.coin_list = coin_list;
        that.$nextTick(()=>{
          that.$refs.coin_list_table.setCurrentRow(that.coin_list[0]);
        })
      }).catch(function (error) {
        console.log(error)
      })
    },
    OnSetCoinList(){
      var that = this;
      this.$prompt('请输入币种列表,例如([["BTC","USDT"],["ETH","USDT"]])', '配置币种', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({ value }) => {
        axios.get('/coin_view/set_coin_list.php?market=huobi&coin_list=[["EOS","USDT"],["EOS","ETH"]]', {
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
      var coin_pair = selection.coin_pair.split("-");
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