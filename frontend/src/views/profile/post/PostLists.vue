<template>
    <div class="col-md-12">
        <div class="hasshadow"><div>
            <div class="shadowhead">
               لیست پست ها
            </div>
            <loading loader="dots" :active.sync="isLoading"
                     :can-cancel="true"></loading>
            <span>جستجو</span>
            <input class="input--style-4" label="جستجو" type="text" @input="input">
           <div class="row justify-content-center mt-5">
                 <div class="col-lg-12">
                    <PostList :results="posts"></PostList>
                </div>
            </div>
        </div>
        </div>
    </div>

</template>

<script>
    import PostList from '@/components/post/PostList'
    import store from '@/store/store'
    import {mapGetters} from 'vuex'
    export default {
        name: "PostLists",
        components: {
            PostList
        },
        methods:{
            input(e){
                this.searchValue=e.target.value
                this.service()
            },

            fetchPosts(){
                this.isLoading=true
                store.dispatch('post/getPosts').then(()=>{
                    this.isLoading=false

                }).catch(()=>{
                    this.isLoading=false
                    this.error='مشکلی در دریافت اطلاعات رخ داده است'
                })
            },
            service(){
                if(this.searchValue!=='')
                {
                    store.dispatch('post/filterPosts',this.searchValue).then(()=>{

                })
                }
                else{
                    this.fetchPosts();
                }
            }
        },
        data(){
            return{
                error:'',
                value:'',
                searchValue:'',
                isLoading:false,

            }
        },
        computed: {
            ...mapGetters('login', ['userInfo']),
            ...mapGetters('post', ['posts'])
        },
        created(){
            if(!this.userInfo){
                store.dispatch('login/getUser')
            }
            this.fetchPosts();

        }
    }
</script>

<style scoped>

</style>