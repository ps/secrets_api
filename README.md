Secrets API
===================
An API used for storing user secrets. Once the API is properly set up on a server
and users are created with '_insert_user()' function, the API can be accessed
by authenticating via HTTP Digest authentication. A live version along with
endpoint descriptions can be found at [api.pawel.pw](http://api.pawel.pw). 

## Requirements ##
The app requires:
- [MongoDB](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/)
- [Flask](http://flask.pocoo.org/)
- [Flask-HTTPAuth](https://flask-httpauth.readthedocs.org/en/latest/)
- [pymongo](https://pypi.python.org/pypi/pymongo/)

## Authentication Description ##
The API is authenticated via HTTP Digest auth as described 
[here](http://en.wikipedia.org/wiki/Digest_access_authentication). Nonces are
generated on the server side only. This implementation does not store
plain text passwords per user (had to modify Flask-HTTPAuth in order to do this) and
instead it stores 'HA1' part of the digest authentication scheme where HA1 = MD5(username:realm:password).
In this implementation, 'Flask-HTTPAuth' has a default realm of "Authorization Required", hence this is
used.

## Potential Improvements ##
There are many things that could have been done here if I spent more time on this. For instance I could
have created one endpoint that would have caught all types of requests. As of right now only 'GET' request
works with the proper HTTP Digest manipulation handled on the client side. Another improvement could
have involved adding one time authentication which would allow future requests to not necessairly 
authenticate all over again. Instead maybe there could be some way to authenticate once and then use
some sort of token that retains the authentication. 


So as mentioned previously, nonces are created on the server side only. This leaves my API vulnerable
to man-in-the-middle attacks. In order to account for this a nonce counter along with a random value (cnonce)
could have been added on the client side which would add complexity to the hash that is being transmitted. 


Another possible improvement for this would be to write my own implementation of HTTP Digest authentication
so that way I would have more control over it.


A different approach to this solution could have been basic HTTP authentication over SSL. With this approach 
we have to pay the price of SSL communication along with certifications. HTTP Digest approach eliminates
such operations along with some factors such as the fact that a password (or hash of password) is not directly
used in the communication. Instead a hash combination is transmitted which then can be recomputed and compared
on the server side. 
