<template>
  <div class="main">
    <Header :current=2 />
    <CoinTable />
    <CoinNews />
    <Footer />
  </div>
</template>
<script> 
import Vue from 'vue'
import Header from '../Common/Header.vue'
import Footer from '../Common/Footer.vue'
import Body from '../Common/ErrorBody.vue'
import CoinTable from './Item/CoinTable.vue'
import CoinNews from './Item/CoinNews.vue'
Vue.component('Header', Header)
Vue.component('Footer', Footer)
Vue.component('CoinTable', CoinTable)
Vue.component('CoinNews', CoinNews)
export default {
  name: 'Main',
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
