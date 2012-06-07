from fabric.api import *
env.use_ssh_config = True

env.directory = '/mnt/xuflus/Webs/foowill'
env.deploy_user = 'root'
env.hosts = ['root@foowill.com']

def syncdb():
    with cd(env.directory):
        run('workon foowill && python manage.py syncdb && python manage.py migrate')

def git_push():
    'Local push to the repository.'
    with cd(env.directory):
        local('git push -u origin master')
        
def git_pull():
    'Updates the repository.'
    with cd(env.directory):
    run('git pull')

def stop_supervisor():
    with cd(env.directory):
        run("workon foowill && python manage.py supervisor stop all" )
        
def start_supervisor():
    with cd(env.directory):
        run("workon foowill && python manage.py supervisor --daemonize --project-dir=%s" % env.directory)
    
def stop_webserver():
    'Restart nginx and run the supervisor for celery, redis, anf gunicorn'
    run("/etc/init.d/nginx stop")
    stop_supervisor()
        
def start_webserver():
    'Restart nginx and run the supervisor for celery, redis, anf gunicorn'
    run("/etc/init.d/nginx start")
    with cd(env.directory):
        run("workon foowill && python manage.py supervisor --daemonize --project-dir=%s" % env.directory)
        
def restart_webserver():
    stop_supervisor()
    run("/etc/init.d/nginx restart")
    start_supervisor()

def deploy():
    git_push()
    stop_webserver()
    git_pull()
    syncdb()
    start_webserver()
    