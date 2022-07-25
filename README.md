# challenge bot

Бот для прохождения спортивных челленджей. Выберите из предложенных, либо создайте свой! Ведите учет упражнений прямо в чате =)

Бот залит на VPS и вполне себе работает
https://t.me/sport_challenges_bot



### Для запуска локально:

* Переименовать **example.env** > **.env**
* Заполнить .env (SITE_ON_SERVER=True переключит SQLite на Postgres)
* Запустить один раз register_bot.py
* выполнить sudo docker-compose up --build -d
* при первом запуске выполнить:

```sudo docker-compose exec backend python manage.py collectstatic; sudo docker-compose exec backend python manage.py migrate; sudo docker-compose exec backend python manage.py createsuperuser```

