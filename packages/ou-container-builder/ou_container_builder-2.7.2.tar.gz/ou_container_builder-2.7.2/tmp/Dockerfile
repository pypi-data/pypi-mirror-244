# ###########
# Build Stage
# ###########


FROM python:3.12-bookworm as base

USER root

ARG TARGETPLATFORM

ENV USER="ou"
ENV UID="1000"
ENV GID="100"
ENV MODULE_CODE="Test"
ENV MODULE_PRESENTATION="1"
ENV HOME="/home/$USER/$MODULE_CODE-$MODULE_PRESENTATION"
ENV SHELL="/bin/bash"

RUN mkdir /home/$USER && useradd -u $UID -g $GID -d $HOME -m -s /bin/bash $USER

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y gcc build-essential curl gnupg

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

RUN curl -fsSL "https://deb.nodesource.com/gpgkey/nodesource.gpg.key" | gpg --dearmor -o "/usr/share/keyrings/nodesource.gpg" && \
    echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_18.x bullseye main" > "/etc/apt/sources.list.d/nodesource.list"

COPY  ["test-requirements.txt", "/usr/share/ou/python/system/requirements-4.txt"]

RUN mkdir -p /usr/share/ou/python/system && \
    echo "pycurl\njupyter_server<4\njupyterlab>=4" > /usr/share/ou/python/system/requirements-0.txt

RUN mkdir -p /usr/share/ou/python/user && \
    echo "pycurl\nipykernel" > /usr/share/ou/python/user/requirements-0.txt

RUN pip wheel --no-cache-dir --extra-index-url=https://www.piwheels.org/simple -w /usr/share/ou/python/system -r /usr/share/ou/python/system/requirements-0.txt -r /usr/share/ou/python/system/requirements-4.txt

RUN pip wheel --no-cache-dir --extra-index-url=https://www.piwheels.org/simple -w /usr/share/ou/python/user -r /usr/share/ou/python/user/requirements-0.txt 


# ############
# Deploy Stage
# ############


FROM python:3.12-bookworm

USER root

ARG TARGETPLATFORM

ENV USER="ou"
ENV UID="1000"
ENV GID="100"
ENV MODULE_CODE="Test"
ENV MODULE_PRESENTATION="1"
ENV HOME="/home/$USER/$MODULE_CODE-$MODULE_PRESENTATION"
ENV SHELL="/bin/bash"

RUN mkdir /home/$USER && useradd -u $UID -g $GID -d $HOME -m -s /bin/bash $USER

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y gcc build-essential curl gnupg

RUN curl -fsSL "https://deb.nodesource.com/gpgkey/nodesource.gpg.key" | gpg --dearmor -o "/usr/share/keyrings/nodesource.gpg" && \
    echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_18.x bullseye main" > "/etc/apt/sources.list.d/nodesource.list"

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y libcurl3-gnutls libcurl3-gnutls-dev gnutls-dev tini

COPY --from=base ["/usr/share/ou/python", "/usr/share/ou/python"]

RUN mkdir -p /var/lib/ou/python && \
    python -m venv /var/lib/ou/python/system && \
    /var/lib/ou/python/system/bin/pip install --no-index --no-deps /usr/share/ou/python/system/*.whl

