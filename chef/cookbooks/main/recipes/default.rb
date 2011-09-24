# install all generally required packages
# dependencies for particular recipes should obviously live
# with those recipes
node[:base_packages].each do |pkg|
  package pkg do
    :upgrade
  end
end
