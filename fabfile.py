import os
from datetime import datetime


from fabric.api import env, local, run, put, lcd, cd, sudo, settings

env.user = 'ho198605'
env.password = 'I86Gh%FeVc'


env.sudo_user = 'root'

env.hosts = ['99.12.135.93']

db_user = 'www-data'
db_password = 'www-data'


_TAR_FILE = 'dist-flaskApp.tar.gz'


def build():
    includes = ['static', 'templates', '*.py', '*.conf']
    # excludes = ['test', '.*', '*.pyc']
    local('rm -f dist/%s' % _TAR_FILE)
    with lcd(os.path.join(os.path.abspath('.'), 'www')):
        cmd = ['tar', '-czvf' '../dist/%s' % _TAR_FILE]
        cmd.extend(includes)

        local(' '.join(cmd))


_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/srv/flaskApp'


def deploy():
    newdir = 'www-%s' % datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    run('rm -f %s ' % _REMOTE_TMP_TAR)
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)

    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)

    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)

    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo('ln -s %s www' % newdir)
        sudo('chown www-data:www-data www')
        sudo('chown -R www-data:www-data %s' % newdir)

    with settings(warn_only=True):
        sudo('supervisorctl stop flaskApp')
        sudo('supervisorctl start flaskApp')
        sudo('nginx -s reload')


def setup():
    build()
    deploy()
