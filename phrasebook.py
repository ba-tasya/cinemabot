import typing as tp

WELCOME = "Напишите название фильма/мультфильма/сериала/аниме, которое вы хотите найти"
HELP = """Просто напишите название фильма, который Вы ищете\n Некоторые доступные команды:\n /help - помощь\n
/history - история ваших запросов\n /stats - количество запросов каждого найденного Вами фильма"""
FOUND = "Похоже на то, что Вы запрашиваете"
NOT_FOUND = """К сожалению, по Вашему запросу ричего не найдено.
Проверьте на ошибки в запросе или попробуйте другой фильм"""
CANCEL = "Напишите название фильма/мультфильма/сериала/аниме, которое вы хотите найти"
SOURCES = """Вот некоторые сайты, где Вы можете посмотреть найденный фильм:

💰 Платно или по подписке
🆓 Бесплатно, но может понадобится VPN или прокси"""

# different logic for names
response_order: tp.List[str] = ['year', 'rating', 'length', 'description', 'contries', 'genres']
response_prefix: tp.List[str] = ['📅', '📈', '⌛️', '🎬', '🗺', 'ℹ️']


# sometimes there is null in data
def null_to_something(record: str) -> tp.Optional[str]:
    if record == 'null':
        return None
    return record


def proseed_parameter(film_json: tp.Dict[str, tp.Any], parameter: str) -> tp.Optional[tp.Any]:
    if parameter in film_json:
        if parameter == 'countries':
            return ', '.join([c['country'] for c in film_json['countries']])
        elif parameter == 'genres':
            return ', '.join([g['genre'] for g in film_json['genres']])
        return null_to_something(film_json[parameter])
    return None


def construct_description(film_json: tp.Dict[str, tp.Any]) -> str:
    name_ru = proseed_parameter(film_json, 'nameRu')
    name_en = proseed_parameter(film_json, 'nameEn')
    description = proseed_parameter(film_json, 'description')
    year = proseed_parameter(film_json, 'year')
    countries = proseed_parameter(film_json, 'countries')
    length = proseed_parameter(film_json, 'filmLength')
    genres = proseed_parameter(film_json, 'genres')
    rating = proseed_parameter(film_json, 'rating')

    result: tp.Dict[tp.Any, tp.Any] = dict(zip(response_order, [year, rating, length, description, countries, genres]))

    name = ''

    if (name_ru is None or name_en is None):
        name = name_ru if name_en is None else name_en
        film_json['name'] = name
    else:
        name = ', '.join([name_ru, name_en])
        film_json['name'] = name_ru

    description = name + '\n'
    for idx, type in enumerate(response_order):
        if not result[type] is None:
            description = description + '\n' + response_prefix[idx] + ' ' + result[type]
        else:
            description = description + '\n' + response_prefix[idx] + ' Неизвестно'

    return description
