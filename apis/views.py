from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .serializers import *
from .models import *
from rest_framework.parsers import JSONParser
import json
import string
import random
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

# ALL User GET/POST Single User
@csrf_exempt
def Users(request):
    if request.method == "GET":
        regis = User.objects.all()
        serializer = UserSerializer(regis, many = True)
        return JsonResponse({'message':'success','body':serializer.data}, safe = False, status = 200)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message':'success', 'body':serializer.data}, status=201)
        return JsonResponse({"message":"failed",'error':serializer.errors}, status = 400)
    return HttpResponse("success")

@csrf_exempt
def UserWithToken(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        jsonData = json.loads(json.dumps(data))
        sign_in_token = jsonData['key']
        try:
            if (User.objects.filter(sign_in_token = sign_in_token)).exists():
                user = User.objects.get(sign_in_token = sign_in_token)
                if (user.status == True):
                    serializer = UserSerializer(user)
                    return JsonResponse({'message':'success','body':serializer.data}, status=200)
                else:
                    return JsonResponse({'message':'User not found.','body':serializer.data}, status=200)
            else:
                return JsonResponse({"message":"check provide information", 'body': []},status=200)
        except User.DoesNotExist:
            return JsonResponse({"message":"not found"}, status=404)
    return HttpResponse("success")


@csrf_exempt
def UserLogin(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        jsonData = json.loads(json.dumps(data))
        email = jsonData['email']
        password = jsonData['pwd']
        try:
            if (User.objects.filter(email = email, pwd = password)).exists():
                user = User.objects.get(email = email)
                if (user.status == True):
                    user.fcm_token = jsonData['fcm_token']
                    user.device_token = jsonData['device_token']
                    token = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.ascii_letters) for _ in range(40))
                    user.sign_in_token = token
                    serializer = UserSerializer(user, data = data, partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({"message":"success","body":serializer.data},status=200)
                    return JsonResponse({'message':'invalid credentials'},status=200)
                else:
                    return JsonResponse({'message':'your account will be de-activated. Please Registered another email account...'},status=200)
            else:
                return JsonResponse({"message":"check your email and password"},status=200)
        except User.DoesNotExist:
            return JsonResponse({"message":"not found"}, status=404)
    return HttpResponse("success")

# Single User GET/PUT/PATCH/DELETE
@csrf_exempt
def UserItem(request, uid):
    try:
        registered = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return JsonResponse({"message":"not found",'body':[]},status=404)
    if request.method == 'GET':
        serializer = UserSerializer(registered)
        return JsonResponse({'message':'success','body':serializer.data}, status=200)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(registered, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message':'success','body':serializer.data}, status=201)
        return JsonResponse({'message':'failed','body':{},'error':serializer.errors}, status=400)
    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = UserSerializer(registered,data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data, status=201)
            return JsonResponse({"message": "updated successfully", "uid": uid}, status=201)
        return JsonResponse({'message':'failed','body':{},'error':serializer.errors},status=400)
    elif request.method == 'DELETE':
        registered.delete()
        return JsonResponse({"message":"Delete successfully"},status=204)
    return HttpResponse("success")

@csrf_exempt
def Categories(request):
    if request.method == "GET":
        regis = Category.objects.all()
        serializer = CategorySerializer(regis, many = True)
        return JsonResponse({'message':'success','body':serializer.data}, safe = False, status = 200)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message':'success', 'user':serializer.data}, status=201)
        return JsonResponse({"message":"failed",'error':serializer.errors}, status = 400)
    return HttpResponse("success")

@csrf_exempt
def CategoriesWithToken(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        jsonData = json.loads(json.dumps(data))
        sign_in_token = jsonData['key']
        try:
            if (User.objects.filter(sign_in_token = sign_in_token)).exists():
                user = User.objects.get(sign_in_token = sign_in_token)
                if (user.status == True):
                    regis = Category.objects.all()
                    serializer = CategorySerializer(regis, many = True)
                    return JsonResponse({'message':'success','body':serializer.data}, status=200)
                else:
                    return JsonResponse({'message':'User not found.','body':serializer.data}, status=200)
            else:
                return JsonResponse({"message":"check provide information", 'body': []},status=200)
        except User.DoesNotExist:
            return JsonResponse({"message":"not found"}, status=404)
    return HttpResponse("success")

@csrf_exempt
def CategoryItem(request, cid):
    try:
        registered = Category.objects.get(pk=cid)
    except Category.DoesNotExist:
        return JsonResponse({"message":"not found",'body':[]},status=404)
    if request.method == 'GET':
        serializer = CategorySerializer(registered)
        try:
            if (SubCategory.objects.filter(category_id = cid)).exists():
                subCategory = SubCategory.objects.all()
                serializerSub = SubCategorySerializer(subCategory, many = True)
                # print("data",serializerSub.data)
                return JsonResponse({'message':'success','body':serializer.data,'subcategory':serializerSub.data}, status=200)
            # print("data",serializer.data)
            return JsonResponse({'message':'success','body':serializer.data,'subcategory':[]}, status=200)
        except Category.DoesNotExist:
            return JsonResponse({"message":"not found","body":[]}, status=404)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(registered, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message':'success','body':serializer.data}, status=201)
        return JsonResponse({'message':'failed','body':{},'error':serializer.errors}, status=400)
    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(registered,data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "updated successfully", "cid": cid}, status=201)
        return JsonResponse({'message':'failed','body':"",'error':serializer.errors},status=400)
    elif request.method == 'DELETE':
        registered.delete()
        return JsonResponse({"message":"Delete successfully"},status=204)
    return HttpResponse("success")

@csrf_exempt
def SubCategories(request):
    if request.method == "GET":
        regis = SubCategory.objects.all()
        serializer = SubCategorySerializer(regis, many = True)
        return JsonResponse({'message':'success','body':serializer.data}, safe = False, status = 200)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = SubCategorySerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message':'success', 'user':serializer.data}, status=201)
        return JsonResponse({"message":"failed",'error':serializer.errors}, status = 400)
    return HttpResponse("success")

@csrf_exempt
def SubCategoryItem(request, scid):
    try:
        registered = SubCategory.objects.get(pk=scid)
    except SubCategory.DoesNotExist:
        return JsonResponse({"message":"not found",'body':""},status=404)
    if request.method == 'GET':
        serializer = SubCategorySerializer(registered)
        return JsonResponse({'message':'success','body':serializer.data}, status=200)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SubCategorySerializer(registered, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message':'success','body':serializer.data}, status=201)
        return JsonResponse({'message':'failed','body':"",'error':serializer.errors}, status=400)
    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = SubCategorySerializer(registered,data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "updated successfully", "id": scid}, status=201)
        return JsonResponse({'message':'failed','body':"",'error':serializer.errors},status=400)
    elif request.method == 'DELETE':
        registered.delete()
        return JsonResponse({"message":"Delete successfully",'body':""},status=204)
    return HttpResponse("success")

@csrf_exempt
def QtyTypes(request):
    if request.method == "GET":
        regis = QtyType.objects.all()
        serializer = QtyTypeSerializer(regis, many = True)
        return JsonResponse({'message':'success','body':serializer.data}, safe = False, status = 200)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = QtyTypeSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message':'success', 'user':serializer.data}, status=201)
        return JsonResponse({"message":"failed",'error':serializer.errors}, status = 400)
    return HttpResponse("success")


@csrf_exempt
def OffersData(request):
    if request.method == "GET":
        regis = Offers.objects.all()
        serializer = OffersSerializer(regis, many = True)
        return JsonResponse({'message':'success','body':serializer.data}, safe = False, status = 200)
    return HttpResponse("success")

# image file upload program
class OfferUpload(APIView):
    def post(self, request):
        qs_serializer = OffersSerializer(
            data = {
                "oid": request.data.get("oid"),
                "name": request.data.get("name"),
                "image": request.FILES.get("media"),
                "status": request.data.get("status"),
                "category_id": request.data.get("category_id"),
                "user_id": request.data.get("user_id"),
                "last_date": request.data.get("last_date"),
                "created_at": request.data.get("created_at"),
            },
            context = {"request": request},
        )

        if qs_serializer.is_valid():
            qs_serializer.save()
            return Response(
                {
                    'message':'Media uploaded successfully.',
                    'body':qs_serializer.data
                },
                status= status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'message':qs_serializer.errors,
                    'body':None
                },
                status= status.HTTP_400_BAD_REQUEST
            )

    def get(self, request):
        om = Offers.objects.all()
        om_serializer = OffersSerializer(om, many=True)
        return Response(
                    om_serializer.data,
                status= status.HTTP_200_OK
            )


@csrf_exempt
def CategoryMapWithToken(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        jsonData = json.loads(json.dumps(data))
        sign_in_token = jsonData['key']
        try:
            if (User.objects.filter(sign_in_token = sign_in_token)).exists():
                user = User.objects.get(sign_in_token = sign_in_token)
                if (user.status == True):
                    regis = CategoryMap.objects.all()
                    serializer = CategoryMapSerializer(regis, many = True)
                    return JsonResponse({'message':'success','body':serializer.data}, status=200)
                else:
                    return JsonResponse({'message':'User not found.','body':serializer.data}, status=200)
            else:
                return JsonResponse({"message":"check provide information", 'body': []},status=200)
        except User.DoesNotExist:
            return JsonResponse({"message":"not found"}, status=404)
    return HttpResponse("success")


@csrf_exempt
def CategoryMapInsert(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        jsonData = json.loads(json.dumps(data))
        sign_in_token = jsonData['key']
        try:
            if (User.objects.filter(sign_in_token = sign_in_token)).exists():
                user = User.objects.get(sign_in_token = sign_in_token)
                if (user.status == True):
                    category_id = jsonData['category_id']
                    user_id = jsonData['user_id']
                    cm_serializer = CategoryMapSerializer(
                    data = {
                            "category_id": category_id,
                            "user_id": user_id,
                        },
                        context = {"request": request},
                    )
                    if cm_serializer.is_valid():
                        cm_serializer.save()
                        return JsonResponse({'message':'success','body':cm_serializer.data}, status=200)
                    else:
                        return Response(
                            {
                                'message':cm_serializer.errors,
                                'body':None
                            },
                            status= status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return JsonResponse({'message':'User not found.','body':[]}, status=200)
            else:
                return JsonResponse({"message":"check provide information", 'body': []},status=200)
        except User.DoesNotExist:
            return JsonResponse({"message":"not found"}, status=404)
    return HttpResponse("success")


@csrf_exempt
def InsertSubCategory(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            jsonData = json.loads(json.dumps(data))
            sign_in_token = jsonData["key"]
            if (User.objects.filter(sign_in_token = sign_in_token)).exists():
                user = User.objects.get(sign_in_token = sign_in_token)
                if (user.status == True):
                    if(SubCategory.objects.filter(name = jsonData["subcategory_name"], brand_name = jsonData['brand_name'])).exists():
                        subcategory = SubCategory.objects.get(name = jsonData["subcategory_name"], brand_name = jsonData['brand_name'])
                        subcategory_serializer = SubCategorySerializer(subcategory)
                        category =  Category.objects.get(cid = subcategory_serializer.data['category_id'])
                        category_serializer = CategorySerializer(category)
                        return JsonResponse({"message": "subcategory already exists.","body": category_serializer.data }, status = 200)
                    else:
                        serializer = SubCategorySerializer(data = {
                        'name': jsonData['subcategory_name'],
                        'brand_name': jsonData['brand_name'],
                        'status': jsonData['status'],
                        'category_id': jsonData['category_id'],
                        },context = {"request": request})
                        if serializer.is_valid():
                            serializer.save()
                            serializerMap = SubCategoryMapSerializer(
                                data = {
                                    "sub_category_id": serializer.data['scid'],
                                    "user_id": user.uid,
                                    "description": jsonData['description']
                                },context = {"request": request}
                            )
                            if serializerMap.is_valid():
                                serializerMap.save()
                                return JsonResponse({'message':'success', 'sub_category':serializer.data}, status=200)
                            return JsonResponse({'message':'error', 'sub_category':serializer.data}, status=200)  
                        return JsonResponse({'message':'error', 'sub_category':serializer.data}, status=400)  
                else:
                    return JsonResponse({'message':'User found. but this user is not active','body':[]}, status=200)
            else:
                return JsonResponse({"message":"check provide information", 'body': []},status=200)
        except User.DoesNotExist:
            return JsonResponse({"message":"not found"}, status = 400)
    return HttpResponse("success")

@csrf_exempt
def GetSubcategoryWithCategoryId(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            jsonData = json.loads(json.dumps(data))
            sign_in_token = jsonData["key"]
            if (User.objects.filter(sign_in_token = sign_in_token)).exists():
                user = User.objects.get(sign_in_token = sign_in_token)
                if (user.status == True):
                    if(SubCategory.objects.filter(category_id = jsonData["category_id"])).exists():
                        data = SubCategory.objects.all()
                        serializer = SubCategorySerializer(data, many = True)
                        return JsonResponse({'message':'success','body':serializer.data}, status=200)
                    else:
                        return JsonResponse({'message':'not exists.','body':[]}, status=200)
                    # if(SubCategory.objects.filter(category_id = jsonData["category_id"])).in_bulk():
                    #     subCategory = SubCategory.objects.all()
                    #     serializer = SubCategorySerializer(subCategory, many = True)
                    #     print(serializer.data)
                    #     return JsonResponse({'message':'success','body':serializer.data}, status=200)
                    # else:
                    #     return JsonResponse({'message':'not exists.','body':[]}, status=200)
                else:
                    return JsonResponse({'message':'User found. but this user is not active','body':[]}, status=200)
            else:
                return JsonResponse({"message":"check provide information", 'body': []},status=200)
        except User.DoesNotExist:
            return JsonResponse({"message":"not found"}, status = 400)
    return HttpResponse("success")



# class GroupedByCategoryAPIView(APIView):
#     def get(self, request):
#         products = Product.objects.filter(status=True)
#         grouped_data = defaultdict(list)

#         for product in products:
#             serialized = ProductSerializer(product).data
#             grouped_data[str(product.category_id)].append(serialized)

#         return Response(grouped_data)