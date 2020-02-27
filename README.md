
# Steps to setup
1) Download unbuntu 18.04
2) cd /var/www/
3) git clone https://github.com/unkown512/AggieSTEM-DL-PRODUCTION.git
4) https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-18-04
5) In host config file/virtual host apache add the github name path to `/var/www/<github>/html/....`
6) Make sure you download python 3.6.9 and redirect python to that verison.
7) Also from step 4. Make sure mod wsgi is for python 3!
8) Enable ssl for apache. can try this link https://hostadvice.com/how-to/configure-apache-with-tls-ssl-certificate-on-ubuntu-18/
9) pip install requriments
10) use command `sudo service apache2 restart` after changes
11) `vi /var/log/apache2/error.log` for errors
12) install mysql
13) create a gmail account and update the `/home/aggie/.smtp/credentials` file
14) create a AWS account and a SNS topic. Update the `/home/aggie/.aws/credentials` file
15) update the `/home/aggie/.mysql/creentials` file with login information from mysql
16) If you want to run __init__.py without apache2: see the run_server.py setup from https://github.com/unkown512/AggieSTEM_DL_TEST



