#!/bin/bash

# Copyright (C) 2012,2013 yogpstop
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the
# GNU Lesser General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

DIRNAME=`readlink -mq "$0"`
DIRNAME=`dirname "${DIRNAME}"`
DIRNAME=`basename "${DIRNAME}"`
echo -en '#!/bin/bash\npython2 "`dirname $0`/'${DIRNAME}'/main.py" $@\n' >`dirname $0`/../AMCFP.sh
echo -en 'if [ $? -ne 0 ] ; then read -rs -p "Press any key to exit..." -n1 ; fi' >>`dirname $0`/../AMCFP.sh
mkdir -p "`dirname $0`/../.api"

