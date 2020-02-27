
# For Collaborators  
Create a branch and submit pull requests to master.
If the results of a pull request fail to compile or work three times, then pull requests from that colaborator will be suspended. 

# Steps to setup
1. Download unbuntu 18.04
2. cd /var/www/
3. git clone https://github.com/unkown512/AggieSTEM-DL-PRODUCTION.git
4. https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-18-04
  1. In host config file/virtual host apache add the github name path to `/var/www/<github>/html/....`
  2. Make sure you download python 3.6.9 and redirect python to that verison.
  3. Also from step 4. Make sure mod wsgi is for python 3!
5. Enable ssl for apache. can try this link https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-18-04
6. pip install requriments
7. use command `sudo service apache2 restart` after changes
8. `vi /var/log/apache2/error.log` for errors
9. install mysql
10. create a gmail account and update the `/home/aggie/.smtp/credentials` file
11. create a AWS account and a SNS topic. Update the `/home/aggie/.aws/credentials` file
12. update the `/home/aggie/.mysql/creentials` file with login information from mysql
13. If you want to run __init__.py without apache2: see the run_server.py setup from https://github.com/unkown512/AggieSTEM_DL_TEST


 Markup : 1. A numbered list
              1. A nested numbered list
              2. Which is numbered
          2. Which is numbered
