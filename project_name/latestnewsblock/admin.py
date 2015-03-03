from blanc_pages import block_admin
from .models import LatestNewsBlock


block_admin.site.register(LatestNewsBlock)
block_admin.site.register_block(LatestNewsBlock, 'Advanced')
