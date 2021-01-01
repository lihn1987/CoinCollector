<template>
  <div >
    <div class="main">
      <div>
        <el-table
          :data="table_data"
          height="350"
          :default-sort = "{prop: 'coin_pair', order: 'ascending'}"
          >
          <el-table-column
            prop="coin_pair"
            label="交易对"
            sortable
            width="180">
          </el-table-column>
          <el-table-column
            prop="huobi_lowest_sell"
            label="火币最低卖价"
            sortable
            width="180">
          </el-table-column>
          <el-table-column
            prop="huobi_highest_buy"
            label="火币最高买价"
            sortable
            width="180">
          </el-table-column>
          <el-table-column
            prop="ok_lowest_sell"
            label="ok最低卖价"
            sortable
            width="180">
          </el-table-column>
          <el-table-column
            prop="ok_highest_buy"
            label="ok最高买价"
            sortable
            width="180">
          </el-table-column>
          <el-table-column
            prop="huobi_buy_profit"
            label="火币购买价差"
            sortable
            width="180">
          </el-table-column>
          <el-table-column
            prop="ok_buy_profit"
            label="ok购买价差"
            sortable
            width="180">
          </el-table-column>

        </el-table>
      </div>
    </div>
    <div class="info_dev">
      <div>
        <div>aaa1</div>
        <div>aaa1</div>
      </div>
      <div>bbb</div>
      <div>ccc</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'HelloWorld',
  data () {
    return {
      table_data: [{
        coin_pair: 'BTC-USDT',
        huobi_lowest_sell: '11.11',
        huobi_highest_buy: '22.22',
        ok_lowest_sell: '33.33',
        ok_highest_buy: '55.55',
        huobi_buy_profit: '1%',
        ok_buy_profit: '2%'
      }, {
        coin_pair: 'BTC-USDT',
        huobi_lowest_sell: '11.11',
        huobi_highest_buy: '22.22',
        ok_lowest_sell: '33.33',
        ok_highest_buy: '55.55',
        huobi_buy_profit: '1%',
        ok_buy_profit: '2%'
      }]
    }
  },
  mounted: function () {
    let that = this
    setInterval(function () {
      that.Flush()
    }, 1000)
  },
  destroyed: function () {

  },
  methods: {
    Flush: function () {
      var that = this
      axios.post('/coin_view/overview.php', {
        method: 'get_overview'
      }).then(function (response) {
        var result = response.data
        that.table_data = []
        for (var i = 0; i < result.length; i++) {
          that.table_data.push({
            coin_pair: result[i].order_coin + '-' + result[i].base_coin,
            huobi_lowest_sell: result[i].forsell_HUOBI,
            huobi_highest_buy: result[i].forbuy_HUOBI,
            ok_lowest_sell: result[i].forsell_OK,
            ok_highest_buy: result[i].forbuy_OK,
            huobi_buy_profit: ((result[i].forbuy_HUOBI - result[i].forsell_OK) * 100 / result[i].forbuy_HUOBI).toFixed(2),
            ok_buy_profit: ((result[i].forbuy_OK - result[i].forsell_HUOBI) * 100 / result[i].forbuy_OK).toFixed(2)
          })
        }
      }).catch(function (error) {
        console.log(error)
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style style="scss">
.main {
  width:1280px;
  margin:0 auto;
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.info_dev{
  width:1280px;
  margin:0 auto;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>
