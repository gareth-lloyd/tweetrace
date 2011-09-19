from fabric.api import env, run, sudo, cd, lcd, settings
from fabric.contrib.project import rsync_project

from ConfigParser import SafeConfigParser
DEFAULTS = {'key_filename': '/Library/Ruby/Gems/1.8/gems/vagrant-0.7.5/keys/vagrant',
    'user': 'vagrant',
    'host': '127.0.0.1:2222',}
config = SafeConfigParser(DEFAULTS)
config.read('local.properties')

env.key_filename = config.get('remote_host', 'key_filename')
env.user = config.get('remote_host', 'user')
env.hosts = [config.get('remote_host', 'host')]

env.chef_dir = '/var/chef'
env.local_chef_dir = './chef'

def install_chef():
    sudo('gem install chef', pty=True)

def sync_config():
    # create /var/chef if not already existing
    with settings(warn_only=True):
        if run('test -d %s' % env.chef_dir).failed:
            sudo('mkdir %s' % env.chef_dir)
            sudo('chown %s %s' % (env.user, env.chef_dir))
            sudo('chgrp %s %s' % (env.user, env.chef_dir))

    create_chef_attrs()

    # sync ./chef with remote chef_dir
    with lcd('chef'):
        rsync_project(env.chef_dir, '.')

def update():
    sync_config()
    sudo('chef-solo -c %s/solo.rb' % env.chef_dir)

def create_chef_attrs():
    with open('keys/tweetrace_deploy', 'r') as priv_key:
        key = priv_key.read().strip()
        key = key.replace('\n', '\\n')
    with open('chef_attrs_template.json', 'r') as attrs_template:
        attrs = attrs_template.read() % key
    with open(env.local_chef_dir + '/node.json', 'w') as output:
        output.write(attrs)
