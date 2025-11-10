# DCM

Development Container Manager

## Instructions

### Installation

* `apt install docker.io docker-compose`
* `docker network create devnet`
* `docker-compose up -d`

## Configuring

If no configuration file is specified with `-c <config>` while creating a container, then it looks for config.json in your current working directory.

### Example configuration file
```json
{
	"base_domain": "example.com",
	"mem_limit": "512m",
	"nano_cpus": 500000000,
	"pids_limit": 100,
	"setup_script_path": "/path/to/setup.sh"
}
```
`setup_script_path` is used for running a bash script on the first start of a container. Leaving it blank will skip it.

## License

This project is licensed under the terms of the [MIT license](https://choosealicense.com/licenses/mit/).
See the [LICENSE](LICENSE) file for more information.
