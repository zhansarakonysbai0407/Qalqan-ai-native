output "service_url" {
  description = "Public URL of the Qalqan Cloud Run service."
  value       = google_cloud_run_v2_service.qalqan.uri
}

output "artifact_registry_repository" {
  description = "Docker repository for Qalqan images."
  value       = google_artifact_registry_repository.qalqan.name
}

output "database_secret_name" {
  description = "Secret Manager secret; add a secret version before deploying the app."
  value       = google_secret_manager_secret.database_url.secret_id
}
