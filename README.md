# Foodgram-project

### Проект доступен по адресу:  
http://84.252.134.130/


## Описание

Приложение «Продуктовый помощник»: сайт, на котором пользователи публикуют рецепты, 
добавляют чужие рецепты в избранное и подписываются на публикации других авторов. 
Сервис «Список покупок» позволит пользователям создавать список продуктов, 
которые нужно купить для приготовления выбранных блюд.

Проект был выполнен в качестве дипломного задания в Яндекс Практикум.

## Стек технологий
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Nginx](https://nginx.org/)
- [Gunicorn](https://gunicorn.org/)
- [Docker](https://www.docker.com/)
- [Яндекс Облако](https://cloud.yandex.ru/)
- [GitHub Actions](https://github.com/features/actions)

## Установка проекта 

- Создайте директорию foodgram `mkdir foodgram` и перейдите в нее `cd foodgram`

- Склонируйте репозиторий в директорию foodgram \
`git clone https://github.com/RenkasVajra/foodgram-project`.

- Запустите docker-compose \
`sudo docker-compose up -d` 

- Примените миграции \
`sudo docker-compose exec web python manage.py migrate`

- Соберите статику \
`sudo docker-compose exec web python manage.py collectstatic --no-input`

- Создайте суперпользователя \
`sudo docker-compose exec web python manage.py createsuperuser`

