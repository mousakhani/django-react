<template>

        <div>
            <div class="box mb-2">
                <i class="fas fa-quote-left quote" aria-hidden="true" style="font-size:12px;color:#c5245e"></i>
                <p class="content">{{title}} </p>
                <p >{{content}}</p>
                <loading loader="dots" :active.sync="isLoading"
                         :can-cancel="true"></loading>
                <div class="content">
                    <span class="writer"> نوشته شده توسط {{user.username}} </span>
                    <div class="info">
                        <div class="job" >
                            <router-link v-if="user.id==userInfo.id" :to="{ name: 'postEdit', params: { id: id } }"> <i class="fas fa-edit"></i> </router-link>
                            <div  v-if="user.id==userInfo.id" class="uk-container uk-container-center uk-margin-top" ></div>

                            <div  v-if="user.id==userInfo.id" class="uk-container uk-container-center uk-margin-top" >

                                <span @click="showModal = true" class="uk-button uk-button-primary delete" ><i class="fas fa-trash mr-2" ></i></span>
                                <DeleteModal @apply="deletePost(id)" class="delete" @closeModal="showModal=false" :show="showModal">
                                </DeleteModal>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </div>


</template>

<script>

    import store from '@/store/store'
    import {mapGetters} from 'vuex'
    import DeleteModal from '@/components/Modal/DeleteModal'
    export default {
        name: "PostPreview",
        components:{
            DeleteModal
        },
        data(){
            return{
                showModal: false,
                isLoading:false,
            }
        },
        props:{
            id: {
                type: String,
                required: true,
                default: () => ('')
            },
            title:{
                type: String,
                required: true,
                default: () => ('')
            },
            content:{
                type: String,
                required: true,
                default: () => ('')
            },
            user:{
                type: Object,
                required: true,
                default: () => ({})
            },


        },
        computed: {
            ...mapGetters('login', ['userInfo'])
        },
        methods:{
            deletePost(id){
                this.isLoading=true
                store.dispatch('post/deletePost',id).then(()=>{
                this.isLoading=false
                this.showModal=false
                    this.$emit("delete",id);

                }).catch((e)=>{
                    console.log(e.response)
                    this.isLoading=false
                    this.error='مشکلی در دریافت اطلاعات رخ داده است'
                })
            }
        }
    }
</script>

<style scoped>
    .uk-button-primary {
        position: absolute;
        top: 0;
        left: 26px;
    }
        .box {
            background: #fff;
            border-radius: 3px;
            padding: 25px;
            -webkit-box-shadow: 7px 5px 30px rgba(72,73,121,0.15);
            box-shadow: 7px 5px 30px rgba(72,73,121,0.15);

        }
        .box i.quote {
            font-size: 20px;
            color: #17a2b8;
        }
        .box .content {
            padding-top: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
    .content{
        display: inline-block!important;
        margin-right: 10px;
    }
    .info{
        position: absolute;
        left: 32px;
    }
    .delete{
        cursor:pointer;
        color:#c5245e;
    }
    .writer{
         position: relative;
         top: 21px;
        font-size:12px;
        right:-7px;
     }

</style>