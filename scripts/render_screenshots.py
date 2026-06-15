"""Серверный пре-рендер страниц блога в статические HTML-файлы для скриншотов.

Каждый шаблон — реальная разметка компонентов React, но с уже подставленными
мок-данными. Используется только для генерации PNG-скриншотов в README, чтобы
избежать гонки с асинхронным fetch в headless Chrome.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "screenshots" / "_render"
OUT.mkdir(parents=True, exist_ok=True)

TAILWIND = ''
TAILWIND_CFG = ''
TAILWIND_FILE = '<link rel="stylesheet" href="tw-built.css"/>'
CSS_LINK = ''


def page(title: str, body: str) -> str:
    inline = """
<style>
  body { font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif; background: #f7f7f8; color: #1a1a22; }
  h1, h2, h3, .font-serif { font-family: Georgia, 'Times New Roman', serif; }
</style>"""
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8"/>
<title>{title}</title>
{TAILWIND_FILE}
{inline}
</head>
<body class="text-ink-900 antialiased">
{body}
</body>
</html>"""


NAVBAR_LOGGED_OUT = """
<header class="sticky top-0 z-30 border-b border-ink-100 bg-white/80 backdrop-blur">
  <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
    <a class="flex items-center gap-2 font-serif text-lg font-semibold">
      <span class="grid h-8 w-8 place-items-center rounded-lg bg-brand-600 text-white">Б</span>
      Блог<span class="text-ink-400">.</span>
    </a>
    <div class="flex items-center gap-2">
      <a class="btn-ghost">Войти</a>
      <a class="btn-primary">Регистрация</a>
    </div>
  </div>
</header>"""

NAVBAR_LOGGED_IN = """
<header class="sticky top-0 z-30 border-b border-ink-100 bg-white/80 backdrop-blur">
  <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
    <a class="flex items-center gap-2 font-serif text-lg font-semibold">
      <span class="grid h-8 w-8 place-items-center rounded-lg bg-brand-600 text-white">Б</span>
      Блог<span class="text-ink-400">.</span>
    </a>
    <nav class="hidden items-center gap-1 md:flex">
      <a class="px-3 py-2 rounded-lg text-sm font-medium text-ink-600 hover:text-ink-900 hover:bg-ink-100">Лента</a>
      <a class="px-3 py-2 rounded-lg text-sm font-medium text-ink-600 hover:text-ink-900 hover:bg-ink-100">Новая запись</a>
      <a class="px-3 py-2 rounded-lg text-sm font-medium text-brand-700 bg-brand-50">Кабинет</a>
    </nav>
    <div class="flex items-center gap-2">
      <a class="flex items-center gap-2 rounded-full p-1 pr-3 hover:bg-ink-100">
        <span class="grid h-7 w-7 place-items-center rounded-full bg-gradient-to-br from-brand-100 to-brand-500 text-white text-xs font-semibold">A</span>
        <span class="text-sm font-medium">alice</span>
      </a>
      <a class="btn-ghost">Выйти</a>
    </div>
  </div>
</header>"""

FOOTER = '<footer class="border-t border-ink-100 py-6 text-center text-xs text-ink-400">Учебный проект · Django REST Framework + React + Tailwind</footer>'


# ---------- 01: Login ----------
LOGIN_BODY = f"""
{NAVBAR_LOGGED_OUT}
<main>
{page.__doc__ and ''}
<div class="mx-auto max-w-md px-4 py-12">
  <div class="rounded-2xl border border-ink-100 bg-white p-7 shadow-[0_1px_2px_rgba(20,20,30,0.04)]">
    <h1 class="font-serif text-2xl font-semibold">С возвращением</h1>
    <p class="mt-1 text-sm text-ink-600">Войдите, чтобы писать посты и оставлять комментарии.</p>
    <form class="mt-6 space-y-4">
      <div>
        <label class="block text-xs font-semibold uppercase tracking-wider text-ink-600 mb-1.5">Email</label>
        <input class="w-full rounded-xl border border-ink-200 bg-white px-3.5 py-2.5 text-sm" value="alice@example.com"/>
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase tracking-wider text-ink-600 mb-1.5">Пароль</label>
        <input type="password" class="w-full rounded-xl border border-ink-200 bg-white px-3.5 py-2.5 text-sm" value="password123"/>
      </div>
      <button class="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm hover:bg-brand-700">Войти</button>
    </form>
    <p class="mt-5 text-center text-sm text-ink-600">Нет аккаунта? <a class="font-medium text-brand-600 hover:underline">Зарегистрироваться</a></p>
    <div class="mt-4 rounded-lg bg-ink-50 p-3 text-xs text-ink-600"><b>Демо:</b> alice@example.com / password123</div>
  </div>
</div>
</main>
{FOOTER}
"""

# ---------- 02: Register ----------
REGISTER_BODY = f"""
{NAVBAR_LOGGED_OUT}
<main>
<div class="mx-auto max-w-md px-4 py-12">
  <div class="rounded-2xl border border-ink-100 bg-white p-7 shadow-[0_1px_2px_rgba(20,20,30,0.04)]">
    <h1 class="font-serif text-2xl font-semibold">Создать аккаунт</h1>
    <p class="mt-1 text-sm text-ink-600">Несколько полей — и можно писать.</p>
    <form class="mt-6 space-y-4">
      <div>
        <label class="block text-xs font-semibold uppercase tracking-wider text-ink-600 mb-1.5">Имя пользователя</label>
        <input class="w-full rounded-xl border border-ink-200 bg-white px-3.5 py-2.5 text-sm" value="newauthor"/>
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase tracking-wider text-ink-600 mb-1.5">Email</label>
        <input class="w-full rounded-xl border border-ink-200 bg-white px-3.5 py-2.5 text-sm" value="new@example.com"/>
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase tracking-wider text-ink-600 mb-1.5">О себе <span class="font-normal normal-case text-ink-400">(необязательно)</span></label>
        <textarea class="w-full rounded-xl border border-ink-200 bg-white px-3.5 py-2.5 text-sm min-h-[80px]">Пишу про Django и React.</textarea>
      </div>
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label class="block text-xs font-semibold uppercase tracking-wider text-ink-600 mb-1.5">Пароль</label>
          <input type="password" class="w-full rounded-xl border border-ink-200 bg-white px-3.5 py-2.5 text-sm" value="password123"/>
        </div>
        <div>
          <label class="block text-xs font-semibold uppercase tracking-wider text-ink-600 mb-1.5">Повторите</label>
          <input type="password" class="w-full rounded-xl border border-ink-200 bg-white px-3.5 py-2.5 text-sm" value="password123"/>
        </div>
      </div>
      <button class="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm hover:bg-brand-700">Создать аккаунт</button>
    </form>
    <p class="mt-5 text-center text-sm text-ink-600">Уже зарегистрированы? <a class="font-medium text-brand-600 hover:underline">Войти</a></p>
  </div>
</div>
</main>
{FOOTER}
"""

# ---------- 03: Home (feed) ----------
POST_CARD = """
<a class="rounded-2xl border border-ink-100 bg-white p-5 block hover:shadow-[0_8px_24px_rgba(20,20,30,0.06)]">
  <div class="flex items-center gap-2 text-xs text-ink-600">
    <span class="grid h-7 w-7 place-items-center rounded-full bg-gradient-to-br from-brand-100 to-brand-500 text-white text-xs font-semibold">A</span>
    <span class="font-medium text-ink-900">{author}</span>
    <span>·</span>
    <span>{when}</span>
  </div>
  <h3 class="mt-3 font-serif text-xl font-semibold text-ink-900">{title}</h3>
  <p class="mt-2 text-sm text-ink-600 line-clamp-3">{excerpt}</p>
  <div class="mt-4 flex items-center gap-3 text-xs text-ink-600">
    <span class="inline-flex items-center rounded-full bg-ink-100 px-2.5 py-0.5 text-xs font-medium text-ink-600">💬 {comments} комм.</span>
  </div>
</a>
"""

HOME_BODY = f"""
{NAVBAR_LOGGED_OUT}
<main>
<section class="mx-auto max-w-5xl px-4 mt-8">
  <div class="rounded-3xl bg-gradient-to-br from-brand-600 to-ink-900 px-6 py-10 text-white sm:px-10 sm:py-14">
    <h1 class="font-serif text-3xl font-semibold sm:text-4xl">Заметки о коде, дизайне и ремесле</h1>
    <p class="mt-2 max-w-xl text-white/80">Маленький блог, где разработчики делятся опытом и обсуждают идеи в комментариях.</p>
    <div class="mt-6 flex max-w-md gap-2 rounded-2xl bg-white/10 p-1.5 backdrop-blur">
      <input placeholder="Поиск по заголовку и тексту…" class="flex-1 rounded-xl bg-transparent px-3 py-2 text-sm placeholder:text-white/50 focus:outline-none"/>
      <button class="rounded-xl bg-white px-3 py-2 text-sm font-semibold text-ink-900">Найти</button>
    </div>
  </div>
  <h2 class="mt-10 mb-4 text-lg font-semibold">Свежие записи</h2>
  <div class="grid gap-4 sm:grid-cols-2">
    {POST_CARD.format(author='alice', when='2 ч назад', title='Как я перестал бояться SPA и полюбил REST', excerpt='REST — это контракт между клиентом и сервером. Когда понятно, что отдаёт и принимает каждый эндпоинт, фронтенд и бэкенд начинают жить дружно. В этом посте — мой чек-лист по дизайну API…', comments=2)}
    {POST_CARD.format(author='bob', when='5 ч назад', title='Django REST Framework за вечер: заметки на полях', excerpt='ViewSets экономят гору кода, но иногда прячут слишком много. Я держусь простого правила: всё, что выходит за пределы CRUD, выношу в отдельный эндпоинт. Так проще документировать…', comments=2)}
    {POST_CARD.format(author='alice', when='вчера', title='Tailwind без боли: как не превратить проект в помойку классов', excerpt='Tailwind даёт скорость, но легко скатиться в свалку utility-классов прямо в JSX. Я завёл себе три привычки: компонентные обёртки, токены в конфиге, лимит на «глубину» одной строки…', comments=0)}
  </div>
</section>
</main>
{FOOTER}
"""

# ---------- 04: Post detail ----------
POST_DETAIL_BODY = f"""
{NAVBAR_LOGGED_IN}
<main>
<article class="mx-auto max-w-3xl px-4 py-8">
  <a class="text-sm text-ink-600 hover:text-ink-900">← Назад к ленте</a>
  <header class="mt-4">
    <h1 class="font-serif text-3xl font-semibold sm:text-4xl">Как я перестал бояться SPA и полюбил REST</h1>
    <div class="mt-4 flex items-center justify-between">
      <div class="flex items-center gap-2 text-sm text-ink-600">
        <span class="grid h-7 w-7 place-items-center rounded-full bg-gradient-to-br from-brand-100 to-brand-500 text-white text-xs font-semibold">A</span>
        <span class="font-medium text-ink-900">alice</span>
        <span>·</span>
        <span>14 июня 2026 г.</span>
      </div>
      <div class="flex gap-2">
        <a class="inline-flex items-center justify-center rounded-xl border border-ink-200 bg-white px-4 py-2.5 text-sm font-medium hover:border-ink-400">Редактировать</a>
        <a class="inline-flex items-center justify-center rounded-xl border border-ink-200 bg-white px-4 py-2.5 text-sm font-medium text-red-600 hover:bg-red-50">Удалить</a>
      </div>
    </div>
  </header>
  <div class="prose-article mt-8 text-ink-900 leading-relaxed">
    <p>REST — это контракт между клиентом и сервером. Когда понятно, что отдаёт и принимает каждый эндпоинт, фронтенд и бэкенд начинают жить дружно.</p>
    <h2 class="mt-8 mb-3 text-xl font-semibold">Чек-лист дизайна API</h2>
    <p>Имена — существительные во множественном числе. Действия — методы HTTP. Состояния — статус-коды. Ошибки — структурированный JSON с понятным сообщением. Пагинация — единая на весь API. Версионирование — в URL или заголовке, но не в обоих сразу.</p>
    <p>Если вы держитесь этих правил, фронтенд-команда перестаёт спрашивать «а что здесь приходит?» и начинает строить.</p>
  </div>
  <hr class="my-10 border-ink-100"/>
  <section>
    <h2 class="font-serif text-xl font-semibold">Комментарии (2)</h2>
    <div class="mt-4">
      <textarea class="w-full rounded-xl border border-ink-200 bg-white px-3.5 py-2.5 text-sm min-h-[88px]" placeholder="Что думаете?">Отличный разбор, согласна с пунктом про пагинацию.</textarea>
      <div class="mt-2 flex items-center justify-between">
        <span class="text-xs text-ink-400">47/1000</span>
        <button class="inline-flex items-center justify-center rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm">Отправить</button>
      </div>
    </div>
    <ul class="mt-6 space-y-3">
      <li class="rounded-2xl border border-ink-100 bg-white p-4">
        <div class="flex items-center gap-2 text-sm">
          <span class="grid h-7 w-7 place-items-center rounded-full bg-gradient-to-br from-brand-100 to-brand-500 text-white text-xs font-semibold">B</span>
          <span class="font-medium">bob</span>
          <span class="text-ink-400">· 2 ч назад</span>
        </div>
        <p class="mt-2 text-sm">Хороший разбор, сохраню себе в закладки.</p>
      </li>
      <li class="rounded-2xl border border-ink-100 bg-white p-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2 text-sm">
            <span class="grid h-7 w-7 place-items-center rounded-full bg-gradient-to-br from-brand-100 to-brand-500 text-white text-xs font-semibold">A</span>
            <span class="font-medium">alice</span>
            <span class="text-ink-400">· 1 ч назад</span>
          </div>
          <a class="text-xs text-ink-400 hover:text-red-600">удалить</a>
        </div>
        <p class="mt-2 text-sm">Спасибо! Если интересно — могу про пагинацию отдельно.</p>
      </li>
    </ul>
  </section>
</article>
</main>
{FOOTER}
"""

# ---------- 05: Post create ----------
POST_FORM_BODY = f"""
{NAVBAR_LOGGED_IN}
<main>
<div class="mx-auto max-w-3xl px-4 py-8">
  <h1 class="font-serif text-2xl font-semibold">Новая запись</h1>
  <p class="mt-1 text-sm text-ink-600">Расскажите что-нибудь полезное.</p>
  <form class="rounded-2xl border border-ink-100 bg-white p-6 mt-6 space-y-4">
    <div>
      <label class="block text-xs font-semibold uppercase tracking-wider text-ink-600 mb-1.5">Заголовок</label>
      <input class="w-full rounded-xl border border-ink-200 bg-white px-3.5 py-2.5 text-sm" value="Идеальная структура Django-приложения"/>
    </div>
    <div>
      <label class="block text-xs font-semibold uppercase tracking-wider text-ink-600 mb-1.5">Текст</label>
      <textarea class="w-full rounded-xl border border-ink-200 bg-white px-3.5 py-2.5 text-sm min-h-[260px] font-serif">Каждый раз, открывая новый проект на Django, я трачу первый час на структуру приложений: какие модели в core, какие выносить в отдельный пакет, как делить сериализаторы и вьюхи. За пару лет у меня сложился набор правил, и я решил их записать — чтобы в следующий раз не вспоминать.</textarea>
    </div>
    <div>
      <label class="block text-xs font-semibold uppercase tracking-wider text-ink-600 mb-1.5">Обложка <span class="font-normal normal-case text-ink-400">(необязательно)</span></label>
      <div class="rounded-xl border border-dashed border-ink-200 bg-ink-50 px-4 py-6 text-center text-sm text-ink-600">PNG, JPG до 5 МБ</div>
    </div>
    <div class="flex items-center justify-end gap-2">
      <a class="inline-flex items-center justify-center rounded-xl border border-ink-200 bg-white px-4 py-2.5 text-sm font-medium hover:border-ink-400">Отмена</a>
      <button class="inline-flex items-center justify-center rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm">Опубликовать</button>
    </div>
  </form>
</div>
</main>
{FOOTER}
"""

# ---------- 06: Profile ----------
PROFILE_BODY = f"""
{NAVBAR_LOGGED_IN}
<main>
<div class="mx-auto max-w-5xl px-4 py-8">
  <div class="rounded-2xl border border-ink-100 bg-white p-6 sm:p-8">
    <div class="flex flex-col items-start gap-6 sm:flex-row sm:items-center">
      <span class="grid h-16 w-16 place-items-center rounded-full bg-gradient-to-br from-brand-100 to-brand-500 text-white text-lg font-semibold">A</span>
      <div class="flex-1">
        <h1 class="font-serif text-2xl font-semibold">alice</h1>
        <p class="text-sm text-ink-600">alice@example.com</p>
        <p class="mt-2 max-w-xl text-sm">Фронтенд-разработчик и любитель хорошего кофе.</p>
        <div class="mt-3 flex gap-2 text-xs text-ink-600">
          <span class="inline-flex items-center rounded-full bg-ink-100 px-2.5 py-0.5 text-xs font-medium text-ink-600">2 постов</span>
          <span class="inline-flex items-center rounded-full bg-ink-100 px-2.5 py-0.5 text-xs font-medium text-ink-600">2 комментариев</span>
        </div>
      </div>
      <div class="flex flex-col gap-2">
        <a class="inline-flex items-center justify-center rounded-xl border border-ink-200 bg-white px-4 py-2.5 text-sm font-medium hover:border-ink-400">Редактировать профиль</a>
        <a class="inline-flex items-center justify-center rounded-xl bg-transparent px-4 py-2.5 text-sm font-medium text-red-600 hover:bg-ink-100">Выйти</a>
      </div>
    </div>
  </div>
  <h2 class="mt-10 mb-4 text-lg font-semibold">Мои записи</h2>
  <div class="grid gap-3">
    <a class="rounded-2xl border border-ink-100 bg-white p-4 flex items-center justify-between">
      <div>
        <h3 class="font-semibold">Как я перестал бояться SPA и полюбил REST</h3>
        <p class="mt-1 text-xs text-ink-600">2 ч назад · 💬 2</p>
      </div>
      <span class="text-ink-400">→</span>
    </a>
    <a class="rounded-2xl border border-ink-100 bg-white p-4 flex items-center justify-between">
      <div>
        <h3 class="font-semibold">Tailwind без боли: как не превратить проект в помойку классов</h3>
        <p class="mt-1 text-xs text-ink-600">вчера · 💬 0</p>
      </div>
      <span class="text-ink-400">→</span>
    </a>
  </div>
</div>
</main>
{FOOTER}
"""


def write(name: str, body: str) -> Path:
    html = page(name, body)
    target = OUT / f"{name}.html"
    target.write_text(html, encoding='utf-8')
    return target


if __name__ == '__main__':
    write('01_login', LOGIN_BODY)
    write('02_register', REGISTER_BODY)
    write('03_home', HOME_BODY)
    write('04_post_detail', POST_DETAIL_BODY)
    write('05_post_create', POST_FORM_BODY)
    write('06_profile', PROFILE_BODY)
    print('rendered:', sorted(p.name for p in OUT.iterdir()))
