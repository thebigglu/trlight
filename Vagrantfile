Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 5000, host: 8080, auto_correct: true

  config.ssh.forward_agent = true

  config.vm.provider "virtualbox" do |v|
    host = RbConfig::CONFIG['host_os']

    if host =~ /darwin/
      mem = `sysctl -n hw.memsize`.to_i / 1024
    elsif host =~ /linux/
      mem = `grep 'MemTotal' /proc/meminfo | sed -e 's/MemTotal://' -e 's/ kB//'`.to_i
    elsif host =~ /mswin|mingw|cygwin/
      mem = `wmic computersystem Get TotalPhysicalMemory`.split[1].to_i / 1024
    end

    mem = mem / 1024 / 4
    v.customize ["modifyvm", :id, "--memory", mem]
  end

  config.vm.network :private_network, ip: '192.168.50.50'

  config.vm.synced_folder '.', '/vagrant', nfs: true

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
    echo deb https://apt.dockerproject.org/repo ubuntu-trusty main > /etc/apt/sources.list.d/docker.list
    sudo apt-get install -y linux-image-extra-$(uname -r)
    sudo apt-get update
    sudo apt-get install -y docker-engine
    sudo service docker start

    sudo apt-get install -y python-pip
    sudo pip install docker-compose httpie

    sudo docker-compose -f "/vagrant/docker-compose.yml" up -d
  SHELL
end
