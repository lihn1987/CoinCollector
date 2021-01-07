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
            width="140">
          </el-table-column>
          <el-table-column
            prop="huobi_lowest_sell"
            label="火币最低卖价"
            sortable
            width="140">
          </el-table-column>
          <el-table-column
            prop="huobi_highest_buy"
            label="火币最高买价"
            sortable
            width="140">
          </el-table-column>
          <el-table-column
            prop="ok_lowest_sell"
            label="ok最低卖价"
            sortable
            width="140">
          </el-table-column>
          <el-table-column
            prop="ok_highest_buy"
            label="ok最高买价"
            sortable
            width="140">
          </el-table-column>
          <el-table-column
            prop="huobi_buy_profit"
            label="火币购买价差"
            sortable
            width="140">
            <template slot-scope="scope">
              <i :class="(table_data[scope.$index].huobi_buy_profit) > 0 ?'el-icon-top green':'el-icon-bottom red'" ></i>
              <span :class="(table_data[scope.$index].huobi_buy_profit) > 0 ?'green':'red'" style="margin-left: 10px">{{ scope.row.huobi_buy_profit }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="ok_buy_profit"
            label="ok购买价差"
            sortable
            width="140">
            <template slot-scope="scope">
              <i :class="(table_data[scope.$index].ok_buy_profit) > 0 ?'el-icon-top green':'el-icon-bottom red'" ></i>
              <span :class="(table_data[scope.$index].ok_buy_profit) > 0 ?'green':'red'" style="margin-left: 10px">{{ scope.row.ok_buy_profit }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="huobi_delay"
            label="火币深度延时"
            sortable
            width="140">
          </el-table-column>
          <el-table-column
            prop="ok_delay"
            label="OK深度延时"
            sortable
            width="140">
          </el-table-column>

        </el-table>
      </div>
    </div>
    <div class="info_dev" style="margin-top:48px">
        <el-card style="width:30%;">
          <div>火币差价排行</div>
          <el-row v-for="n in huobi_top.length" :class="huobi_top[n-1].profit > 0 ? 'green' : 'red'" :key="'huobi_pro_item'+n">
            <el-col :span="12" style="text-align:left">{{ huobi_top[n-1].coin_pair }}</el-col>
            <el-col :span="12" style="text-align:right">{{ huobi_top[n-1].profit }}</el-col>
          </el-row>
        </el-card>

        <el-card style="width:30%">
          <div>OK差价排行</div>
          <el-row v-for="n in ok_top.length" :class="ok_top[n-1].profit > 0 ? 'green' : 'red'" :key="'ok_pro_item'+n">
            <el-col :span="12" style="text-align:left">{{ ok_top[n-1].coin_pair }}</el-col>
            <el-col :span="12" style="text-align:right">{{ ok_top[n-1].profit }}</el-col>
          </el-row>
        </el-card>
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
      }],
      huobi_top: [{
        coin_pair: 'aabb',
        profit: 1
      }, {
        coin_pair: 'ccdd',
        profit: -1
      }],
      ok_top: [{
        coin_pair: 'aabb',
        profit: 1
      }, {
        coin_pair: 'ccdd',
        profit: -1
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

.green{
  color: #00aa00;
}

.red{
  color: #aa0000;
}
</style>
