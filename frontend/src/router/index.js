import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Operator/HomeView.vue'
import LoginView from '../views/Operator/LoginView.vue'
import SignupView from '../views/Operator/SignupView.vue'
import Units from '../views/Operator/Units.vue'
import AddUnit from '../views/Operator/AddUnit.vue'
import Profile from '@/views/Operator/Profile.vue'
import NotFound from '../views/NotFound.vue' 
import Index from '../views/Index.vue' 
import Topup from '../views/Teller/Topup.vue' 
import Deduct from '../views/Teller/Deduct.vue' 
import LoginTeller from '../views/Teller/LoginTeller.vue'
import AddTeller from '../views/Teller/AddTeller.vue'
import HomeTeller from '../views/Teller/HomeTeller.vue'
import Test from '../views/Test.vue' 
import ResetPassword from '../views/ResetPassword.vue' 
import LoginUnitView from '../views/Unit/LoginUnitView.vue'
import UnitDashboard from '../views/Unit/UnitDashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: '',
      component: Index
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true },
      props: (route) => ({ user: route.params.user })
    },  {
      path: '/homeTeller',
      name: 'homeTeller',
      component: HomeTeller,
      meta: { requiresAuth: true },
      props: (route) => ({ Teller: route.params.Teller })
    },{
      path: '/homeunit',
      name: 'homeunit',
      component: UnitDashboard,
      meta: { requiresAuth: true },
      props: (route) => ({ unit: route.params.unit })
    }, {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },{
      path: '/addTeller',
      name: 'addTeller',
      component: AddTeller
    }, {
      path: '/login',
      name: 'login',
      component: LoginView
    },{
      path: '/loginUnit',
      name: 'loginUnit',
      component: LoginUnitView
    },{
      path: '/loginTeller',
      name: 'loginTeller',
      component: LoginTeller
    },{
      path: '/reset',
      name: 'reset',
      component:  ResetPassword
    },{
      path: '/units',
      name: 'units',
      component: Units,
      meta: { requiresAuth: true },
      props: (route) => ({ user: route.params.user })
    },{
      path: '/addunit',
      name: 'addunit',
      component: AddUnit,
      meta: { requiresAuth: true },
      props: (route) => ({ user: route.params.user })
    },{
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: { requiresAuth: true },
      props: (route) => ({ user: route.params.user })
    },{
      path: '/topup',
      name: 'topup',
      component: Topup,
      meta: { requiresAuth: true },
      props: (route) => ({ user: route.params.user })
    },{
      path: '/deduct',
      name: 'deduct',
      component: Deduct,
      props: (route) => ({ user: route.params.user })
    },{
      path: '/test',
      name: 'test',
      component: Test,
      meta: { requiresAuth: true },
      props: (route) => ({ user: route.params.user })
    },
    // Route for handling 404 errors
    {
      path: '/:catchAll(.*)',
      component: NotFound
    }
  ]
})
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token')
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'login' }) // Redirect to login if not authenticated
  } else {
    next() // Proceed to the requested route
  }
})

export default router
