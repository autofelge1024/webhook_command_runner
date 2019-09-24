# Webhook command runner

This module provides a simple method for automatically execution calling scripts when a webhook-call is received.

In the configuration file you define, which script will be called on wich request. e.g.:

```
[webserver-settings]
listen_ip: 127.0.0.1
listen_port: 8080

[/print/hello]
method: GET, POST
command: echo "Hello!"

[/wall/hello]
method: GET, POST
command: wall "Hello!"

[/sleep]
method: GET
command: sleep 5 && wall "Hello!"

[/git/pull/webhook_script_execution]
method: GET
path: /data/scripts/webhook_script_execution
command: git pull
```

To start the webhook command runner simply install it with pip and call `webhook-command-runner`:

```
$ pip3 install webhook-command-runner
$ webhook-command-runner config.ini
```

The configuration has following sections:

## `webserver-settings`:

In this section, the IP-Adress and Port configuration can be done.

## `/request/paths`:

In these sections, it is defined, wich script will be called:
You can define:

- `method`: Which HTTP-Method can be used to trigger the script-execution. Today, `GET`and `POST` are implemented.
- `path`: Optionally, you can define a Filesystem-Path, where the script shall be executed.
- `command`: The command to be executed. 