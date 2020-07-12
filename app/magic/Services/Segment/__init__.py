import os
import analytics

analytics.write_key = os.getenv('SEGMENT_WRITE_KEY')
analytics.sync_mode = True
