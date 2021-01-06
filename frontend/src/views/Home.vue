<template>
    <div >
        <div class="bg-slider">
            <div class="container">
                <div class="row searchbox2" id="row-554569930">
                    <div class="col-12">

                        <div class="custom-search">
                            <div class="text-field">
                                <multiselect @open="asyncFind" placeholder="نام کاربر مورد نظر خود را وارد کنید"
                                             v-model="user"
                                             :options="options"
                                             :selectLabel=" meh"
                                             :hide-selected="true"
                                             selectedLabel="انتخاب شده"
                                             deselectLabel="حذف"
                                             label="username"
                                             track-by="name"
                                             openDirection="bottom"
                                             :showNoOptions="false"
                                             :optionHeight="7"


                                >
                                    <template slot="noResult">گزینه‌ای یافت نشد</template>

                                </multiselect>
                               </div>
                            <div class="search-top">
                                <i class="fas fa-search"></i>
                            </div>
                            <p></p>
                        </div>

                    </div>


                </div>
            </div>
        </div>
        <div class="container latest-top">
            <div class="row justify-content-center mt-5">
                <div class="col-lg-12 text-center">
                  <span class="latest">  آخرین مطالب</span>
                </div>
            </div>
        </div>
        <div class="container">
            <div class="row justify-content-center mt-5 posts-container">
                <div class="col-lg-12" v-if="posts">
                    <PostList :results="posts.results"></PostList>
                    <infinite-loading
                            spinner="waveDots"
                            @infinite="infiniteScroll"
                    >
                        <div slot="no-more"> </div>
                        <div slot="no-results"> </div>

                    </infinite-loading>


                </div>
                <div class="col-lg-12 text-center" v-else>
                    اطلاعاتی برای نمایش وجود ندارد
                </div>
            </div>
        </div>

    </div>
</template>

<script>
    import {mapGetters} from 'vuex'
    import store from '@/store/store'
    import Service from '@/services/Service.js'
    import PostList from '@/components/post/PostList'
    import Multiselect from 'vue-multiselect'
    export default {
        name: "Home",
        components: {
            PostList, Multiselect
        },
        data(){
            return{
                posts:{
                    results:[

                    ]
                },
                deletedId:'',
                meh:'',
                user: null,
                options: [
                ],
                perPage: 2,
                eventsTotal:'',
                currentPage:0,
                searchData:true,
                searchValue:'',
            }
        },
        created(){
            if(this.loggedIn && !this.userInfo){
                store.dispatch('login/getUser')
            }


        },
        mounted () {

        },

        computed: {
            ...mapGetters('login', ['loggedIn','userInfo']),


        },
        watch:{
            currentPage:function(value){
                return value
            },
            user:function(value){
                this.$router.push({ name: 'profileUser', params: { id: value.id } })
            },

        },
        methods:{
            infiniteScroll($state) {
                setTimeout(() => {
                        this.currentPage++;

                        Service.fetchAllPosts(
                            this.perPage,
                            this.currentPage-1,
                        ).then((res)=>{
                            console.log('3333333333',res)
                            if (res.data.results.length > 1) {
                                res.data.results.forEach((item) => this.posts.results.push(item))
                                $state.loaded()
                            } else {
                                $state.complete()
                            }
                        })
                    },500
                )

            },


            fetchAllPosts(currentPage){
                Service.fetchAllPosts(
                    this.perPage,
                    currentPage-1,
                ).then((res)=>{
                    this.posts=res.data
                    this.eventsTotal=res.data.count
                })
            },
            getRoute(){
                if(this.$route.query.page){
                    this.fetchAllPosts(this.$route.query.page)
                }
                else{
                    this.fetchAllPosts()
                }
            },
            asyncFind () {
                if(this.searchData==true)
                {

                    Service.getAll(
                    ).then((res)=>{

                        this.options=res.data
                        this.searchData=false

                    }).catch(()=>{

                    })
                }

            }
        }

    }
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
    .bg-slider{
        background-image:url('../assets/images/header-min.jpg');
        height:700px;
    }
    .searchbox2 {
        position: absolute;
        bottom: 120px;
        left: 50%;
        width:60%;
        transform: translateX(-50%);
        background: #fff;
        padding-top: 14px;
        border-top-left-radius: 25px;
        border-bottom-left-radius: 25px;
        border-top-right-radius: 25px;
        border-bottom-right-radius: 25px;
        box-shadow: 3px 2px 20px 8px #2f064d29;
    }
    #homesearch .custom-search {
        display: table;
        border: 2px solid #c7cad7;
        border-radius: 15px;
        overflow: hidden;
        margin: 0 auto;
    }
    .search-top{
        color:purple;
        font-size:25px;
        float:left;
        width:10%;
    }


    .text-field{
        float:right;
        width:50%;
    }
    .no-more{
        color:white!important;
    }
    .latest{
        border-bottom: 2px solid purple;
    }



</style>