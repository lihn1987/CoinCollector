<template>
  <div class="main">
    <mHeader :current=2 />
    <mCoinTable />
    <mCoinNews />
    <mFooter />
  </div>
</template>
<script> 
import Vue from 'vue'
import mHeader from '../Common/mHeader.vue'
import mFooter from '../Common/mFooter.vue'
import mBody from '../Common/mErrorBody.vue'
import mCoinTable from './Item/mCoinTable.vue'
import mCoinNews from './Item/mCoinNews.vue'
Vue.component('mHeader', mHeader)
Vue.component('mFooter', mFooter)
Vue.component('mCoinTable', mCoinTable)
Vue.component('mCoinNews', mCoinNews)
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
