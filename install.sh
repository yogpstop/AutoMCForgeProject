#!/bin/bash
DIRNAME=`readlink -mq "$0"`
DIRNAME=`dirname "${DIRNAME}"`
DIRNAME=`basename "${DIRNAME}"`
echo -en '#!/bin/bash\npython "`dirname $0`/'${DIRNAME}'/main.py" $@\n' >`dirname $0`/../AMCFP.sh
mkdir -p "`dirname $0`/../.api"

