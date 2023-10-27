# Training_portal
дипломная работа GB 2023
Training_portal
Stack:
Python 3.10
Django 4.2.5

# Правила работы с [Git-ом](https://git-scm.com/book/ru/v2)
1. Все изменения в проекте должны происходить в отдельных ветках. В мейн не коммитим.
2. Мерж в мейн происходит только после одного аппрува.
3. Ветка мейн всегда должна быть актуальной. Перед созданием новой ветки, нужно сделать ```git pull origin/main```
4. Если ветка долго живущая, то в неё нужно переодически мержить мейн, чтобы не было конфликтов. См. [FAQ](#Как-подмержить-мейн-с-свою-ветку)
5. Ветку ведёт один человек и свою ветку мержит автор после аппрува. Только автор знает, когда работа закончена.
6. Ветка называется по названию задачи в трелло (транслитом). Например, ```git checkout -b add_user_model```


# FAQ
## Как подмержить мейн с свою ветку
Для того, чтобы всегда работать с актуальными изменениями и не резолвить потом конфликты, если ветка живёт долго, лучше переодически подмерживать в неё мейн. Для этого, **находять в своей ветке**, сделать следующее:

```bash
git fetch --all
git merge origin/main
```
В процессе могут возникнуть конфликты, их надо резолвить.

## Как удалить локальную ветку
```bash
git branch -d <branch_name>
```
Обратите внимание на то, что ветка, которую вы удаляете, не должна быть вашей текущей веткой, в которой вы работаете, иначе отобразится ошибка вида:
error: Cannot delete branch ’mybranch’ checked out at ’/path/to
Поэтому, если вам нужно удалить текущую ветку, то сначала нужно переключиться на какую-либо другую ветку, а только потом выполнять удаление.
Если вдруг возникает ошибка: The branch ’mybranch’ is not fully merged. If you are sure you want to delete it и вы по прежнему хотите удалить ветку,
то для принудительного удаления ветки можно воспользоваться опцией -D:

```bash
git branch -D <branch_name>
```

## Как удалить удалённую (remote) ветку (ветку которая не на твоём компе, а на гитхабе )
```bash
git push origin -d <branch_name>
```

# Как запустить проект локально
### Устанавливаем Docker (под Windows ставим Docker Desktop)
в docker.com > логинишься | регистрируешься ->
-> продкуты ->  кнопка "download for Windows" -> устанавливаешь
-> получаем Docker Desktop

### Запускаем контейнеры rabbitMQ, postgreSQL, Mail Hog
```bash
docker compose -f local.docker-compose.yaml up -d
```
### Ставим зависимости
```bash
pdm install 
```
### Запускаем worker celery из папки src/ в отдельном терминале
```bash
cd src
pdm run celery -A config worker -l info
```
### Запускаем Джангу из директории src
```bash
pdm run python manage.py collectstatic
pdm run python manage.py migrate
pdm run python manage.py runserver
```
### Удаление базы данных 
```bash
docker compose -f src/local.docker-compose.yaml down --volumes

```
### Веб интерфейс Mail Hog находится тут -> localhost:8025

# Фикстуры
### Создание фикстуры
```bash
Папку fixtures предварительно необходимо создать внутри src (/fixtures)
Далее выполняем команду для создания фикстуры если находимся в src>
python -Xutf8 manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude auth.group  --exclude admin.logentry --exclude sessions --indent 2 -o ./fi
xtures/007_all.json
```
### Загрузка фикстур из директории src
```bash
Удаляем старую базу
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata ./fixtures/007_all.json
```
# Логирование
Создать папку var/log в src
```bash
mkdir -p ./var/log
```

# Загрузка картинок и видео
При создании курсов и лекций можно подгружать 
файлы картинок, картинки по ссылке и видео по ссылке
### Файлы картинок 
Файлы картинок загружаются в папку /static/, при создании курса в поле
"файл картинки" указывается название файла формата img/diz_04.jpeg
### Картинки по ссылке
Для картинки по ссылке  в поле
"URL картинки" указывается ссылка на картинку в формате 
https://.....  .jpg
### Видео по ссылке
Для видео по ссылке  в поле "Video URL"
указывается ссылка на видео в формате 
https://www.youtube.com/embed/Xiy8xwhbmew?si=vb7hqtiDATouk30x

Такую ссылку можно получить из youtube(на странице видео)
-> "поделиться" > "встроить" > 
из предложенного взять нужную часть вида как выше. 
-> вставить в поле "Video URL" при создании урока

