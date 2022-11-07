# IDA-Data-Deeder
## Overview
A Python utility to import data into IDA component.

## List of components needs to deployed to import the data
- All IDA Components (Internal Service, Auth Service, OTP Service)
- Data Share Service
- Kernel Key Manager Service (Data Share Service call Key Manager APIs to perform data encryption)
- PMS Service (To onboard partner for performing Authentication for the imported data)
- Websub Service (To publish the onboarded partner details to IDA Service) 


## Steps to Run the Utility 

### Pre-requisites

- Initialize virtualenv:
    ```sh
    virtualenv -p python3 venv_ida_data_seeder
    ```

- Install the python requirements:
    ```sh
    source venv_ida_data_seeder/bin/activate
    pip3 install -r requirements.txt
    deactivate
    ```
- Create a new folder `secrets-store` under data_seeder folder, The folder is used to store the secrets required for the seeder.
	-- Export `uin_hash_salt` table data from `ID_REPO` database from the environment and create an csv file with only id & slat values
	
	-- Example:
	```sh
    1,PwNa9oV+GtusHPxAumIssA== 
    ```
		
- Edit the environment related details in `config/config.toml` file. Refer comments in config file to update the necessary values.

- Data to be import should in a text file with an separator. Default separator is `|`. 
	-- Note:
	```sh
	The column header names in the text file should match with the master id schema field names. 
	```
	-- Mandatory column headers are `language`, `id or vid` 
		

### Run the Utility
```sh
source venv_ida_data_seeder/bin/activate
python3 data_seeder/seeder_main.py
```
