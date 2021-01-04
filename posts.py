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


def main():
    result = []
    users = {'model': 'post.customuser'}
    for i in range(300, 301):
        users['pk'] = i
        users['fields'] = {
            'password': random_str(),
            'last_login': random_date(),
            'is_superuser': False,
            'username': random_str()+str(i),
            'first_name': random_str(),
            'last_name': random_str(),
            'is_staff': False,
            'is_active': True,
            'date_joined': random_date(),
            'email': random_email(),
            'phone': random_phone(),
            'adres': random_str(),
            'bio': random_str(),
            'avatar': None,
            'date_sent': random_date(),
            'groups': [],
            'user_permissions': []
        }
        result.append(users)    
    print(result)


if __name__ == "__main__":
    print(main())
