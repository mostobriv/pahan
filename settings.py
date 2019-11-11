from backends.database import PgDatabase



FLAG_FORMAT = '\w{31}='


DB_SETTINGS = {
    "user"              :   "test",
    "database"          :   "test",
    "password"          :   "test",
    "host"              :   "database",
    "command_timeout"   :   60
}

DATABASE = PgDatabase(DB_SETTINGS)

SLICER = {
    'type': 'traffic.slicer.Slicer',
    'args': [
        'dumps',
        DATABASE
    ],
    'kwargs': {
        'ports': [1337, 1488]
    }
}

WEBAPP = {
    'type': 'web.app.WebApp',
    'kwargs': {
        'database': DATABASE,
        'addr':     '0.0.0.0',
        'port':     '8888'
    }
}