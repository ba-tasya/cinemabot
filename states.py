from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):  # type: ignore

    main = State()
    waiting_for_film = State()
    history = State()  # not implemented
    stats = State()   # not implemented
