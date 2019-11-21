#JFrog Artifactory Exporter

```
usage: jae [-h] --url URL --access-token ACCESS_TOKEN [--interval INTERVAL]
           [--ignore-ssl-verification] [--log-level LOG_LEVEL] [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Artifactory URL which will be monitored
  --access-token ACCESS_TOKEN
                        Access token used for authentication against
                        Artifactory
  --interval INTERVAL   Interval in seconds
  --ignore-ssl-verification
  --log-level LOG_LEVEL
                        Log level. It can be DEBUG, INFO, WARNING, ERROR,
                        CRITICAL. Default is INFO
  --port PORT, -p PORT  The port that JAE will listen on. Default is 8998
```
