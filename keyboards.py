import typing as tp
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import quote
from phrasebook import proseed_parameter


def film_choice(response_json: tp.Dict[str, tp.Any], choice_limit: int = 5) \
        -> tuple[InlineKeyboardMarkup, tp.List[tp.Any]]:
    kb = InlineKeyboardMarkup(row_width=1)

    assert 'films' in response_json, "Not found films, but should"
    films_json = response_json['films']
    assert isinstance(films_json, list) and len(films_json) > 0, "Not films, but should"

    films = []
    counter = 0
    for film_json in films_json:
        if counter >= choice_limit:
            break
        try:
            name_ru = proseed_parameter(film_json, 'nameRu')
            name_en = proseed_parameter(film_json, 'nameEn')
            year = proseed_parameter(film_json, 'year')
            names = [name_ru, name_en, year]
            film = ', '.join([name for name in names if name is not None and len(name) > 0])
            if not len(film) > 0:
                continue
        except (KeyError, TypeError):
            continue

        button = InlineKeyboardButton(film, callback_data=f"film {counter}")
        kb.add(button)
        films.append(film_json)
        counter += 1

    cancel = InlineKeyboardButton('Cancel', callback_data="film cancel")
    kb.add(cancel)

    return kb, films


def source_choice(film_name: str) -> InlineKeyboardMarkup:
    film_encoded = quote(film_name)

    kb = InlineKeyboardMarkup(row_width=2)

    ivi = InlineKeyboardButton('💰IVI', url=f"https://www.ivi.ru/search/?q={film_encoded}")
    okko = InlineKeyboardButton('💰OKKO', url=f"https://okko.tv/search/{film_encoded}")
    kb.row(ivi, okko)

    hdrezka = InlineKeyboardButton('🆓HDREZKA',
                                   url=f"https://rezka.ag/search/?do=search&subaction=search&q={film_encoded}")
    animenime_url = f"https://animenime.ru/?s={film_encoded}"
    animenime = InlineKeyboardButton('🆓ANIMENIME',
                                     url=animenime_url)
    kb.row(hdrezka, animenime)

    return kb


# for stats and history, but not implemented
def controls(previous: bool, next: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    prev_button = InlineKeyboardButton('<', callback_data='prev')
    next_button = InlineKeyboardButton('>', callback_data='next')

    if previous and next:
        kb.row(prev_button, next_button)
    elif previous:
        kb.add(prev_button)
    elif next:
        kb.add(next_button)

    return kb
