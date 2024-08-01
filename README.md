This project will enable you to display your CUCM devices call statistics into your Grafana dashboard.

1- You need a linux virtual machine with an SFTP server installed on it, you can find many tutorials online on how to get that up and running.

2- Login into your CUCM GUI and navigate to Cisco Unified Serviceability -> Tools -> CDR Management and add a new billing application server.

![image](https://github.com/user-attachments/assets/1a006f34-6653-4ac8-9747-b0351c99439a)

3- SSH to your linux VM and navigate to your SFTP directory , you should begin to see files starting with cdr_* and cmr_* , those are sent by CUCM and contains the calls info.

4- You need to install MariaDB/MYSQL if you don't have one yet, it's recommended to install it in the same VM , and configure a new DB and user/password to use later.

5- Modify the python script to include your DB credentials , the script will login to the DB, create the table and columns.

6- Run the script and if it's working you should see the files with cdr_* are deleted, login to DB and you should see the data inserted.







