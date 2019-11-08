
FLAG_FORMAT = '\w{31}='


SLICER = {
    'type': 'traffic.slicer.Slicer',
    'args': [
        'dumps'
    ],
    'kwargs': {
        'database': {
            'type': 'traffic.database.PgDatabase',
            'kwargs': {
                "user"              :   "test",
                "database"          :   "test",
                "password"          :   "test",
                "host"              :   "database",
                "command_timeout"   :   60
            }
        }
    }
}