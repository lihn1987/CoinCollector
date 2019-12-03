<template>
  <div class="main">
    <mHeader :current=3 />
    <mErrorBody />
    <mFooter />
  </div>
</template>

<script> 
import Vue from 'vue'
import Header from '../Common/mHeader.vue'
import Footer from '../Common/mFooter.vue'
import Body from '../Common/mErrorBody.vue'
Vue.component('mHeader', Header)
Vue.component('mFooter', Footer)
Vue.component('mErrorBody', Body)
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
