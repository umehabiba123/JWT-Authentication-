from rest_framework import serializers
from django.contrib.auth.models import User

class Userserializers(serializers.ModelSerializer):
    class Meta:
        field = ( id , )