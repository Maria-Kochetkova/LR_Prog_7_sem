import json
import csv
import io
import base64
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from django.db.models import Count, Sum, Q
from polls.models import Question, Choice
import pandas as pd


class AnalyticsService:
    """Сервис для аналитики опросов"""

    @staticmethod
    def get_question_stats(question_id):
        """Получить статистику по конкретному опросу"""
        try:
            question = Question.objects.get(id=question_id)
            choices = question.choice_set.all()

            total_votes = question.total_votes
            choices_stats = []

            for choice in choices:
                percentage = 0
                if total_votes > 0:
                    percentage = round((choice.votes / total_votes) * 100, 2)

                choices_stats.append({
                    'choice_text': choice.choice_text,
                    'votes': choice.votes,
                    'percentage': percentage,
                    'choice_id': choice.id
                })

            return {
                'question_id': question.id,
                'question_text': question.question_text,
                'pub_date': question.pub_date,
                'total_votes': total_votes,
                'choices_stats': choices_stats
            }
        except Question.DoesNotExist:
            return None

    @staticmethod
    def get_all_questions_stats():
        """Получить статистику по всем опросам"""
        questions = Question.objects.all()
        result = []

        for question in questions:
            stats = AnalyticsService.get_question_stats(question.id)
            if stats:
                result.append(stats)

        return result

    @staticmethod
    def filter_questions(search_text=None, start_date=None, end_date=None, min_votes=None):
        """Фильтрация и поиск опросов"""
        queryset = Question.objects.all()

        if search_text:
            queryset = queryset.filter(question_text__icontains=search_text)

        if start_date:
            queryset = queryset.filter(pub_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(pub_date__lte=end_date)

        if min_votes is not None:
            # Аннотируем общее количество голосов для каждого вопроса
            queryset = queryset.annotate(
                total_votes_annotation=Sum('choice__votes')
            ).filter(total_votes_annotation__gte=min_votes)

        return queryset

    @staticmethod
    def sort_questions(queryset, sort_by='pub_date', order='desc'):
        """Сортировка опросов"""
        sort_fields = {
            'pub_date': 'pub_date',
            'popularity': 'total_votes_annotation',
            'votes': 'total_votes_annotation',
        }

        if sort_by not in sort_fields:
            sort_by = 'pub_date'

        # Если сортируем по голосам, нужно добавить аннотацию
        if sort_by in ['popularity', 'votes']:
            queryset = queryset.annotate(
                total_votes_annotation=Sum('choice__votes')
            )

        field = sort_fields[sort_by]

        if order == 'asc':
            return queryset.order_by(field)
        else:
            return queryset.order_by(f'-{field}')


class ChartService:
    """Сервис для создания графиков и диаграмм"""

    @staticmethod
    def create_bar_chart_base64(question_id):
        """Создать столбчатую диаграмму и вернуть в base64"""
        stats = AnalyticsService.get_question_stats(question_id)

        if not stats:
            return None

        choices = stats['choices_stats']
        choice_texts = [c['choice_text'] for c in choices]
        percentages = [c['percentage'] for c in choices]
        votes = [c['votes'] for c in choices]

        # Создаем график matplotlib
        plt.figure(figsize=(10, 6))
        bars = plt.bar(choice_texts, percentages, color='skyblue')

        # Добавляем значения на столбцы
        for bar, vote, percentage in zip(bars, votes, percentages):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                     f'{vote} ({percentage}%)', ha='center', va='bottom')

        plt.title(f'Результаты опроса: {stats["question_text"]}')
        plt.xlabel('Варианты ответа')
        plt.ylabel('Процент голосов')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Сохраняем в буфер
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        # Конвертируем в base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return image_base64

    @staticmethod
    def create_pie_chart_svg(question_id):
        """Создать круговую диаграмму в формате SVG"""
        stats = AnalyticsService.get_question_stats(question_id)

        if not stats:
            return None

        choices = stats['choices_stats']
        labels = [c['choice_text'] for c in choices]
        values = [c['votes'] for c in choices]

        # Создаем круговую диаграмму Plotly
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.3,
            textinfo='label+percent',
            hoverinfo='label+value+percent'
        )])

        fig.update_layout(
            title=f'Распределение голосов: {stats["question_text"]}',
            showlegend=True
        )

        # Конвертируем в SVG
        svg = fig.to_image(format='svg')
        return svg.decode('utf-8')

    @staticmethod
    def create_interactive_chart(question_id):
        """Создать интерактивный график Plotly (возвращает JSON)"""
        stats = AnalyticsService.get_question_stats(question_id)

        if not stats:
            return None

        choices = stats['choices_stats']
        labels = [c['choice_text'] for c in choices]
        votes = [c['votes'] for c in choices]
        percentages = [c['percentage'] for c in choices]

        # Создаем столбчатую диаграмму
        fig = go.Figure(data=[
            go.Bar(
                name='Голоса',
                x=labels,
                y=votes,
                text=[f'{p}%' for p in percentages],
                textposition='auto',
                marker_color='lightblue'
            )
        ])

        fig.update_layout(
            title=f'Результаты опроса: {stats["question_text"]}',
            xaxis_title="Варианты ответа",
            yaxis_title="Количество голосов",
            template='plotly_white'
        )

        # Конвертируем в JSON для фронтенда
        return fig.to_json()


class ExportService:
    """Сервис для экспорта данных"""

    @staticmethod
    def export_to_csv(question_id):
        """Экспорт данных опроса в CSV"""
        stats = AnalyticsService.get_question_stats(question_id)

        if not stats:
            return None

        output = io.StringIO()
        writer = csv.writer(output)

        # Заголовок
        writer.writerow(['Опрос', stats['question_text']])
        writer.writerow(['Дата создания', stats['pub_date']])
        writer.writerow(['Всего голосов', stats['total_votes']])
        writer.writerow([])
        writer.writerow(['Вариант ответа', 'Голоса', 'Процент'])

        # Данные
        for choice in stats['choices_stats']:
            writer.writerow([
                choice['choice_text'],
                choice['votes'],
                f"{choice['percentage']}%"
            ])

        return output.getvalue()

    @staticmethod
    def export_to_json(question_id):
        """Экспорт данных опроса в JSON"""
        stats = AnalyticsService.get_question_stats(question_id)
        return json.dumps(stats, default=str, indent=2, ensure_ascii=False)

    @staticmethod
    def export_all_to_csv():
        """Экспорт всех опросов в CSV"""
        all_stats = AnalyticsService.get_all_questions_stats()

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['ID опроса', 'Текст опроса', 'Дата', 'Всего голосов'])

        for stats in all_stats:
            writer.writerow([
                stats['question_id'],
                stats['question_text'],
                stats['pub_date'],
                stats['total_votes']
            ])

        return output.getvalue()