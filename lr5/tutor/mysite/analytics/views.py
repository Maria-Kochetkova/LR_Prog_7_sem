from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from polls.models import Question
from .serializers import QuestionSerializer, QuestionStatsSerializer, ExportSerializer
from .services import AnalyticsService, ChartService, ExportService
import json



# Микросервис 1: Статистика по голосованиям
class QuestionStatsAPI(APIView):
    """API для получения статистики по опросам"""

    def get(self, request):
        question_id = request.GET.get('question_id')

        if question_id:
            # Статистика по конкретному опросу
            stats = AnalyticsService.get_question_stats(question_id)
            if stats:
                return Response(stats)
            return Response(
                {'error': 'Question not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            # Статистика по всем опросам
            all_stats = AnalyticsService.get_all_questions_stats()
            return Response(all_stats)


# Микросервис 2: Поиск и фильтрация опросов
class QuestionSearchAPI(APIView):
    """API для поиска и фильтрации опросов"""

    def get(self, request):
        search_text = request.GET.get('search', '')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        min_votes = request.GET.get('min_votes')
        sort_by = request.GET.get('sort_by', 'pub_date')
        order = request.GET.get('order', 'desc')

        # Конвертируем min_votes в int если он есть
        if min_votes:
            try:
                min_votes = int(min_votes)
            except ValueError:
                min_votes = None

        # Фильтрация
        queryset = AnalyticsService.filter_questions(
            search_text=search_text,
            start_date=start_date,
            end_date=end_date,
            min_votes=min_votes
        )

        # Сортировка
        queryset = AnalyticsService.sort_questions(queryset, sort_by, order)

        # Сериализация
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)


# Микросервис 3: Графики и диаграммы
class ChartAPI(APIView):
    """API для создания графиков"""

    def get(self, request):
        question_id = request.GET.get('question_id')
        chart_type = request.GET.get('type', 'bar')

        if not question_id:
            return Response(
                {'error': 'question_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if chart_type == 'bar':
            # Столбчатая диаграмма в base64
            image_base64 = ChartService.create_bar_chart_base64(question_id)
            if image_base64:
                return Response({
                    'chart_type': 'bar',
                    'image_base64': image_base64,
                    'format': 'image/png'
                })

        elif chart_type == 'pie':
            # Круговая диаграмма SVG
            svg = ChartService.create_pie_chart_svg(question_id)
            if svg:
                return Response({
                    'chart_type': 'pie',
                    'svg': svg,
                    'format': 'image/svg+xml'
                })

        elif chart_type == 'interactive':
            # Интерактивный график Plotly
            chart_json = ChartService.create_interactive_chart(question_id)
            if chart_json:
                return Response({
                    'chart_type': 'interactive',
                    'chart_data': json.loads(chart_json)
                })

        return Response(
            {'error': 'Chart generation failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


# Микросервис 4: Экспорт данных
class ExportAPI(APIView):
    """API для экспорта данных"""

    def get(self, request):
        question_id = request.GET.get('question_id')
        export_format = request.GET.get('format', 'json')
        export_all = request.GET.get('all', 'false').lower() == 'true'

        if export_all:
            # Экспорт всех опросов
            if export_format == 'csv':
                csv_data = ExportService.export_all_to_csv()
                response = HttpResponse(csv_data, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="all_polls.csv"'
                return response
            else:
                all_stats = AnalyticsService.get_all_questions_stats()
                return JsonResponse(all_stats, safe=False, json_dumps_params={'ensure_ascii': False})

        elif question_id:
            # Экспорт конкретного опроса
            if export_format == 'csv':
                csv_data = ExportService.export_to_csv(question_id)
                if csv_data:
                    response = HttpResponse(csv_data, content_type='text/csv')
                    response['Content-Disposition'] = f'attachment; filename="poll_{question_id}.csv"'
                    return response
                return Response(
                    {'error': 'Question not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            else:
                json_data = ExportService.export_to_json(question_id)
                if json_data:
                    return HttpResponse(json_data, content_type='application/json')
                return Response(
                    {'error': 'Question not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            {'error': 'question_id parameter or all=true is required'},
            status=status.HTTP_400_BAD_REQUEST
        )


# Комбинированный API для фронтенда
class PollAnalyticsAPI(APIView):
    """Комбинированный API для аналитики опросов"""

    def get(self, request):
        action = request.GET.get('action', 'stats')

        if action == 'stats':
            question_id = request.GET.get('question_id')
            if question_id:
                stats = AnalyticsService.get_question_stats(question_id)
                if stats:
                    return Response(stats)
                return Response(
                    {'error': 'Question not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        elif action == 'search':
            search_text = request.GET.get('search', '')
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            queryset = AnalyticsService.filter_questions(
                search_text=search_text,
                start_date=start_date,
                end_date=end_date
            )
            serializer = QuestionSerializer(queryset, many=True)
            return Response(serializer.data)

        elif action == 'chart':
            question_id = request.GET.get('question_id')
            if question_id:
                chart_json = ChartService.create_interactive_chart(question_id)
                if chart_json:
                    return Response(json.loads(chart_json))

        return Response(
            {'error': 'Invalid action'},
            status=status.HTTP_400_BAD_REQUEST
        )