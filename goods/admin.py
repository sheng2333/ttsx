from django.contrib import admin

# Register your models here.
from goods.models import *




class GoodsSKUAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        from ttsx_tasks.ttsx_celery import task_generate_static_index
        task_generate_static_index.delay()
        print('save model...')



    def delete_model(self, request, obj):
        super().delete_model(request, obj)

        from ttsx_tasks.ttsx_celery import task_generate_static_index
        task_generate_static_index.delay()
        print('delete model...')




admin.site.register(GoodsType)
admin.site.register(Goods)
admin.site.register(GoodsSKU,GoodsSKUAdmin)
admin.site.register(GoodsImage)
admin.site.register(GoodSComment)

admin.site.register(IndexGoodsBanner)
admin.site.register(IndexTypeGoodsBanner)
admin.site.register(IndexPromotionBanner)
# admin.site.register(GoodsSKUAdmin)