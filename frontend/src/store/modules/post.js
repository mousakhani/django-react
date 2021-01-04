import Service from '@/services/Service.js'
export const namespaced = true

export const state = {
    posts:[],
    post:''

}
export const mutations = {
    SET_POSTS(state,posts){
        state.posts=posts
    },

    DELETE_POST(state,id){
        let index= state.posts.findIndex(item=>item.id==id)
        state.posts.splice(index,1)
    },
    EDIT_POST(state,post){
        state.posts=[...state.posts.map(item=>item.id !== post.id ?  item:{...post})]
    },
    FILTER_POST(state,value){
        state.posts=value
        console.log('bnn',state.posts)
    },
    SET_POST(state,post){
        state.post=post
    },

}
export const actions= {
    deletePost({commit},id){
        return Service.deletePost(id)
            .then(() => {
                commit('DELETE_POST', id)

            })
            .catch(error => {
                console.log(error)

            })
    },
    getPosts ({ commit }) {

            return Service.getPosts().then((res)=>{
                console.log('userPost',res.data)
                commit('SET_POSTS',res.data)
            })


    },
    getPost({ commit, getters }, id) {

        let post = getters.getPostById(id)

        if (post) {
            commit('SET_POST', post)
            return post
        } else {
            return Service.getPost(id)
                .then(response => {
                    console.log('o',response)
                    commit('SET_POST', response.data)
                    return response.data
                })

        }
    },
    editPost({ commit},post ) {

        return Service.editPost(post)
            .then((res) => {
                commit('EDIT_POST',post)
                return res
            })
            .catch(error => {
                console.log(error)
            })
    },
    filterPosts({ commit},value ) {
        return Service.filterPosts(value).then((res)=>{

            commit('FILTER_POST',res.data)
            return res
        }).catch((e)=>{
            console.log(e.response)
        })
    },





}
export const getters= {
    posts(state){
        return state.posts
    },
    getPosts(state){
        return state.posts
    },
    getPostById:state=>id=>{
        return state.posts.find(post=>post.id===id)
    }
}