# -*- mode: ruby -*-

Vagrant::Config.run do |config|
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  # for selenium tests
  config.ssh.forward_x11 = true

  # for the gunicorn server to host port 8080
  config.vm.forward_port 80, 8080
  # forward 8000 to 8000 for development use
  config.vm.forward_port 8000, 8000

  config.vm.share_folder "share", "/usr/local/vegphilly", "."

  config.vm.provision :shell, :path => "utils/provision_vagrant.py"

  if ENV['VAGRANT_MORE_MEMORY']
    if ENV['VAGRANT_MORE_MEMORY'] == 'true'
      print "running vagrant with extra memory\n"
      config.vm.customize ["modifyvm", :id, "--memory", "1024"]
    end
  else
    print "NOTE: set the environment variable 'VAGRANT_MORE_MEMORY' to 'true' to use more RAM.\n"
  end
end
