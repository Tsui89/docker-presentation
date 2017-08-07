FROM influxdb:latest
ARG branch
ARG commit
ARG buildtime
ARG owner
LABEL branch=$branch \
        commit=$commit \
        buildtime=$buildtime \
        owner=$owner 
# put your commands here
COPY demo.sh /opt/
COPY Readme.txt /docs/

ENTRYPOINT ["/entrypoint.sh"]
CMD ["influxd"]
