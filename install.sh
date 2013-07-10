#!/bin/bash
echo -en "#!/bin/bash\npython "`basename $(pwd)`"/main.py\n" >../AMCFP.sh
mkdir ../.api
