import asyncio
import ollama


class AIOllamaService:
    # TODO сделать интерфейс для данного класса
    DEFAULT_PERSONA = (
        "Ты — дружелюбный Twitch-бот по имени ПУДЖ. Общайся по-русски, "
        "коротко (1–3 предложения), позитивно и по-человечески. "
        "Можно немного шутить. Без политики, жесткой токсичности "
        "и нарушений Twitch. Допустим легкий несерьёзный мат, "
        "но не оскорбляй людей и не задевай чувствительные темы."
    )
    BASE_PROMPT = (
        "Отвечай кратко, не больше одного абзаца. "
        "Не нарушай правила Twitch. "
        "Будь толерантен к полу, расе и ориентации. "
        "Всегда отвечай только на русском языке."
    )

    def __init__(self, model: str = "aya:8b") -> None:
        self.model = model
        self.persona = self.DEFAULT_PERSONA

    async def answer(self, question: str) -> str:
        system_prompt = self._build_system_prompt()

        response = await asyncio.to_thread(
            ollama.chat,
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            options={
                "stop": ["\n\n"],
            },
        )

        return response["message"]["content"]

    async def ask_streamer(self, context: str) -> str:
        system_prompt = self._build_system_prompt()

        user_prompt = (
            f"Контекст стрима:\n{context}\n\n"
            "Сгенерируй вопрос стримеру в стиле своего персонажа."
        )

        response = await asyncio.to_thread(
            ollama.chat,
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return response["message"]["content"]

    def _build_system_prompt(self) -> str:
        return (
            f"Описание твоего персонажа: {self.persona}\n" f"Важно: {self.BASE_PROMPT}"
        )

    async def set_random_persona(self) -> None:
        prompt = (
            "Сгенерируй интересного персонажа. Персонаж должен отличаться особенным "
            "характером. Персонаж может быть из любого времени. "
            "Персонаж должен использовать какой то особый жаргон (укажи конкретно)."
            "Дай персонажу имя."
            "Начни с 'ТЫ - '."
            "Пиши только описание личности, без разговорного ответа."
        )

        # TODO ОБРАБОТКА ОШИБКО?
        response = await asyncio.to_thread(
            ollama.chat,
            model=self.model,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        self.persona = response["message"]["content"]
