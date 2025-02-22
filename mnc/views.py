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
from .apicall import api_calls

@api_view(['GET'])
@authentication_classes([apikeycheck])
def ph_prod_cat(request):
    data=api_methods.get("Select * from ph_product_catagory")
    
    if not data:
        fail_data={
        "Result":0,
        "Message":"Fail",
        "Api-result":"No-records!"
        }
        return JsonResponse(fail_data,safe=False,status=204)
    result_data={
        "Result":1,
        "Message":"Success",
        "Api-result":data
    }
    return JsonResponse(result_data,safe=False)

@api_view(['GET'])
@authentication_classes([apikeycheck])
def ph_business(request,table_name):
    try:
        query=f'Select * from {table_name}'

        data=api_calls.get_common(query,table_name)
        print(f"Data returned: {data}") 
        if isinstance(data,dict) and data.get("Result")==0:
            return JsonResponse(data,safe=False,status=204)
        return JsonResponse(data,safe=False,status=200)
    except Exception as err:
         return JsonResponse({"Result": 0, "Message": "Internal Server Error", "Api-result": str(err)}, safe=False, status=500)
    

@api_view(['GET'])
@authentication_classes([apikeycheck])
def ph_product_catagory(request,table_name):
    try:
        query=f'Select * from {table_name}'

        data=api_calls.get_common(query,table_name)
        if isinstance(data,dict) and data.get("Result")==0:
            return JsonResponse(data,safe=False,status=204)
        return JsonResponse(data,safe=False,status=200)
    except Exception as err:
        return JsonResponse(err,safe=False,status=500)
    


@api_view(['POST'])
@authentication_classes([apikeycheck])
def post_ph_business(request):
    try:
        code=request.data.get('code')
        name=request.data.get('name')
        user=request.data.get('user')
        date=request.data.get('date')
        dele=request.data.get('dele')

        if not code or not name or not user or not date or not dele:
            return JsonResponse({
                "Result":0,
                "Message":"Fail to add data",
                "Api-result":"Parameters are must"
            },safe=False,status=400)
        
        query="insert into ph_business(buscode,busname,adduser,adddate,deleted) values(%s,%s,%s,%s,%s)"
        params=(code,name,user,date,dele)

        insert_data=api_methods.post(query,params)

        if "Error" in insert_data:
            return JsonResponse({
                "Result":0,
                "Message":"Fail to add New",
                "Api-result":insert_data["Error"]
            },safe=False,status=400)
        
        return JsonResponse({
            "Result":1,
            "Message":"Success",
            "Api-result":"Data Inserted Successfully"
        },safe=False)
    except Exception as err:
        return JsonResponse({
            "Results":0,
            "Message":"Fails",
            "Api-result":str(err)
        },safe=False,status=500)


@api_view(['PUT'])
@authentication_classes([apikeycheck])
def put_ph_business(request,code):
    try:
        #values
        # code=request.data.get('code')
        name=request.data.get('name')
        user=request.data.get('user')
        date=request.data.get('date')
        dele=request.data.get('dele')

        if not code or not name or not user or not date or not dele:
            return JsonResponse({
                "Result":0,
                "Message":"Fail to add data",
                "Api-result":"Parameters are must"
            },safe=False,status=400)
        
        query="Update ph_business set busname=%s,adduser=%s,adddate=%s,deleted=%s where buscode=%s;"
        params=(name,user,date,dele,code)

        update_data=api_methods.put(query,params)

        if "Error" in update_data:
            return JsonResponse({
                "Result":0,
                "Message":"Fail to Update!",
                "Api-result":update_data["Error"]
            },safe=False,status=400)
        
        return JsonResponse({
            "Result":1,
            "Message":"Updated Succesfully!",
            "Api-result":update_data
        },safe=False,status=201)
    except Exception as err:
        return JsonResponse({
            "Result":0,
            "Message":"Failed To update",
            "Api-result":str(err)
        })

@api_view(['DELETE'])
@authentication_classes([apikeycheck])
def delete_ph_business(request,code):
    try:
        if not code:
            return JsonResponse({
                "Result":0,
                "Message":"Unable To Delete",
                "Api-result":"Code Required to Delete"
            },safe=False,status=404)
        
        query="Delete from ph_business where buscode=%s"
        param=(code,)

        delete_data=api_methods.delete(query,param)

        if "Error" in delete_data:
            return JsonResponse({
                "Result":0,
                "Message":"Fail to Delete data",
                "Api-result":delete_data["Error"]
            },safe=False,status=404)
        
        return JsonResponse({
            "Result":1,
            "Message":"Success",
            "Api-result":delete_data
        },safe=False,status=200)
    except Exception as err:
        return JsonResponse({
            "Result":0,
            "Message":"Failed to Delete",
            "Api-result":str(err)
        },safe=False,status=400)




@api_view(['POST'])
@authentication_classes([apikeycheck])
def master_data(request):
    name=request.data.get('name')
    lasupd=request.data.get('lasupd')
    time=request.data.get('time')
    newupd=request.data.get('newupd')

    res={
        'Table_Name':name,
        'Last_Update':lasupd,
        'Duration':time,
        'New_Update':newupd
    }

    data_serializer = master_serial(data=res)
    
    try:
        if data_serializer.is_valid():
            data_serializer.save()  
            return JsonResponse({"Message": "Data Submitted Successfully!", "data": data_serializer.data}, status=201)
        else:
            return JsonResponse({"Message": "Not Submitted", "Error": data_serializer.errors}, status=400)
    except Exception as err:
        return JsonResponse({"Message": "Error occurred", "Error": str(err)}, status=500)
    



@api_view(['POST'])
@authentication_classes([apikeycheck])
def example_master(request):
    name=request.data.get('name')
    # lasupd=request.data.get('lasupd')
    time=request.data.get('time')
    newupd=request.data.get('newupd')

    current_time = timezone.now()
    local_time=timezone.localtime(current_time)

    res={
        'Table_Name':name,
        'Last_Update':local_time,
        'Duration':time,
        'New_Update':newupd
    }

    data_serializer = example_serial(data=res)
    
    try:
        if data_serializer.is_valid():
            data_serializer.save()  
            return JsonResponse({"Message": "Data Submitted Successfully!", "data": data_serializer.data}, status=201)
        else:
            return JsonResponse({"Message": "Not Submitted", "Error": data_serializer.errors}, status=400)
    except Exception as err:
        return JsonResponse({"Message": "Error occurred", "Error": str(err)}, status=500)
    






#--------------------------------------------------------
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