from django.urls import path
from . import api
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    
    path('oficinaambiente/', api.OficinaAmbienteList.as_view()),
    path('oficinaambiente/<int:pk>/', api.OficinaAmbienteDetail.as_view()),
    
    path('user/', api.UserList.as_view()),
    path('user/<int:pk>/', api.UserDetail.as_view()),
    
    path('solicitud/', api.SolicitudList.as_view()),
    path('solicitud/<int:pk>/', api.SolicitudDetail.as_view()),
    
    
    path('caso/', api.CasoList.as_view()),
    path('caso/<int:pk>/', api.CasoDetail.as_view()),
    
    
    path('tipoprocedimiento/', api.TipoProcedimientoList.as_view()),
    path('tipoprocedimiento/<int:pk>/', api.TipoProcedimientoDetail.as_view()), 
    
    
    path('solucioncaso/', api.SolucionCasoList.as_view()),
    path('solucioncaso/<int:pk>/', api.SolucionCasoDetail.as_view()),
    
    
    path('solucioncasotipoprocedimientos/', api.SolucionCasoTipoProcedimientosList.as_view()),
    path('solucioncasotipoprocedimientos/<int:pk>/', api.SolucionCasoTipoProcedimientosDetail.as_view()), 
    
    path('docs/', include_docs_urls(title="Documentacion API")),
   

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
