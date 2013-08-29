#!/bin/bash
echo -en "#!/bin/bash\npython `dirname $0`/main.py \$@\n" >../AMCFP.sh
mkdir ../.api
