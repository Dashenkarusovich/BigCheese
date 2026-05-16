"""
Big Cheese Languages — тексты Telegram-бота
Stage 1: новые сегменты, сегментированные CTA и 4-дневная прогревающая цепочка.
"""

CHANNEL_URL = "https://t.me/BigCheesemaster"

LANG_SELECT = {
    "ru": "Выбери язык / Choose language:",
    "en": "Выбери язык / Choose language:"
}

DAY0_WELCOME = {
    "ru": """Привет{name}! 👋

Я Дарья, основатель <b>Big Cheese Languages</b>.

Здесь учим языки для реальной жизни: переезд, работа, семья, адаптация и живое общение.

Держи подарок 🎁 — PDF с фразами для аренды, банка, врача и соседей.

А чтобы я могла присылать тебе более полезные материалы, выбери, что сейчас актуальнее:""",

    "en": """Hi{name}! 👋

I'm Darya, founder of <b>Big Cheese Languages</b>.

Here we learn languages for real life: relocation, work, family, adaptation and everyday conversations.

Here is your gift 🎁 — a PDF with phrases for housing, bank, doctor and neighbours.

To make the next messages useful for you, choose what matters most right now:"""
}

DAY0_SEGMENT = {
    "ru": "Что сейчас актуальнее для тебя?",
    "en": "What is most relevant for you right now?"
}

DAY0_CONFIRM = {
    "ru": "Буду присылать полезное раз в день несколько дней. Без спама.",
    "en": "I'll send useful messages once a day for a few days. No spam."
}

BTN_SEGMENT = {
    "ru": [
        "✈️ Переезд и адаптация",
        "💼 Работа и карьера",
        "👨‍👩‍👧 Семья / ребёнок",
        "🗣 Хочу говорить увереннее",
    ],
    "en": [
        "✈️ Relocation & adaptation",
        "💼 Work & career",
        "👨‍👩‍👧 Family / child",
        "🗣 Speaking confidence",
    ]
}

SEGMENT_LABELS = {
    "ru": {
        "relocation": "Переезд и адаптация",
        "career": "Работа и карьера",
        "family": "Семья / ребёнок",
        "speaking": "Разговорная уверенность",
        "other": "Другое",
    },
    "en": {
        "relocation": "Relocation & adaptation",
        "career": "Work & career",
        "family": "Family / child",
        "speaking": "Speaking confidence",
        "other": "Other",
    }
}

SEG_CONFIRM = {
    "ru": {
        "relocation": "✈️ Поняла. Значит, тебе нужен язык не “по учебнику”, а для реальных ситуаций после переезда.",
        "career": "💼 Поняла. Здесь язык нужен не просто для “знания английского”, а для рабочих ситуаций и уверенности.",
        "family": "👨‍👩‍👧 Поняла. Если язык нужен ребёнку или семье, важны понятный прогресс и спокойная система.",
        "speaking": "🗣 Поняла. Часто проблема не в знаниях, а в ступоре, стеснении и страхе ошибки в живом разговоре.",
        "other": "🌍 Поняла. Буду присылать полезные материалы для живого использования языка.",
    },
    "en": {
        "relocation": "✈️ Got it. You need language not from a textbook, but for real situations after relocation.",
        "career": "💼 Got it. Here language is not just knowledge — it is a tool for work situations and confidence.",
        "family": "👨‍👩‍👧 Got it. If language is for a child or family, progress and a calm system matter most.",
        "speaking": "🗣 Got it. Often the problem is not knowledge, but freezing, shame and fear of mistakes in real conversations.",
        "other": "🌍 Got it. I'll send useful content for real-life language use.",
    }
}

