FROM ollama/ollama:rocm

COPY ./entrypoint.sh /tmp/entrypoint.sh

WORKDIR /tmp

EXPOSE 11434

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/usr/bin/bash", "entrypoint.sh"]
