# Public Ansible Demo Repo

**Check Dynamic inventories section for learning about how to make it work!!!**

---

Setup
-----
Clone the repository to a directory, enter that directory and then run: 

    make

The make command:
1. Creates a virtual environment in a directory called `.venv` 
2. Installs all the requirements from `requirements.txt` on it.
3. Installs the roles from roles/requirements.yml in roles/:

**Note**: You can use `make help` for getting info about the steps in the Makefile.


Usage
-----
After the Setup step you can enable the virtualenv by executing on your current terminal and inside of the project directory:

    source .venv/bin/activate

**Note**: You can also run `make` again to update the workspace

Ensure you export the AWS Account profile you wish to use:

    export AWS_PROFILE=foo

Dynamic inventories
-------------------
This repo uses `dynamic inventories`. The inventories are constructed based on tags it gets from EC2 at runtime. 

```bash
ansible-inventory -i inventories/foo/inventory_aws_ec2.yml --graph
```


Role Development
----------------
You can use the workspace to develop roles: 

    ansible-galaxy install git+git@github.com:foo.git,1.2.3 -p roles/development/

The previous example will install the foo role with version 1.2.3 into roles/development directory. Roles in that directory will be prioritised over installed roles placed on `roles/`.

**Note**: Once you have finished your work and committed your changes back to
SCM remember to clean up. You can use ``make clean && make`` to reset to a
clean workspace.


Setup Credentials
--------------------
Ansible will need to have some credentials in order to decrypt
some encrypted values that can be on playbooks, group/host vars, inventory variables etc... The credentials are usually found in Keypass, ask devops otherwise.

For setting up the credentials file just create the next file with just the password on it on the home directory of the user you are using for calling ansible:

    ~/.ansible_vault_credentials

The vault password can also be set as the environmental variable
``ANSIBLE_VAULT_PASSWORD``. 

    ANSIBLE_VAULT_PASSWORD=123456 ansible-playbook -i inventories...

If the environmental variable is present the password will
be taken from it not the file.

**Note:** This logic is being done by the `vault_pass.py` script which is called by Ansible through the configuration `vault_password_file = vault_pass.py` on `ansible.cfg`


Setup SSH Config
----------------

It is a good idea to set up your SSH Configuration to allow for transparent ProxyJumping through the bastion host.:

```bash
Host bastion-01.foo.libertybelljerseys.com
  User [USER]
  IdentityFile ~/.ssh/id_rsa_foo
  HostName [BASTION PUBLIC IP]
  ProxyCommand None
Host *.foo.libertybelljerseys.com
  User [USER]
  IdentityFile ~/.ssh/id_rsa_foo
  ProxyJump bastion-01.foo.libertybelljerseys.com
```


Bootstrap a node
----------------

When launching a new node, it should be boostrapped so that the default `centos` user is disabled, and a new `backdoor` user is established.