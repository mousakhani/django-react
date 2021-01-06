import apiClient from '@/services/config.js'
import axios from "axios"
let source;

export default {
    setToken (token) {
        apiClient.defaults.headers.common['Authorization'] = `Token ${token}`;

    },
    createUser(user) {
       return apiClient.post('/users/', user)
    },
    loginUser(user) {
        return apiClient.post('/users/login/', user)
    },
    getUser() {
        return apiClient.put('/users/profile/',{update:''})

    },
    getPosts(){
        return apiClient.get('/posts/user/')
    },
    getPost(id){
        return apiClient.get('/posts/user/'+id+'/')
    },
    editPost(post){
        console.log('c',post)
        return apiClient.put('/posts/user/'+post.id+'/',{title:post.title,content:post.content})
    },
    updateUser(data){
        console.log('00',data)
        return apiClient.put('/users/profile/',data,{
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }
        )

    },
    updatePassword(data){
        console.log('899999',data)
        return apiClient.put('/users/profile/',{update:'password',...data
        })

    },

    createPost(post){
        return apiClient.post('/posts/user/',post)
    },
    deletePost(id){
        return apiClient.delete('/posts/user/'+id+'/')
    },

     filterPosts(value){
        console.log('0',value)
        if(source){
            console.log('ddddddddddddd')
            source.cancel()
        }
        source= axios.CancelToken.source()
        console.log('bn',source.token)
        return  apiClient.get('/posts/search/',{
            cancelToken:source.token,
            params: {

                title: value,
                content: value,
            }}

        )
    },
    fetchAllPosts(perPage, page) {
        console.log('pageeeee',page)
        console.log('perPage',perPage)
        return apiClient.get('/posts/?limit='+ perPage + '&offset=' + page*perPage)
    },
    getAllusers(query){
        return apiClient.get('/users/search/?username='+query+'&firstname=+'+query+'&lastname='+query)
    },
    getAll(){
        return apiClient.get('/users/')
    }


}
