# -*- mode: rcey -*-
# vi: set ft=rcey :

Vagrant.configure(2) do |config|

    config.vm.define "fortis" do |ce|
        ce.vm.box = "centos/7"
        ce.vm.hostname = "fortis"
        ce.vm.network "private_network", ip: "192.168.33.23"
    end

end
