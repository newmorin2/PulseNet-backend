from django.urls import path

from .views import RegisterView,current_user

urlpatterns=[

    path(
        "signup/",
        RegisterView.as_view()
    ),


    path(
        "me/",
        current_user
    )

]