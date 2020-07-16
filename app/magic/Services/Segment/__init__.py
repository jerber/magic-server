import os
import analytics

from app.magic.config import settings

analytics.write_key = settings.segment_write_key
analytics.sync_mode = True
