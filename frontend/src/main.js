import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';
import store from '@/store/store'
Vue.config.productionTip = false
Vue.config.baseurl = process.env.BASE_URL
import Vuelidate from 'vuelidate'
Vue.use(Vuelidate)
Vue.component('BaseInput', BaseInput)
Vue.component('BaseButton',BaseButton)
Vue.component('Loading', Loading)
import Pagination from 'vue-pagination-2';
import InfiniteLoading from 'vue-infinite-loading'

Vue.component('infinite-loading', InfiniteLoading)
Vue.component('pagination', Pagination);
import BaseInput from '@/components/BaseInput'
import BaseButton from '@/components/BaseButton'
import './assets/css/bootstrap.min.css';
import './assets/css/style.css';
import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'
import apiClient from '@/services/config.js'
new Vue({
    router,
    store,
    created(){
        const userString=localStorage.getItem('user')
        const userSession=sessionStorage.getItem('user')
        console.log('ccc',userString || userSession)
        if(userString || userSession){
            let userData;
            let credentials={};
            if(userString){
                userData=JSON.parse(userString)
            }
            else{
                userData=JSON.parse(userSession)
            }
            credentials.userData=userData
            console.log(credentials)
            this.$store.commit('login/SET_USER_DATA',credentials)
        }
        apiClient.interceptors.response.use(
            response=>response,
            error=>{
                if(error.response.status===401){
                    console.log(error)
                    this.$store.dispatch('login/logout')
                }
                return Promise.reject(error)
            }
        )
    },
    render: h => h(App),
}).$mount('#app')
