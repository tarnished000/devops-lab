variable "yc_token" {
  description = "Yandex Cloud OAuth or IAM token (pass via TF_VAR_yc_token, never commit)"
  type        = string
  sensitive   = true
}

variable "cloud_id" {
  type        = string
  description = "Yandex Cloud cloud ID"
}

variable "folder_id" {
  type        = string
  description = "Yandex Cloud folder ID"
}

variable "zone" {
  type    = string
  default = "ru-central1-a"
}

variable "vm_name" {
  type    = string
  default = "devops-lab-app"
}

variable "vm_platform_id" {
  type    = string
  default = "standard-v3"
}

variable "vm_cores" {
  type    = number
  default = 2
}

variable "vm_memory_gb" {
  type    = number
  default = 2
}

variable "vm_disk_gb" {
  type    = number
  default = 20
}

variable "ssh_public_key_path" {
  type    = string
  default = "~/.ssh/id_ed25519.pub"
}

variable "image_family" {
  type    = string
  default = "ubuntu-2204-lts"
}
