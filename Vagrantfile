# -*- mode: ruby -*-

Vagrant::Config.run do |config|
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  config.vm.network :bridged

  # Forward guest port 80 to host port 8080
  config.vm.forward_port 80, 8080
  #this is no longer needed because we are giving
  #this vm its own IP on the local network.
  #config.vm.forward_port 8000, 8000

  # Share Host "~/projects" with guest "/var/projects/share"
  config.vm.share_folder "share", "/var/projects/vegphilly", "."

  # this is still way too much of a wip
  #config.vm.provision :shell, :path => "build.sh"

end
