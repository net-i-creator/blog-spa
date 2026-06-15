# Как залить проект на vcs.uni-dubna.ru

## Что я подготовил

1. **ZIP-архив** `blog-spa-submission.zip` (~1 МБ) в корне проекта — это полный снимок репозитория (всё, что есть в `git archive HEAD`), без локального `venv`, `node_modules`, `db.sqlite3`, `media/`.
2. **README.md** уже внутри архива — со скриншотами, моделями, маршрутами API и фронта, инструкцией запуска.
3. **docs/Blog-SPA-Report.pdf** — то же содержимое в виде PDF, можно прикрепить отдельно.
4. **Сами файлы проекта** в `backend/`, `frontend/`, `scripts/` — без сборок и зависимостей.

## Шаг 1. Создать репозиторий в ЛК университета

На `vcs.uni-dubna.ru` — New Project / Создать проект:

- **Project name:** `blog-spa`
- **Visibility Level:** Private (или Internal, по требованиям вуза)
- **Initialize repository with a README:** выключить
- Нажать **Create project**

После создания скопировать URL — он будет вида:
```
https://vcs.uni-dubna.ru/<ваш-логин>/blog-spa.git
```

## Шаг 2. Залить код

### Вариант A — через веб-интерфейс (без git на машине)

1. Открыть созданный репозиторий в GitLab.
2. Нажать `+` → `Upload file` (или `git push` инструкции, но в вузовском GitLab обычно есть веб-загрузка).
3. Перетащить **содержимое** распакованного архива (папки `backend/`, `frontend/`, `screenshots/`, `docs/`, `scripts/`, файлы `README.md`, `.gitignore`).
4. Commit message: `Initial commit`.
5. В корне репозитория должны оказаться `README.md`, `backend/`, `frontend/` и т.д. **Не должно быть обёртки `blog-spa-submission/`** — файлы должны лежать прямо в корне.

### Вариант B — через git в терминале (если есть локальный git и токен)

1. Распаковать архив:
   ```bash
   cd ~/Downloads
   unzip blog-spa-submission.zip
   cd blog-spa
   ```

2. Добавить remote и запушить:
   ```bash
   git init -b main
   git add .
   git commit -m "Initial commit: blog SPA (Django REST Framework + React + Tailwind)"
   git remote add origin https://vcs.uni-dubna.ru/<ваш-логин>/blog-spa.git
   git push -u origin main
   ```
   На запрос логина/пароля — ввести логин и **Personal Access Token** (не сам пароль). Токен создаётся в GitLab: Settings → Access Tokens → выдать `write_repository`.

## Шаг 3. Проверить

После загрузки открыть `https://vcs.uni-dubna.ru/<ваш-логин>/blog-spa` — README должен отрендериться с картинками. На GitLab mermaid-блок и таблицы отображаются корректно.

## Если нужно «с нуля» с моей машины

У меня нет доступа к vcs.uni-dubna.ru — логин/токен от вузовского GitLab у вас. Я подготовил архив, чтобы загрузка заняла одну операцию.
