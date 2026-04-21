# uninstall.sh

#!/bin/bash

echo "Starting uninstall..."

# Uninstall steps

# Remove all files from /opt/evomap-workbench-min/
rm -rf /opt/evomap-workbench-min/

# Remove any cron jobs
if [ -f /etc/cron.d/evomap-min ]; then
  rm -f /etc/cron.d/evomap-min
fi

# Remove package files
if [ -f /opt/evomap-workbench-min/evomap-workbench-min-secure.tar.gz ]; then
  rm -f /opt/evomap-workbench-min/evomap-workbench-min-secure.tar.gz
fi

# Remove startup script
if [ -f /etc/init.d/evomap-min ]; then
  rm -f /etc/init.d/evomap-min
fi

# Remove any scheduled tasks
if [ -f /etc/cron.d/evomap-min ]; then
  rm -f /etc/cron.d/evomap-min
fi

# Verify cleanup
if [ ! -d /opt/evomap-workbench-min ]; then
  echo "Successfully uninstalled"
  exit 0
fi

exit 1

# End of uninstall script