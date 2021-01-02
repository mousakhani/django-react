
جدید


لیست یوزرها
'users/?limit=num&offset=num

لیست پست ها 
posts/?limit=num&offset=num






#----------------------------------------------------------------------------------------------------------------
url:'http://localhost:8000/'




user:{
    create:{
        uri:'users/',
        method:'POST',
        send:{
            username:'username',  //required
            password:'password',    //required
            first_name:'first_name',
            last_name:'lastname',
            email:'email',  //required
            phone:'phone',
            adres:'adres',
            desc:'bio',
            avatar:'image'
        },
        receive:{
            success: user infoes
            status:201,
            error_status:400,406,
        }
    },
    login:{
        uri:'users/login/,
        method:'POST',
        send:{
            username:'username',
            password:'password',
        },
        receive:{
            token:'token string',
            status:200,
            error_status:400
        }
    },
    //edit profile
    //login_required
    profile:{
        uri:'users/profile/',
        method:'PUT',
        send:{
            update:'password','data', None
            در صورتی که پسورد ارسال کنید، درخواست تغییر پسورد داده اید. و در صورتی که دیتا ارسال
            کنید درخواست تغییر چیزهایی به غیر از پسورد داده اید. 
            و در صورتی که خالی ارسال کنید، اطلاعات فعلی یوزر را درخواست کرده اید.

            username 
            last_login
            date_joined
            غیر قابل تغییر می باشند

            username و email : required

        },
        receive:{
            user infoes
            }
            status:200,
            error_status=400, 403, 406, 411
            ایمیل وارد شده، تکراری باشد 406
            نام کاربری تکراری باشد 406
    },
    password_recovery:{
        uri:'users/password-recovery',
        method:'GET',
        send:{
            'email':' email',
        },
        receive:{
            'email:'sent',
        },
        status:200,
        not_found_status:404

    }
}


post:{
    all_posts:{
        uri:'posts/',
        method:'GET',
        send:{},
        receive:{
            all posts 
        },
        status:200,
    },

    //login_required
    create:{
        uri:'posts/user/',
        method:'POST',
        send:{
            title:'post title', //required
            content:'post content', //required
        },
        receive:{
            new post
        },
        status: 200,
    },
    //login_required
    list:{
        //لیست کردن پست های یک یوزر خاص
        uri:'posts/user/',
        method:'GET',
        send:{},
        receive:{
            all user posts
        },
        status: 200,
        err_status: 404
    },
    //login_required
    one_post:{
        //گرفتن یک پست از یک یوزر خاص
        uri:'posts/user/<post_pk>/',
        method:'GET',
        send:{},
        receive:{
            one user post
        },
        status: 201,
        err_status: 400
    },
    //login_required
    update:{
        uri:'posts/user/<post_pk>/',
        method:'PUT',
        send:{
            title:'new title',
            content:'new content'
        },
        receive:{
            new post
        },
        status: 200,
        err_status: 400
    },
    DELETE:{
        uri:'posts/user/<post_pk>/',
        method:'DELETE',
        send:{}
        recevive:{
            'post':'deleted'
        },
        status: 200,
        err_status: 400
    }
},


search:{
    user:{
        uri:'users/search/',
        method:'GET',
        send:{
            search:'something',
        },
        receive:{
            search result
        },
        status: 200,
        not_found_status:404,
        bad_request_status:400
    },
    post:{
        uri:'posts/search/',
        method:'GET',
        send:{
            search:'something'
        },
        receive:{
            search result
        },
        status: 200,
        not_found_status:404,
        bad_request_status:400
    }
}