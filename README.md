# ozbargainpi
A python screen scraper that sends you emails on popular deals from www.ozbargain.com.au.

Instructions:

You will need to configure some of the parameters in runme.py before you proceed.
These parameters are mainly email addresses and the file location for the deals_data file.

You will also need to add an entry to crontab so that runme.py gets executed automatically by cron.
You can edit your crontab as follows:

	$ crontab -e
	
Then add the following line to the bottom of the file:

	*/30 * * * * ~/location/of/runme.py
	
The line above just means that it will run every 30 minutes.

Save and that's it! 

