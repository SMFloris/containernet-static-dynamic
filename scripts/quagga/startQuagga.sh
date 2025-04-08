#!/usr/bin/env bash

while [[ $# -gt 0 ]]; do
  case $1 in
    --hostname) HOSTNAME="$2"; shift ;;
    --interfaces) INTERFACES="$2"; shift ;;
    *) echo "Unknown option: $1" ;;
  esac
  shift
done

# just in case hostname is not provided by docker
if [[ -z "$HOSTNAME" || -z "$INTERFACES" ]]; then
  echo "Usage: $0 --hostname <name> --interfaces <intf1>,<intf2>,...,<intfn>"
  exit 1
fi

IFS=',' read -ra intfs <<< "$INTERFACES"

daemonsConf=$(cat <<EOF
zebra=yes
bgpd=no
ospfd=no
ospf6d=no
ripd=yes
ripngd=no
isisd=no
EOF
)

zebraConf=$(cat <<EOF
hostname $HOSTNAME
password zebra
enable password zebra
log file /var/log/quagga/zebra.log
EOF
)

ripdConf=$(cat <<EOF
hostname $HOSTNAME
password zebra

router rip
EOF
)

for net in "${intfs[@]}"; do
  ripdConf+="
 network $net"
done

ripdConf+="
log file /var/log/quagga/ripd.log
"

echo -e "$daemonsConf" > /etc/quagga/daemons
echo -e "$zebraConf" > /etc/quagga/zebra.conf
echo -e "$ripdConf" > /etc/quagga/ripd.conf

/etc/init.d/quagga restart
