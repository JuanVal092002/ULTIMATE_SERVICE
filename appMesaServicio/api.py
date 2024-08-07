# Para la api
from rest_framework import generics
from .models import *
""" from .serializers import UserSerializer, OficinaAmbienteSerializer, SolicitudSerializer """
from .serializers import *


# Clase que permite listar los datos del modelo y crear un elemento
class OficinaAmbienteList(generics.ListCreateAPIView):    
    queryset = OficinaAmbiente.objects.all()
    serializer_class = OficinaAmbienteSerializer
    

# Clase que permite consultar por id, actualizar y eliminar
class OficinaAmbienteDetail(generics.RetrieveUpdateDestroyAPIView):    
    queryset = OficinaAmbiente.objects.all()
    serializer_class = OficinaAmbienteSerializer
    
    
    
# Clase que permite listar los datos del modelo y crear un elemento
class UserList(generics.ListCreateAPIView):    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

# Clase que permite consultar por id, actualizar y eliminar
class UserDetail(generics.RetrieveUpdateDestroyAPIView):    
    queryset = User.objects.all()
    serializer_class = UserSerializer    
        


# Clase que permite listar los datos del modelo y crear un elemento
class SolicitudList(generics.ListCreateAPIView):    
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    

# Clase que permite consultar por id, actualizar y eliminar
class SolicitudDetail(generics.RetrieveUpdateDestroyAPIView):    
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer   
    
    
    
# Clase que permite listar los datos del modelo y crear un elemento
class CasoList(generics.ListCreateAPIView):    
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer
    

# Clase que permite consultar por id, actualizar y eliminar
class CasoDetail(generics.RetrieveUpdateDestroyAPIView):    
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer 
    
    
    
    
    
# Clase que permite listar los datos del modelo y crear un elemento
class TipoProcedimientoList(generics.ListCreateAPIView):    
    queryset = TipoProcedimiento.objects.all()
    serializer_class = TipoProcedimientoSerializer
    

# Clase que permite consultar por id, actualizar y eliminar
class TipoProcedimientoDetail(generics.RetrieveUpdateDestroyAPIView):    
    queryset = TipoProcedimiento.objects.all()
    serializer_class = TipoProcedimientoSerializer    
    
    
    
# Clase que permite listar los datos del modelo y crear un elemento
class SolucionCasoList(generics.ListCreateAPIView):    
    queryset = SolucionCaso.objects.all()
    serializer_class = SolucionCasoSerializer
    

# Clase que permite consultar por id, actualizar y eliminar
class SolucionCasoDetail(generics.RetrieveUpdateDestroyAPIView):    
    queryset = SolucionCaso.objects.all()
    serializer_class = SolucionCasoSerializer    
    
    
    
# Clase que permite listar los datos del modelo y crear un elemento
class SolucionCasoTipoProcedimientosList(generics.ListCreateAPIView):    
    queryset = SolucionCasoTipoProcedimientos.objects.all()
    serializer_class = SolucionCasoTipoProcedimientosSerializer
    

# Clase que permite consultar por id, actualizar y eliminar
class SolucionCasoTipoProcedimientosDetail(generics.RetrieveUpdateDestroyAPIView):    
    queryset = SolucionCasoTipoProcedimientos.objects.all()
    serializer_class = SolucionCasoTipoProcedimientosSerializer 
    
    
    