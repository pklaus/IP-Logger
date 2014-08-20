
# IP-Logger

Do you want to know which IPs your computers had during the day / the week / the year?
You may use this Python Tool! It is written for Python 3.2+ and the `server.py` script
depends on [bottle](http://bottlepy.org).

Start the server on a computer that will be available from the Internet:

    ./server.py --server-secret I5au1y9d ./logfile

Call the client whenever you think is the right time to log your IP:

    ./client.py --server-secret I5au1y9d --client-secret V91RS3d7 --name your_name --shelvefile clientlogfile HOSTNAME_OF_SERVER 2000

### More Data Storage Options

Currently the [shelve](https://docs.python.org/3/library/shelve.html) module is used to store information. Here are alternatives:

* Python Standard Library [Persistance Options](https://docs.python.org/3/library/persistence.html):
  * SQlite
    <https://docs.python.org/3/library/sqlite3.html>
    Good option because the schema should be the same at all times. But you need to provide the SQL to create the table etc.
  * dbm (anydbm in Python2.x)
    <https://docs.python.org/3/library/dbm.html>
* MongoDB, CouchDB, ...

### Author

* Philipp Klaus  
  <philipp.l.klaus@web.de>

