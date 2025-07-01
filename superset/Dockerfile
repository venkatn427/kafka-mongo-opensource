FROM apache/superset:latest

USER root

# Copy entrypoint and init scripts from current folder (superset/)
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
COPY init.sh /app/init.sh
COPY superset_setup.py /app/superset_setup.py
COPY config/superset_config.py /app/superset_config.py

RUN chmod +x /app/docker-entrypoint.sh /app/init.sh

USER superset

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["superset", "run", "-h", "0.0.0.0", "-p", "8088"]