AFTER_SEGMENT = {
    "ru": {
        "relocation": """Здесь важно не учить всё подряд, а собрать язык вокруг твоей жизни и страны:

— аренда и жильё
— банк и документы
— врач и бытовые вопросы
— школа ребёнка
— разговоры с соседями и людьми вокруг

Дарья может помочь понять, что учить в первую очередь именно тебе.""",

        "career": """Для работы язык нужен в конкретных ситуациях:

— собеседование
— рабочие созвоны
— письма и сообщения
— клиенты и переговоры
— самопрезентация

Главная задача — не говорить идеально, а говорить уверенно и по делу. Дарья может помочь разобрать твою цель и подобрать формат занятий.""",

        "family": """Для ребёнка или семьи важно не просто “заниматься”, а видеть понятный прогресс:

— что ребёнок уже понимает
— что может сказать сам
— где застрял
— как закрепляет материал
— как родитель видит результат

Дарья может подобрать формат под возраст, цель и текущий уровень.""",

        "speaking": """Если ты понимаешь слова, но в разговоре теряешься — это не значит, что “язык не даётся”.

Часто нужен не новый учебник, а безопасная практика вокруг реальных ситуаций.

Дарья может помочь понять, что мешает именно тебе и как начать говорить спокойнее.""",

        "other": """Язык работает лучше, когда он привязан к реальной задаче: поездка, работа, семья, общение, переезд или личная уверенность.

Дарья может помочь уточнить цель и выбрать первый шаг.""",
    },
    "en": {
        "relocation": """The key is not to learn everything at once, but to build language around your real life and country:

— housing and rent
— bank and documents
— doctor and everyday questions
— child's school
— neighbours and people around you

Darya can help you understand what to learn first for your situation.""",

        "career": """For work, language is needed in specific situations:

— interviews
— work calls
— emails and messages
— clients and negotiations
— self-presentation

The goal is not perfect English. The goal is to speak clearly, confidently and professionally.""",

        "family": """For a child or family, lessons should not be just “classes”. You need visible progress:

— what the child understands
— what they can say
— where they get stuck
— how they practise
— how parents see the result

Darya can help choose a format for the child's age, goal and current level.""",

        "speaking": """If you know words but freeze in conversation, it does not mean languages are “not for you”.

Often you do not need another textbook. You need safe practice around real situations.

Darya can help identify what blocks you and how to start speaking more calmly.""",

        "other": """Language works better when it is connected to a real task: travel, work, family, communication, relocation or confidence.

Darya can help clarify your goal and choose the first step.""",
    }
}

# День 1 / 24 часа
DAY2 = {
    "ru": {
        "relocation": """Многие начинают готовиться к переезду с учебника.

Но в первые недели за границей чаще нужны не сложные правила, а простые фразы для реальных ситуаций:

— снять жильё
— объясниться у врача
— открыть счёт
— поговорить с соседями
— понять школу ребёнка

Если учить язык под жизнь, прогресс становится понятнее.

Хочешь, Дарья поможет определить, что тебе нужно учить в первую очередь?""",
        "career": """Для работы язык нужен не “вообще”.

Он нужен в конкретных ситуациях:

— рассказать о себе на собеседовании
— не потеряться на созвоне
— написать понятное письмо
— обсудить задачу с клиентом
— звучать профессионально, даже если язык не идеальный

Хочешь, Дарья поможет понять, с чего начать именно тебе?""",
        "family": """Если ребёнок учит язык, но не говорит — это не всегда проблема способностей.

Часто нет понятной системы:

— что он уже умеет
— где застрял
— как закрепляет материал
— есть ли живое использование языка
— видит ли родитель прогресс

Хочешь, Дарья подскажет, какой формат подойдёт вашему ребёнку?""",
        "speaking": """Если ты понимаешь отдельные слова, но в разговоре зависаешь — это не значит, что “язык не даётся”.

Чаще всего мешает не грамматика, а страх ошибки и отсутствие безопасной практики.

Говорить начинают не тогда, когда знают идеально. Говорить начинают, когда есть понятные ситуации и поддержка.

Хочешь, Дарья поможет понять, что мешает именно тебе?""",
        "other": """Одна из частых ошибок — учить язык слишком широко.

“Хочу английский” — это не цель.

Цель звучит иначе:

— хочу пройти собеседование
— хочу объясниться у врача
— хочу помочь ребёнку адаптироваться
— хочу говорить без ступора
— хочу понимать людей вокруг

Когда цель конкретная, уроки становятся практичнее.""",
    },
    "en": {
        "relocation": """Many people start preparing for relocation with a textbook.

But in the first weeks abroad, you usually need simple phrases for real situations:

— renting a place
— explaining yourself to a doctor
— opening a bank account
— talking to neighbours
— understanding your child's school

When language is connected to life, progress becomes clearer.

Would you like Darya to help you define what to learn first?""",
        "career": """For work, you do not need language “in general”.

You need it in specific situations:

— introducing yourself in an interview
— staying confident on a call
— writing a clear message
— discussing a task with a client
— sounding professional even if your language is not perfect

Would you like Darya to help you choose where to start?""",
        "family": """If a child studies a language but does not speak, it is not always about ability.

Often there is no clear system:

— what they can already do
— where they get stuck
— how they practise
— whether they use the language alive
— whether parents can see progress

Would you like Darya to suggest the right format for your child?""",
        "speaking": """If you understand separate words but freeze in conversation, it does not mean language is not for you.

Most often the barrier is not grammar. It is fear of mistakes and lack of safe practice.

People do not start speaking when they know perfectly. They start speaking when there are clear situations and support.

Would you like Darya to help find what blocks you?""",
        "other": """One common mistake is learning a language too broadly.

“I want English” is not a goal.

A goal sounds different:

— I want to pass an interview
— I want to explain myself to a doctor
— I want to help my child adapt
— I want to stop freezing when I speak
— I want to understand people around me

When the goal is specific, lessons become more practical.""",
    }
}

