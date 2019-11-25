<template>
  <div class="main">
    <Header :current=2 />
    <HuobiDepth />
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
import HuobiDepth from './Item/HuobiDepth'
Vue.component('Header', Header)
Vue.component('CoinDescribeIntruduce', CoinDescribeIntruduce)
Vue.component('CoinNewsOnCoin', CoinNewsOnCoin)
Vue.component('Footer', Footer)
Vue.component('HuobiDepth', HuobiDepth)


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
