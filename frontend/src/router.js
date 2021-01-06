import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
//
import Register from './views/Register.vue'
import Login from './views/Login.vue'
import EmailConfirm from './views/email/EmailConfirm.vue'
import NewEmail from './views/email/NewEmail.vue'
import ProfileEdit from './views/profile/ProfileEdit.vue'
import ProfileChangepassword from './views/profile/ProfileChangepassword.vue'
import PostCreate from './views/profile/post/PostCreate.vue'
import PostLists from './views/profile/post/PostLists.vue'
import PostEdit from './views/profile/post/PostEdit.vue'
import Profile from './views/profile/Profile.vue'
import ProfileUser from './views/profile/ProfileUser.vue'
//
// import Loading from 'vue-loading-overlay';
import NotFound from './views/NotFound'


Vue.use(Router)



const router = new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/register',
            name: 'register',
            component: Register
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
            meta: { requiresVisitor: true }
        },
        {
            path: '/newemail',
            name: 'newEmail',
            component: NewEmail,
            meta: { requiresAuth: true }
        },
        {
            path: '/emailConfirm',
            name: 'emailConfirm',
            component: EmailConfirm,
            meta: { requiresAuth: true }
        },
        {
            path: '/email',
            name: 'NewEmail',
            component: NewEmail,
            meta: { requiresAuth: true }
        },
        {
            path: '/user/profile',
            name: 'profile',
            component: Profile,
            redirect: "user/profile/edit",
            meta: { requiresAuth: true },
            children:[
                {
                    path: 'edit',
                    name: 'profileEdit',
                    component: ProfileEdit,
                    props:true,
                },
                {
                    path: 'user/:id',
                    name: 'profileUser',
                    component: ProfileUser,
                    props:true,
                },
                {
                    path: 'changepassword',
                    name: 'profileChangepassword',
                    component: ProfileChangepassword,
                    props:true,
                },
                {
                    path: 'postcreate',
                    name: 'postCreate',
                    component: PostCreate,
                    props:true,
                },
                {
                    path: 'postlist',
                    name: 'postLists',
                    component: PostLists,
                    props:true,
                },
                {
                    path: 'postedit/:id',
                    name: 'postEdit',
                    component: PostEdit,
                    props:true,
                },



            ]

        },

        {
            path: '/404',
            name: '404',
            component: NotFound
        },

        {
            path:'*',
            redirect:{name:'404'}
        }


    ]
})

router.beforeEach((to, from, next) => {
    let loggedIn;
    if(localStorage.getItem('user')){
        loggedIn = localStorage.getItem('user')
    }
    else if(sessionStorage.getItem('user')){
        loggedIn = sessionStorage.getItem('user')
    }

    if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
        next('/')
    }
    else if (to.matched.some(record => record.meta.requiresVisitor)) {
        if (loggedIn) {
            console.log('ddddddd')
            next({
                path: '/',
            })
        }
       else{
            next()
       }
    }
    else{
        next()
    }
})

export default router
