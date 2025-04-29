from django.urls import path
from .views import quiz_page, check_answer
from .views import register_view, login_view, logout_view, select_category

urlpatterns = [
    path('', select_category, name='select_category'),
    path('quiz/<int:category_id>/<str:difficulty>/<int:num_questions>/', quiz_page, name="quiz_page"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('submit/', check_answer, name="check_answer"),
]
