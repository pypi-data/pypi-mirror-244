"""Settings for Member Audit."""

from django.utils.translation import gettext_lazy as _

from app_utils.app_settings import clean_setting

from memberaudit.utils import get_unidecoded_slug

MEMBERAUDIT_APP_NAME = clean_setting(
    "MEMBERAUDIT_APP_NAME", _("Member Audit"), required_type=str
)
"""Name of this app as shown in the Auth sidebar and page titles."""

MEMBERAUDIT_BASE_URL = get_unidecoded_slug(MEMBERAUDIT_APP_NAME)


MEMBERAUDIT_BULK_METHODS_BATCH_SIZE = clean_setting(
    "MEMBERAUDIT_BULK_METHODS_BATCH_SIZE", 500
)
"""Technical parameter defining the maximum number of objects processed per run
of Django batch methods, e.g. bulk_create and bulk_update.
"""

MEMBERAUDIT_DATA_RETENTION_LIMIT = clean_setting(
    "MEMBERAUDIT_DATA_RETENTION_LIMIT", default_value=360, min_value=7
)
"""Maximum number of days to keep historical data for mails, contracts and wallets.
Minimum is 7 day.
"""

# Activate developer mode for additional debug output. Undocumented feature
MEMBERAUDIT_DEVELOPER_MODE = clean_setting("MEMBERAUDIT_DEVELOPER_MODE", False)

MEMBERAUDIT_FEATURE_ROLES_ENABLED = clean_setting(
    "MEMBERAUDIT_FEATURE_ROLES_ENABLED", False
)
"""Feature flag to enable or disable the corporation roles feature."""

MEMBERAUDIT_DATA_EXPORT_MIN_UPDATE_AGE = clean_setting(
    "MEMBERAUDIT_DATA_EXPORT_MIN_UPDATE_AGE", 60
)
"""Minimum age of existing export file before next update can be started in minutes."""

MEMBERAUDIT_LOCATION_STALE_HOURS = clean_setting("MEMBERAUDIT_LOCATION_STALE_HOURS", 24)
"""Hours after a existing location (e.g. structure) becomes stale and gets updated
e.g. for name changes of structures.
"""

MEMBERAUDIT_LOG_UPDATE_STATS = clean_setting("MEMBERAUDIT_LOG_UPDATE_STATS", False)
"""When set True will log the update stats at the start of every run
The update stats include the measures durations from the last run per round and section.
"""

MEMBERAUDIT_MAX_MAILS = clean_setting("MEMBERAUDIT_MAX_MAILS", 250)
"""Maximum amount of mails fetched from ESI for each character."""

MEMBERAUDIT_NOTIFY_TOKEN_ERRORS = clean_setting("MEMBERAUDIT_NOTIFY_TOKEN_ERRORS", True)
"""When enabled will automatically notify users when their character has a token error.
But only once per character until the character is re-registered or this notification
is reset manually by admins.
"""

MEMBERAUDIT_UPDATE_STALE_RING_1 = clean_setting("MEMBERAUDIT_UPDATE_STALE_RING_1", 60)
"""Character sections are updated on different schedules, called rings.
Ring 1 is the quickest, Ring 3 is the slowest
Settings define after how many minutes a section is considered stale.

Minutes after which sections belonging to ring 1 are considered stale:
location, online status
"""

MEMBERAUDIT_UPDATE_STALE_RING_2 = clean_setting("MEMBERAUDIT_UPDATE_STALE_RING_2", 240)
"""Minutes after which sections belonging to ring 2 are considered stale,
all except those in ring 1 & 3.
"""

MEMBERAUDIT_UPDATE_STALE_RING_3 = clean_setting("MEMBERAUDIT_UPDATE_STALE_RING_3", 480)
"""Minutes after which sections belonging to ring 3 are considered stale, assets."""

MEMBERAUDIT_UPDATE_STALE_OFFSET = clean_setting("MEMBERAUDIT_UPDATE_STALE_OFFSET", 5)
"""Actual value for considering staleness of a ring will be the above value
minus this offset. Required to avoid time synchronization issues.
"""

MEMBERAUDIT_TASKS_HIGH_PRIORITY = clean_setting(
    "MEMBERAUDIT_TASKS_HIGH_PRIORITY", default_value=3, min_value=1, max_value=9
)
"""Priority for high priority tasks, e.g. user requests an action."""

MEMBERAUDIT_TASKS_MAX_ASSETS_PER_PASS = clean_setting(
    "MEMBERAUDIT_TASKS_MAX_ASSETS_PER_PASS", 2500
)
"""Technical parameter defining the maximum number of asset items processed in each pass
when updating character assets.
A higher value reduces duration, but also increases task queue congestion.
"""

MEMBERAUDIT_TASKS_LOW_PRIORITY = clean_setting(
    "MEMBERAUDIT_TASKS_LOW_PRIORITY", default_value=7, min_value=1, max_value=9
)
"""Priority for low priority tasks, e.g. updating characters."""

MEMBERAUDIT_TASKS_NORMAL_PRIORITY = clean_setting(
    "MEMBERAUDIT_TASKS_NORMAL_PRIORITY", default_value=5, min_value=1, max_value=9
)
"""Priority for normal tasks, e.g. updating characters."""

MEMBERAUDIT_TASKS_TIME_LIMIT = clean_setting("MEMBERAUDIT_TASKS_TIME_LIMIT", 7200)
"""Global timeout for tasks in seconds to reduce task accumulation during outages."""


####################
# Internal settings

# Timeout for caching objects when running tasks in seconds
MEMBERAUDIT_TASKS_OBJECT_CACHE_TIMEOUT = clean_setting(
    "MEMBERAUDIT_TASKS_OBJECT_CACHE_TIMEOUT", 600
)
