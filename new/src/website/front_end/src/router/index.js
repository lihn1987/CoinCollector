import Vue from 'vue'
import Router from 'vue-router'
import CoinView from '@/components/CoinView'
import Login from '@/components/Login'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'CoinView',
      component: CoinView
    }, {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})
