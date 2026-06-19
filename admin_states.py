from aiogram.fsm.state import State, StatesGroup


class AddSponsor(StatesGroup):
    channel_id = State()
    channel_link = State()
    title = State()