# Ansible: server configuration

Configures a target host to run the `notes` app stack from the repo root
(Docker Engine + Compose plugin, firewall, checkout + `docker compose up`).

## Status

Written and ready to run, but **not yet executed against a real server** —
there is no provisioned host yet. The `[app_servers]` group in
`inventory.ini` is a placeholder. Once the Terraform stage provisions a
Yandex Cloud VM, add its IP there (or point inventory.ini at it) and run
this for real.

## Setup

```bash
ansible-galaxy collection install -r requirements.yml
```

Create the vaulted secrets file (not committed, see `.gitignore`):

```bash
ansible-vault create group_vars/all/vault.yml
# inside, add:
# vault_postgres_password: <a real generated password>
```

## Run

```bash
ansible-playbook -i inventory.ini site.yml --ask-vault-pass
```

Dry run first with `--check --diff` before applying against a real host.
