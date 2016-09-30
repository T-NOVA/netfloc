# T-NOVA Netfloc Ansible Installation

This playbook provides the deployment of T-NOVA Netfloc software on Ubuntu 14 server. 
Optionally, the playbook can be configured to provision an Openstack Virtual Machine in which to deploy Netfloc.  


## How to run

```sh
ansible-playbook -i inventory site.yml
```

## How to choose Openstack VM provisioning

In ansible_installation/site.yml make sure **"- include: openstack-vm-provision.yml"** is included and not commented out.
```yml
- include: openstack-vm-provision.yml
- include: openjdk-7.yml
- include: netfloc.yml
- include: openstack-sfc-installation.yml
```

In ansible_installation/inventory leave **[vm_group]** empty
```conf
[openstack-controller]
10.143.0.240 ansible_user=localadmin ansible_python_interpreter="~/ansible_venv/bin/python"

[vm_group]

```

## Files to edit

**File 1.** ansible_installation/group_vars/all:

```yml
# Username for openstack virtual machines
GLOB_OS_SSH_USERNAME: ubuntu
# Directory where python virtual environment containing ansible resides in openstack server
GLOB_OS_PYTHON_VENV: /home/localadmin/ansible_venv/bin/
```

**File 2. - Optional** ansible_installation/roles/openstack-vm-provision/vars/main.yml:
```yml
# Openstack Identity URL
OS_AUTH_URL: http://10.143.0.240:5000/v2.0
# Openstack Username & Password
OS_USERNAME: admin
OS_PASSWORD: enter_password_here
# Openstack Tenant name
OS_TENANT_NAME: admin

OS_AUTH:
  auth_url: "{{ OS_AUTH_URL }}"
  username: "{{ OS_USERNAME }}"
  password: "{{ OS_PASSWORD }}"
  project_name: "{{ OS_TENANT_NAME }}"


# Openstack key pair name
KEY_NAME: os_key
# Openstack Internal network name for VM
INTERNAL_NETWORK: int-net
# Openstack Enternal network name for VM
EXTERNAL_NETWORK: ext-net
# Openstack Flavor name for VM
FLAVOR: m1.medium
# Openstack Image or Snapshot name for VM
OSIMG: trusty64cloud
# Number of instances to provision
INSTCNT: 1
# Name of instance to provision
INSTNAME: ansible-provision-tnova_sfc
```