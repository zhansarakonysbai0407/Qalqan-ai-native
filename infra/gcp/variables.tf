variable "project_id" {
  description = "Google Cloud project ID."
  type        = string
}

variable "region" {
  description = "Cloud Run and Artifact Registry region."
  type        = string
  default     = "asia-southeast1"
}

variable "container_image" {
  description = "Full Artifact Registry image URL including tag."
  type        = string
}
