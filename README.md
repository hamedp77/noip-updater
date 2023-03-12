# About this script

This script simply updates hostnames provided by [No-IP](https://www.noip.com/). No-IP is a DDNS (Dynamic DNS) provider which offers free and paid tier DDNS services.

If you are looking for a pretty solution or something that works flawlessly, this probably isn't the project you're looking for (check [this](https://github.com/pv8/noipy) out). This is more of a learning project for my own Python skills which I also made available on GitHub so it might inspire or help someone in any possible way.

## Usage

Before we get to deployment methods and steps, you should know that the proceess is not very elegant or easy and you might need somewhat of a knowledge before getting to it.

Currently, there are 3 methods of deployment if you want to use or test this script.

1. Docker (Linux)
2. Pyinstaller (Windows)
3. Running the script manually (Virtually everywhere)

### Dokcer CLI

1. First you should clone the project using `git clone https://github.com/hamedp77/noip-updater.git`
2. The Dockerfile is in the root of the project directory. You can build the docker image using `sudo docker build . -t noip-updater`. You can name your image whatever you want by putting the name after the `-t` switch.
3. For running the image you should pass 3 parameters as environment variables.
   - EMAIL: which is the email address you use for logging in to No-IP.
   - PASSWORD: which is the password for your No-IP account.
   - HOSTNAME: which is your No-IP hostname.

- **Note**: This is far from secure but it's in your local machine and is never shared with anyone. The process of updating the hostname is also using HTTPS so it's encrypted.

4. Now to run the container, do:

```bash
docker run -e NOIP_HOSTNAME=yourhostname -e NOIP_PASSWORD=yourpassword -e NOIP_EMAIL=youremailaddress noip-updater
```

### Pyinstaller (Windows)

This method is using [Pyinstaller](https://pyinstaller.org/) which is a Python package that can be installed using pip. This package converts Python scripts into Microsoft Windows executable. You can also use alternatives like [py2exe](https://github.com/py2exe/py2exe) or [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe) if you prefere a GUI.

To get started:

1. Make sure you have Python and pip installed on your system.
2. Clone the project using `git clone https://github.com/hamedp77/noip-updater.git`
3. In the root of the project directory create a new file called `.env` and open it with a text editor. Put the content bellow in the .env file and save it. These are the necessary information for updating No-IP hostnames using the API.

```bash
NOIP_EMAIL=youremailaddress
NOIP_PASSWORD=yourpassword
NOIP_HOSTNAME=yourhostname
```

- **WARNING**: Don't forget to fill it with **your own** account information.
- **Note**: Of course this is far from secure but it's in your local machine and is never shared with anyone. The process of updating the hostname is also using HTTPS so it's encrypted.

4. Install Pyinstaller using `pip install pyinstaller`
5. Install the required packages to run the script using `pip install -r requirements.txt`
6. After the installations, run `pyinstaller <path-to-script> --onefile`.
   - `--onefile` makes the whole thing a single .exe file which you can run manually or schedule to run using windows task scheduler.
   - `<path-to-script>` is the absolute or relative path of the Python script you're trying to convert to .exe.
