Subfork Python API
==================

This package provides the Subfork Python API and command line interface.


Installation
------------

The easiest way to install:

```shell
$ pip install subfork
```

Quick Start
-----------

In order to authenticate with the Subfork API, you will first need to create
API access keys for your site at [subfork.com](https://subfork.com).

To use the Subfork Python API your site must have a verified domain. Then
instantiate a client using the site domain and access keys:

```python
import subfork
sf = subfork.get_client(domain=domain, access_key=access_key, secret_key=secret_key)
```

Configuration
-------------

Using the Subfork Python API requires basic authentication. To use
environment variables, set the following:

```shell
$ export SUBFORK_DOMAIN=<site domain>
$ export SUBFORK_ACCESS_KEY=<access key>
$ export SUBFORK_SECRET_KEY=<secret key>
```

To use a shared config file, copy the `example_subfork.yml` file to `subfork.yml`
at the root of your project and make required updates:

```shell
$ cp example_subfork.yml subfork.yml
$ nano subfork.yml
```

Or set `$SUBFORK_CONFIG_FILE` to the path to `subfork.yml`:

```shell
$ export SUBFORK_CONFIG_FILE=/path/to/subfork.yml
```

A minimal `subfork.yml` config file contains the following values:

```yaml
domain: <site domain>
access_key: <access key>
secret_key: <secret key>
```

Basic Commands
--------------

To test the site using the dev server:

```shell
$ subfork run
```

To deploy a site:

```shell
$ subfork deploy -c <comment> [--release]
```

To process tasks:

```shell
$ subfork worker [options]
```

Site Templates
--------------

Site template data is required for testing and deploying sites.

Required:

- `domain` : the domain or hostname of the site (no http)
- `templates` : named list of site template files and routes

Optional:

- `template_folder` : template folder path (default "templates")
- `static_folder` : static file folder path (default "static")
- `auto_minimize` : minimize file contents if possible

For example:

```yaml
domain: example.fork.io
templates:
  index:
    route: /
    file: index.html
  user:
    route: /user/<username>
    file: user.html
```

Data
----

Data is organized into `datatypes` and must be JSON serializable. 

Insert a new datatype record, where `datatype` is the name of the
datatype, and `data` is a dictionary:

```python
sf = subfork.get_client()
sf.get_data(datatype).insert(data)
```

Find data matching a list of search `params` for a given `datatype`:

```python
results = sf.get_data(datatype).find(params)
```

where `params` is a list of `[key, op, value]`, for example:

```python
results = sf.get_data(datatype).find([[key, "=", value]])
```

More info can be found using pydoc:

```shell
$ pydoc subfork.api.data
```

Workers
-------

Workers process tasks created either via API clients or users.
By default, running the `subfork worker` command will pull tasks from a
specified queue and process them.

```shell
$ subfork worker [--queue <queue> --func <pkg.mod.func>]
```

For example:

```shell
$ subfork worker --queue test --func subfork.worker.test
```

Will poll the `test` queue for new tasks, and run the function `subfork.worker.test`.
Workers can also be defined in the `subfork.yml` file, and can contain
more than one worker specification:

```yaml
workers:
  worker1:
    queue: test
    function: subfork.worker.test
  worker2:
    queue: stress
    function: subfork.worker.stress
```

To create a task, pass a function kwargs dict to a named task queue,
for example, to pass `t=3` to worker2 defined above:

```python
sf = subfork.get_client()
task = sf.get_queue("test").create_task({"t": 3})
```

To get the results of completed tasks:

```python
task = sf.get_queue("test").get_task(taskid)
task.get_results()
```

More info can be found using pydoc:

```shell
$ pydoc subfork.api.task
```

Running a worker as a service:

See the `bin/worker` and `services/worker.service` files for an example of how
to set up a systemd worker service. 

Update the ExecStart and Environment settings with the correct values, and copy
the service file to /etc/systemd/system/ and start the service.

```shell
$ sudo cp services/worker.service /etc/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl start worker
$ sudo systemctl enable worker
```

Checking worker logs:

```shell
$ sudo journalctl -u worker -f
```