# День 2 / 48 часов
DAY4 = {
    "ru": {
        "relocation": """Язык для переезда — это не “выучить всё”.

Это собрать первые сценарии, в которых тебе придётся действовать:

1. жильё и аренда
2. документы и банк
3. врач и здоровье
4. школа / ребёнок / семья
5. разговоры в районе

Если хочешь, можешь написать Дарье страну и ситуацию. Она подскажет, с чего начать.""",
        "career": """Карьерный язык — это не только business vocabulary.

Чаще всего человеку нужно:

1. спокойно рассказать о себе
2. понимать вопросы на созвоне
3. переспросить без стыда
4. написать коротко и понятно
5. звучать профессионально

Можешь написать Дарье свою рабочую ситуацию одним сообщением.""",
        "family": """Для ребёнка важен не только преподаватель, но и маршрут.

Родителю важно понимать:

— какие темы проходят
— что ребёнок уже может сказать
— есть ли домашняя практика
— где нужна поддержка
— как меняется уверенность

Можешь написать Дарье возраст ребёнка и цель — она ответит лично.""",
        "speaking": """Разговорный барьер редко снимается фразой “просто говори”.

Нужны:

— безопасная практика
— понятные ситуации
— спокойная коррекция
— повторение живых фраз
— ощущение, что ошибаться можно

Можешь написать Дарье, где именно ты зависаешь: на работе, в поездках, с носителями или в обычном разговоре.""",
        "other": """Язык начинает работать, когда цель становится конкретной.

Не “хочу знать язык”, а:

— хочу говорить с врачом
— хочу пройти интервью
— хочу помочь ребёнку
— хочу общаться в поездках
— хочу не бояться разговора

Напиши Дарье свою ситуацию одним сообщением — она ответит лично.""",
    },
    "en": {
        "relocation": """Language for relocation is not about learning everything.

It is about the first situations where you must act:

1. housing and rent
2. documents and bank
3. doctor and health
4. school / child / family
5. everyday conversations nearby

You can write Darya your country and situation. She will suggest where to start.""",
        "career": """Career language is not only business vocabulary.

Most often people need to:

1. present themselves calmly
2. understand questions on calls
3. ask again without shame
4. write short and clear messages
5. sound professional

You can write Darya your work situation in one message.""",
        "family": """For a child, the teacher matters — but the route matters too.

Parents need to understand:

— what topics are covered
— what the child can already say
— whether there is home practice
— where support is needed
— how confidence changes

You can write Darya the child's age and goal. She will reply personally.""",
        "speaking": """The speaking barrier rarely disappears after “just speak”.

You need:

— safe practice
— clear situations
— calm correction
— repetition of living phrases
— permission to make mistakes

You can write Darya where you freeze: at work, while travelling, with native speakers or in everyday conversation.""",
        "other": """Language starts working when the goal becomes specific.

Not “I want to know the language”, but:

— I want to speak to a doctor
— I want to pass an interview
— I want to help my child
— I want to communicate while travelling
— I want to stop being afraid of conversation

Write Darya your situation in one message — she will reply personally.""",
    }
}

