from fabric.api import env, run, cd, prefix,local
env.use_ssh_config = True

def prod():
    env.server = 'prod'
    env.vcs = 'git'
    env.hosts = ['foowill.com', ]
    env.user = 'root'
    env.app = 'foowill'
    env.APP_DIR = '/var/pywww/foowill/'
    env.virtualenv = 'foowill'

def pre():
    env.server = 'pre'
    env.vcs = 'git'
    env.hosts = ['eduherraiz.no-ip.org', ]
    env.user = 'root'
    env.app = 'foowill'
    env.APP_DIR = '/var/pywww/foowill/'
    env.virtualenv = 'foowill'
  
def requirements():
    """ install requeriments on app """
    with cd(env.APP_DIR):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix('workon %s' % env.virtualenv):
                run('pip install -r requirements.txt')

def lessc():
    'Compile lessc to the final css file'
    APP_DIR = '/mnt/xuflus/Webs/foowill/'
    local("cd %s; lessc app/static/css/less/bootstrap.less > app/static/css/bootstrap.css" % APP_DIR)
    local("cd %s; lessc app/static/css/lessless.css > app/static/css/final.css" % APP_DIR)
                    
def get_requeriments():
    with cd(env.APP_DIR):
        local('pip freeze > requirements.txt')
                
def push():
    'Local push to the repository.'
    with cd('/mnt/xuflus/Webs/foowill'):
        local('git add app/static')
        try:
            local('git commit -m "Auto push on deploy - small changes"')
        except:
            pass
        local('git push -u origin master')
        
def pull():
    'Updates the repository.'
    local("ssh -A %s 'cd %s; git pull'" % (env.hosts[0], env.APP_DIR))

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
		run('python manage.py collectstatic --noinput')

def supervisor():
    with cd(env.APP_DIR):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix('workon %s' % env.virtualenv):
                run('python manage.py supervisor --daemonize --project-dir=%s' % env.APP_DIR)
def stop():
    with cd(env.APP_DIR):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix('workon %s' % env.virtualenv):
		run('python manage.py supervisor stop all')

def start():
    with cd(env.APP_DIR):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix('workon %s' % env.virtualenv):
		run('python manage.py supervisor start all')

def restart():
    stop()
    start()

def newserver():
    #install nginx
    #configure nginx
    #install git
    #install redis-server
    #install mkvirtualenv
    #install python-crypto
    #install python-dev
    #first git on /var/pywww/foowill
        #git clone git@bitbucket.org:eduherraiz/foowill.git
        #Adding key ssh on bitbucket

    requirements()
    
def update():
    'Update all'
    pull()
    requirements()
    syncdb()
    migrate()
    collectstatic()
    restart()

def updatelessc():
    'No changes in DB or requeriments'
    lessc()
    push()
    pull()
    collectstatic()
    restart()
    
def updatefast():
    'No changes in DB or requeriments'
    pull()
    collectstatic()
    restart()