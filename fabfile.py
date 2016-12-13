"""Fabfile to deploy stuff."""

from fabric.api import env, cd, run, sudo, local, lcd, put
from fabric.contrib.files import exists

import os

app_dir = '/apps/fortis'
git_repo = 'https://github.com/musale/fortis.git'

tmp = "/tmp/fortis"
tmp_f = "%s/fortis.tar.gz" % tmp

env.use_ssh_config = True
env.hosts = ['fortis']

user = 'vagrant'
sql = "CREATE DATABASE fortis;CREATE USER 'fortis'@'%'" +\
      " IDENTIFIED BY 'user@fmob';GRANT ALL PRIVILEGES ON " +\
      "fortis.* TO  'fortis'@'%';FLUSH PRIVILEGES;"


def db():
    env.hosts = ['sdb']


def stage():
    env.hosts = ['fortis']


def live():
    env.hosts = ['web']


def setup():
    sudo('yum -y install epel-release')
    sudo('yum -y update')
    setup_db()
    setup_app()


def deploy():
    pull_updates()
    prep_remote()
    restart_services()


def pull_updates():
    with cd(app_dir):
        if not exists('static'):
            run('mkdir static')
        if not exists('media'):
            run('mkdir media')
        if not exists('fortis'):
            run('git clone %s' % git_repo)
        with cd('fortis'):
            run('git pull origin master')
        with cd('/var/log'):
            if not exists('fortis'):
                sudo('mkdir -p fortis/app')
                sudo('chown -R %s:%s fortis')
                run('touch fortis/app/fortis.log')


def xdeploy():
    if os.path.exists(tmp):
        local('rm -rf %s' % tmp)
    local('mkdir %s' % tmp)
    with lcd(app_dir):
        local('tar -czhf %s fortis --exclude=".git*"' % (tmp_f))
    if exists(tmp):
        run('rm -rf %s' % tmp)
    run('mkdir %s' % tmp)
    put(tmp_f, tmp_f)
    with cd(app_dir):
        if exists('fortis'):
            run('rm -rf fortis')
        run('tar -xzf %s' % tmp_f)
        with cd('/var/log'):
            if not exists('fortis'):
                sudo('mkdir -p fortis/app')
                sudo('chown -R %s:%s fortis' % (user, user,))
                run('touch fortis/app/fortis.log')
    prep_remote()
    restart_services()


def prep_remote():
    """Prepare remote for deployment."""
    with cd('%s/fortis' % app_dir):
        sudo('pip install -r requirements.txt')
        run('python manage.py makemigrations')
        run('python manage.py migrate')
        run('python manage.py collectstatic --noinput')


def setup_db():
    sudo('yum install -y mariadb mariadb-devel mariadb-server')
    start_mysql()
    enable_mysql()
    sudo('mysql_secure_installation')
    run('mysql -u root -proot@fmob -e "%s"' % (sql,))


def setup_app():
    """Set up app server."""
    sudo('yum install -y gcc nginx python-pip python-devel')

    if not exists(app_dir):
        sudo('mkdir -p %s' % (app_dir,))
        sudo('chown -R %s:%s /apps' % (user, user,))
        run('mkdir %s/static' % (app_dir,))
        run('mkdir %s/media' % (app_dir,))
    xdeploy()
    sudo('cp /apps/fortis/fortis/config/fortis.conf ' +
         '/etc/nginx/conf.d/fortis.conf')
    sudo('cp /apps/fortis/fortis/config/fortis.service ' +
         '/etc/systemd/system/fortis.service')
    sudo('systemctl daemon-reload')
    start_nginx()
    start_fortis()


def restart_services():
    restart_fortis()


def restart_fortis():
    sudo('systemctl restart fortis')


def start_fortis():
    sudo('systemctl start fortis')


def install_reqs():
    sudo('pip install -r requirements.txt')


def start_mysql():
    sudo('systemctl start mariadb')


def enable_mysql():
    sudo('systemctl enable mariadb')


def start_nginx():
    sudo('systemctl start nginx')


def enable_nginx():
    sudo('systemctl enable nginx')
