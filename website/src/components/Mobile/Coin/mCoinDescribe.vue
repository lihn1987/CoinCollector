<template>
  <div class="main">
    <mHeader :current=2 />
    <mCoinDescribeIntruduce :id="this.$route.params.id" />
    <mCoinDepth :id="this.$route.params.id" />
    <mCoinDetail :id="this.$route.params.id" />
    <mCoinTradeInfo :id="this.$route.params.id" />
    <mCoinNewsOnCoin :id="this.$route.params.id" />
    <mFooter />
  </div>
</template>
<script> 
import Vue from 'vue'
import mHeader from '../Common/mHeader.vue'
import mFooter from '../Common/mFooter.vue'
import mCoinDescribeIntruduce from './Item/mCoinDescribeIntruduce'
import mCoinNewsOnCoin from './Item/mCoinNewsOnCoin'
import mCoinDepth from './Item/mCoinDepth'
import mCoinDetail from './Item/mCoinDetail'
import mCoinTradeInfo from './Item/mCoinTradeInfo'
Vue.component('mHeader', mHeader)
Vue.component('mCoinDescribeIntruduce', mCoinDescribeIntruduce)
Vue.component('mCoinNewsOnCoin', mCoinNewsOnCoin)
Vue.component('mFooter', mFooter)
Vue.component('mCoinDepth', mCoinDepth)
Vue.component('mCoinDetail', mCoinDetail)
Vue.component('mCoinTradeInfo', mCoinTradeInfo)



export default {
  name: 'mCoinDescrebe',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
