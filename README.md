# aruba-aos-s-pw-update
A python script for updating Aruba network switch administrator passwords en masse from a CSV file. It does this by leveraging the switch's built-in REST API. This circumvents the need to login to each switch individually to rotate the password manually with any kind of regularity. This script should be used with care as it **will** change administrator passwords to the switch and it will also **write the running config to memory**. It is advised to test the script on a small subset of switches.

## Requirements
To run the script:
- You must have [Python](https://www.python.org/) installed.
- The device you are running the script from must be able to access the switches at the provided IP addresses.
- The switches provided must have their rest-interface enabled. This setting is enable by default on this flavor of Aruba switch.
- All the switches must have the same current administrator password.

## Compatibility
This script is designed to work with the following Aruba switch models:
- Aruba 2530 Switch Series (J9772A, J9773A, J9774A, J9775A, J9776A, J9777A, J9778A, J9779A, J9780A, J9781A, J9782A, J9783A, J9853A, J9854A, J9855A, J9856A, JL070A)
- Aruba 2540 Switch Series (JL354A, JL355A, JL356A, JL357A)
- Aruba 2920 Switch Series (J9726A, J9727A, J9728A, J9729A, J9836A)
- Aruba 2930F Switch Series (JL253A, JL254A, JL255A, JL256A, JL258A, JL259A, JL260A, JL261A, JL262A, JL263A, JL264A, JL557A, JL558A, JL559A, JL692A)
- Aruba 2930M Switch Series (JL319A, JL320A, JL321A, JL322A, JL323A, JL324A, R0M67A, R0M68A)
- Aruba 3810 Switch Series (JL071A, JL072A, JL073A, JL074A, JL075A, JL076A)
- Aruba 5400R zl2 Switch Series (J9821A, J9822A, J9850A, J9851A, JL001A, JL002A, JL003A, JL095A)

## How to use the script
1. Populate the first column in the CSV with the IP addresses of the switch that you want to change. Do not include a header.
2. Edit the global variables USERNAME, OLD_PASS and NEW_PASS to the manager username, current password and desired password.
3. Run the script! It will print debug messages so be sure to review the log and make sure that the password was successfully updated on every switch.
