<template>
  <div class="app" style = "min-width:1280px">
    <el-card>
      {{username}}
    </el-card>
    <el-card style="margin-top:24px">
      <el-tabs v-model="main_tb_index" @tab-click="FlushECharts(2)">
        <el-tab-pane v-for="n in 2" :label="config[n-1].lbl" v-bind:key= "n" :name="config[n-1].name" style="text-align:center">
          <el-card style="width:1280px;margin:0 auto;margin-top:24px">
            <el-row style="display: -webkit-flex;display:flex;flex-direction: row;justify-content:space-between">
              <div></div>
              <div>当日已实现利润</div>
              <div style="font-size:12px;line-height:24px">当前账户资产估值({{config[n-1].amount_balance}}usdt)</div>
            </el-row>
            <el-table
              :data="config[n-1].profit_history.detail"
              style="width: 1260px;margin:24px auto"
              >
              <el-table-column
                prop="coin_name"
                label="币种"
                sortable
                width="auto">
              </el-table-column>
              <el-table-column
                prop="status"
                label="当前状态"
                sortable
                width="120">
              </el-table-column>
              <el-table-column
                prop="latest_time"
                label="上次量化时间差"
                sortable
                width="150">
              </el-table-column>
              <el-table-column
                prop="amount"
                label="总交易量"
                sortable
                width="110">
              </el-table-column>
              <el-table-column
                prop="profit"
                label="总收益"
                sortable
                width="100">
                <template slot-scope="scope">
                  <div class="clearfix">
                    <div :class="scope.row.profit == 0?'tb_normal':(scope.row.profit > 0? 'tb_up':'tb_down')+' left'">{{ scope.row.profit }}</div>
                    <div :class="scope.row.profit == 0?'tb_normal':(scope.row.profit > 0? 'tb_up el-icon-top ':'tb_down el-icon-bottom')+' left'"></div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                prop="profit_buy"
                label="平空收益"
                sortable
                width="110">
                <template slot-scope="scope">
                  <div class="clearfix">
                    <div :class="(scope.row.profit_buy == 0?'tb_normal':(scope.row.profit_buy > 0? 'tb_up':'tb_down')+' left')">{{ scope.row.profit_buy }}</div>
                    <div :class="scope.row.profit_buy == 0?'tb_normal':(scope.row.profit_buy > 0? 'tb_up el-icon-top ':'tb_down el-icon-bottom')+' left'"></div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                prop="profit_sell"
                label="平多收益"
                sortable
                width="110">
                <template slot-scope="scope">
                  <div :class="(scope.row.profit_sell == 0?'tb_normal':(scope.row.profit_sell > 0? 'tb_up':'tb_down')+' left')">{{ scope.row.profit_sell }}</div>
                  <div :class="scope.row.profit_sell == 0?'tb_normal':(scope.row.profit_sell > 0? 'tb_up el-icon-top ':'tb_down el-icon-bottom')+' left'"></div>
                </template>
              </el-table-column>
              <el-table-column
                prop="count"
                label="交易次数"
                sortable
                width="110">
              </el-table-column>
              <el-table-column
                label="操作"
                sortable
                width="260">
                <template slot-scope="scope">
                  <div class="clearfix">
                    <el-button type="primary" @click="OnStop(scope.row.coin_name, n)">停止</el-button>
                    <el-button type="primary" @click="OnLiquidation(scope.row.coin_name, n)">平仓</el-button>
                    <el-button type="primary" @click="OnReset(scope.row.coin_name, n)">重启</el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
            <el-row>
              <el-col :span="8">总利润:{{config[n-1].profit_history.profit_sum}}</el-col>
              <el-col :span="8">总交易量:{{config[n-1].profit_history.amount_sum}}</el-col>
              <el-col :span="8">总波段数{{config[n-1].profit_history.count_sum}}</el-col>
            </el-row>
          </el-card>
          <el-card style="width:1280px;margin:0 auto;margin-top:24px">
            <el-row>未完成交易</el-row>
            <el-table
              :data="config[n-1].profit_now.detail"
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
                  <div :class="scope.row.profit == 0?'tb_normal':(scope.row.profit > 0? 'tb_up left':'tb_down left')">{{ scope.row.profit }}</div>
                  <div :class="scope.row.profit == 0?'tb_normal':(scope.row.profit > 0? 'tb_up el-icon-top ':'tb_down el-icon-bottom')+' left'"></div>
                </template>
              </el-table-column>
              <el-table-column
                prop="profit_rate"
                label="利润率"
                sortable
                width="180">
                <template slot-scope="scope">
                  <div :class="scope.row.profit_rate == 0?'tb_normal':(scope.row.profit_rate > 0? 'tb_up left':'tb_down left')">{{ scope.row.profit_rate }}%</div>
                  <div :class="scope.row.profit_rate == 0?'tb_normal':(scope.row.profit_rate > 0? 'tb_up el-icon-top ':'tb_down el-icon-bottom')+' left'"></div>
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
              <el-col :span="8">总利润:{{config[n-1].profit_now.profit_sum}}</el-col>
              <el-col :span="8">抵押量:{{config[n-1].profit_now.amount_sum}}</el-col>
            </el-row>
          </el-card>
          <el-card style="width:1280px;margin:0 auto;margin-top:24px">
            <el-row>交易历史</el-row>
            <el-table
              :data="history[n-1].data_list"
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
                label="交易类型"
                sortable
                width="180">
              </el-table-column>
              <el-table-column
                prop="profit"
                label="利润"
                sortable
                width="180">
                <template slot-scope="scope">
                  <div :class="scope.row.profit == 0?'tb_normal':(scope.row.profit > 0? 'tb_up left':'tb_down left')">{{ scope.row.profit }}</div>
                  <div :class="scope.row.profit == 0?'tb_normal':(scope.row.profit > 0? 'tb_up el-icon-top ':'tb_down el-icon-bottom')+' left'"></div>
                </template>
              </el-table-column>
              <el-table-column
                prop="amount"
                label="交易资金"
                sortable
                width="180">
              </el-table-column>
              <el-table-column
                prop="timestamp"
                label="时间"
                sortable
                width="180">
              </el-table-column>
            </el-table>
            <el-pagination
              @current-change="FlushHistory"
              :current-page.sync="history[n-1].page_index"
              :page-size="10"
              layout="prev, pager, next, jumper"
              :total="history[n-1].page_size">
            </el-pagination>
          </el-card>

          <el-card style="width:1280px;margin:0 auto;margin-top:24px">
            <el-row>历史统计</el-row>
            <el-row style="margin-top:36px">
              <el-col :span="8">
                <div class="grid-content">
                  <span class="demonstration">起始时间</span>
                  <el-date-picker
                    v-model="config[n-1].statistic.start_time"
                    type="date"
                    value-format='timestamp'
                    @change = "FlushECharts(n)"
                    placeholder="选择日期">
                  </el-date-picker>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="grid-content">
                  <span>币种</span>
                  <el-select v-model="config[n-1].statistic.statistic_coin" @change = "FlushECharts(n)" placeholder="请选择">
                    <el-option key="ALL" label="所有币种" value="ALL"></el-option>
                    <el-option key="XRP" label="XRP" value="XRP"></el-option>
                    <el-option key="DOGE" label="DOGE" value="DOGE"></el-option>
                    <el-option key="DOT" label="DOT" value="DOT"></el-option>
                    <el-option key="ALGO" label="ALGO" value="ALGO"></el-option>
                    <el-option key="LINK" label="LINK" value="LINK"></el-option>
                    <el-option key="ZEC" label="ZEC" value="ZEC"></el-option>
                  </el-select>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="grid-content">
                  <span>统计类型</span>
                  <el-select v-model="config[n-1].statistic.statistic_type" @change = "FlushECharts(n)" placeholder="请选择">
                    <el-option key="1" label="收益" value="1"></el-option>
                    <el-option key="2" label="交易额" value="2"></el-option>
                    <el-option key="3" label="交易次数" value="3"></el-option>
                  </el-select>
                </div>
              </el-col>
            </el-row>
            <div :id = "'echart'+n" style="width:100%;height:500px"></div>
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>
<script src="../script/CoinView.js"></script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
  @import '../scss/common.scss';
// @import '../scss/CoinView.scss'
  .updown_font{
    font-weight: 1200;
    font-size:28px;
  }
  .tb_up{
    color:#00aa00;
  }
  .tb_down{
    color:#aa0000;
  }
</style>
