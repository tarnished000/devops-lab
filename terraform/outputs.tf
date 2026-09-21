output "app_public_ip" {
  description = "Public IP of the app VM - add this to ansible/inventory.ini"
  value       = yandex_compute_instance.app.network_interface.0.nat_ip_address
}

output "app_internal_ip" {
  value = yandex_compute_instance.app.network_interface.0.ip_address
}
