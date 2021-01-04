<template>
    <div class="col-md-12">
        <div class="hasshadow"><div>
            <div class="shadowhead">
                ویرایش اطلاعات
            </div>
            <loading loader="dots" :active.sync="isLoading"
                     :can-cancel="true"></loading>
            <div class="row justify-content-center mt-5">
                <div class="col-lg-12">
                    <form @submit.prevent="update">
                        <div class="row">
                            <div class="col-lg-6">
                                <div class="input-container">
                                    <BaseInput type="text" inputClass="input--style-4" label="نام" v-model="user.first_name" ></BaseInput>
                                </div>
                            </div>
                            <div class="col-lg-6">
                                <BaseInput type="text" inputClass="input--style-4" label="نام خانوادگی" v-model="user.last_name" ></BaseInput>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-lg-6">
                                <div class="input-container">
                                    <BaseInput type="text" inputClass="input--style-4" label="درباره شما" v-model="user.bio" ></BaseInput>
                                </div>
                            </div>

                            <div class="col-lg-6">
                                <div class="input-container">
                                    <BaseInput type="text" inputClass="input--style-4" label="شماره موبایل" v-model="user.phone" ></BaseInput>
                                </div>
                            </div>

                        </div>
                        <div class="row ">
                            <div class="col-lg-6">
                                <div class="input-container">
                                    <label class="label">آدرس</label>
                                    <textarea v-model="user.adres" class="textarea--style-4" type="text" ></textarea>
                                </div>
                            </div>

                            <div class="col-lg-6">
                                <div class="input-container">
                                    <BaseInput type="email" inputClass="input--style-4" label="ایمیل" v-model="user.email"  @blur="$v.user.email.$touch()"></BaseInput>
                                    <div v-if="$v.user.email.$error">
                                        <p class="text-right error" v-if="!$v.user.email.required"> ایمیل باید وارد شود</p>
                                        <p class="text-right error" v-if="!$v.user.email.email"> ایمیل باید فرمت معتبر باشد</p>
                                    </div>
                                </div>
                            </div>

                        </div>
                        <div class="row mb-3">
                            <div class="col-lg-6">
                                <div class="input-container">
                                    <label class="label">عکس</label>
                                    <input type="file" @change="onFileChanged" style="display:none" ref="fileInput" accept="image/*">
                                    <button class="primary btn-img btn--radius-2 " @click.prevent="onPickFile">انتخاب عکس</button>
                                   <div class="mt-2" v-if="user.avatar">
                                       <img  :src="baseUrl+user.avatar" height="150">
                                       <span class="removeImg" @click="removeImg">
                                                <i class="fas fa-times"></i>
                                            </span>
                                   </div>
                                    <div class="mt-2" v-if="imageUrl">
                                        <img  :src="imageUrl" height="150">
                                        <span class="removeImg" @click=" removeImgPreview">
                                                <i class="fas fa-times"></i>
                                            </span>
                                    </div>

                                </div>
                            </div>
                            </div>


                        <div v-if="error" class="text-right error mt-4 mr-3">
                            {{error}}
                        </div>
                        <div class="p-t-15 text-center ">
                            <BaseButton buttonClass="btn btn--radius-2 submit" type="submit"   >ویرایش</BaseButton>
                        </div>

                    </form>
                </div>
            </div>
        </div>
        </div>
    </div>
</template>

<script>
    import { required,email } from 'vuelidate/lib/validators'
    import {mapGetters} from 'vuex'
    import store from '@/store/store'
    import { baseUrl } from '@/config'

    export default {
        name: "ProfileEdit",
        validations:{
            user:{
                email:{required,email}
            }
        },
        data(){
            return{
                user:{
                    first_name:'',
                    last_name:'',
                    bio:'',
                    email:'',
                    phone:'',
                    adres:'',
                    avatar:''
                },
                formData : new FormData(),
                imageUrl:'',
                error:'',
                isLoading:false,
                baseUrl: baseUrl


            }
        },
        computed: {
            ...mapGetters('login', ['userInfo'])
        },
        created(){
            this.getUser()
        },
        watch:{
            user: {
                handler() {
                    this.error=''
                },
                deep: true
            }
        },
        methods:{
            onFileChanged (event) {
                this.formData.append('avatar', '')
                this.user.avatar=null
                const file = event.target.files[0]
                let filename=file.name
                if(filename.lastIndexOf('.')<=0){
                    this.error='فرمت مناسب انتخاب کنید'
                }
                this.imageUrl = URL.createObjectURL(file)
                this.formData.append('avatar', file, file.name)



            },
            getUser(){
                  if(this.userInfo)
                  {
                      this.setInfUser()
                  }
                  else{
                      store.dispatch('login/getUser').then(()=>{
                          this.setInfUser()
                          console.log('userInfo',this.userInfo)
                      })
                  }

            },
            setInfUser(){
                let user=this.userInfo
                this.user.last_name=user.last_name=='null'?'':user.last_name
                this.user.first_name=user.first_name=='null'?'':user.first_name
                this.user.email=user.email=='null'?'':user.email
                this.user.bio=user.bio=='null'?'':user.bio
                this.user.adres=user.adres=='null'?'':user.adres
                this.user.phone=user.phone=='null'?'':user.phone
                if( user.avatar.lastIndexOf('.')<=0){
                    this.user.avatar=''
                }
                else{
                    this.user.avatar=user.avatar
                }



            },
            update(){
                this.$v.$touch()
                if(!this.$v.$invalid){
                    this.formData.append('update', 'data')
                    this.user.last_name==''?this.formData.set('last_name',null): this.formData.append('last_name',this.user.last_name)
                    this.user.first_name==''?this.formData.set('first_name',null): this.formData.append('first_name',this.user.first_name)
                    this.user.email==''?this.formData.set('email',null): this.formData.append('email',this.user.email)
                    this.user.bio==''?this.formData.set('bio',null): this.formData.append('bio',this.user.bio)
                    this.user.adres==''?this.formData.set('adres',null): this.formData.append('adres',this.user.adres)

                    if(this.user.phone!=null)
                    {
                        this.user.phone==''?this.formData.set('phone',null): this.formData.append('phone',this.user.phone)
                    }
                    this.isLoading=true;
                    store.dispatch('login/updateUser',this.formData).then((res)=>{
                        this.isLoading=false;
                        if (res.status === 200){
                            this.error='اطلاعات با موفقیت ویرایش شد'
                        }
                    }).catch((e)=>{
                        this.isLoading=false;
                        if (e.response && e.response.status === 400) {
                            if(e.response.data.email)
                            {
                                this.error=e.response.data.email
                            }
                            else if(e.response.data.phone)
                            {
                                this.error=e.response.data.phone
                            }
                            else{
                                this.error='لطفا ورودی ها را کنترل نمایید'
                            }


                        }
                    })

            }
            },
            onPickFile(){
                this.$refs.fileInput.click()

            },
            removeImgPreview(){
                this.imageUrl=null
                this.formData.append('avatar',null);
            },
            removeImg(){
                this.user.avatar=null
                this.formData.append('avatar',null);
            }

        }
    }
</script>

<style scoped>
.btn-img{
    padding:5px;
    color:white!important;
    background: linear-gradient(315deg, rgb(148 18 82) 40%, rgba(151,8,150,1) 100%)!important;
}
.btn-img:focus{
    border:0;
    outline:0
}
.removeImg{
    position: absolute;
    color: red;
    cursor:pointer;
    top:60px;

}
</style>