FROM kathara/quagga

COPY ./startQuagga.sh /scripts/startQuagga.sh

ENV VTYSH_PAGER=more
