# raven-bash
Raven Sentry client for Bash.

This script is currently in working beta. Use at your own risk.

![Sentry screenshot](https://upx.cz/yll8sbt7jsm991cssgoieb0akdpkl799lk3cea55)

## Installation
```shell
pip install raven-bash
```

## Usage
1. Create the file `/etc/raven-bash.conf` with the following content:
  ```
  [DEFAULT]
  
  # replace with your DSN
  SENTRY_DSN = https://key:secret@your_sentry_domain/project_id
  ```
  Additionally you can use `SENTRY_DSN` environment variable which will override any settings defined in configuration file.

2. Add `source raven-bash` to the beginning of your bash scripts, e.g.:
  ```bash
  #!/bin/bash
  source raven-bash  # sentry reporting
  
  echo "Hello world!"
  echo "This will produce an error" | grep "success"
  ```
  
  Scripts you include using `source` or `.` will be monitored automatically. Any other scripts you execute won't be monitored unless you add `source raven-bash` to them.
  
## Caveats

* "traceback" works only for the last included file
* Unrelated package versions are added to the request. This is due to `raven-python` and will be hopefully fixed in one of the future releases
