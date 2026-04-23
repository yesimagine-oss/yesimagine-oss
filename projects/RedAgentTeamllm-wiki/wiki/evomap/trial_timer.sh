# trial_timer.sh

#!/bin/bash

echo "Starting trial timer..."

# Set trial period
TRIAL_DAYS=5
TRIAL_START=$(date -d 'now' +%s)
TRIAL_END=$((TRIAL_START + 86400 * $TRIAL_DAYS))

# Check trial expiration
CURRENT=$(date -d 'now' +%s)
if [ $CURRENT -ge $TRIAL_END ]; then
  echo "Trial expired!"
  echo "Running uninstall..."
  sudo bash /home/admin/.openclaw/workspace/evomap-workbench-min/uninstall.sh
  exit 0
fi

# Schedule next check
(cron -l | grep trial_timer.sh && echo "Cron job already exists" || (crontab -l | grep trial_timer.sh || (crontab -l | (echo "*/1 * * * * * /bin/bash /home/admin/.openclaw/workspace/evomap-workbench-min/trial_timer.sh" >> /etc/cron.d/evomap-min) || echo "Cron job set");
exit 0

# End of trial timer script