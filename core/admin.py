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
import io

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
        gender_type = obj.gender
        df = pd.read_excel(obj_file_name,  engine='openpyxl')

        
        if obj.label == "A":

            for index, row in df.iterrows():
                id = row["id"]
                name =row["nom d'article"]
                # images = sheet["E" + str(index)]
                brand_name = row["brand_name"]
                brand_id = row['brand_id']
                # product_Group_Id = sheet["F" + str(index)]
                sellingPrice = row['prix']
                discountPrice = row['prix reduction']
                try:
                    image_src = row['images_prod']
                except:
                    image_src = row['chemins photos']

                if not pd.isna(row['code produit']):
                    article_id = row['code produit']
                else:
                    article_id = name.split(" ")[-1]
                
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
                idxn=row["id"]
                
                try:
                        
                    shipping = row["delivery"]
                except:
                    shipping = row["duree de livraison"]
                rating = 0
                # if rating:
                #     rating = float(rating)
                # else:
                #     rating = 0
                # stock = row["stock"]
                stock = +99
                # Use regular expression to extract only the numbers
                # if stock:
                #     pass
                    
                # else:
                #     stock = 0


                details = row['product_details_attr']
                try:
                    image_src = row['images_prod']
                except:
                    image_src = row['chemins photos']

                
                if image_src :
                    image_src ="https://cdn.dsmcdn.com"+ image_src.split(",")[0].replace("\\","/").replace(" ","")
                    image_folder = image_src.split("/")[-3]
                    
                    local_image_path = image_src 
                    # Replace this with the actual path of the image on your computer

                    # Construct the path to the media_root directory
                    media_root = os.path.join(settings.MEDIA_ROOT, 'images')
                    # Construct the path to the media_root directory
                    media_root1 = os.path.join(settings.MEDIA_ROOT,"images_upload_product", image_folder)

                    # Create the 'images' directory if it doesn't exist
                    if not os.path.exists(media_root):
                        os.makedirs(media_root)
                    
                    if not os.path.exists(media_root1):
                        os.makedirs(media_root1)

                    # Get the image filename from the local path
                    filename = os.path.basename(local_image_path)
                    image_path = os.path.join(media_root,media_root1, f"{filename.split('.')[0]}.webp")
                
                    
                    # Copy the image file to the media_root directory
                    # response=requests.get(local_image_path)
                    
                    # if response.status_code == 200 :
                        
                    #     # with open(image_path, 'wb') as dest_file:
                            
                    #     #     dest_file.write(response.content)
                    #     image_data = response.content
                    #     image = Image.open(io.BytesIO(image_data))
                    #     rgba_image = image.convert("RGBA")

                    #     # Create a file path for saving the WebP image
                    #     webp_file_path = os.path.join(media_root,media_root1, f"{filename.split('.')[0]}.webp")

                    #     # Save the RGBA image as WebP
                    #     rgba_image.save(webp_file_path, "WEBP")
                            
                        

                

                            
                    
                    if categoryName:
                        
                        doesexist = Category.objects.filter(title=categoryName)
                        if len(doesexist) > 0:
                            categoryName=doesexist.first().title
                        else:
                            Category.objects.create(
                                title=categoryName,
                                slug=slugify(categoryName),
                                
                                image=image_path.replace("/workspace/media_root","") 
                            )


                    if image_src:
                        if name:

                            slug = slugify(name)
                            queryset = Item.objects.filter(slug=slug)
                            numbr = 1
                            new_slug = slug
                            random_number = random.randint(0, 10000)
                            if queryset.filter(slug=new_slug).exists():
                            
                                new_slug = f"{slug}-{ random_number }"
                                
                            
                            doesexist11 = Item.objects.filter(id_item = idxn)
                            imagepathitem = os.path.join(media_root,"images_upload_product",media_root1, f"{filename.split('.')[0]}.webp")
                            if len(doesexist11) == 0:
                                itemnow = Item.objects.create(
                                    id_item=idxn,
                                    title=name,
                                    slug=  new_slug,
                                    price=sellingPrice,
                                    discount_price=discountPrice,
                                    brand_name=brand_name,
                                    category=Category.objects.filter(title=categoryName).first(),
                                    label="N",
                                    article_id=article_id,
                                    stock_no=stock,
                                    details= details ,
                                    gender=gender_type,
                                    description_short=description,
                                    description_long=description,
                                    tags= details ,
                                    image=imagepathitem.replace("/workspace/media_root",""),
                                    rating=rating,
                                    color_exist="M,S",
                                    color_not_exist="F",
                                    size_exist=sizes,
                                    size_not_exist=sizes_not_exist,
                                    wishlist_num=0,
                                    opinion_num=0,
                                    shipping=shipping,


                                )
                                
                                
                                
                                try:
                                    image_src = row['images_prod']
                                    for image_url in  image_src.split(",")[1:]:
                                        image_src = "https://cdn.dsmcdn.com"+ image_url.replace(" ","")
                                        image_folder = image_src.split("/")[-3]
                                        
                                        local_image_path = image_src 
                                        # Replace this with the actual path of the image on your computer

                                        
                                        
                                        # Create the 'images' directory if it doesn't exist
                                        

                                        # Get the image filename from the local path
                                        filename = os.path.basename(local_image_path)
                                        print(f"{local_image_path}/{filename}")
                                        image_path = os.path.join(media_root,media_root1, f"{filename.split('.')[0]}.webp")
                                        
                                        
                                        # image_path = os.path.join(media_root,media_root1, f"{filename.split('.')[0]}.webp")
                                        slug_ex=itemnow.slug
                                            
                                        
                                        # Copy the image file to the media_root directory
                                        
                                        ImageItem.objects.create(
                                            item=Item.objects.filter(slug=slug_ex).first(),
                                            slug=slug_ex,
                                            image=image_path.replace("/workspace/media_root","") 
                                        )
                                        
                                        # response = requests.get(local_image_path)
                                        # if response.status_code == 200:
                                            
                                        #     # with open(image_path, 'wb') as dest_file:
                                            
                                                
                                        #     #     dest_file.write(response.content)
                                                
                                        #     image_data = response.content
                                        #     image = Image.open(io.BytesIO(image_data))
                                        #     rgba_image = image.convert("RGBA")

                                        #     # Create a file path for saving the WebP image
                                        #     webp_file_path = os.path.join(media_root,media_root1, f"{filename.split('.')[0]}.webp")

                                        #     # Save the RGBA image as WebP
                                        #     rgba_image.save(webp_file_path, "WEBP")
                                except:
                                    image_src = row['chemins photos']
                                    for image_url in  image_src.split(",")[1:]:
                                        image_src = "https://cdn.dsmcdn.com"+ image_url.replace(" ","")
                                        image_folder = image_src.split("/")[-3]
                                        
                                        local_image_path = image_src 
                                        # Replace this with the actual path of the image on your computer

                                        
                                        
                                        # Create the 'images' directory if it doesn't exist
                                        

                                        # Get the image filename from the local path
                                        filename = os.path.basename(local_image_path)
                                         
                                        image_path = os.path.join(media_root,media_root1, f"{filename.split('.')[0]}.webp")
                                        
                                        
                                        # image_path = os.path.join(media_root,media_root1, f"{filename.split('.')[0]}.webp")
                                        slug_ex=itemnow.slug
                                            
                                        
                                        # Copy the image file to the media_root directory
                                        
                                        ImageItem.objects.create(
                                            item=Item.objects.filter(slug=slug_ex).first(),
                                            slug=slug_ex,
                                            image=image_path.replace("/workspace/media_root","") 
                                        )
                                                
        else:
            for index, row in df.iterrows():
                
                id = row["id"]
                try:
                    tar_pro= Item.objects.get(id_item=id)
                except:
                    pass
                
                try:
                    if not pd.isna(row["nom d'article arabe"])  :
                        arabe_title = row["nom d'article arabe"]
                        tar_pro.title_ar=arabe_title
                except:
                    pass
                
                
                try:
                    if not pd.isna(row["nom d'article anglais"])    :
                        english_title = row["nom d'article anglais"]
                        tar_pro.title_en=english_title
                except:
                    pass
                
                try:
                    if not pd.isna(row["product_details_attr_ar"])  :
                        det_ar = row["product_details_attr_ar"]
                        tar_pro.details_ar=det_ar
                except:
                    pass
                
                try:
                    if not pd.isna(row["product_details_attr_en"])  :
                        det_en = row["product_details_attr_en"]
                        tar_pro.details_en=det_en
                except:
                    pass
                
                try:
                    if not pd.isna(row["details d'article"])  :
                        desc = row["details d'article"]
                        tar_pro.description_long=desc
                except:
                    pass
                try:
                    if not pd.isna(row["details d'article arabe"])  :
                        desc_ar = row["details d'article arabe"]
                        tar_pro.description_long_ar=desc_ar
                     
                except:
                    pass
                
                try:
                    if not pd.isna(row["details d'article anglais"])  :
                        desc_en = row["details d'article anglais"]
                        tar_pro.description_long_en=desc_en
                    
                except:
                    pass
                
                
                try:
                    sizes = row['sizes_exist']
                    tar_pro.size_exist=sizes
                except:
                    pass
                try:
                    size_not_exist = row['sizes_not_exist']
                    tar_pro.size_not_exist=size_not_exist
                except:
                    pass
                    
                try:
                    
                
                    price = row['prix']
                    tar_pro.price=price
                except:
                    pass
                    
                
                try:
                    
                
                    pricerid = row['prix reduction']
                    tar_pro.discount_price=pricerid
                except:
                    pass
                try:
                    try:
                        
                        shipping = row["delivery"]
                    except:
                        shipping = row["duree de livraison"]
                        
                    tar_pro.shipping=shipping
                
                except:
                    pass
                
               
                
                try:
                    details =row['product_details_attr']
                    tar_pro.details=details
                
                except:
                    pass
                
                try:
                    tar_pro.save()
                except:
                    pass
                print("modified")
                                     

                                    
                

                    
                    
                    

            
        super().save_model(request, obj, form, change)
             



 


 
 
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
    ]
    list_filter = ['title', 'category']
    search_fields = ['title', 'description_long']
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

