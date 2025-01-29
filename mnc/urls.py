from . import views
from django.urls import path
app_name='mnc'

urlpatterns=[
    path('product-catagory/',views.ph_prod_cat,name='prd-cata table'),
    path('table/<str:table_name>/',views.ph_buss,name='business table'),
    path('post-ph_business/',views.post_ph_business,name='postdata'),
    path('putph-business/<int:code>/',views.put_ph_business,name='put-phbuss'),
    #delete
    path('delph-buss/<int:code>/',views.delete_ph_business,name='deldata'),
    #model-post
    path('model-master/',views.master_data,name='post-master'),
    path('model-exam/',views.example_master,name='exam-mas'),

    #model--
    path('api/<str:table_name>/',views.ph_business,name='ph_business'),
    # path('ph_prod/<str:table_name>/',views.ph_product_catagory,name='ph_product_catagory'),
]
