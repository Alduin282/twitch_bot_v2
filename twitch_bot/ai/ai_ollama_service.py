import asyncio
import ollama


class AIOllamaService:
    DEFAULT_PERSONA = (
        "Ты — дружелюбный Twitch пользователь. Общайся по-русски, "
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
        "Не начинай с приветствия"
    )

    def __init__(self, model: str = "aya:8b", request_timeout: int = 30) -> None:
        self.model = model
        self.persona = self.DEFAULT_PERSONA
        self.request_timeout = request_timeout

    async def answer(self, question: str) -> str:
        system_prompt = self._build_system_prompt()

        response = await self._chat(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ]
        )
        return response

    async def ask_streamer(self, context: str = "без контекста") -> str:
        system_prompt = self._build_system_prompt()

        user_prompt = (
            f"Контекст стрима:\n{context}\n\n"
            "Сгенерируй вопрос стримеру в стиле своего персонажа."
        )

        response = await self._chat(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response

    async def set_random_persona(self) -> None:
        prompt = (
            "Сгенерируй интересного персонажа. Персонаж должен отличаться особенным "
            "характером. Персонаж может быть из любого времени. "
            "Персонаж должен использовать какой то особый жаргон (укажи конкретно)."
            "Дай персонажу имя."
            "Начни с 'ТЫ - '."
            "Пиши только описание личности, без разговорного ответа."
        )

        response = await self._chat([{"role": "user", "content": prompt}])

        self.persona = response

    def reset_persona(self) -> None:
        self.persona = self.DEFAULT_PERSONA

    def get_persona(self) -> str:
        return self.persona

    def _build_system_prompt(self) -> str:
        return (
            f"Описание твоего персонажа: {self.persona}\n" f"Важно: {self.BASE_PROMPT}"
        )

    async def _chat(self, messages: list[dict]) -> str:
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    ollama.chat,
                    model=self.model,
                    messages=messages,
                    options={
                        "stop": ["\n\n"],
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "repeat_penalty": 1.3,
                    },
                ),
                timeout=self.request_timeout,
            )

            return response.get("message", {}).get("content", "…у меня ступор 🥲")

        except asyncio.TimeoutError:
            return "Не повезло. Попробуй ещё раз, может получится 😅"
        except Exception:
            return "Что-то пошло не так 😬"
