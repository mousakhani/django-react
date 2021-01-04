import random
from datetime import datetime, timedelta


def random_str():
    strs = 'abcdefghijklmnopqrstuvwxyz'
    result = ''
    for i in range(random.randint(1, 5), random.randint(6, 10)):
        result += random.choice(strs)
    return result


def random_phone():
    result = '09'
    for i in range(9):
        result += str(random.randint(0, 9))
    return result


def random_email():
    result = random_str()
    result += '@'
    result += random_str()
    result += '.'
    result += random_str()
    return result


def random_date():
    return str(datetime.now() + timedelta(days=random.randint(-9, 9)))


def random_bool():
    return random.choice([False, True])


def main():
    users = {"model": "post.customuser"}
    user_file_name = './user.json'
    file = open(user_file_name, 'w')
    file.write('[')

    # start users
    for i in range(500, 700):
        users['pk'] = i
        users['fields'] = {
            "password": random_str(),
            "last_login": random_date(),
            "is_superuser": random_bool(),
            "username": random_str()+str(i),
            "first_name": random_str(),
            "last_name": random_str(),
            "is_staff": random_bool(),
            "is_active": random_bool(),
            "date_joined": random_date(),
            "email": random_email(),
            "phone": random_phone(),
            "adres": random_str(),
            "bio": random_str(),
            "avatar": random_str(),
            "date_sent": random_date(),
            "groups": [],
            "user_permissions": []
        }
        file.write(str(users))
        file.write(',')
    file.write(']')
    file.close()
    file = open(user_file_name, 'r')
    str1 = file.read().replace("'", '"')
    str1 = str1.replace('False', 'false')
    str1 = str1.replace('True', 'true')
    file.close()
    file = open(user_file_name, 'w')
    file.write(str1)
    file.close()
    # end users

    # posts start
    posts = {'model': "post.post"}
    post_file_name = './post.json'
    file = open(post_file_name, 'w')
    file.write('[')
    for i in range(500, 700):
        for j in range(10):
            posts['pk'] = (i-500)*10 + j
            posts['fields'] = {
                'user': i,
                'title': random_str()+str(j),
                'content': random_str()+str(j),
                'create_date': random_date(),
                'last_update': random_date()
            }
            file.write(str(posts))
            file.write(',')
    file.write(']')
    file.close()
    file = open(post_file_name, 'r')
    str_post = file.read().replace("'", '"')
    str_post = str_post.replace('False', 'false')
    str_post = str_post.replace('True', 'true')
    file.close()
    file = open(post_file_name, 'w')
    file.write(str_post)
    file.close()
    print('ok')


if __name__ == "__main__":
    main()
