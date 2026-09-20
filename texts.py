"""Parallel test corpus for Lab 01.

The same three items in English, Russian and Kazakh. Parallel meaning is the
point: any difference in token count is a property of the tokenizer, not of
what is being said.

Instructors: the Kazakh and Russian wordings are a starting point. Substitute
your own if you prefer -- but keep the three versions semantically parallel,
otherwise the comparison measures translation length instead of tokenization.
"""

from __future__ import annotations

from typing import Dict

LANGUAGES = ("en", "ru", "kk")

#: One sentence. Short enough to inspect token by token.
SENTENCE: Dict[str, str] = {
    "en": "I transferred money to my savings account yesterday.",
    "ru": "Вчера я перевёл деньги на свой сберегательный счёт.",
    "kk": "Кеше мен жинақ шотыма ақша аудардым.",
}

#: A realistic support request about a bank transfer.
COMPLAINT: Dict[str, str] = {
    "en": (
        "Good afternoon. I made a transfer from my account yesterday, "
        "but the money has not arrived. The amount was deducted from my balance. "
        "I have attached the transaction receipt. Please explain why the transfer "
        "has not been completed and tell me what I should do next."
    ),
    "ru": (
        "Добрый день. Вчера я совершил перевод со своего счёта, "
        "но деньги ещё не поступили. Эта сумма была списана с моего баланса. "
        "Я прилагаю квитанцию о переводе. Пожалуйста, объясните, почему перевод "
        "не был завершён, и сообщите, что мне делать дальше."
    ),
    "kk": (
        "Қайырлы күн. Кеше өз шотымнан ақша аудардым, "
        "бірақ ақша әлі түскен жоқ. Бұл сома шотымдағы қалдықтан есептен шығарылды. "
        "Аударым туралы түбіртекті қоса тіркеп отырмын. Аударымның неге аяқталмағанын "
        "түсіндіріп, әрі қарай не істеу керектігін айтып беруіңізді сұраймын."
    ),
}

#: A short bank notice used as an additional parallel corpus item.
NOTICE: Dict[str, str] = {
    "en": (
        "Your transfer was received by the bank and is being processed. "
        "Please wait for the confirmation before contacting support."
    ),
    "ru": (
        "Ваш перевод получен банком и обрабатывается. "
        "Пожалуйста, дождитесь подтверждения, прежде чем обращаться в поддержку."
    ),
    "kk": (
        "Сіздің аударымыңыз банкке түсті және өңделіп жатыр. "
        "Қолдау қызметіне хабарласпас бұрын растауды күтіңіз."
    ),
}

KK_SHARED: Dict[str, str] = {
    "en": "The bank checks the transfer and sends a message.",
    "ru": "Банк проверяет перевод и отправляет сообщение.",
    "kk": "Банк аударымды тексереді және хабарлама жібереді.",
}

KK_SPECIFIC: Dict[str, str] = {
    "en": "The bank checks the transfer and sends a message.",
    "ru": "Банк проверяет перевод и отправляет сообщение.",
    "kk": "Әрбір ұйым қызметкері жаңа өтінішті мұқият тексереді.",
}

#: A system prompt -- the part you resend on every single request.
SYSTEM_PROMPT: Dict[str, str] = {
    "en": (
        "You are a support assistant for a retail bank. Answer only from the "
        "documents provided. If the answer is not in them, say so. Never invent "
        "an account number, a rate or a date."
    ),
    "ru": (
        "Вы — ассистент поддержки розничного банка. Отвечайте только по "
        "предоставленным документам. Если ответа в них нет, так и скажите. "
        "Никогда не выдумывайте номер счёта, ставку или дату."
    ),
    "kk": (
        "Сіз — бөлшек банктің қолдау көрсету ассистентісіз. Тек берілген "
        "құжаттар бойынша жауап беріңіз. Егер жауап оларда болмаса, солай деп "
        "айтыңыз. Шот нөмірін, мөлшерлемені немесе күнді ешқашан ойдан "
        "шығармаңыз."
    ),
}

#: Everything the lab measures, keyed by a short id.
CORPUS: Dict[str, Dict[str, str]] = {
    "sentence": SENTENCE,
    "complaint": COMPLAINT,
    "notice": NOTICE,
    "system_prompt": SYSTEM_PROMPT,
    "kk_shared": KK_SHARED,
    "kk_specific": KK_SPECIFIC,
}
