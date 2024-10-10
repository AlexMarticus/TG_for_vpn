from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = list(map(lambda x: int(x), env.list("ADMINS")))

DB_NAME = env.str('DB_NAME')
MY_EMAIL = env.str('MY_EMAIL')
MY_CLIENT_ID = env.str('MY_CLIENT_ID')
MY_NAME = env.str('MY_NAME')
MY_USERNAME = env.str('MY_USERNAME')
BOT_USERNAME = env.str('BOT_USERNAME')
MY_PHONE = env.str('MY_PHONE')