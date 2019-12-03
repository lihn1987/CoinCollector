<template>
  <div class="main">
    <mHeader :current=4 />
    <mErrorBody />
    <mFooter />
  </div>
</template>

<script> 
import Vue from 'vue'
import mHeader from '../Common/mHeader.vue'
import mFooter from '../Common/mFooter.vue'
import mBody from '../Common/mErrorBody.vue'
Vue.component('mHeader', mHeader)
Vue.component('mFooter', mFooter)
Vue.component('mErrorBody', mBody)
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
