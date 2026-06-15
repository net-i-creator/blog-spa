"""Seed demo data for screenshots and local testing."""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from blog.models import Post, Comment

User = get_user_model()


class Command(BaseCommand):
    help = 'Создаёт демо-пользователей, посты и комментарии.'

    def handle(self, *args, **options):
        if User.objects.filter(username='alice').exists():
            self.stdout.write(self.style.WARNING('Демо-данные уже созданы — пропускаю.'))
            return

        alice = User.objects.create_user(
            username='alice', email='alice@example.com',
            password='password123', bio='Фронтенд-разработчик и любитель хорошего кофе.',
        )
        bob = User.objects.create_user(
            username='bob', email='bob@example.com',
            password='password123', bio='Бэкенд на Django, немного DevOps.',
        )

        posts_data = [
            (
                alice,
                'Как я перестал бояться SPA и полюбил REST',
                'REST — это контракт между клиентом и сервером. Когда понятно, что отдаёт и принимает каждый эндпоинт, фронтенд и бэкенд начинают жить дружно. В этом посте — мой чек-лист по дизайну API: предикаты, статус-коды, пагинация, версионирование и понятные ошибки. Никакой магии, только договорённости.',
            ),
            (
                bob,
                'Django REST Framework за вечер: заметки на полях',
                'ViewSets экономят гору кода, но иногда прячут слишком много. Я держусь простого правила: всё, что выходит за пределы CRUD, выношу в отдельный эндпоинт. Так проще документировать и тестировать. Ниже — шаблон, к которому я возвращаюсь снова и снова.',
            ),
            (
                alice,
                'Tailwind без боли: как не превратить проект в помойку классов',
                'Tailwind даёт скорость, но легко скатиться в свалку utility-классов прямо в JSX. Я завёл себе три привычки: компонентные обёртки, токены в конфиге, лимит на «глубину» одной строки. Этого хватило, чтобы вернуться к проекту через полгода и не упасть в обморок.',
            ),
        ]

        for author, title, body in posts_data:
            Post.objects.create(author=author, title=title, body=body)

        first = Post.objects.first()
        second = Post.objects.all()[1]
        Comment.objects.create(post=first, author=bob, text='Хороший разбор, сохраню себе в закладки.')
        Comment.objects.create(post=first, author=alice, text='Спасибо! Если интересно — могу про пагинацию отдельно.')
        Comment.objects.create(post=second, author=alice, text='Согласна про «тонкий» эндпоинт, ловлю этот антипаттерн постоянно.')
        Comment.objects.create(post=second, author=bob, text='Скоро допишу про throttling — это сюда просится.')

        self.stdout.write(self.style.SUCCESS('Демо-данные созданы. Логины: alice / bob, пароль: password123'))
