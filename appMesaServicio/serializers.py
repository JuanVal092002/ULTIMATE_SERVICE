from rest_framework import serializers
from .models import *

class OficinaAmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OficinaAmbiente
        fields = '__all__' 
        
        
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 
        
        
        
class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__' 
        
        
        
class CasoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caso
        fields = '__all__'                 
                
                
                
class TipoProcedimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProcedimiento
        fields = '__all__'
        
        
class SolucionCasoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolucionCaso
        fields = '__all__'        
        
        
        
class SolucionCasoTipoProcedimientosSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolucionCasoTipoProcedimientos
        fields = '__all__'                                      
                                