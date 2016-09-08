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

##### Basic Configurations

| Property | Details |
| --- | --- |
| `username` | Your *UTORid*. |
| `password` | Your *UTORid* password. |
| `months` | The number of months you'd like to export, default `8` for September to April. |
| `sleep` | the number of seconds to wait for the page to load, default `5` adjust depending on your connection. |
| `verbose` | Print out statuses throughout execution if set to `true`. Nothing if set to `false`.|
| `outfile` | The name of the output file (use `.ics` for file extension). |
| `driver` | The name of the executable driver file (This is the one you downloaded.) Please place it in the same folder as `uoftical.py`|

##### Browser Configurations
| Options| Note |
| --- | --- |
| `firefox` | It seems the latest version 48.0.2 does not work with selenium, so use a older version. <br> <br> This is probably the easiest option as it requires you to only install Firefox.|
| `chrome` | You will need to install `chromedriver` see above for instructions. <br> <br> For this, you will need to install Google Chrome Browser as well as the driver as detailed above. |
| `headless` | You will need to install `PhantomJS` see above for instructions. <br> <br> This option has no visible GUI, only the command line status should you chose to enable them using the `verbose` property. And you only need the driver as detailed above. |

### Usage
```
python3 uoftical.py
```
Note that the script may take a while to execute depending on your internet connection so give it some time
