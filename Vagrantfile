# -*- mode: ruby -*-

Vagrant::Config.run do |config|
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  # disable this as needed
  config.vm.network :bridged

  # Forward guest port 80 to host port 8080
  config.vm.forward_port 80, 8080

  # Share Host "~/projects" with guest "/var/projects/share"
  config.vm.share_folder "share", "/var/projects/vegphilly", "."

  # run provisioner script from utils
  config.vm.provision :shell, :path => "utils/spin_up/build.sh"

end
