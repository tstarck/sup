
# sup <img src="https://raw.githubusercontent.com/humppa/sup/master/static/favicon.png" alt="sup" />

[dockimg]: https://hub.docker.com/r/tuomasstarck/sup

Sup is tightly-scoped and secure file upload utility with sane defaults and no
cruft. Flask is used for light framework, uWSGI for performance, and Docker for
easy deployment.

Get it from: [https://hub.docker.com/r/tuomasstarck/sup][dockimg]


## Usage

Production deployment uses uWSGI and requires a proxy server which speaks
`uwsgi`. By default *one* worker process is created and port *5000* is used.

    $ docker run [-e ENV_OPTS] -p 5000:5000 -v <confdir>:/conf:ro -v <datadir>:/data tuomasstarck/sup:latest

For development, testing, and simple deployments run `sup.py` inside the
container. In that case the server speaks HTTP and uses port 8000 by default.

    $ docker run [-d/-it] [-e DEBUG=1] -p 8000:8000 -v $(pwd):/app --entrypoint /usr/local/bin/python
        -v <confdir>:/conf:ro -v <datadir>:/data tuomasstarck/sup:latest sup.py


## Configuration

Sup uses following environment variables for configuration:

* `DEBUG': Set true (e.g. `1`) for debug mode.
* `PORT': Change the `uwsgi` server listening port.
* `PROC': Set the number of uWSGI worker processes.

To use a configuration file, mount a directory with `config.yaml` to container
path `/conf`. See `examples/config.yaml` for configuration switches.


## License

[MIT](LICENSE)
