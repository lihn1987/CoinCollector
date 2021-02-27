<template>
  <div class="app">
    <el-card>
      <el-tabs v-model="main_tb_index">
        <el-tab-pane label="火币主账户" name="1" style="text-align:center">
          <el-card style="width:1280px;margin:0 auto">总结余:{{parseFloat(huobi_main_profit_sum)+huobi_main_now_profit_sum}}</el-card>
          <el-card style="width:1280px;margin:0 auto;margin-top:24px">
            <el-row>已实现利润</el-row>
            <el-table
              :data="huobi_main"
              style="width: 1260px;margin:24px auto"
              >
              <el-table-column
                prop="coin_name"
                label="币种"
                sortable
                width="180">
              </el-table-column>
              <el-table-column
                prop="latest_time"
                label="上次量化时间差"
                sortable
                width="180">
              </el-table-column>
              <el-table-column
                prop="amount"
                label="当日总交易量"
                sortable
                width="180">
              </el-table-column>
              <el-table-column
                prop="profit"
                label="当日总收益"
                sortable
                width="180">
                <template slot-scope="scope">
                  <div :class="scope.row.profit == 0?'tb_normal':(scope.row.profit > 0? 'tb_up':'tb_down')">{{ scope.row.profit }}</div>
                </template>
              </el-table-column>
              <el-table-column
                prop="profit_buy"
                label="当日平多收益"
                sortable
                width="180">
                <template slot-scope="scope">
                  <div :class="scope.row.profit_buy == 0?'tb_normal':(scope.row.profit_buy > 0? 'tb_up':'tb_down')">{{ scope.row.profit_buy }}</div>
                </template>
              </el-table-column>
              <el-table-column
                prop="profit_sell"
                label="当日平空收益"
                sortable
                width="180">
                <template slot-scope="scope">
                  <div :class="scope.row.profit_sell == 0?'tb_normal':(scope.row.profit_sell > 0? 'tb_up':'tb_down')">{{ scope.row.profit_sell }}</div>
                </template>
              </el-table-column>
              <el-table-column
                prop="count"
                label="当日交易次数"
                sortable
                width="180">
              </el-table-column>
            </el-table>
            <el-row>
              <el-col :span="8">总利润:{{huobi_main_profit_sum}}</el-col>
              <el-col :span="8">总交易量:{{huobi_main_amount_sum}}</el-col>
              <el-col :span="8">总波段数{{huobi_main_count_sum}}</el-col>
            </el-row>
          </el-card>
          <el-card style="width:1280px;margin:0 auto;margin-top:24px">
            <el-row>未完成交易</el-row>
            <el-table
              :data="huobi_main_now"
              style="width: 900px;margin:24px auto"
              >
              <el-table-column
                prop="coin_order"
                label="币种"
                sortable
                width="180">
              </el-table-column>
              <el-table-column
                prop="dir"
                label="方向"
                sortable
                width="180">
              </el-table-column>
              <el-table-column
                prop="profit"
                label="利润"
                sortable
                width="180">
                <template slot-scope="scope">
                  <div :class="scope.row.profit == 0?'tb_normal':(scope.row.profit > 0? 'tb_up':'tb_down')">{{ scope.row.profit }}</div>
                </template>
              </el-table-column>
              <el-table-column
                prop="profit_rate"
                label="利润率"
                sortable
                width="180">
                <template slot-scope="scope">
                  <div :class="scope.row.profit_rate == 0?'tb_normal':(scope.row.profit_rate > 0? 'tb_up':'tb_down')">{{ scope.row.profit_rate }}%</div>
                </template>
              </el-table-column>
              <el-table-column
                prop="position_margin"
                label="抵押资产"
                sortable
                width="180">
              </el-table-column>
            </el-table>
            <el-row>
              <el-col :span="8">总利润:{{huobi_main_now_profit_sum}}</el-col>
              <el-col :span="8">抵押量:{{huobi_main_now_amount_sum}}</el-col>
            </el-row>
          </el-card>
        </el-tab-pane>
        <el-tab-pane label="火币子账户1" name="2">
          <el-card style="width:1280px;margin:0 auto">总结余:{{parseFloat(huobi_sub1_profit_sum)+huobi_sub1_now_profit_sum}}</el-card>
          <el-card style="width:1280px;margin:0 auto;margin-top:24px">
            <el-row>已完成交易</el-row>
            <el-table
              :data="huobi_sub1"
              style="width: 1260px;margin:24px auto"
              >
              <el-table-column
                prop="coin_name"
                label="币种"
                sortable
                width="180">
              </el-table-column>
              <el-table-column
                prop="latest_time"
                label="上次量化时间差"
                sortable
                width="180">
              </el-table-column>
              <el-table-column
                prop="amount"
                label="当日总交易量"
                sortable
                width="180">
              </el-table-column>
              <el-table-column
                prop="profit"
                label="当日总收益"
                sortable
                width="180">
                <template slot-scope="scope">
                  <div :class="scope.row.profit == 0?'tb_normal':(scope.row.profit > 0? 'tb_up':'tb_down')">{{ scope.row.profit }}</div>
                </template>
              </el-table-column>
              
              <el-table-column
                prop="profit_buy"
                label="当日平多收益"
                sortable
                width="180">
                <template slot-scope="scope">
                  <div :class="scope.row.profit_buy == 0?'tb_normal':(scope.row.profit_buy > 0? 'tb_up':'tb_down')">{{ scope.row.profit_buy }}</div>
                </template>
              </el-table-column>
              <el-table-column
                prop="profit_sell"
                label="当日平空收益"
                sortable
                width="180">
                <template slot-scope="scope">
                  <div :class="scope.row.profit_sell == 0?'tb_normal':(scope.row.profit_sell > 0? 'tb_up':'tb_down')">{{ scope.row.profit_sell }}</div>
                </template>
              </el-table-column>
              <el-table-column
                prop="count"
                label="当日交易次数"
                sortable
                width="180">
              </el-table-column>
            </el-table>
            <el-row>
              <el-col :span="8">总利润:{{huobi_sub1_profit_sum}}</el-col>
              <el-col :span="8">总交易量:{{huobi_sub1_amount_sum}}</el-col>
              <el-col :span="8">总波段数{{huobi_sub1_count_sum}}</el-col>
            </el-row>
          </el-card>
          <el-card style="width:1280px;margin:0 auto;margin-top:24px">
            <el-row>未完成交易</el-row>
            <el-table
              :data="huobi_sub1_now"
              style="width: 900px;margin:24px auto"
              >
              <el-table-column
                prop="coin_order"
                label="币种"
                sortable
                width="180">
              </el-table-column>
              <el-table-column
                prop="dir"
                label="方向"
                sortable
                width="180">
              </el-table-column>
              <el-table-column
                prop="profit"
                label="利润"
                sortable
                width="180">
                <template slot-scope="scope">
                  <div :class="scope.row.profit == 0?'tb_normal':(scope.row.profit > 0? 'tb_up':'tb_down')">{{ scope.row.profit }}</div>
                </template>
              </el-table-column>
              <el-table-column
                prop="profit_rate"
                label="利润率"
                sortable
                width="180">
                <template slot-scope="scope">
                  <div :class="scope.row.profit_rate == 0?'tb_normal':(scope.row.profit_rate > 0? 'tb_up':'tb_down')">{{ scope.row.profit_rate }}%</div>
                </template>
              </el-table-column>
              <el-table-column
                prop="position_margin"
                label="抵押资产"
                sortable
                width="180">
              </el-table-column>
            </el-table>
            <el-row>
              <el-col :span="8">总利润:{{huobi_sub1_now_profit_sum}}</el-col>
              <el-col :span="8">抵押量:{{huobi_sub1_now_amount_sum}}</el-col>
            </el-row>
          </el-card>
          
        </el-tab-pane>
        <el-tab-pane label="角色管理" name="3">xxx</el-tab-pane>
        <el-tab-pane label="定时任务" name="4">yyy</el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>
<script src="../script/CoinView.js"></script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
// @import '../scss/color.scss';
// @import '../scss/CoinView.scss'
  .tb_up{
    color:#00aa00;
  }
  .tb_down{
    color:#aa0000;
  }
</style>
