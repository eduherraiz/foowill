from fabric.api import *
env.use_ssh_config = True

SERVER_PATH = '/mnt/xuflus/Webs/foowill'

env.directory = '/mnt/xuflus/Webs/foowill'
env.activate = 'source /mnt/xuflus/virtualenvs/foowill/bin/activate'
env.deploy_user = 'root'

def virtualenv(command):
    with cd(env.directory):
        sudo(env.activate + '&&' + command, user=env.deploy_user)


def server():
    env.hosts = ['foowill.com']
    env.user = 'root'
    #env.key_filename = ['my-server-ssh-key']
    
#def restart_webserver():
    #""" Restart NGINX & UWSGI
    #"""
    #sudo("stop uwsgi-pricedag")
    #sudo("start uwsgi-pricedag")

def syncdb():
    with cd(SERVER_PATH):
        run('python manage.py syncdb')

def git_push():
    'Local push to the repository.'
    with cd(env.directory):    
        local('git push -u origin master')
        
def git_pull():
    'Updates the repository.'
    with cd(env.directory):    
        run('git pull')
        
def deploy():
    local("source /usr/bin/foowill")
    local("git push -u origin master")
    run("source foowill")
    run("git pull")
