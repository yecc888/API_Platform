import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
// import login from '@/components/login/Login'
import login1 from  '@/components/login/login1'
import brand from '@/components/brand/brand'
import api from '@/components/api/api'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {path: '/login',
    name: 'login1',
    component: login1,
    },
    {path: '/brand',
    name: 'barnd',
    component: brand,
    },
    {path: '/api',
    name: 'api',
    component: api,
    }
  ]
})
