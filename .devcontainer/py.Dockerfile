FROM aaweaver9/py:latest

WORKDIR /app

SHELL ["/bin/zsh", "-c"]

RUN apt-get update && apt-get install -y \
        python3-pip \
        python3-venv \
        libgl-dev \
        libgl-image-display-dev \
        python3-opencv \
    && rm -rf /var/lib/apt/lists/* \
    && if [ -d /app/.venv ]; then rm -rf /app/.venv; fi \
    && python3 -m venv /app/.venv \
    && source /app/.venv/bin/activate \
    && pip install --upgrade pip \
    && apt-get remove -y python3-pip \
    && apt-get remove -y python3-venv \
    && apt-get remove -y libgl-dev \
    && apt-get remove -y libgl-image-display-dev \
    && apt-get clean \
    && apt-get autoremove -y

CMD ["/bin/zsh"]