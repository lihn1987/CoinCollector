import Vue from 'vue'
import Router from 'vue-router'

import Main from '@/components/PC/Main/Main'
import Coin from '@/components/PC/Coin/Main'
import CoinDescribe from '@/components/PC/Coin/CoinDescribe'
import Stone from '@/components/PC/Stone/Main'
import News from '@/components/PC/News/Main'

import mMain from '@/components/Mobile/Main/mMain'
import mCoin from '@/components/Mobile/Coin/mMain'
import mCoinDescribe from '@/components/Mobile/Coin/mCoinDescribe'
import mStone from '@/components/Mobile/Stone/mMain'
import mNews from '@/components/Mobile/News/mMain'

Vue.use(Router)
var route_pc = [
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
    path: '/Coin/Describe/:id',
    name: 'coin_describe',
    component: CoinDescribe
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
  }]

var route_mobile = [
  {
    path: '/',
    name: 'mMain',
    component: mMain
  },
  {
    path: '/Coin',
    name: 'mCoin',
    component: mCoin
  },
  {
    path: '/Coin/Describe/:id',
    name: 'mcoin_describe',
    component: mCoinDescribe
  },
  {
    path: '/Stone',
    name: 'mStone',
    component: mStone
  },
  {
    path: '/News',
    name: 'mNews',
    component: mNews
  }
]

const flag = window.navigator.userAgent.match(/(phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|BlackBerry|IEMobile|MQQBrowser|JUC|Fennec|wOSBrowser|BrowserNG|WebOS|Symbian|Windows Phone)/i);

let rouMap = route_pc;
if (flag) {
  rouMap = route_mobile;
  console.log('移动端' + flag );
} else {
  rouMap = route_pc;
  console.log('pc端');
}
export default new Router({
  routes: rouMap
})
