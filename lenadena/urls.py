"""
URL configuration for lenadena project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from apis import views
from django.conf import settings

urlpatterns = [
    # path('admin', admin.site.urls),
    path('admin/', admin.site.urls),
    path('user', views.Users),
    path('userInfo', views.UserWithToken),
    path('categoryInfo', views.CategoriesWithToken),
    path('user/<int:uid>', views.UserItem),
    path('login', views.UserLogin),
    path('category', views.Categories),
    path('category/<int:cid>', views.CategoryItem),
    path('subcategory', views.SubCategories),
    path('qty_type', views.QtyTypes),
    path('subcategory/<int:scid>', views.SubCategoryItem),
    path("",include("apis.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# if settings.DEBUG:
# else:
    # urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)