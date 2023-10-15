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
```bash 
через pdm
pdm install 
pdm run python src/manage.py collectstatic
pdm run python src/manage.py migrate
pdm run python src/manage.py runserver
через pip
pip install -r requirements.txt
pip freeze
cd src
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
создание суперпользователя
python manage.py csu
python manage.py runserver
```
# Создание фикстуры
```bash
Папку fixtures предварительно необходимо создать внутри приложения (mainapp, authapp) (/mainapp/fixtures)
Далее выполняем команду для создания фикстуры для соответствующего приложения
python manage.py dumpdata mainapp > mainapp/fixtures/004_mainapp.json
python manage.py dumpdata authapp > authapp/fixtures/004_authapp.json
```
# Загрузка фикстур
```bash
python manage.py loaddata ./mainapp/fixtures/004_mainapp.json
python manage.py loaddata ./authapp/fixtures/004_authapp.json