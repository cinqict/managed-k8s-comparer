output "postgres_pw" {
  value = stackit_postgresflex_user.postgres_user.password
}

output "postgres_user" {
  value = stackit_postgresflex_user.postgres_user.username
}