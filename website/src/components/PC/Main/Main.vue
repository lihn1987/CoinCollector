<template>
  <div class="main">
    <Header :current=1 />
    <Body />
    <Footer />
  </div>
</template>

<script> 
import Vue from 'vue'
import Header from '../Common/Header.vue'
import Body from './Body.vue' 
import Footer from '../Common/Footer.vue'
Vue.component('Header', Header)
Vue.component('Body', Body)
Vue.component('Footer', Footer)
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
