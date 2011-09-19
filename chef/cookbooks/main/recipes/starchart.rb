execute "sudo pip install virtualenv" do
  user "root"
  action :run
end

# create a home for the project code
%w{projects projects/tweetrace projects/tweetrace/srv}.each do |dir|
  directory "/home/tweetrace/#{dir}" do
    mode 0775
    owner "tweetrace"
    group "tweetrace"
    action :create
  end
end

# Install everything into a virtualenv
execute "virtualenv --no-site-packages tweetrace-venv" do
  cwd "/home/tweetrace/projects/tweetrace/"
  action :run
  user node[:users][:tweetrace][:id]
  creates "/home/tweetrace/projects/tweetrace/tweetrace-venv/bin/python"
end

execute "/home/tweetrace/projects/tweetrace/tweetrace-venv/bin/pip install -r requirements.txt" do
  cwd "/home/tweetrace/projects/tweetrace/srv"
  user "root"
  action :run
end

# grab from repo
git "/home/tweetrace/projects/tweetrace/srv" do
  repository "git@github.com:gareth-lloyd/tweetrace.git"
  revision "HEAD"
  user "tweetrace"
  group "tweetrace"
  action :sync
end

