# List of cities, sorted alphabetically, without Nur-Sultan
cities = sorted([
    'Актау', 'Актобе', 'Алматы', 'Аркалык', 'Атбасар',
    'Атырау', 'Астана', 'Зайсан', 'Павлодар', 'Петропавловск',
    'Усть-Каменогорск', 'Балхаш', 'Боровое', 'Караганда', 'Кокшетау',
    'Костанай', 'Кызылорда', 'Риддер', 'Шымкент', 'Тараз',
    'Сарыагаш', 'Семей', 'Экибастуз', 'Жезказган', 'Орал', 'Талдыкорган'
])

# Distribute cities into rows for the reply keyboard
cities_reply_keyboard = [cities[i:i + 5] for i in range(0, len(cities), 5)]
