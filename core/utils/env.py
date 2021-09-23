from dotenv import dotenv_values


def environment_vars(file=".env"):
    config = dict(dotenv_values(file))
    return config
