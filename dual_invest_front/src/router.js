// router.js
// import DataTable from './components/DataTable.vue'
import BTC_SC from './components/BTC_SC.vue'
import BTC_SP from './components/BTC_SP.vue'
import ETH_SC from './components/ETH_SC.vue'
import ETH_SP from './components/ETH_SP.vue'

import { createMemoryHistory, createRouter } from 'vue-router'



const routes = [
    { name: 'home', path: '/', component: BTC_SC },   
    { name: 'btc_sc', path: '/btc/sc', component: BTC_SC},    
    { name: 'btc_sp', path: '/btc/sp', component: BTC_SP},
    { name: 'eth_sc', path: '/eth/sc', component: ETH_SC },
    { name: 'eth_sp', path: '/eth/sp', component: ETH_SP },
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

export default router