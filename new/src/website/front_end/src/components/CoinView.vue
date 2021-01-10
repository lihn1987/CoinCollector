<template>
  <div >
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
      </el-col>
      <el-col :span="6">
        ccc
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
