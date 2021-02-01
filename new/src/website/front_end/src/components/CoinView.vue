<template>
  <div class="app">
    <el-row>
      <el-col :span="6" style="padding:12px">
        <div style="background:$color_back2;color:$color_front1;padding:4px;">
          <span style="color:#ffffff">币种列表</span>
          <div style="text-align:right;margin-top:-18px"><i class="el-icon-s-tools" style="color:#ffffff;" @click="OnSetCoinList"></i></div>
          <el-table
            ref="coin_list_table"
            :data="coin_list"
            highlight-current-row
            style="width: 100%;background:#141826;border:none;margin-top:24px;border-radius:4px"
            height="560"
            class="customer-table"
            @current-change="OnCoinListSelectChange"
            >
            <el-table-column
              property="coin_pair"
              label="交易对"
              min-width="50%">
            </el-table-column>
            <el-table-column
              property="coin_price"
              label="价格"
              min-width="50%">
            </el-table-column>
          </el-table>
        </div>
      </el-col>
      <el-col :span="12" style="margin-top:64px;text-align:left;font-size:12px" class="color_front1">
        <el-row>
          <el-col :span="4">基础币种&nbsp;&nbsp;{{coin_info.base_coin}}</el-col>
          <el-col :span="4" :offset="1">交易币种&nbsp;&nbsp;{{coin_info.order_coin}}</el-col>
          <el-col :span="4" :offset="1">价格精度&nbsp;&nbsp;{{coin_info.price_precision}}</el-col>
          <el-col :span="4" :offset="1">数量精度&nbsp;&nbsp;{{coin_info.amount_precision}}</el-col>
          <el-col :span="4" :offset="1">交易区&nbsp;&nbsp;{{coin_info.symbol_partition==1?"主区":"交易区"}}</el-col>
        </el-row>

        <el-row style="margin-top:8px">
          <el-col :span="4">交易名称&nbsp;&nbsp;{{coin_info.symbol}}</el-col>
          <el-col :span="4" :offset="1">能否交易&nbsp;&nbsp;{{coin_info.state==0?"不能交易":"能够交易"}}</el-col>
          <el-col :span="4" :offset="1">交易金额精度&nbsp;&nbsp;{{coin_info.value_precision}}</el-col>
          <el-col :span="4" :offset="1">最小限价量&nbsp;&nbsp;{{coin_info.limit_order_min_order_amt}}</el-col>
          <el-col :span="4" :offset="1">最大限价量&nbsp;&nbsp;{{coin_info.limit_order_max_order_amt}}</el-col>
        </el-row>
        <el-row style="margin-top:8px">
          <el-col :span="4">最小市价量&nbsp;&nbsp;{{coin_info.sell_market_min_order_amt}}</el-col>
          <el-col :span="4" :offset="1">最大市价量&nbsp;&nbsp;{{coin_info.sell_market_max_order_amt}}</el-col>
          <el-col :span="4" :offset="1">最大买金额&nbsp;&nbsp;{{coin_info.buy_market_max_order_value}}</el-col>
          <el-col :span="4" :offset="1">最小金额&nbsp;&nbsp;{{coin_info.min_order_value}}</el-col>
          <el-col :span="4" :offset="1">最大金额&nbsp;&nbsp;{{coin_info.max_order_value}}</el-col>
        </el-row>
        <el-row style="margin-top:16px;">
          <el-table
            :data="pre_profit"
            style="width: 100%">
            <el-table-column
              prop="kline_type"
              label="k线类型"
              width="60">
            </el-table-column>
            <el-table-column
              prop="max_profit"
              label="最大收益"
              width="180">
            </el-table-column>
            <el-table-column
              prop="best_buy_width_range"
              label="窗口宽度">
            </el-table-column>
            <el-table-column
              prop="best_buy_point"
              label="最佳买点">
            </el-table-column>
            <el-table-column
              prop="best_sell_point_low"
              label="最佳止损点">
            </el-table-column>
            <el-table-column
              prop="best_sell_point_hight"
              label="最佳止盈点">
            </el-table-column>
            <el-table-column
              prop="normal_profit"
              label="无操作收益">
            </el-table-column>
          </el-table>
        </el-row>
        <el-row>
          <!-- "order_coin"=>$order_coin, "base_coin"=>$base_coin, "is_buy"=>$is_buy, "amount"=>$amount, "price"=>$price -->
          <div>当前正在进行的交易</div>
          <el-table
            :data="transaction_now"
            style="width: 100%">
            <el-table-column
              prop="order_coin"
              label="交易币种"
              sortable
              width="120">
            </el-table-column>
            <el-table-column
              prop="base_coin"
              label="基础币种"
              width="120">
            </el-table-column>
            <el-table-column
              prop="is_buy"
              label="买卖方向"
              width="80">
            </el-table-column>
            <el-table-column
              prop="amount"
              label="当前持仓"
              width="120">
            </el-table-column>
            <el-table-column
              prop="profit"
              label="当前波段利润"
              width="180">
            </el-table-column>
            <el-table-column
              prop="price"
              label="持仓价格"
              width="120">
            </el-table-column>
            <el-table-column
              prop="all"
              label="USDT价格"
              width="auto">
            </el-table-column>
          </el-table>
        </el-row>
      </el-col>
      
      <el-col :span="6" style="padding-right:24px">
        <el-tabs v-model="active_right_pan" style="margin-top:48px;border:none;border-radius:4px;padding:12px" class="back2">
          <el-tab-pane label="盘口" name="first" style="text-align:left;font-size:12px">
            <el-row>
              <el-col :span="12">价格</el-col>
              <el-col :span="12">数量</el-col>
            </el-row>
            <el-row class="red" v-for="n in sell_depth.length" :key="'sell'+n">
              <el-col :span="12">{{sell_depth[buy_depth.length-n][0]}}</el-col>
              <el-col :span="12">{{sell_depth[buy_depth.length-n][1]}}</el-col>
            </el-row>
            <el-row>
              <el-col :span="24" style="font-size:14px;">当前价格:00.00</el-col>
            </el-row>
            <el-row class="green" v-for="n in buy_depth.length" :key="'buy'+n">
              <el-col :span="12">{{buy_depth[n-1][0]}}</el-col>
              <el-col :span="12">{{buy_depth[n-1][1]}}</el-col>
            </el-row>
          </el-tab-pane>
          <el-tab-pane label="实时成交" name="second">配置管理</el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>
<script src="../script/CoinView.js"></script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
@import '../scss/color.scss';
@import '../scss/CoinView.scss'

</style>
