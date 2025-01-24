from django.utils import timezone
from .models import Post, Comment  # . Это обозначает текущий каталог или пакет. Это называется ОТНОСИТЕЛЬНЫЙ ИМПОРТ.
# Тобиш искать файл forms.py в том же каталоге, что и текущий файл Python, в котором находится этот оператор импорта.
# Import Post это означает - импортируй из этого файла класс Post
from django.shortcuts import render, get_object_or_404  # Имя модуля, из которого импортируем данные.
from .forms import PostForm, CommentForm
from django.shortcuts import redirect


def post_list(request):  # Отвечает за отображение списка опубликованных постов блога.
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # Запрос к базе данных для извлечения постов. Этот метод фильтрует только те посты,
    # у которых published_date равна текущему времени (timezone.now()). Грубо говоря публикует посты у которых
    # проставлено время.
    # .order_by('-published_date'): Этот метод сортирует посты по дате публикации. Сейчас от новых к старым.
    # По дефолту без '-' от старых к новым.
    return render(request, 'blog/post_list.html', {'posts': posts})
    # Возвращаем шаблон blog/post_list.html, передавая ему список постов. Request  — это объект
    # HttpRequest, который содержит данные о запросе.


def post_detail(request, pk):  # request: Объект HTTP-запроса содержащий информацию о запросе
    # юзера (метод, заголовки, текст); primary key: Это первичный ключ - значение является частью URL-адреса;
    # например, URL-адрес, подобный /blog/123/, передаст 123 как pk.
    post = get_object_or_404(Post, pk=pk)  # Это внутренняя функция Django. Она пытается найти в базе данных объект
    # Post и pk которого совпадает со значением, переданным в функцию. Если совпадений Post не найдено - выдаст Http404
    comment_form = CommentForm()
    comments = post.comments.filter(is_deleted=False)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'blog/post_detail.html', context)
    # Отображает HTML-шаблон, расположенный по адресу blog/post_detail.html. Тобиш это путь к файлу в котором будут
    # отображаться сведения о публикации. Он будет содержать заполнители для заголовка публикации, её содержания,
    # автора, даты и всего что туда запихнем, которые будут заполняться динамически.
    # {'post': post}: Это словарь, содержащий контекст для шаблона. Он передаёт объект post в шаблон.
    # В шаблоне можем получить доступ к например, post.title, post.content...


def post_new(request):  # А тут уже POST-запросы и GET-запросы. Тобиш отправка формы и создания нового поста.
    if request.method == "POST":  # Проверяет, является ли запрос POST-запросом.
        form = PostForm(request.POST)  # Если это POST-запрос, создается форма PostForm где(request.POST означает -
        # (данные, отправленные пользователем через форму)).
        if form.is_valid():  # Проверяет, валидны ли данные формы
            post = form.save(commit=False)  # Если валидны, создает объект Post(commit=False значит не сохраняй в БД).
            post.author = request.user  # Создаем объект автор = получаем данные из запроса поля User
            post.published_date = timezone.now()  # Создаем объект дата публикации = текущее время.
            post.save()  # Сохраняем объект в БД.
            return redirect('post_detail', pk=post.pk)  # Выполняет перенаправление на страницу детализации только
            # что созданного поста (post_detail), передавая в неё primary_key поста.
    else:  # Тогда отдай пустую форму.
        form = PostForm()  # Создает пустую форму, аналогично def post_new(request).
    return render(request, 'blog/post_edit.html', {'form': form})
    # Рендерим шаблон blog/post_edit.html, передавая в него созданную форму в качестве контекста с ключом form.
    # Тобиш это отображает пустую форму для ввода данных для нового поста.


def post_edit(request, pk):  # Функция принимает 2 аргумента: request - HTTP-запрос пользователя.
    # primary key поста, который нужно отредактировать.
    post = get_object_or_404(Post, pk=pk)  # Это внутренняя функция Django. Работает так: получает из базы данных объект
    # модели Post с pk нужного поста, если такого нет поста то возвращает HTTP-ответ с кодом 404(Not Found)
    if request.method == "POST":  # Проверяет, является ли запрос = POST (то есть отправляется ли форма с изменениями)
        form = PostForm(request.POST, instance=post)  # Создает дубль формы PostForm, заполняя её данными из
        # Request.POST (отправленные данные из формы) и передавая существующий post через параметр instance.
        # Тобиш чтобы форма обновила данные существующего поста, а не создала новый.
        if form.is_valid():  # Дальше все как из прошлой функции, то есть проверка валидности.
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
