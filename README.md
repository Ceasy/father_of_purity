
# Father of Purity

This application is designed to help ordinary users to solve basic problems caused in the system operation, such as "Bitrix24 freezing, 1C cache cleaning, restarting print services".

## Working Principle

The application provides a user-friendly interface to help users tackle common system operation issues. Once initiated, the application connects to the server to check for updates. If a newer version is detected, the application prompts the user for an update. The main functionalities include resolving "Bitrix24 freezing", clearing "1C cache", and restarting print services. The application also leverages system utilities to provide notifications to the user and interface with the Windows shell.

## TODO

- [x] Добавить лицензию в констекстое меню "О программе"
- [ ] Уведомления в Windows в низу экрана. Временно отключил notify_user(APP_NAME, "Чистка завершена успешно!") и т.д.
- [ ] Добавить описание в констекстое меню "О программе"
- [ ] Убрать возможность редактировать в поле вывода.
- [ ] Добавить обработку ошибок если сервер не доступен (при обновлении)


## Installation

### Dependencies
The project requires the following Python libraries:
- `tkinter` for the user interface.
- `psutil` for system and process utilities.
- `winshell` for interfacing with Windows shell functionalities.
- `plyer` for accessing device-specific features.
- `requests` for making HTTP requests.

To install these dependencies, run:
```bash
pip install -r requirements.txt
```

## Settings

### Customize `settings.py` file:<br/> 

- Specify your encrypted data: <br/> 
    `KEY = b"YOU KEY"`<br/> 
    `USER = b"YOU_ADMIN_USERNAME"`<br/> 
    `PWD = b"YOU_ADMIN_PASSWORD"`<br/> 

This is the credentials of the administrator account that will be used to run this code. <br/>
In order to generate `KEY, USER, PWD` you need to specify your data and run the script `cryptor_key.py` which will generate 
the key and encrypted data. This data should be saved in `settings.py`

- Replace with your ip server and port:
    `SERVER_URL = "http://192.168.200.157:19343"`


## Usage

To run the application:
```bash
python main.py
```

## Structure

- `main.py`: The entry point for the application which initializes and runs the GUI interface.
- `ui`: Contains components and main app window for the user interface.
- `utils`: Contains utility functions, including a helper for sending notifications to the user.
- `updater`: Contains functionality for checking and applying updates to the application.
- `tests`: Contains test files for the application. Ensure all test files are in the correct format.


## Server Setup on Linux with Nginx

### Installation of Nginx:
```bash
sudo apt update
sudo apt install nginx
```

### Start and enable Nginx:
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Place your files:
Ensure your update files are placed in the directory `/var/www/father_of_purity/`. For example:
- `/var/www/father_of_purity/update_manifest.json`
- `/var/www/father_of_purity/fop-v1.x.x.exe`

Update update_manifest.json file:
- `version` select your actual version app

```bash
{
  "version": "1.0.2"
}
```

### Nginx Configuration:
Edit the default Nginx configuration or create a new one:
```bash
sudo nano /etc/nginx/sites-available/father_of_purity
```

Add or modify the server block to serve your files (change listen port 80 to 19343):<br/> 
`Note:` You can specify any port you want, then you will need to change it in the url as well
```bash
server {
    listen 19343;

    location / {
        alias /var/www/father_of_purity/;
        autoindex on;
    }
}
```

Restart Nginx to apply the changes:
```bash
sudo systemctl restart nginx
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

Copyright (c) [2023] [Alexey Fedotov].

Permission is hereby granted, free of charge, to any person obtaining a copy of the
of this software and associated documentation files ("Futher of purity"), to operate
with the Software without restriction, including without limitation the right to
use, copy, modify, merge, publish, distribute, sublicense and/or sell
copies of the Software and to permit persons to whom the Software is furnished to
to do so subject to the following conditions:

The above copyright notice and this permission notice must be included in all
copies or substantial portions of the Software.

The SOFTWARE is provided "AS IS" WITHOUT WARRANTY OF ANY kind, express or implied, including but not limited to.
IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT
AUTHORS OR OWNERS ARE NOT LIABLE FOR ANY PRETENTIAL, DAMAGE OR OTHER
LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING OUT OF,
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER PERFORMANCE OF THE
Software.

---