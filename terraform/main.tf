resource "yandex_vpc_network" "app" {
  name = "devops-lab-network"
}

resource "yandex_vpc_subnet" "app" {
  name           = "devops-lab-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.app.id
  v4_cidr_blocks = ["10.10.0.0/24"]
}

data "yandex_compute_image" "ubuntu" {
  family = var.image_family
}

resource "yandex_compute_instance" "app" {
  name        = var.vm_name
  platform_id = var.vm_platform_id
  zone        = var.zone

  resources {
    cores  = var.vm_cores
    memory = var.vm_memory_gb
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.id
      size     = var.vm_disk_gb
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.app.id
    nat       = true
  }

  metadata = {
    ssh-keys = "deploy:${file(var.ssh_public_key_path)}"
  }
}
