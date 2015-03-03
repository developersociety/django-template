from blanc_pages import block_admin
from .models import CarouselBlock, CarouselSlide


class CarouselSlideInline(block_admin.StackedInline):
    model = CarouselSlide
    extra = 1


class CarouselBlockAdmin(block_admin.BlockModelAdmin):
    inlines = [CarouselSlideInline]


block_admin.site.register(CarouselBlock, CarouselBlockAdmin)
block_admin.site.register_block(CarouselBlock, 'Advanced')
