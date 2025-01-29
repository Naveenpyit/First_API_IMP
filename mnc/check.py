from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes # type: ignore
import os
import json
from .models import Example_master,New_main_table
from . import api_methods, serialize_data
from django.conf import settings
from .dbconnect  import api_methods
from .authentication import apikeycheck
from .serializer import serialize_data

@api_view(['GET'])
@authentication_classes([apikeycheck])
def ph_buss(request, table_name):
    try:
        
        master_obj, created = New_main_table.objects.get_or_create(Table_Name=table_name)

        current_time = timezone.now()
        local_time=timezone.localtime(current_time)

        duration_hour = int(master_obj.Duration)

        if created or (local_time - master_obj.Last_Update > timedelta(hours=duration_hour)):

            query = f"Select * from {table_name}"  
            data = api_methods.get(query)
            
            if not data:
                fail_data = {
                    "Result": 0,
                    "Message": "Fails to fetch",
                    "Api-result": "No Records!"
                }
                return JsonResponse(fail_data, safe=False, status=204)

    
            serial_data = serialize_data.serial_data(data)

            master_obj.Last_Update = current_time
            master_obj.New_Update = 'Yes'  
            master_obj.save()

            file_path = os.path.join(settings.BASE_DIR, 'Datas_file', f'{table_name}.txt')
            if not os.path.exists(os.path.join(settings.BASE_DIR, 'Datas_file')):
                os.makedirs(os.path.join(settings.BASE_DIR, 'Datas_file'))

            with open(file_path, 'w') as file:
                json.dump(serial_data, file, indent=4)


            success_data = {
                "Result": 1,
                "Message": "Success",
                "Api-result": serial_data
            }
            return JsonResponse(success_data, safe=False, status=200)

        file_path = os.path.join(settings.BASE_DIR, 'Datas_file', f'{table_name}.txt')
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)
            success_data = {
                "Result": 1,
                "Message": "Success",
                "Api-result": data
            }
            return JsonResponse(success_data, safe=False, status=200)

        fail_data = {
            "Result": 0,
            "Message": "File not found or empty",
            "Api-result": "No Records!"
        }
        return JsonResponse(fail_data, safe=False, status=204)

    except Exception as err:
        return JsonResponse({
            "Result": 0,
            "Message": "Fail to fetch!",
            "Api-result": str(err)
        }, safe=False, status=500)



@api_view(['GET'])
@authentication_classes([apikeycheck])
def ph_buss(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'Datas_file', 'ph_business.txt')
        # print(f"file path:{file_path}")
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)
            success_data = {
                "Result": 1,    
                "Message": "Success",
                "Api-result": data
            }
            return JsonResponse(success_data, safe=False, status=200)

        data = api_methods.get("Select * from ph_business")

        if not data:
            fail_data = {
                "Result": 0,
                "Message": "Fails to fetch",
                "Api-result": "No Records!"
            }
            return JsonResponse(fail_data, safe=False, status=204)

        if not os.path.exists(os.path.join(settings.BASE_DIR, 'Datas_file')):
            os.makedirs(os.path.join(settings.BASE_DIR, 'Datas_file'))

        serial_data = serialize_data.serial_data(data)

        with open(file_path, 'w') as file:
            json.dump(serial_data, file,indent=4)  

        success_data = {
            "Result": 1,
            "Message": "Success",
            "Api-result": serial_data
        }
        return JsonResponse(success_data, safe=False, status=200)

    except Exception as err:
        return JsonResponse({
            "Result": 0,
            "Message": "Fail to fetch!",
            "Api-result": str(err)
        }, safe=False, status=500)