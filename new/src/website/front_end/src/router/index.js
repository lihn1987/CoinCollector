import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/CoinView'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'CoinView',
      component: HelloWorld
    }
  ]
})
