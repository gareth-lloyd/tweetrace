package "nginx" do
    :upgrade
end

service "nginx" do
  enabled true
  running true
  supports :status => true, :restart => true, :reload => true
  action [:start, :enable]
end

cookbook_file "/etc/nginx/nginx.conf" do
  source "nginx/nginx.conf"
  mode 00640
  owner "root"
  group "root"
  notifies :restart, resources(:service => "nginx")
  action :create
end
