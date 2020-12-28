<template>
  <div class="main">
    <Header :current=4 />
    <ErrorBody />
    <Footer />
  </div>
</template>

<script> 
import Vue from 'vue'
import Header from '../Common/Header.vue'
import Footer from '../Common/Footer.vue'
import Body from '../Common/ErrorBody.vue'
Vue.component('Header', Header)
Vue.component('Footer', Footer)
Vue.component('ErrorBody', Body)
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
