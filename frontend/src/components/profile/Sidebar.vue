<template>
    <div class="pageaside">
        <div class="sticky">
            <div class="dashCard">
                <ul>
                    <li class="first-card">

                        <div class="c-profile__user-avatar" v-if="userInfo.avatar" style="display: inline-grid;">
                            <img v-if="userInfo.avatar.lastIndexOf('.')>=0" :src="baseUrl+userInfo.avatar" height="150">
                            <img v-else src="@/assets/images/default.jpg" height="150">
                        </div>
                        <div class="c-profile__user-avatar" v-else style="display: inline-grid;">
                            <img  src="@/assets/images/default.jpg" height="150">
                        </div>
                        <p class="firstname d-inline-block">{{userInfo.username}}</p></li>
                </ul>
                <div class="row">
                    <div class=" half col-6" >
                    <router-link  :to="{name:'profileEdit'}">
                        ویرایش پروفایل
                    </router-link>
                  </div>
                    <div  class=" half col-6">
                        <router-link  :to="{name:'profileChangepassword'}">
                           تغییر رمز عبور
                        </router-link>
                    </div>
                </div>
            </div>

            <div class="dashCard menu">
                <ul>
                    <li @click="this.show=!this.show" class="showmenu2 active" >
                            منوی حساب کاربری
                      </li>
                    <div class="menu" v-show="show">
                        <li  :class="[currentPage.includes('/profile/create')?'active':'']">
                            <router-link :to="{name:'postCreate'}">
                         ایجاد پست
                            </router-link>
                        </li>
                        <li :class="[currentPage.includes('/profile/list')?'active':'']">
                            <router-link :to="{name:'postLists'}" >
                         لیست پست ها
                            </router-link>
                        </li>

                    </div>
                </ul>

            </div>
        </div>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex'
    import { baseUrl } from '@/config'
    export default {
        name: "Sidebar",
        data(){
            return{
                show:true,
                baseUrl:baseUrl

            }
        },
        methods:{

        },
        mounted(){
            this.currentPage;

        },
        computed:{
            ...mapGetters('login', ['userInfo']),
            currentPage () {
                return this.$route.path
            }
        }
    }
</script>

<style scoped>

</style>