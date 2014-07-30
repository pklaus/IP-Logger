
# IP-Logger

Do you want to know which IPs your computers had during the day / the week / the year?
You may use this Python Tool!

Start the server on a computer that will be available from the Internet:

    ./server.py --server-secret I5au1y9d ./logfile

Call the client whenever you think is the right time to log your IP:

    ./client.py --client-secret V91RS3d7 --server-secret I5au1y9d --name your_name localhost 2000

### ToDo

1. Log IPv4 and IPv6 if available.

### Other Approaches


* It would be also possible to store the information on the client side...

### Data Storage Options

* Python Standard Library [Persistance Options](https://docs.python.org/3/library/persistence.html):
  * SQlite
    <https://docs.python.org/3/library/sqlite3.html>
    Good option because the schema should be the same at all times. But you need to provide the SQL to create the table etc.
  * shelve
    <https://docs.python.org/3/library/shelve.html>
  * dbm (anydbm in Python2.x)
    <https://docs.python.org/3/library/dbm.html>
* MongoDB, CouchDB, ...

### Author

* Philipp Klaus  
  <philipp.l.klaus@web.de>

