
# IP-Logger

Do you want to know which IPs your computers had during the day / the week / the year?
You may use this Python Tool!

Start the server on a computer that will be available from the Internet:

    ./server.py --server-secret I5au1y9d iplog.server.shelve

Call the client whenever you think is the right time to log your IP:

    ./client.py --server-secret I5au1y9d --client-secret V91RS3d7 --name your_name --shelvefile iplog.client.shelve HOSTNAME_OF_SERVER 2000

The result will be logged on the server and on the client in the .shelve files.

### Requirements

IP-Logger is written for Python 3.2+ and the `server.py` script
depends on [bottle](http://bottlepy.org).

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

