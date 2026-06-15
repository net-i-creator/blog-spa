"""Генерация PDF-отчёта по проекту из README + скриншотов."""
import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Регистрация шрифта с поддержкой кириллицы
ARIAL_PATH = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
pdfmetrics.registerFont(TTFont('ArialUni', ARIAL_PATH))
pdfmetrics.registerFont(TTFont('ArialUni-Bold', ARIAL_PATH))

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "Blog-SPA-Report.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

doc = SimpleDocTemplate(
    str(OUT), pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=18*mm, bottomMargin=18*mm,
    title="Blog SPA — Django REST Framework + React + Tailwind",
    author="Student",
)

styles = getSampleStyleSheet()
H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='ArialUni-Bold', fontSize=20, spaceAfter=10, textColor=colors.HexColor('#1a1a22'))
H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='ArialUni-Bold', fontSize=14, spaceBefore=14, spaceAfter=6, textColor=colors.HexColor('#384ec4'))
H3 = ParagraphStyle('H3', parent=styles['Heading3'], fontName='ArialUni-Bold', fontSize=11, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#4a4a55'))
BODY = ParagraphStyle('Body', parent=styles['BodyText'], fontName='ArialUni', fontSize=9.5, leading=13, spaceAfter=4, alignment=TA_LEFT)
CODE = ParagraphStyle('Code', parent=BODY, fontName='ArialUni', fontSize=8.5, leading=10.5, leftIndent=8, backColor=colors.HexColor('#f7f7f8'), borderPadding=4, spaceAfter=6, textColor=colors.HexColor('#1a1a22'))
META = ParagraphStyle('Meta', parent=BODY, fontName='ArialUni', fontSize=8, textColor=colors.HexColor('#8a8a96'), alignment=TA_CENTER)

flow = []


def md_table(rows):
    data = [[Paragraph(str(c), BODY) for c in row] for row in rows]
    t = Table(data, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eef4ff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1a1a22')),
        ('FONTNAME', (0, 0), (-1, 0), 'ArialUni-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'ArialUni'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#d6d6dd')),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


def heading(level, text):
    s = {1: H1, 2: H2, 3: H3}[level]
    flow.append(Paragraph(text, s))


def para(text):
    flow.append(Paragraph(text, BODY))


def code(text):
    flow.append(Paragraph(text.replace('\n', '<br/>'), CODE))


def image(path, width_mm=160):
    from PIL import Image as PILImage
    with PILImage.open(path) as im:
        iw, ih = im.size
    width = width_mm * mm
    height = width * (ih / iw)
    img = Image(str(path), width=width, height=height)
    flow.append(Spacer(1, 3 * mm))
    flow.append(img)
    flow.append(Spacer(1, 2 * mm))


# ----- Cover -----
flow.append(Paragraph('<b>Blog SPA</b>', H1))
para('Учебный проект: текстовый блог с комментариями на Django REST Framework и React.')
para('<b>Стек:</b> Django 5.1, DRF, SimpleJWT, SQLite, Pillow · React 18, Vite 5, Tailwind 3, react-router-dom, axios.')
para('<b>Репозиторий:</b> https://github.com/net-i-creator/blog-spa')
flow.append(Spacer(1, 4 * mm))
flow.append(Paragraph('Локальный запуск', H3))
code(
    "cd backend<br/>"
    "python3.12 -m venv .venv && source .venv/bin/activate<br/>"
    "pip install -r requirements.txt && cp .env.example .env<br/>"
    "python manage.py migrate && python manage.py seed_demo<br/>"
    "python manage.py runserver 127.0.0.1:8001<br/><br/>"
    "# второй терминал:<br/>"
    "cd frontend && npm install && npm run dev   # http://127.0.0.1:5180"
)
flow.append(PageBreak())

# ----- 1. Screenshots -----
heading(2, '1. Скриншоты')
para('Демо-аккаунты (создаются через seed_demo): alice@example.com / bob@example.com, пароль password123.')

shots = [
    ('1.1 Страница входа', '01_login.png'),
    ('1.2 Регистрация', '02_register.png'),
    ('1.3 Лента постов', '03_home.png'),
    ('1.4 Страница статьи с комментариями', '04_post_detail.png'),
    ('1.5 Создание новой записи', '05_post_create.png'),
    ('1.6 Личный кабинет', '06_profile.png'),
]
for title, fname in shots:
    flow.append(Paragraph(f'<b>{title}</b>', BODY))
    image(ROOT / 'screenshots' / fname)
    flow.append(PageBreak())

# ----- 2. Models -----
heading(2, '2. Модели')
heading(3, 'accounts.User')
para('Кастомный пользователь на базе AbstractUser. USERNAME_FIELD = email.')
md_table([
    ['Поле', 'Тип', 'Описание'],
    ['id', 'Auto', 'первичный ключ'],
    ['username', 'CharField', 'имя пользователя (REQUIRED)'],
    ['email', 'EmailField (unique)', 'используется для логина'],
    ['avatar', 'ImageField', 'upload_to=avatars/, опционально'],
    ['bio', 'TextField (≤500)', 'опционально'],
    ['date_joined', 'DateTime', 'заполняется автоматически'],
])
flow.append(Spacer(1, 3*mm))
heading(3, 'blog.Post')
md_table([
    ['Поле', 'Тип', 'Описание'],
    ['id', 'Auto', 'первичный ключ'],
    ['author', 'FK → accounts.User', 'CASCADE, related_name=posts'],
    ['title', 'CharField (≤200)', 'заголовок'],
    ['slug', 'SlugField (unique)', 'автогенерация из title, ≤220'],
    ['body', 'TextField', 'содержимое статьи'],
    ['image', 'ImageField', 'upload_to=posts/, опционально'],
    ['created_at', 'DateTime', 'auto_now_add'],
    ['updated_at', 'DateTime', 'auto_now'],
])
flow.append(Spacer(1, 3*mm))
heading(3, 'blog.Comment')
md_table([
    ['Поле', 'Тип', 'Описание'],
    ['id', 'Auto', 'первичный ключ'],
    ['post', 'FK → Post', 'CASCADE, related_name=comments'],
    ['author', 'FK → User', 'CASCADE, related_name=comments'],
    ['text', 'TextField (≤1000)', 'содержимое комментария'],
    ['created_at', 'DateTime', 'auto_now_add'],
    ['updated_at', 'DateTime', 'auto_now'],
])
flow.append(PageBreak())

# ----- 3. REST API -----
heading(2, '3. REST API')
para('Базовый URL: http://127.0.0.1:8001/api/ (или через Vite-прокси: http://127.0.0.1:5180/api/).')
md_table([
    ['Метод', 'Эндпоинт', 'Auth', 'Описание'],
    ['POST', '/api/auth/register/', '—', 'Регистрация. Возвращает user, access, refresh.'],
    ['POST', '/api/auth/login/', '—', 'Логин по email + пароль.'],
    ['POST', '/api/auth/token/refresh/', '—', 'Обновление access-токена.'],
    ['GET', '/api/auth/me/', 'Bearer', 'Профиль текущего пользователя.'],
    ['PATCH', '/api/auth/me/', 'Bearer', 'Обновить username, bio, avatar.'],
    ['GET', '/api/auth/users/<id>/', '—', 'Публичный профиль.'],
    ['GET', '/api/posts/', '—', 'Список постов. ?search=, ?author=, пагинация.'],
    ['POST', '/api/posts/', 'Bearer', 'Создать пост.'],
    ['GET', '/api/posts/<slug>/', '—', 'Полная статья + комментарии.'],
    ['PATCH', '/api/posts/<slug>/', 'Bearer, автор', 'Редактировать пост.'],
    ['DELETE', '/api/posts/<slug>/', 'Bearer, автор', 'Удалить пост.'],
    ['GET', '/api/posts/<slug>/comments/', '—', 'Список комментариев к посту.'],
    ['POST', '/api/posts/<slug>/comments/', 'Bearer', 'Добавить комментарий.'],
    ['GET', '/api/comments/<id>/', '—', 'Получить комментарий.'],
    ['PATCH', '/api/comments/<id>/', 'Bearer, автор', 'Изменить комментарий.'],
    ['DELETE', '/api/comments/<id>/', 'Bearer, автор', 'Удалить комментарий.'],
    ['GET', '/admin/', 'staff', 'Django admin для User, Post, Comment.'],
])
flow.append(PageBreak())

# ----- 4. Frontend routes -----
heading(2, '4. Маршруты фронтенда')
md_table([
    ['Путь', 'Компонент', 'Защита'],
    ['/', 'Home', 'публичный — лента постов с поиском'],
    ['/login', 'Login', 'публичный'],
    ['/register', 'Register', 'публичный'],
    ['/posts/:slug', 'PostDetail', 'публичный — статья + комментарии'],
    ['/users/:id', 'UserPage', 'публичный — профиль автора'],
    ['/posts/new', 'PostForm', 'ProtectedRoute — создание поста'],
    ['/posts/:slug/edit', 'PostForm', 'ProtectedRoute + авторство'],
    ['/profile', 'Profile', 'ProtectedRoute — личный кабинет'],
    ['*', 'NotFound', 'публичный — 404'],
])
flow.append(PageBreak())

# ----- 5. Tech -----
heading(2, '5. Технические детали')
heading(3, 'JWT-флоу на клиенте')
para('src/api/client.js: axios-интерсептор подставляет Authorization: Bearer &lt;access&gt;. При 401 автоматически вызывает /auth/token/refresh/ и повторяет запрос. Если refresh протух — пользователь выкидывается на /login.')
heading(3, 'Permissions')
para('Кастомный класс IsAuthorOrReadOnly в blog/views.py: анонимные пользователи могут только читать, автор поста/комментария может редактировать и удалять свои записи.')
heading(3, 'Slug')
para('Генерируется автоматически в Post.save() из title через django.utils.text.slugify. При коллизии добавляется -2, -3 и т.д.')
heading(3, 'CORS')
para('django-cors-headers разрешает http://localhost:5173 и http://127.0.0.1:5180 (настраивается в backend/.env).')
heading(3, 'MEDIA')
para('Папка media/ хранит аватары (avatars/) и обложки постов (posts/). В режиме DEBUG раздаётся самим Django.')
heading(3, 'Пагинация и фильтрация')
para('PageNumberPagination с PAGE_SIZE=10. На /api/posts/ доступны ?search= (по title и body), ?author=, ?ordering=-created_at|created_at|title.')

doc.build(flow)
print(f"PDF: {OUT} ({OUT.stat().st_size/1024:.1f} KB)")
