FROM rabbitmq:3-management

# Define environment variables.
ENV RABBITMQ_USER container
ENV RABBITMQ_PASSWORD container_pwd
ENV RABBITMQ_PID_FILE /var/lib/rabbitmq/mnesia/rabbitmq

ADD rabbitmq/init.sh /init.sh
RUN chmod +x /init.sh
EXPOSE 15672
EXPOSE 5672

# Define default command
CMD ["/init.sh"]