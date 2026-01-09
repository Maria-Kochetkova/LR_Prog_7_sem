from django.urls import path
from . import views

app_name = 'analytics'
urlpatterns = [
    # Микросервис 1: Статистика
    path('api/stats/', views.QuestionStatsAPI.as_view(), name='stats_api'),

    # Микросервис 2: Поиск и фильтрация
    path('api/search/', views.QuestionSearchAPI.as_view(), name='search_api'),

    # Микросервис 3: Графики
    path('api/charts/', views.ChartAPI.as_view(), name='charts_api'),

    # Микросервис 4: Экспорт
    path('api/export/', views.ExportAPI.as_view(), name='export_api'),

    # Комбинированный API
    path('api/analytics/', views.PollAnalyticsAPI.as_view(), name='analytics_api'),
]