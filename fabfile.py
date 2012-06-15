from fabric.api import env, run, cd, prefix,local
env.use_ssh_config = True

def prod():
    env.vcs = 'git'
    env.hosts = ['foowill.com', ]
    env.user = 'root'
    env.app = 'foowill'
    env.APP_DIR = '/var/pywww/foowill/'
    env.virtualenv = 'foowill'

def pre():
    env.vcs = 'git'
    env.hosts = ['localhost', ]
    env.user = 'root'
    env.app = 'foowill'
    env.APP_DIR = '/mnt/xuflus/Webs/foowill/'
    env.virtualenv = 'foowill'

def requirements():
    """ install requeriments on app """
    with cd(env.APP_DIR):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix('workon %s' % env.virtualenv):
                run('pip install -r requirements.txt')

def lessc():
    'Compile lessc to the final css file'
    with cd(env.APP_DIR):
        local('lessc app/static/js/style.less > app/static/css/less.css')
    collectstatic()
                
def get_requeriments():
    with cd(env.APP_DIR):
      local('pip freeze > requirements.txt')
                
def push():
    'Local push to the repository.'
    with cd(env.APP_DIR):
        local('git push -u origin master')
        
def pull():
    'Updates the repository.'
    with cd(env.APP_DIR):
	run('git pull')

def syncdb():
    with cd(env.APP_DIR):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix('workon %s' % env.virtualenv):
		run('python manage.py syncdb')

def migrate():
    with cd(env.APP_DIR):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix('workon %s' % env.virtualenv):
		run('python manage.py migrate')

def collectstatic():
    with cd(env.APP_DIR):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix('workon %s' % env.virtualenv):
		run('python manage.py collectstatic')

def stop():
    with cd(env.APP_DIR):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix('workon %s' % env.virtualenv):
		run('python manage.py supervisor stop all')

def start():
    with cd(env.APP_DIR):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix('workon %s' % env.virtualenv):
		run('python manage.py supervisor --daemonize --project-dir=%s' % env.APP_DIR)

def restart():
    stop()
    start()

def update():
    'Update all'
    pull()
    requirements()
    syncdb()
    migrate()
    collectstatic()
    #compress()
    restart()

def updatefast():
    'No changes in DB or requeriments'
    pull()
    collectstatic()
    #compress()
    restart()