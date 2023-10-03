# Logging

This specification dictates logging requirements for codemodder frameworks. Fameworks need to align on a general design, some important messages to log, and formats. This way, users get a relatively consistent experience, design problems are solved once and only once, and downstream tooling can make assumptions about expected output.

# Output format

The `--log-format` parameter tells the framework whether the output should be human readable by specifying `human` (which is the default) or `json`, which causes each message to be logged as its own self-contained JSON object.

## `human` output

For `human` output, we expect a message like the following:
```
$ ./run-my-codemod.sh (...) /my/project
[starting] 
codemodder: java/1.2
```

Notice there is very little context for the log message. The log message doesn't show the timestamp, origin, thread, or any other contextual metadata. We believe CLI users would prefer a very simple, undecorated set of messages.

## `json` output

For `json` output, we expect a message like the following:

```
$ ./run-my-codemod.sh (...) /my/project
{ "level" : "INFO", "message" : "[starting]" }
{ "level" : "INFO", "message" : "codemodder: java/1.2" }
```

The level should be one of `DEBUG`, `INFO`, or `ERROR`. In general:
 - `ERROR` messages should contain unexpected errors
 - `INFO` should contain information about changes
 - `DEBUG` should contain diagnostic or forensic information

# Verbosity

The `--verbose` flag tells the codemodder framework to emit all log messages, regardless of their level. This flag has nothing to do with the output format, and strictly controls the volume of messages emitted.

# Output streams

Generally, logs are expected to go to `stdout`. When the user specificies that the output format should be `human`, or the default case where no output format is specified, it's preferred that error messages be emitted to `stderr`.

# Message Design

We take inspiration from YAML as a format for designing log messages. Outputting in a YAML-like structure gives us some helpful strategies for how to visualize familiar structures, like lists of files, section breaks, and displaying simple key-value pairs.

# Messages

The following example output shows all the required messages. Frameworks can emit more messages, but the following messages serve as a reasonable first milestone or baseline for good-enough logging to support users and downstream tooling. Most of these messages feel self-explanatory, but the specification can go into more detail over time as actual elicits a clearer vision of what's important.

```
$ ./run-codemodder-codemod.sh -o /tmp/my_project.codetf /tmp/my_project

[startup] 
codemodder: javascript/1.2

[setup]
running: pixee:javascript/limit-readline, pixee:javascript/secure-random
including paths: **/*.js
excluding paths: **/tests/**,**/test.js

[scanning]
codemod: pixee:javascript/limit-readline
scanned: 100 files...
scanned: 200 files...
scanned: 300 files...
failed:
  - /tmp/my_project/file_a
  - /tmp/my_project/file_b
  - /tmp/my_project/file_c
changes:
  - /tmp/my_project/file_d:57,59
  - /tmp/my_project/file_e:194

codemod: pixee:javascript/secure-random
scanned: 100 files...
scanned: 200 files...  
scanned: 300 files...
failed:
  - /tmp/my_project/file_a
  - /tmp/my_project/file_b
  - /tmp/my_project/file_c
changes:
  - /tmp/my_project/file_d:81

[report]
scanned: 356 files
failed: 6 files (3 unique)
changed: 3 changes across 3 files
reported_to: /tmp/my_project.codetf
elapsed: 14050ms 
```