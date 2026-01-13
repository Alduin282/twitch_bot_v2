import asyncio
import ollama


class AIOllamaService:
    # TODO сделать интерфейс для данного класса
    DEFAULT_PERSONA = (
        "Ты — дружелюбный Twitch-бот. Общайся по-русски, коротко (1–3 предложения), "
        "позитивно и по-человечески. Будь дружелюбным, живым и немного шутливым, "
        "но без токсичности, мата, политики и нарушений Twitch. "
        "Отвечай ясно, помогай зрителям и поддерживай атмосферу стрима."
        "Твое имя - ПУДЖ"
    )
    BASE_PROMPT = (
        "Отвечай кратко, не больше абзаца."
        "не нарушай правила платформы Twitch"
        "Будь толлерантен к полу, расе и сексуальной ориентации "
        "(в остальном можешь использовать ругательства). "
        "Всегда отвечай только на русском языке."
    )
    # TODO убрать противоречия в канстантах сверху

    def __init__(self, model: str = "aya:8b") -> None:
        self.model = model
        self.persona = self.DEFAULT_PERSONA

    async def answer(self, question: str) -> str:
        # TODO убрать дублирование по систем промпт
        system_prompt = (
            f"Описание твоего персонажа: {self.persona} Важно: {self.BASE_PROMPT}"
        )

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

    async def ask_streamer(self, context: str) -> str:

        system_prompt = (
            f"Описание твоего персонажа: {self.persona} Важно: {self.BASE_PROMPT}"
        )

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
