from django.contrib import admin
import os 
import requests
import pandas as pd
from .models import *
import time
import re
import ast
import json
import random
from openpyxl import load_workbook
# Register your models here.
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify
 

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'



class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


def copy_items(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()


copy_items.short_description = 'Copy Items'



@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')

    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_images')
    os.makedirs(temp_dir, exist_ok=True)

     


    def save_model(self, request, obj, form, change):
        obj_file_name= obj.file
        df = pd.read_excel(obj_file_name, sheet_name='Sheet1', engine='openpyxl')

        

        for index, row in df.iterrows():
            id = row["id"]
            name =row["nom d'article"]
            # images = sheet["E" + str(index)]
            brand_name = row["brand_name"]
            brand_id = row['brand_id']
            # product_Group_Id = sheet["F" + str(index)]
            sellingPrice = row['prix']
            discountPrice = row['prix reduction']
            image_src = row['images_prod']
           

            article_id = row['code produit']
            sizes = row['sizes_exist']
            if sizes:
                sizes = sizes
            else:
                sizes="not"
            
            sizes_not_exist = row['sizes_not_exist']
            if sizes_not_exist:
                sizes_not_exist =  sizes_not_exist
            else:
                sizes_not_exist="not"
                


            categoryName = row["category_name"]
            
            description = row["details d'article"]
            
            delivery = row["delivery"]
            rating = row["rating"]
            if rating:
                rating = float(rating)
            else:
                rating = 0
            stock = row["stock"]

            # Use regular expression to extract only the numbers
            if stock:
                pass
                
            else:
                stock = 0


            details = row['product_details_attr']
            image_src = row['images_prod']
            
            if row["images_prod"] :
                image_src ="https://cdn.dsmcdn.com"+ row["images_prod"].split(",")[0].replace("\\","/").replace(" ","")
                image_folder = image_src.split("/")[-3]
                
                local_image_path = image_src 
                # Replace this with the actual path of the image on your computer

                # Construct the path to the media_root directory
                media_root = os.path.join(settings.MEDIA_ROOT, 'images')
                # Construct the path to the media_root directory
                media_root1 = os.path.join(settings.MEDIA_ROOT, image_folder)

                # Create the 'images' directory if it doesn't exist
                if not os.path.exists(media_root):
                    os.makedirs(media_root)
                
                if not os.path.exists(media_root1):
                    os.makedirs(media_root1)

                # Get the image filename from the local path
                filename = os.path.basename(local_image_path)
                image_path = os.path.join(media_root,media_root1, filename)
                 
                print('request image file ..')
                # Copy the image file to the media_root directory
                response=requests.get(local_image_path)
                print("requested..")
                if response.status_code == 200 :
                    print("responsed..")
                    with open(image_path, 'wb') as dest_file:
                        print("opened..")
                        dest_file.write(response.content)
                      

              

                         
                print('check ..',os.path.exists(image_path))
                print('----',image_path)
                if categoryName and os.path.exists(image_path):
                    print('creted cat ..')
                    doesexist = Category.objects.filter(title=categoryName)
                    if len(doesexist) > 0:
                        categoryName=doesexist.first().title
                    else:
                        Category.objects.create(
                            title=categoryName,
                            slug=slugify(categoryName),
                            description=categoryName,
                            image=os.path.join('images',media_root1, filename).replace("/workspace/media_root","")
                        )


                if row['images_prod'] and os.path.exists(image_path):
                    if name:

                        slug = slugify(name)
                        queryset = Item.objects.filter(slug=slug)
                        numbr = 1
                        new_slug = slug
                        random_number = random.randint(0, 10000)
                        if queryset.filter(slug=new_slug).exists():
                        
                            new_slug = f"{slug}-{ random_number }"
                            
                        
                        
                        
                        itemnow = Item.objects.create(
                            title=name,
                            slug=  new_slug,
                            price=sellingPrice,
                            discount_price=discountPrice,
                            category=Category.objects.filter(title=categoryName).first(),
                            label="N",
                            article_id=article_id,
                            stock_no=stock,
                            details= details ,
                            gender="F",
                            description_short=description,
                            description_long=description,
                            tags= details ,
                            image=image_path.replace("/workspace/media_root",""),
                            rating=rating,
                            color_exist="M,S",
                            color_not_exist="F",
                            size_exist=sizes,
                            size_not_exist=sizes_not_exist,
                            wishlist_num=0,
                            opinion_num=0,
                            shipping="2 days",


                        )
                        
                        
                        for image_url in  row['images_prod'].split(",")[1:]:
                            image_src = "https://cdn.dsmcdn.com"+ image_url.replace(" ","")
                            image_folder = image_src.split("/")[-3]
                            print("loopin imgs")
                            local_image_path = image_src 
                            # Replace this with the actual path of the image on your computer

                            # Construct the path to the media_root directory
                            media_root = os.path.join(settings.MEDIA_ROOT, 'images')
                            # Construct the path to the media_root directory
                            media_root1 = os.path.join(settings.MEDIA_ROOT, image_folder)

                            # Create the 'images' directory if it doesn't exist
                            if not os.path.exists(media_root):
                                os.makedirs(media_root)
                                
                            if not os.path.exists(media_root1):
                                os.makedirs(media_root1)

                            # Get the image filename from the local path
                            filename = os.path.basename(local_image_path)
                            image_path = os.path.join(media_root,media_root1, filename)
                                
                            slug_ex=itemnow.slug
                                
                            print("keeping..")
                            # Copy the image file to the media_root directory
                            
                            ImageItem.objects.create(
                                item=Item.objects.filter(slug=slug_ex).first(),
                                slug=slug_ex,
                                image=image_path.replace("/workspace/media_root","") 
                            )
                            print("img item created")
                            response = requests.get(local_image_path)
                            if response.status_code == 200:
                                print("dwnloding img item ..")
                                with open(image_path, 'wb') as dest_file:
                                    print("opened..")
                                    dest_file.write(response.content)
                                    print("dwnloded img item ..")
                                     

                                
              

                
                
                

            
        super().save_model(request, obj, form, change)
             


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
    ]
    list_filter = ['title', 'category']
    search_fields = ['title', 'category']
    prepopulated_fields = {"slug": ("title",)}
    actions = [copy_items]
    list_display = ('id', 'has_coupon', 'coupon_code')  # Customize the displayed columns in the admin list view
   

    def save_model(self, request, obj, form, change):
        
        sizes_list=[]
        colors_list=[]
        sizes_ex=""
        colors_ex=""
        colors_list_not1=[]
        sizes_list_not1=[]
        if  obj.color_exist:
            colors_list = obj.color_exist.replace(" ","").split(',')
            colors_list_not1 = obj.color_not_exist
            colors_ex= obj.color_exist
        
        if  obj.size_exist:
            sizes_list = obj.size_exist.replace(" ","").split(',')
            sizes_list_not1 = obj.size_not_exist
            sizes_ex= obj.size_exist
        
        if sizes_list_not1 and sizes_list:
            list1 = set(sizes_list_not1.replace(" ","").split(','))
            list2 = set(sizes_list)

            unique_to_list1 = [item for item in list1 if item not in list2]
            unique_to_list2 = [item for item in list2 if item not in list1]


            
            sizes_ex = ",".join(unique_to_list2)

 
        # Add each color to the colors array
        
        
        
        if colors_list_not1 and colors_list:
            list1 = set(colors_list_not1.replace(" ","").split(','))
            list2 = set(colors_list)
           
            unique_to_list1 = [item for item in list1 if item not in list2]
            unique_to_list2 = [item for item in list2 if item not in list1]

 
                            
            colors_ex = ",".join(unique_to_list2)
               

              
        obj.size_exist = sizes_ex
        obj.color_exist = colors_ex
        
                 
        
         
        if obj.has_coupon:
            # If has_coupon is True, set a default value for coupon_code
            obj.coupon_code = obj.coupon_code
        else:
            # If has_coupon is False, set coupon_code to None
            obj.coupon_code = None

        super().save_model(request, obj, form, change)


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'is_active'
    ]
    list_filter = ['title', 'is_active']
    search_fields = ['title', 'is_active']
    prepopulated_fields = {"slug": ("title",)}




admin.site.register(GenderCategory)
admin.site.register(ImageItem)
admin.site.register(Banner_category)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Slide)
admin.site.register(Essential)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(WishList)
admin.site.register(TopCategory)