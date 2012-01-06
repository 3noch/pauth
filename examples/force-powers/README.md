Quickstart
==========

To start the server for the first time, run this in the top-level directory:

    $ ./server/configure
    $ ./server/start


To start the client, run this:

    $ ./client/start


You'll probably want to run these in separate terminal windows so you
can see each request and response for both.


Starting the Server
===================

To setup the server, you need to go into the `server` directory and
run this:

    $ ./configure

This command will create and initialize the SQLite3 database that the
server uses. It will prompt you for a super-user login and email.
Provide whatever you like.

Now you can start the server like this:

    $ ./start


Configuring the Server
----------------------
You can add your own clients, scopes, and redirection URIs to the
server by going to the following URL (once the server is running):

    http://localhost:8000/admin

You'll be prompted for the super-user credentials you provided earlier
when you setup the database. Enter those and you will be presented
with Django's awesome admin interface for you to tweak things.


Starting the Client
===================

The client doesn't need nearly as much setup as does the server. Go
into the `client` directory and run this:

    $ ./start

Once the client is running, go to this URL to use it:

    http://localhost:8001/


Dependencies
============
Dependencies can be installed with

    pip install -r requirements.txt
* `httplib2` - install with `sudo easy_install httplib2`