# День 3 / 72 часа
DAY6 = {
    "ru": {
        "relocation": """В Big Cheese Languages мы не начинаем с абстрактного учебника.

Мы смотрим на твою ситуацию:

— куда ты переезжаешь
— где язык нужен срочно
— какой уровень сейчас
— сколько времени реально есть
— какие ситуации вызывают тревогу

Так появляется понятный маршрут, а не хаос из тем.

Хочешь разобрать свой маршрут с Дарьей?""",
        "career": """В Big Cheese Languages рабочий язык собирается вокруг твоей задачи.

Не “пройти тему”, а подготовиться к тому, что реально нужно:

— интервью
— созвон
— письмо
— клиент
— презентация себя

Хочешь, Дарья поможет определить первый рабочий фокус?""",
        "family": """Если язык нужен ребёнку, важно видеть не просто факт уроков, а движение.

Мы смотрим на возраст, цель, уровень, мотивацию и формат, который ребёнок реально выдержит.

Так занятия становятся понятнее и для ребёнка, и для родителя.

Хочешь обсудить формат для вашего ребёнка?""",
        "speaking": """Если цель — начать говорить, важно не перегружать себя правилами.

Сначала нужны ситуации, в которых ты сможешь говорить маленькими шагами:

— представиться
— спросить
— уточнить
— объяснить
— поддержать разговор

Хочешь, Дарья поможет выбрать первые ситуации для практики?""",
        "other": """В Big Cheese Languages язык не учат ради галочки.

Мы смотрим на ситуацию человека:

— зачем нужен язык
— где человек теряется
— какой уровень сейчас
— сколько времени реально есть
— что должно измениться через месяц

Если хочешь, можно начать с первого урока и понятного маршрута.""",
    },
    "en": {
        "relocation": """At Big Cheese Languages, we do not start with an abstract textbook.

We look at your situation:

— where you are moving
— where language is needed urgently
— your current level
— how much time you really have
— which situations feel stressful

This creates a clear route, not chaos.

Would you like to map your route with Darya?""",
        "career": """At Big Cheese Languages, work language is built around your task.

Not “covering a topic”, but preparing for what you actually need:

— interview
— work call
— email
— client
— self-presentation

Would you like Darya to help define your first work focus?""",
        "family": """If language is for a child, you need to see movement, not just lessons.

We look at age, goal, level, motivation and the format the child can actually follow.

This makes learning clearer for both the child and the parent.

Would you like to discuss the right format?""",
        "speaking": """If the goal is to start speaking, you do not need to overload yourself with rules first.

You need situations where you can speak in small steps:

— introduce yourself
— ask
— clarify
— explain
— keep a conversation going

Would you like Darya to help choose your first speaking situations?""",
        "other": """At Big Cheese Languages, language is not learned just to tick a box.

We look at the person's situation:

— why the language is needed
— where the person gets stuck
— current level
— real available time
— what should change in a month

You can start with a first lesson and a clear route.""",
    }
}

# День 4 / 96 часов
DAY7 = {
    "ru": """Если язык тебе нужен для реальной жизни, лучше не ждать “идеального момента”.

Начать можно с малого:

— разобрать твою ситуацию
— понять уровень
— выбрать язык и цель
— составить первый маршрут
— попробовать формат урока

Дарья отвечает лично в течение 24 часов.

Оставить заявку?""",
    "en": """If you need language for real life, it is better not to wait for the “perfect moment”.

You can start small:

— explain your situation
— understand your level
— choose the language and goal
— build the first route
— try the lesson format

Darya replies personally within 24 hours.

Would you like to leave a request?"""
}

BTN_CTA = {
    "ru": ["✅ Записаться на урок", "❓ Написать Дарье"],
    "en": ["✅ Book a lesson", "❓ Message Darya"]
}

BTN_CHANNEL = {
    "ru": "📌 Канал Big Cheese",
    "en": "📌 Big Cheese channel"
}

CTA_BOOKED = {
    "ru": """Отлично! 🎉

Дарья ответит тебе лично в течение 24 часов — договоритесь об удобном времени.

Пока ждёшь — посмотри наш канал 👉 https://t.me/BigCheesemaster""",
    "en": """Awesome! 🎉

Darya will reply personally within 24 hours to schedule a convenient time.

While you wait — check our channel 👉 https://t.me/BigCheesemaster"""
}

CTA_QUESTION = {
    "ru": """Напиши свой вопрос прямо сюда одним сообщением.

Дарья получит его и ответит лично в течение 24 часов 🙂

Пока ждёшь — посмотри наш канал 👉 https://t.me/BigCheesemaster""",
    "en": """Write your question here in one message.

Darya will receive it and reply personally within 24 hours 🙂

While you wait — check our channel 👉 https://t.me/BigCheesemaster"""
}

FREE_TEXT_REPLY = {
    "ru": """Спасибо! Передала вопрос Дарье.

Она ответит лично в течение 24 часов 🙂

Канал Big Cheese: https://t.me/BigCheesemaster""",
    "en": """Thank you! I sent your question to Darya.

She will reply personally within 24 hours 🙂

Big Cheese channel: https://t.me/BigCheesemaster"""
}

# Legacy placeholders: старые интерактивные вопросы больше не используются в новой воронке,
# но оставлены, чтобы старые callback-паттерны не ломали код.
BTN_WHEN = {
    "ru": ["В ближайшие 1–3 месяца", "Через полгода", "Пока думаю"],
    "en": ["In 1–3 months", "In 6 months", "Still thinking"]
}
BTN_CAREER = {
    "ru": ["Говорить на созвонах", "Писать письма", "Собеседование"],
    "en": ["Speak on calls", "Write emails", "Interview"]
}
BTN_OTHER = {
    "ru": ["Да, узнаю", "Нет, другая ситуация"],
    "en": ["Yes, that's me", "No, different situation"]
}
ANSWERS = {"ru": {}, "en": {}}
