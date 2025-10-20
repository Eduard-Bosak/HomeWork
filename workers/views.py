# ========================================
# ИСПРАВЛЕНО: Убраны дублирующие импорты, добавлены нужные
# ========================================
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from .models import Person


# ========================================
# ГЛАВНАЯ СТРАНИЦА (К2, К3, К4 - требования ТЗ)
# ========================================
def home(request):
    """
    КОММЕНТАРИЙ ДЛЯ СТУДЕНТКИ:
    Это представление для главной страницы.
    
    ЧТО ДОЛЖНО БЫТЬ ВЫВЕДЕНО (по ТЗ):
    К3 - Общее количество сотрудников в базе данных
    К4 - Карточки 4-х последних нанятых сотрудников
    К2 - Каждая карточка содержит: имя, фамилию, навыки, первое фото, стаж
    
    КАК РАБОТАЕТ:
    1. .count() - подсчитывает всех сотрудников
    2. .order_by('-employment_date') - сортирует по дате (новые первые)
    3. [:4] - берёт только первые 4 записи
    """
    template_name = 'HomeWork/index.html'
    
    # К3: Получаем общее количество сотрудников
    total_employees = Person.objects.count()
    
    # К4: Получаем 4 последних нанятых сотрудника
    # ИСПРАВЛЕНО: Не используем values_list, а получаем полные объекты
    recent_employees = Person.objects.all().order_by('-employment_date')[:4]
    
    context = {
        'total_employees': total_employees,  # Общее количество
        'recent_employees': recent_employees,  # 4 последних сотрудника
    }
    
    return render(request, template_name, context)


# ========================================
# СПИСОК ВСЕХ СОТРУДНИКОВ (К5, К7 - требования ТЗ)
# ========================================
def list(request):
    """
    КОММЕНТАРИЙ ДЛЯ СТУДЕНТКИ:
    Это представление для списка всех сотрудников с пагинацией.
    
    ЧТО ДОЛЖНО БЫТЬ (по ТЗ):
    К5 - Карточки сотрудников с пагинацией по 10 на странице
    К2 - Каждая карточка: имя, фамилия, навыки, фото, стаж
    К7 - Оптимизация запросов (пока не требуется select_related)
    
    КАК РАБОТАЕТ ПАГИНАЦИЯ:
    1. Paginator делит список на страницы по 10 элементов
    2. request.GET.get('page') - получает номер страницы из URL (?page=2)
    3. paginator.get_page() - возвращает нужную страницу
    """
    template_name = 'HomeWork/personal.html'
    
    # ИСПРАВЛЕНО: Получаем полные объекты Person, а не values_list
    all_employees = Person.objects.all().order_by('-employment_date')
    
    # К5: Добавляем пагинацию (по 10 сотрудников на страницу)
    paginator = Paginator(all_employees, 10)  # 10 записей на странице
    page_number = request.GET.get('page')  # Получаем номер страницы из URL
    page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы
    
    context = {
        'page_obj': page_obj,  # Объект страницы для шаблона
    }
    
    return render(request, template_name, context)


# ========================================
# ДЕТАЛЬНАЯ ИНФОРМАЦИЯ О СОТРУДНИКЕ (К6 - требование ТЗ)
# ========================================
@login_required
def detail(request, pk):
    """
    КОММЕНТАРИЙ ДЛЯ СТУДЕНТКИ:
    Это представление для подробной карточки одного сотрудника.
    
    ЧТО ДОЛЖНО БЫТЬ (по ТЗ):
    К6 - Полная информация: заглавное фото, имя, фамилия, пол, 
         навыки с уровнем, стаж в днях, номер стола, галерея фото
    
    КАК РАБОТАЕТ:
    1. get_object_or_404 - находит сотрудника по id или выдаёт ошибку 404
    2. В шаблоне можно использовать все поля и методы модели
    3. Например: person.get_work_experience_days для получения стажа
    """
    template_name = 'HomeWork/detail.html'
    
    # ИСПРАВЛЕНО: Используем get_object_or_404 для безопасности
    person = get_object_or_404(Person, pk=pk)
    
    context = {
        'person': person,  # Передаём объект сотрудника в шаблон
    }
    
    return render(request, template_name, context)



