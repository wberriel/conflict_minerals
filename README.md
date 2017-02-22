# conflict_minerals
A script I adapted to find the SEC disclosures of conflict minerals that companies are required to release under filing 13p-1. 

Until an executive order was signed during February 2017, SEC listed companies had to disclose their conflict minerals use. 
I created this script to have an easy way to gain a link to the disclosures in the EDGAR database. Use is simple: 
python3 edgar-pull.py -c $STOCK_TICKER

It will return the http address of the latest filing if it exists. Please note that many companies did not file 13p-1 forms even though 
they are required to by law.
