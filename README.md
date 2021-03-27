# twitter-faunadb
Storing tweets in faunadb for later analyze


Expects 

* FAUNA_KEY - access key to fauna db
* BEARER_TOKEN - twitter bearer token
* DISCORD_WEBHOOK - discord webhook

To run the server use.

```
uvicorn main:app --reload
```

## Todo

* Add CI github actions for health check
* some test cases
* new tags for more twitter scanning
* redeploy on push

### References

* https://twitter-faunadb.friendlyuser.repl.co/