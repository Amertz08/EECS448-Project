APP_NAME = "tickets"
REMOTE_DIR = "/opt/#{APP_NAME}"
ANS_DIR = "#{REMOTE_DIR}/ansible"

Vagrant.configure("2") do |config|

    if Vagrant.has_plugin?("vagrant-hostmanager")
        config.hostmanager.enabled = true
        config.hostmanager.manage_host = true
        config.hostmanager.ignore_private_ip = false
    else
          raise 'vagrant-hostmanager is not installed. run: vagrant plugin install vagrant-hostmanager'
    end

    config.vm.define APP_NAME do |app|
        app.vm.box = "centos/7"
        app.vm.hostname = APP_NAME
        app.hostmanager.aliases = %w(APP_NAME)
        app.vm.network :private_network, ip: "10.10.10.10"
        app.vm.hostname = APP_NAME
        app.vm.synced_folder "./app", REMOTE_DIR, type: "nfs"

        app.vm.provider :virtualbox do |v|
            v.memory = 2048
            v.cpus = 4
        end

        app.vm.provision :ansible_local do |a|
            a.playbook = "#{ANS_DIR}/playbook.yml"
            a.limit = APP_NAME
            a.sudo = true
            a.extra_vars = { ansible_ssh_user: 'vagrant' }
            a.inventory_path = "#{ANS_DIR}/hosts.yml"
        end
    end
end
