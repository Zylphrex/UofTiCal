# UofTiCal
A Python Script for exporting U of T's Acorn Calendar to iCal


### Dependencies (Tested on)
* selenium  2.53.6
* pytz 2016.6.1
* icalendar 3.10
* phantomjs 2.1.1 (optional)
* chromedriver (version depends on your chrome version) (optional)


#### Installing the Dependencies:

###### PhantomJS

`PhantomJS` binaries can be downloaded at http://phantomjs.org/download.html.

Once downloaded, move the executable to the project directory (i.e. into the same folder as uoftical.py)

`chromedriver` binaries can be downloaded at https://sites.google.com/a/chromium.org/chromedriver/downloads

You will need to download the correct version for your version of chrome. Once downloaded, move the executable to the project directory (i.e. into the same folder as uoftical.py)

###### Remaining Dependencies
```
pip3 install -r requirements.txt
```

### Python (Tested on)
* version 3.5.2

### Configurations
Inside the config.json file
* **username** - insert your UTORid login
* **password** - insert your UTORid password
* **browser** - below are the supported options
  * firefox (it seems the latest version 48.0.2 does not work with selenium, so use a older version)
  * chrome (you will need to install `chromedriver` see above)
  * headless (you will need to install `PhantomJS` see above)
* **months** - the number of months you'd like to export, default `8` for September to April
* **sleep** - the number of seconds to wait for the page to load, default `5` adjust depending on your connection
* **verbose** - print out statuses throughout execution
* **outfile** - the name of the output file (use `.ics` for file extension)

### Usage
```
python3 uoftical.py
```
Note that the script may take a while to execute depending on your internet connection so give it some time
