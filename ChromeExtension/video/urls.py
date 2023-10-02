from django.urls import path
from . import views

urlpatterns = [
    path('video', views.VideoPost.as_view()),
    path('video-chunks', views.VideoChunkView.as_view()),
    path('video/<int:id>', views.AssembleAndRetreieveVideo.as_view()),
    path('complete-video', views.CompleteVideo.as_view()),
    
]