from socket import gethostname

hostname = gethostname()

is_live = hostname == 'centos-512mb-fra1-01'
is_dev = hostname == 'fortis'

if is_live:
    DEBUG = False

if is_live:
    DB = {
        'name': 'fortis', 'host': hostname,
        'user': 'root', 'password': 'root@fmob'
    }


if is_dev:
    DB = {
        'name': 'fortis', 'host': 'fortis',
        'user': 'root', 'password': 'root@fmob'
    }
