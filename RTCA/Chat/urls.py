# ------------ urls.py ------------
from django.urls import path
from . import views
from .views import LoginView, RegisterView, LogoutView

urlpatterns = [
    path("chat/inbox/", views.MyInbox.as_view(), name="my-inbox"),
    path("chat/history/<int:user_id>/", views.ChatHistory.as_view(), name="chat-history"),
    path("chat/messages/<int:sender_id>/<int:receiver_id>/", views.GetMessages.as_view(), name="get-messages"),
    path("chat/send/", views.SendMessage.as_view(), name="send-message"),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # ... your existing chat URLs ...

]