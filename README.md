
# sup

[img]: https://hub.docker.com/r/tuomasstarck/sup

Sup is tightly-scoped and secure file upload utility with sane defaults and no
cruft. Python Flask is used for backend and Docker for easy deployment.

Get it from: [https://hub.docker.com/r/tuomasstarck/sup][img]

# Usage

    $ docker run -it --rm -p 8000:8000 -v <confdir>:/sup:ro -v <datadir>:/data tuomasstarck/sup:latest

## Configuration

FIXME

## License

[MIT](LICENSE)
