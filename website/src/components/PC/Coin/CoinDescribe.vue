<template>
  <div class="main">
    <Header :current=2 />
    <CoinDepth :id="this.$route.params.id" />
    <CoinDescribeIntruduce :id="this.$route.params.id" />
    <CoinNewsOnCoin :id="this.$route.params.id" />
    <Footer />
  </div>
</template>
<script> 
import Vue from 'vue'
import Header from '../Common/Header.vue'
import Footer from '../Common/Footer.vue'
import CoinDescribeIntruduce from './Item/CoinDescribeIntruduce'
import CoinNewsOnCoin from './Item/CoinNewsOnCoin'
import CoinDepth from './Item/CoinDepth'
Vue.component('Header', Header)
Vue.component('CoinDescribeIntruduce', CoinDescribeIntruduce)
Vue.component('CoinNewsOnCoin', CoinNewsOnCoin)
Vue.component('Footer', Footer)
Vue.component('CoinDepth', CoinDepth)


export default {
  name: 'CoinDescrebe',
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
