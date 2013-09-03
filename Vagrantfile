# -*- mode: ruby -*-

Vagrant::Config.run do |config|
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  # Forward guest port 80 to host port 8080
  config.vm.forward_port 80, 8080
  config.vm.forward_port 8000, 8000

  config.vm.share_folder "share", "/usr/local/vegphilly", "."

  # run provisioner script from utils
  config.vm.provision :shell, :path => "utils/dev_env/apt_requirements.py"
  config.vm.provision :shell, :path => "utils/dev_env/perms.sh"
  config.vm.provision :shell, :path => "utils/dev_env/sys.sh"
  config.vm.provision :shell, :path => "utils/dev_env/postgres.sh"
  config.vm.provision :shell, :path => "utils/dev_env/os.sh"
  config.vm.provision :shell, :path => "utils/dev_env/build.sh"

end
