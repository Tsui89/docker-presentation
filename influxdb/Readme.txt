InfluxDB

InfluxDB is a time series database built from the ground up to handle high write and query loads. InfluxDB is meant to be used as a backing store for any use case involving large amounts of timestamped data, including DevOps monitoring, application metrics, IoT sensor data, and real-time analytics.

InfluxDB Documentation

logo

Using this Image

Running the container

The InfluxDB image exposes a shared volume under /var/lib/influxdb, so you can mount a host directory to that point to access persisted container data. A typical invocation of the container might be:

$ docker run -p 8086:8086 \
      -v $PWD:/var/lib/influxdb \
      influxdb
Modify $PWD to the directory where you want to store data associated with the InfluxDB container.

You can also have Docker control the volume mountpoint by using a named volume.

$ docker run -p 8086:8086 \
      -v influxdb:/var/lib/influxdb \
      influxdb
Exposed Ports

The following ports are important and are used by InfluxDB.

8086 HTTP API port
8083 Administrator interface port, if it is enabled
2003 Graphite support, if it is enabled
The HTTP API port will be automatically exposed when using docker run -P.

The administrator interface is not automatically exposed when using docker run -P and is disabled by default. The adminstrator interface requires that the web browser have access to InfluxDB on the same port in the container as from the web browser. Since -P exposes the HTTP port to the host on a random port, the administrator interface is not compatible with this setting.

The administrator interface is deprecated as of 1.1.0 and will be removed in 1.3.0.

Find more about API Endpoints & Ports here.

Configuration

InfluxDB can be either configured from a config file or using environment variables. To mount a configuration file and use it with the server, you can use this command:

Generate the default configuration file:

$ docker run --rm influxdb influxd config > influxdb.conf
Modify the default configuration, which will now be available under $PWD. Then start the InfluxDB container.

$ docker run -p 8086:8086 \
      -v $PWD/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
      influxdb -config /etc/influxdb/influxdb.conf
Modify $PWD to the directory where you want to store the configuration file.

For environment variables, the format is INFLUXDB_$SECTION_$NAME. All dashes (-) are replaced with underscores (_). If the variable isn't in a section, then omit that part.

Examples:

INFLUXDB_REPORTING_DISABLED=true
INFLUXDB_META_DIR=/path/to/metadir
INFLUXDB_DATA_QUERY_LOG_ENABLED=false
Find more about configuring InfluxDB here

Graphite

InfluxDB supports the Graphite line protocol, but the service and ports are not exposed by default. To run InfluxDB with Graphite support enabled, you can either use a configuration file or set the appropriate environment variables. Run InfluxDB with the default Graphite configuration:

docker run -p 8086:8086 -p 2003:2003 \
    -e INFLUXDB_GRAPHITE_ENABLED=true \
    influxdb
See the README on GitHub for more detailed documentation to set up the Graphite service. In order to take advantage of graphite templates, you should use a configuration file by outputting a default configuration file using the steps above and modifying the [[graphite]] section.

Administrator Interface

The administrator interface is deprecated as of 1.1.0 and will be removed in 1.3.0. It is disabled by default. If needed, it can still be enabled by setting an environment variable like below:

docker run -p 8086:8086 -p 8083:8083 \
    -e INFLUXDB_ADMIN_ENABLED=true \
    influxdb
To use the administrator interface, both the HTTP API and the administrator interface API's must be forwarded to the same port.

HTTP API

Creating a DB named mydb:

$ curl -G http://localhost:8086/query --data-urlencode "q=CREATE DATABASE mydb"
Inserting into the DB:

$ curl -i -XPOST 'http://localhost:8086/write?db=mydb' --data-binary 'cpu_load_short,host=server01,region=us-west value=0.64 1434055562000000000'
Read more about this in the official documentation

CLI / SHELL

Start the container:

$ docker run --name=influxdb -d -p 8086:8086 influxdb
Run the influx client in another container:

$ docker run --rm --link=influxdb -it influxdb influx -host influxdb
At the moment, you cannot use docker exec to run the influx client since docker exec will not properly allocate a TTY. This is due to a current bug in Docker that is detailed in docker/docker#8755.

Image Variants

The influxdb images come in many flavors, each designed for a specific use case.

influxdb:<version>

This is the defacto image. If you are unsure about what your needs are, you probably want to use this one. It is designed to be used both as a throw away container (mount your source code and start the container to start your app), as well as the base to build other images off of. This tag is based off of buildpack-deps. buildpack-deps is designed for the average user of docker who has many images on their system. It, by design, has a large number of extremely common Debian packages. This reduces the number of packages that images that derive from it need to install, thus reducing the overall size of all images on your system.

influxdb:alpine

This image is based on the popular Alpine Linux project, available in the alpine official image. Alpine Linux is much smaller than most distribution base images (~5MB), and thus leads to much slimmer images in general.

This variant is highly recommended when final image size being as small as possible is desired. The main caveat to note is that it does use musl libc instead of glibc and friends, so certain software might run into issues depending on the depth of their libc requirements. However, most software doesn't have an issue with this, so this variant is usually a very safe choice. See this Hacker News comment thread for more discussion of the issues that might arise and some pro/con comparisons of using Alpine-based images.

To minimize image size, it's uncommon for additional related tools (such as git or bash) to be included in Alpine-based images. Using this image as a base, add the things you need in your own Dockerfile (see the alpine image description for examples of how to install packages if you are unfamiliar).

License

View license information for the software contained in this image.

Average Rating:
3 Ratings