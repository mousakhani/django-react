<template>
    <div >
        <div class="bg-slider">
            <div class="container">
                <div class="row searchbox2" id="row-554569930">
                    <div class="col-12">

                        <div class="custom-search">
                            <div class="text-field">
                                <input type="text" value="" name="s" id="search" placeholder="نام کاربر مورد نظر را وارد نمایید"></div>
                            <div class="search-top">
                                <i class="fas fa-search"></i>
                            </div>
                            <p></p>
                        </div>

                    </div>


                </div>
            </div>
        </div>
        <div class="container">
            <div class="row justify-content-center mt-5">
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
    export default {
        name: "Home",
        components: {
            PostList
        },
        data(){
            return{
                posts:{
                    results:[

                    ]
                },
                deletedId:'',

                perPage: 5,
                eventsTotal:'',
                currentPage:0
            }
        },
        created(){
            if(this.loggedIn && !this.userInfo){
                store.dispatch('login/getUser')
            }
            this.getPosts()

        },
        mounted () {
            window.scrollTo(0, 0)
        },

        computed: {
            ...mapGetters('login', ['loggedIn','userInfo']),


        },
        watch:{
            currentPage:function(v1){
                return v1
            }
        },
        methods:{
            infiniteScroll($state) {
                setTimeout(() => {
                        this.currentPage++;

                        Service.fetchAllPosts(
                            this.perPage,
                            this.currentPage,
                        ).then((res)=>{
                            console.log('reees',res)
                            if (res.data.results.length > 1) {
                                console.log('55',res.data.results)
                                res.data.results.forEach((item) => this.posts.results.push(item))
                                $state.loaded()
                            } else {
                                $state.complete()
                            }
                        })
                    },500
                )

            },
            getPosts()
            {
                Service.fetchAllPosts(
                    this.perPage,
                    this.currentPage-1,
                ).then((res)=>{
                    this.posts=res.data

                })


            },
            fetchAllPosts(currentPage){
                Service.fetchAllPosts(
                    this.perPage,
                    currentPage-1,
                ).then((res)=>{
                    console.log('res',res)
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
            }
        }

    }
</script>

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
    }

    .text-field{
        float:right;
        width:50%;
    }
    .no-more{
        color:white!important;
    }


</style>