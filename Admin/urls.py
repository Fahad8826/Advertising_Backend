from django.urls import path
from .views import CategoryRetrieveUpdateDestroyView, EditUserByIdView,RegisterView, LoginView, SubCategoryRetrieveUpdateDestroyView,UserList

from .views import CategoryListCreateView, SubCategoryListCreateView, ImageUploadView,ImageUploadDeleteView


urlpatterns = [
    
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/',UserList.as_view(),name='users'),
   path('edit-user/<int:pk>/', EditUserByIdView.as_view(), name='edit-user-by-id'),

     path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    path('subcategories/', SubCategoryListCreateView.as_view(), name='subcategory-list'),
    path('subcategories/<int:pk>/', SubCategoryRetrieveUpdateDestroyView.as_view(), name='subcategory-detail'),

    path('images/', ImageUploadView.as_view(), name='image-upload'),
    path('images/<int:pk>/', ImageUploadDeleteView.as_view(), name='image-delete'),
]
