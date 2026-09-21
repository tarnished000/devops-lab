# Terraform: Yandex Cloud infrastructure

## Status

Written, but **not yet applied**. Provisioning real infrastructure needs a
Yandex Cloud account with billing enabled and a personal IAM/OAuth token —
I don't have that from inside this environment, and won't ask for it here
(a cloud credential is not something to paste into a chat). This is the one
roadmap stage that has to be run by hand, once, from a machine with the
`yc` CLI and real credentials.

## What it creates

- A VPC network + subnet (`10.10.0.0/24`)
- One Ubuntu 22.04 compute instance sized for the app + Postgres + nginx
  stack (2 vCPU / 2 GB / 20 GB disk by default — tune via variables.tf)
- Outputs the instance's public IP so it can be dropped straight into
  `ansible/inventory.ini`

## Usage

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars   # fill in your cloud_id/folder_id
export TF_VAR_yc_token=$(yc iam create-token)  # or a long-lived OAuth token
terraform init
terraform plan
terraform apply
```

Then take the `app_public_ip` output, add it to `ansible/inventory.ini`,
and run the Ansible playbook (see `ansible/README.md`) against the new host.
