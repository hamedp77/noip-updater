# No-IP Updater

This script simply updates hostnames provided by [No-IP](https://www.noip.com/). No-IP is a DDNS (Dynamic DNS) provider which offers free and paid tier DDNS services.

If you are looking for a pretty solution or something that works flawlessly, this probably isn't the project you're looking for (check [this](https://github.com/pv8/noipy) out). This is more of a learning project for my own Python skills which I also made available on GitHub so it might inspire or help someone in any possible way.

## Usage

In this document we'll go through setting up the script using 3 different methods. These should cover most of the operating systems out there in a way that it's not too much  of a hassle.

1. Docker
2. Pyinstaller
3. Running the script manually (Anywhere you can install Python)

### Dokcer CLI

1. First you should clone the project using `git clone https://github.com/hamedp77/noip-updater.git`
2. The Dockerfile is in the root of the project directory. You can build the docker image using the following command.

   ```bash
   docker build . -t noip-updater
   ```

   You can name your image whatever you want by putting the name after the `-t` option.
3. For running the image you should pass 3 parameters as environment variables.

   - NOIP_EMAIL: which is the email address you use for logging in to No-IP.
   - NOIP_PASSWORD: which is the password for your No-IP account.
   - NOIP_HOSTNAME: which is your No-IP hostname.

   - **Note**: This is far from secure but it's in your local machine and is never shared with anyone. The process of updating the hostname is also using HTTPS so it's encrypted.

4. Now to run the container, do:

   ```bash
   docker run -e NOIP_HOSTNAME=yourhostname -e NOIP_PASSWORD=yourpassword -e NOIP_EMAIL=youremailaddress noip-updater
   ```

### Pyinstaller

This method is using [Pyinstaller](https://pyinstaller.org/) which is a Python package that can be installed using pip. This package  bundles a Python application and all its dependencies into a single package. You can also use alternatives like [py2exe](https://github.com/py2exe/py2exe) or [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe) if you prefere a GUI.

To get started:

1. Make sure you have Python and pip installed on your system.
2. Clone the project using `git clone https://github.com/hamedp77/noip-updater.git`
3. In the root of the project directory create a new file called `.env` and open it with a text editor. Put the content below in the .env file and save it. These are the necessary information for updating No-IP hostnames using the API.

   ```bash
   NOIP_EMAIL=youremailaddress
   NOIP_PASSWORD=yourpassword
   NOIP_HOSTNAME=yourhostname
   ```

   - **WARNING**: Don't forget to fill it with **your own** account information.

4. Install Pyinstaller using `pip install pyinstaller`
5. Install the required packages to run the script using `pip install -r requirements.txt`
6. After the installations, run `pyinstaller <path-to-script> --onefile`.
   - `--onefile` makes the whole thing a single .exe file which you can run manually or schedule to run using windows task scheduler.
   - `<path-to-script>` is the absolute or relative path of the Python script you're trying to convert to .exe.

### Running the script manually (Anywhere you can install Python)

In case none of the above methods work for you or you don't want to install anything extra (besides Python ovbiously) you can run the script manually and keep your hostname up-to-date.

1. Make sure you have Python and pip installed on your system.
2. Clone the project using `git clone https://github.com/hamedp77/noip-updater.git`
3. In the root of the project directory create a new file called `.env` and open it with a text editor. Put the content below in the .env file and save it. These are the necessary information for updating No-IP hostnames using the API.

   ```bash
   NOIP_EMAIL=youremailaddress
   NOIP_PASSWORD=yourpassword
   NOIP_HOSTNAME=yourhostname
   ```

   - **WARNING**: Don't forget to fill it with **your own** account information.

4. Install the required packages to run the script using `pip install -r requirements.txt`
5. Run the script using `python no_ip.py`
