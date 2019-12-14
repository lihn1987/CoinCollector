<template>
  <div class="TranslateMid">
    <TranslateGraph class="TranslateGraph"/>
    <TranslateTrust class="TranslateTrust"/>
    <TranslateTrustHistory class="TranslateTrustHistory"/>
  </div>
</template>

<script>

import Vue from 'vue'
import TranslateGraph from './TranslateGraph.vue'
import TranslateTrust from './TranslateTrust.vue'
import TranslateTrustHistory from './TranslateTrustHistory.vue'
Vue.component('TranslateGraph', TranslateGraph)
Vue.component('TranslateTrust', TranslateTrust)
Vue.component('TranslateTrustHistory', TranslateTrustHistory)
export default {
  name: 'TranslateMid',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss" scoped>
@import "../../../style/index.scss";
.TranslateGraph{
  background:#ffff00;
  height:480px;
}
.TranslateTrust{
  background:#ff00ff;
  height:280px;
}
.TranslateTrustHistory{
  background:#00ffff;
  height:280px;
}
</style>
