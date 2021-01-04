<template>
    <div class="container">
        <div class="row" v-if="results.length>=1">
            <PostPreview   v-for="post in results"  @delete="removechild"
                        :user="post.user" :key="post.id" :title="post.title" :content="post.content" :id="post.id.toString()" class="col-lg-4 mt-2 text-right"></PostPreview>

        </div>
    </div>
</template>

<script>

    import PostPreview from '@/components/post/PostPreview'
    export default {
        name: "PostList",
        props:{
         results:{
             type:Array,
             required: true,
             default: () => ([])
         }
        },
        components: {
            PostPreview
        },
        methods:{
            removechild(id){
               let index= this.results.findIndex(item=>item.id==id)
                this.results.splice(index,1)
            }
        }
    }
</script>

<style scoped>

</style>