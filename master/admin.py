from django.contrib import admin

from master.models import MasterModel, ServiceModel, AvailableSlotsModel, ChoosenSlotsModel, AnketaMasterModel, \
    PhotoMasterModel, PortfolioMasterModel

admin.site.register(MasterModel)
admin.site.register(ServiceModel)
admin.site.register(AvailableSlotsModel)
admin.site.register(ChoosenSlotsModel)
admin.site.register(AnketaMasterModel)
admin.site.register(PhotoMasterModel)
admin.site.register(PortfolioMasterModel)
