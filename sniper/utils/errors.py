CODE_SYS_UNKNOWN = 'SYS.0001'
CODE_SYS_DB_ERROR = 'SYS.0002'
CODE_SYS_CONNECTION_ERROR = 'SYS.0003'
CODE_SYS_MONGO_ERROR = 'SYS.0004'

CODE_WRONG_AUTHENTICATION_INFO = 'USER.0001'

ERROR_CODES = {
    'SYS.0001': {
        'CN': '未知错误',
        'EN': 'unknown error',
    },
    'SYS.0002': {
        'CN': '数据库错误',
        'EN': 'db error',
    },
    'SYS.0003': {
        'CN': '请求错误',
        'EN': 'connection error',
    },
    'SYS.0004': {
        'CN': 'Mongo错误',
        'EN': 'Mongo error',
    },

    'USER.0001': {
        'CN': '错误的账号或密码',
        'EN': 'wrong name or password',
    }

}


def get_error_message(code, language):
    return ERROR_CODES[code][language]
