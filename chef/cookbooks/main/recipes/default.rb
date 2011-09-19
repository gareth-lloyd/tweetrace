# install all generally required packages
# dependencies for particular recipes should obviously live
# with those recipes
node[:base_packages].each do |pkg|
  package pkg do
    :upgrade
  end
end

# create all users
node[:users].each_pair do |username, info|
  group username do
    gid info[:id]
  end
  # creates a group and user pair with a matching uid/guid
  user username do
    comment info[:full_name]
    uid info[:id]
    gid info[:id]
    shell info[:disabled] ? "/sbin/nologin" : "/bin/bash"
    supports :manage_home => true
    home "/home/#{username}"
  end

  # create home directory and .ssh folder
  directory "/home/#{username}/.ssh" do 
    owner username
    group username
    mode 0700
  end

  file "/home/#{username}/.ssh/id_rsa" do
    owner username
    group username
    mode 0600
    content info[:key]
  end
end

node[:groups].each_pair do |name, info|
  group name do
    gid info[:gid]
    members info[:members]
  end
end
