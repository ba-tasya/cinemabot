Простой бот, который предлагает варианты для просмотра фильмов

Имеет команды /start, /help, /history, /stats:

- /start - Выводит приветсвенное сообщение

- /help - Выводит подсказку по использованию бота

- /history - Для пользователя выводит историю фильмов, которые он нашёл

- /stats - Выводит куммулятивную статистику для пользователя, отсортированную по количеству запросов каждого фильма

Бот захощен на yandex cloud и доступен в телеграмм: https://t.me/python_film_finder_bot

Для бота был использован aiogram==2.23.1, а для хранения базы данных sqlite

Для поиска фильма был использован kinopoisk unofficial api. Бот делает запрос к нему по команде search-by-keyword и тексту, который дал пользователь. После этого он получает список из всех фильмов, которые подошли по данному запросу, в порядке реливантности. Пользователю даётся выбор из 5 первых в списке.

В качестве вариантов просмотра пользователю предлагается 4 сайта: okko, ivi, hdrezka, animenime(для аниме)
