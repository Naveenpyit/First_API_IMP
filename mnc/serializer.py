from datetime import date
from .models import Master_Table_Lists,Example_master
from rest_framework.serializers import ModelSerializer # type: ignore

class serialize_data:
    @staticmethod
    def serial_data(data):
        if isinstance(data, list):
            return [serialize_data.serial_data(item) for item in data]
        elif isinstance(data, dict):
            return {key: serialize_data.serial_data(value) for key, value in data.items()}
        elif isinstance(data, date):
            return data.isoformat()  
        return data

class master_serial(ModelSerializer):
    class Meta:
        model=Master_Table_Lists
        fields='__all__'


class example_serial(ModelSerializer):  
    class Meta:
        model=Example_master
        fields='__all__'     