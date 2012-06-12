import os
from fabric.api import local
from localconf import mongo_host, mongo_port, mongo_app, mongo_user, mongo_pass

def update_data():
    data = {
        'host': mongo_host,
        'port': mongo_port,
        'app': mongo_app,
        'user': mongo_user,
        'pass': mongo_pass
    }

    for datafile in os.listdir('data'):
        if datafile.endswith('.json'):
            print 'Processing %s' % datafile
            data.update({
                'file': datafile,
                'collection': ''.join(datafile.split('.')[:-1]),
            })
            local('mongoimport -h %(host)s:%(port)i -d %(app)s -c %(collection)s -u %(user)s -p %(pass)s --drop --file data/%(file)s' % data)

def pull():
    local('git pull origin master')

def stage():
    local('git push staging master')

def deploy():
    local('git push production master')
