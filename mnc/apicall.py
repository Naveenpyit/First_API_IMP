from datetime import timedelta
from django.shortcuts import render
from .dbconnect import api_methods
from django.http.response import JsonResponse
from .authentication import apikeycheck
from rest_framework.decorators import api_view,authentication_classes # type: ignore
from rest_framework import status # type: ignore
from .serializer import serialize_data,master_serial,example_serial,main_serial
from .models import New_main_table
import os
import json
from django.conf import settings
from django.utils import timezone



class api_calls:
    @staticmethod
    def get_common(table_name,query):
        try:
            master_obj, created = New_main_table.objects.get_or_create(Table_Name=table_name)

            current_time = timezone.now()
            local_time = timezone.localtime(current_time)  

            duration_time = int(master_obj.Duration)  

            if created or (local_time - master_obj.Last_Update > timedelta(hours=duration_time)):

                data = api_methods.get(query)

                if not data:
                    fail_data = {
                        "Result": 0,
                        "Message": "Fail to get",
                        "Api-result": "No Records!"
                    }
                    return fail_data

                serial_data = serialize_data.serial_data(data)

                master_obj.Last_Update = local_time
                master_obj.New_Update = 'Yes'
                master_obj.save()

                file_path = os.path.join(settings.BASE_DIR, 'Datas_file', f'{table_name}.txt')
                if not os.path.exists(os.path.join(settings.BASE_DIR, 'Datas_file')):
                    os.makedirs(os.path.join(settings.BASE_DIR, 'Datas_file'))

                with open(file_path, 'w') as file:
                    json.dump(serial_data, file, indent=3)

                success_data = {
                    "Result": 1,
                    "Message": "Success",
                    "Api-result": serial_data
                }
                return success_data


            file_path = os.path.join(settings.BASE_DIR, 'Datas_file', f'{table_name}.txt')
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                success_data = {
                    "Result": 1,
                    "Message": "Success",
                    "Api-result": data
                }
                return success_data

            return {
                "Result": 0,
                "Message": "File or data not found",
                "Api-result": "No Records!"
            }

        except Exception as err:
            return {
                "Result": 0,
                "Message": "Fail to fetch!",
                "Api-result": str(err)
            }
