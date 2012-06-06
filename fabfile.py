from fabric.api import *
env.use_ssh_config = True

env.directory = '/mnt/xuflus/Webs/foowill'
env.deploy_user = 'root'
env.hosts = ['root@foowill.com']
workon = "source /root/.virtualenvs/foowill/bin/activate && cd %s" % env.directory

def syncdb():
        run('python manage.py syncdb')
        run('python manage.py migrate')

def git_push():
    'Local push to the repository.'
    with cd(env.directory):
        local('git push -u origin master')
        
def git_pull():
    'Updates the repository.'
    with cd(env.directory):
	run('git pull')
        
def run_webserver():
    'Restart nginx and run the supervisor for celery, redis, anf gunicorn'
    run("/etc/init.d/nginx restart")
    with prefix(workon):
	run("python manage.py supervisor")
        
def deploy():
    git_push()
    #server()
    git_pull()
    #syncdb()
    run_webserver()
    