#!/usr/bin/env python3

import docker
import secrets
import string
import sys


docker_client = docker.from_env()
exit_main_loop = False

BASE_DOMAIN = "dev.wagoogus.top"


def generate_password(length=10):
	alphabet = string.ascii_lowercase + string.digits
	return ''.join(secrets.choice(alphabet) for _ in range(length))


def create_container(name: str):
	image = "codercom/code-server:latest"
	container_name = f"dev_{name}"
	subdomain = f"{name}.{BASE_DOMAIN}"
	pwd = generate_password()

	try:
		existing = docker_client.containers.list(all=True, filters={"name": container_name})
		if existing:
			print(f"Container '{container_name}' already exists.")
			return
		
		labels = {
			"traefik.enable": "true",
			f"traefik.http.routers.{name}.rule": f"Host(`{subdomain}`)",
			f"traefik.http.routers.{name}.entrypoints": "web",
			f"traefik.http.services.{name}.loadbalancer.server.port": "8080",
			"project": "devhub"
		}

		container = docker_client.containers.run(
			image=image,
			name=container_name,
			detach=True,
			tty=True,
			labels=labels,
			environment={"PASSWORD": pwd},
			ports={"8080/tcp": None},
			volumes={f"/home/code/{name}": {"bind": "/home/coder/project", "mode": "rw"}},
			network="devnet",

			# Resource limits
			mem_limit="512m",
			nano_cpus=500000000, # 1/2 CPU
			pids_limit=100,
			restart_policy={"Name": "always"}
		)

		print(f"Created '{name}' | pass {pwd} | https://{subdomain}")

	except docker.errors.ImageNotFound:
		print(f"Docker image '{image}' not found. Try: docker pull {image}")
	except docker.errors.APIError as e:
		print(f"Docker API error: {e.explanation}")


def delete_container(name: str):
	container_name = f"dev_{name}"
	try:
		container = docker_client.containers.get(container_name)
		container.stop()
		container.remove()
		print(f"Deleted container '{name}'.")
	except docker.errors.NotFound:
		print(f"Container '{name}' not found.")
	except docker.errors.APIError as e:
		print(f"Docker API error: {e.explanation}")


def list_containers():
	containers = docker_client.containers.list(all=True, filters={"label": "project=devhub"})
	if not containers:
		print("No containers found.")
		return
	print("Current containers:")
	for c in containers:
		status = c.status
		name = c.name.removeprefix("dev_")
		host_rule = next(
			(v for k, v in c.labels.items() if k.startswith("traefik.http.routers.") and ".rule" in k),
			"N/A"
		)
		print(f" - {name:20s} | {status:10s} | {host_rule}")


def parse_command(cmd):
	cmd = cmd.split(" ")
	match cmd[0]:
		case "help" | "h":
			print("h, help - list of commands")
			print("e, exit - exit the program")
			print("c, create <name> - Create a new dev container")
			print("d, delete <name> - Delete an existing container")
			print("l, list - List all dev containers")
		case "exit" | "e":
			global exit_main_loop
			exit_main_loop = True
			print("Exiting...")
		case "c" | "create":
			create_container(cmd[1])
		case "d" | "delete":
			delete_container(cmd[1])
		case "l" | "list":
			list_containers()


def main():
	print("h = help, e = exit")
	while not exit_main_loop:
		cmd = input("Enter a command: ")
		parse_command(cmd)
	print("Done.")


if __name__ == "__main__":
	main()
