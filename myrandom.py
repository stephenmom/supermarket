import string
import random


def random_user_info():
    minlength = 6
    maxlength = 16

    mobile_begin_seed = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '157', '158', '159', '182',
                         '183',
                         '187', '188', '130', '131', '132', '155', '156', '175', '185', '186', '133', '153', '177',
                         '180',
                         '181', '189']
    mobile_seed = string.digits
    username_seed = string.digits + string.ascii_letters
    password_seed = string.digits + string.ascii_letters + string.punctuation

    mobile = random.choice(mobile_begin_seed) + ''.join(random.choice(mobile_seed) for m in range(8))
    username = ''.join(random.choice(username_seed) for u in range(random.randint(minlength, maxlength)))
    password = ''.join(random.choice(password_seed) for p in range(random.randint(minlength, maxlength)))

    return mobile, username, password


if __name__ == '__main__':
    rs = random_user_info()
    print(rs[1])
