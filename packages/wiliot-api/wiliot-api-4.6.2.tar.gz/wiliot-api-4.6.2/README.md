# PyWiliot: wiliot-api #

wiliot-api is a python library for accessing Wiliot's cloud services from Python

## Public Library

### MAC Installation
#### Getting around SSL issue on Mac with Python 3.7 and later versions

Python version 3.7 on Mac OS has stopped using the OS's version of SSL and started using Python's implementation instead. As a result, the CA
certificates included in the OS are no longer usable. To avoid getting SSL related errors from the code when running under this setup you need
to execute Install Certificates.command Python script. Typically you will find it under
~~~~
/Applications/Python\ 3.7/Install\ Certificates.command
~~~~

#### Python 3 on Mac
The default Python version on mac is 2.x. Since Wiliot package requires Python 3.x you should download Python3 
(e.g.  Python3.7) and make python 3 your default.
There are many ways how to do it such as add python3 to your PATH (one possible solution https://www.educative.io/edpresso/how-to-add-python-to-the-path-variable-in-mac) 

#### Git is not working after Mac update
please check the following solution:
https://stackoverflow.com/questions/52522565/git-is-not-working-after-macos-update-xcrun-error-invalid-active-developer-pa


### Installing pyWiliot
````commandline
pip install wiliot-api
````

### Using pyWiliot
Wiliot package location can be found, by typing in the command line:
````commandline
pip show wiliot-api
````
please check out our examples, including:
* [edge](wiliot_api/edge/examples)
* [manufacturing](wiliot_api/manufacturing/examples)
* [platform](wiliot_api/platform/examples)

For more documentation and instructions, please contact us: support@wiliot.com


## Release Notes:

Version 4.6.2:
-----------------
* Added optional parameters to filter returned gateways and bridges


Version 4.5.0:
-----------------
* Added option to change gateway name when updating its configuration
* Added functionality to filter the list of returned pixels by sub strings
* Implemented function to get pixel count
* Added function to batch create assets using a CSV file
* Added a function to get event counts in a time range

Version 4.4.4:
-----------------
* Added support for updating bridges with version 3.16 and newer (MEL)

Version 4.4.3:
-----------------
* Added shipment api support
* Improved post function to handle different type of payload

Version 4.4.2:
-----------------
* Improved support for alternate clouds and regions

Version 4.4.0:
-----------------
* Forcing a token refresh when an access token is less than a minute from expiry
* Added support for alternate clouds and regions
* Streamlined API paths to match between the platform and edge modules

Version 4.3.2:
-----------------
* Added an option to get a binary file from the API
* Added a function for sending actions to a gateway

Version 4.3.1:
-----------------
~~* Added a function for sending actions to a gateway~~

Version 4.3.0:
-----------------
* Change code to match the changes in asset label API endpoint
* All 2xx status code returned by the API are considered a success

Version 4.2.0:
-----------------
* Changed API URLs to support new cloud environment
* Added support for pulling paginated bridge and gateway lists (when an owner has more than 100 bridges/gateways)
* Added a function to update multiple bridges' configuration in one call
* Removed GATEWAY as an association type for location - not supported by the platform
* Requiring at least one pixel to be provided when creating an asset

Version 4.1.2:
-----------------
* Changed additional functions use the metadataFetch API to support larger returned data sets:
    * Get Locations
    * Get zones
    * Get location associations
    * Get zone associations
* Added the ability to associate pixels to zones
* Added the ability to associate bridges and gateways to locations

Version 4.1.0:
-----------------
* Changed get_locations and get_categories to use the metadataFetch API endpoint to support:
    * Fetching more than the first 100 items
    * To return the underlying zones for each location when fetching locations
* Added calls to get, create and delete asset labels
* Changed get_asset function call to use the metdataFetch endpoint for compatibility with the get_assets call
* Removed an unsupported event type (geolocation)

Version 4.0.3:
-----------------
* Changed logic for get_assets in Platform module to remove limitation of only getting back the first 100 assets
* Fixed bug in call to add pixel to asset

Version 4.0.2:
-----------------
* First version


The package previous content was published under the name 'wiliot' package.
for more information please read 'wiliot' package's release notes
  
  
   



