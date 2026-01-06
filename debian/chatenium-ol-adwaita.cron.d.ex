#
# Regular cron jobs for the chatenium-ol-adwaita package.
#
0 4	* * *	root	[ -x /usr/bin/chatenium-ol-adwaita_maintenance ] && /usr/bin/chatenium-ol-adwaita_maintenance
