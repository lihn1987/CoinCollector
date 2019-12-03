<template>
  <div class="mmmmm">
    <mHeader :current=1 />
    <mBody />
    <mFooter />
  </div>
</template>

<script> 
import Vue from 'vue'
import mHeader from '../Common/mHeader.vue'
import mBody from './mBody.vue' 
import mFooter from '../Common/mFooter.vue'
Vue.component('mHeader', mHeader)
Vue.component('mBody', mBody)
Vue.component('mFooter', mFooter)
export default {
  name: 'mMain',
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
