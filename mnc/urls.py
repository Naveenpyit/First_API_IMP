from . import views
from django.urls import path
app_name='mnc'

urlpatterns=[
    path('product-catagory/',views.ph_prod_cat,name='prd-cata table'),
    path('ph-business/',views.ph_buss,name='business table'),
    path('post-ph_business/',views.post_ph_business,name='postdata'),
    path('putph-business/<int:code>/',views.put_ph_business,name='put-phbuss'),
    #delete
    path('delph-buss/<int:code>/',views.delete_ph_business,name='deldata'),
]
