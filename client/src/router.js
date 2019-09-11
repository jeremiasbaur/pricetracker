import Vue from 'vue';
import Router from 'vue-router';
import Ping from './components/Ping.vue';
import Books from './components/Books.vue';
import Prices from './components/Prices.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Prices',
      component: Prices,
    },
    {
      path: '/prices',
      name: 'Prices',
      component: Prices,
    },
  ],
});
