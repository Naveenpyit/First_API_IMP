from django.shortcuts import render
from .dbconnect import api_methods
from django.http.response import JsonResponse
from .authentication import apikeycheck
from rest_framework.decorators import api_view,authentication_classes # type: ignore
from rest_framework import status # type: ignore

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
def ph_buss(request):
    data=api_methods.get("Select * from ph_business")

    if not data:
        fail_data={
            "Result":0,
            "Message":"Fail",
            "Api-result":"No records"
        }
        return JsonResponse(fail_data,safe=False,status=204)
    
    res_data={
        "Result":1,
        "Message":"Success",
        "Api-result":data
    }
    return JsonResponse(res_data,safe=False,status=200)

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



