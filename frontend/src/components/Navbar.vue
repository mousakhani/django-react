<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-bg ftco_navbar  ftco-navbar-light site-navbar-target" id="ftco-navbar">
            <div class="container">
                <button @click="show=!show" class="navbar-toggler js-fh5co-nav-toggle fh5co-nav-toggle" type="button" data-toggle="collapse" data-target="#ftco-nav" aria-controls="ftco-nav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="oi oi-menu"></span><img src="@/assets/images/icons8-menu-24.png" alt="">
                </button>

                <div class="flex-items">
                    <router-link v-if="!loggedIn" data-toggle="tooltip" data-placement="right" :to="{name:'register'}" :class="{order:!show}" class="navbar-brand">
                        <svg aria-labelledby="svg-inline--fa-title-RtIOD4oBszjx" data-prefix="far" data-icon="sign-in-alt" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="signup svg-inline--fa fa-sign-in-alt fa-w-16 fa-fw fa-lg"><title id="svg-inline--fa-title-RtIOD4oBszjx" class="">ثبت نام</title><path fill="white" d="M144 112v51.6H48c-26.5 0-48 21.5-48 48v88.6c0 26.5 21.5 48 48 48h96v51.6c0 42.6 51.7 64.2 81.9 33.9l144-143.9c18.7-18.7 18.7-49.1 0-67.9l-144-144C195.8 48 144 69.3 144 112zm192 144L192 400v-99.7H48v-88.6h144V112l144 144zm80 192h-84c-6.6 0-12-5.4-12-12v-24c0-6.6 5.4-12 12-12h84c26.5 0 48-21.5 48-48V160c0-26.5-21.5-48-48-48h-84c-6.6 0-12-5.4-12-12V76c0-6.6 5.4-12 12-12h84c53 0 96 43 96 96v192c0 53-43 96-96 96z" class=""></path></svg>
                    </router-link>
                    <span :class="{order:!show}" @click="logout">
                    <i v-if="loggedIn" data-toggle="tooltip" data-placement="right" title="خروج" class="fas fa-sign-out-alt navbar-brand logout"></i>
                     </span>
                    <router-link  :to="{name:!loggedIn?'login':'profile'}" :class="{order:!show}" class="navbar-brand">
                        <img  data-toggle="tooltip" data-placement="right" :title="!loggedIn?'ورود':'پروفایل'" class="login-height" src="@/assets/images/top-icon.png" alt="">
                    </router-link>

                </div>

                <div :class="{collapse:!show}" class=" navbar-collapse text-right" id="ftco-nav" >
                    <ul class="navbar-nav nav ml-auto">
                        <li class="nav-item ml-3"><router-link to="/" class="nav-link active">خانه</router-link></li>
                        <li class="nav-item ml-3"><router-link to="/" class="nav-link active">درباره ما</router-link></li>
                        <li class="nav-item ml-3"><router-link to="/" class="nav-link active">بلاگ</router-link></li>
                        <li class="nav-item ml-3"><router-link to="/" class="nav-link active">تماس با ما</router-link></li>


                    </ul>
                </div>

            </div>
        </nav>
        <Notification :confirmShow="mailConfirm" :confirmDay="confirmDay" :loggedIn="loggedIn"></Notification>
    </div>
</template>

<script>

    import {mapGetters} from 'vuex'
    import Notification from '@/components/Notification'
    import store from '@/store/store'
    export default {
        name: "Navbar",
        components:{
            Notification
        },
        data(){
            return{
                show:false,
            }
        },
        computed: {
            ...mapGetters('login', ['loggedIn','mailConfirm','confirmDay'])
        },
        methods:{
            logout(){
                store.dispatch('login/logout').then(()=>{

                })
            }
        }
    }
</script>

<style scoped>
.order{
    order:2!important;
}
    .navbar-bg{
        background: #212529;
        color:white!important;
    }
    .nav-item a{
        color:white!important;
    }
    .navbar{
        position:fixed!important;
        width:100%;
        z-index:999;
    }
    .login-height{
        height:25px;
    }
    .signup{
        height: 25px;
        width: 45px;
        position: relative;
        top: 2px;
    }
@media(min-width:992px){
    .flex-items{
        display:contents!important;
    }
}
    .logout{
        font-size:32px;
        position: relative;
        top: 6px;
        cursor:pointer;
    }
</style>