# LM_Scraper
A Scrapy, Selenium, PhantomJS based scraper for LM

First of all setup your MySQL server. Lets assume that you have created a database "pyScraper".

The associated table creation statement for this project can be found in "cTable.txt".

Now you would need Python 2.7.* and the following packages:

<ul>
<li>python-dev</li>
<li>python-setuptools</li>
<li>python-mysqldb</li>
</ul>

Use you package manager to install those. Now, you will have access to the command "easy_install". Use that to install 
"pip" (Python package manager)

<strong>*sudo easy_install pip*</strong>

Now use "pip" to install "scrapy"

<strong>*sudo -H pip install scrapy*</strong>

This scraper is based on PhantomJS 2.0. It wouldn't work with the previous version of PhantomJS, as they don't support
clicking an anchor element. 

Finally you need to plug in your database related info in <strong>"Lamudi/pipelines.py" (Line 11)</strong>.
Thats it!!

Now simply run:
<strong>scrapy crawl lmspider > output 2>&1</strong>

Depending on your bandwidth it will take between 1-2 days to crawl the entire website.

In case a particular listing hasn't been added to the database, the relevant information can be found in "output". 
Don't forget to check it out in the end.