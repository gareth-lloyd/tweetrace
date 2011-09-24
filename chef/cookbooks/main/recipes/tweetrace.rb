#execute "sudo pip install virtualenv" do
#  user "root"
#  action :run
#end

# create a home for the project code
directory "/srv" do
  mode 0775
  owner "tweetrace"
  group "tweetrace"
  action :create
end

# Install everything into a virtualenv
execute "virtualenv --no-site-packages tweetrace-venv" do
  cwd "/srv"
  action :run
  user node[:users][:tweetrace][:id]
  creates "/srv/tweetrace-venv/bin/python"
end

# grab from repo
git "/srv/tweetrace" do
  repository "git@github.com:gareth-lloyd/tweetrace.git"
  revision "HEAD"
  user "tweetrace"
  group "tweetrace"
  action :sync
end

execute "/srv/tweetrace-venv/bin/pip install -r requirements.txt" do
  cwd "/srv/tweetrace"
  user "tweetrace"
  action :run
end

directory "/var/bluepill" do
  owner "tweetrace"
  group "tweetrace"
  mode "0755"
  action :create
end

gem_package "bluepill" do
  action :install
end

template "/srv/tweetrace/linkwatch.pill" do
  source "linkwatch.pill"
  mode 0755
  owner "tweetrace"
  group "tweetrace"
end


#execute "bluepill_load" do
#  command "bluepill load /srv/tweetrace/linkwatch.pill"
#  action :run
#end
#
#execute "bluepill_restart" do
#  command "bluepill linkwatch restart"
#  action :run
#end

template "/srv/tweetrace/gunicorn.pill" do
  source "gunicorn.pill"
  mode 0755
  owner "tweetrace"
  group "tweetrace"
end

#execute "bluepill_load" do
#  command "bluepill load /srv/tweetrace/gunicorn.pill"
#  action :run
#end
#
#execute "bluepill_restart" do
#  command "bluepill gunicorn restart"
#  action :run
#end
