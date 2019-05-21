import me_classes
import auth
import pprint

# input('Begin auth.createUser()')
# auth.createUser()

# input('Continue to auth.login()')
# print('Log in?')
# response = input(' > ')
# if response == 'y':
#     user_session = auth.Session()

newthing = me_classes.Thing(
    tags=['hat', 'sunscreen', 'sun protection'],
    name='wide brimmed hat'
    # user=user
)
# newthing.save()

pprint.pprint(newthing.meta)
