import {
    createRouter,
    createWebHashHistory,     
    createWebHistory          
} from "vue-router"


const routes = [
    {path: '', name: 'aam-home', component: () => import('@/views/aam-home.vue')}
]

const router = createRouter({
    history:createWebHashHistory(),
    routes,
})

export default router