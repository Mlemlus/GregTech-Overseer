# GregTech Overseer
> The one stop shop for hosting and monitoring a GTNH server
---
## Features
- **GT machines monitoring:** GT Overseer collects all information it can about connected machines and provides it to you in summarized form.
- **Whole GTNH in one package**: The docker stack includes the GTNH server, GT Overseer and Tailscale which manages networking so you and your friends can easily play together.
- **Trivial setup**: Literally just look down how easy it is to install. 
---
## Installation
1. Download the latest release
2. Unzip it
3. [Configure](#configuration) the `.env` file
4. In `gtnh-server` directory put [downloaded gtnh server](https://downloads.gtnewhorizons.com/ServerPacks/) named `gtnh_server.zip`
	1. To install/restore a world backup from serverutilities put it alongside named `backup.zip`
5. Run inside the folder:
```
docker compose up -d
```
5. While waiting for gtnh_tailscale
	1. Go to [Tailscale Admin Console]([https://login.tailscale.com/admin/machines](https://login.tailscale.com/admin/machines))
	2. On the machine `gtnh` click on three dots
	3. Edit route settings
	4. Enable the subnet (default 10.20.30.0/24)
	5. Save
6. After `docker compose` finishes you can log in
---
## Usage
- When the docker stack is running access the application with your defined IP
	- Default is `http://10.20.30.40/`
- To actually connect machines to GregTech Overseer they have to be connected with a OC computer running the GTOcontroller lua script
![OC Diagram](docs/imgs/OCDiagram.png)
- To run the lua script run commands on the OC Station:
```
wget https://raw.githubusercontent.com/Mlemlus/mlemlus-openprograms/refs/heads/master/gtoverseer/gto_controller.lua

gto_controller.lua
```
- The OC station's terminal should look like this:
![OC Setup](docs/imgs/OCSetup.png)
- In case of crashes just restart the station and run `gto_controller.lua`
 
---
## Configuration
All default configuration is in `.env` file
- Tailscale key can be obtained from the  [Tailscale Admin Console]([https://login.tailscale.com/admin/machines](https://login.tailscale.com/admin/machines))
	- Add device
	- Linux server
	- Generate install script
	- Copy the `auth-key`
```
TS_AUTHKEY=tskey-auth-k3ohAff...
```
- Admin login credentials, `your_nickname` would be your mc nickname, `email` and `password` can be anything
```
ADMIN_USERNAME=your_nickname
ADMIN_EMAIL=your_login
ADMIN_PASSWORD=your_password
```
- GTNH server utilities backups location, specify a path to your local storage so you can access it (and backup your saves ofc)
```
GTNHS_BACKUPS_DIR=/path/to/local/directory
```
- Database data directory, so you can easily do and restore backups
```
POSTGRES_DATA_DIRECTORY_LOCAL=/path/to/local/directory
```
