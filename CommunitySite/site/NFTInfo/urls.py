from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.page_home,
         name='page_home'
         ),
    path('interactions',
         views.page_interactions,
         name='page_interactions'
         ),
    path('events',
         views.page_events,
         name='page_events'
         ),
]