class CategoryGenTopAdmin(admin.ModelAdmin):
    
    
    prepopulated_fields = {"slug": ("title",)}
    
    def save_model(self, request, obj, form, change):
        if obj.title.lower() in ["hommes", "homme","man","men"]:
            obj.slug = "/shop?gender=M"
        elif obj.title.lower() in ["femmes", "femme","women","woman"]:
            obj.slug = "/shop?gender=F"
        elif obj.title.lower() in ["enfants", "enfant","kids","kid"]:
            obj.slug = "/shop?gender=E"
        else:
            slug1="/shop?topcat="
            try:
                if len(obj.items.all()) == 1:
                  
                    slug1= slug1 +  obj.items.first().slug
                elif len(obj.items.all()) > 1:
                    for item in obj.items.all():
                        slug1 += "_" +item.slug
                obj.slug=slug1 
            except:
                obj.slug = obj.title
        super().save_model(request, obj, form, change)


admin.site.register(GenderCategory,CategoryGenTopAdmin)
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
admin.site.register(TopCategory,CategoryGenTopAdmin)
# admin.site.register(ShopHeader)
admin.site.register(Matacor_info)
admin.site.register(Images_upload)
admin.site.register(NewsLetterEmails)
admin.site.register(Comments_and_Ratings)
admin.site.register(Profile)
 
 