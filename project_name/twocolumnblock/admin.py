from blanc_pages import block_admin
from .models import TwoColumnTextBlock


block_admin.site.register(TwoColumnTextBlock)
block_admin.site.register_block(TwoColumnTextBlock, 'Advanced')
