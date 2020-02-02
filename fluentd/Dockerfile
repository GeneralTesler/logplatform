from fluentd

USER root
RUN fluent-gem install fluent-plugin-s3
RUN fluent-gem install fluent-plugin-kafka

COPY entrypoint.sh /bin/
USER fluent
ENTRYPOINT ["tini",  "--", "/bin/entrypoint.sh"]
CMD ["fluentd"]

