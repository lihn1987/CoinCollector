import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/PC/Main/Main'
import Coin from '@/components/PC/Coin/Main'
import Stone from '@/components/PC/Stone/Main'
import News from '@/components/PC/News/Main'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main
    },
    {
      path: '/Coin',
      name: 'Coin',
      component: Coin
    },
    {
      path: '/Stone',
      name: 'Stone',
      component: Stone
    },
    {
      path: '/News',
      name: 'News',
      component: News
    }
  ]
})
