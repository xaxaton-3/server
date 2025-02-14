from mistralai import Mistral

from django.conf import settings


class AiClient:
    mistalai_token = settings.MISTRAL_TOKEN
    ai_model = 'mistral-large-latest'

    def __init__(self):
        self.client = Mistral(api_key=self.mistalai_token)

    def send_request(self, prompt: str) -> str:
        response = self.client.chat.complete(
            model=self.ai_model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }
            ]
        )
        return response.choices[0].message.content

    def get_beautiful_text(self, text_before: str) -> str:
        prompt = self.get_beautiful_text_template(text_before)
        response = self.send_request(prompt)
        return response

    def get_beautiful_text_template(self, text_to_refactor: str) -> str:
        template = f"""
        Дан текст о Герое, защитнике нашей Родины: {text_to_refactor}
        Представь, что ты являешься профессиональным редактором и тебе требуется подготовить данный текст
        к публикации на информационном ресурсе, посвященном Героям отечества. Нужно, чтобы ты очень аккуратно
        отредактировал данный текст, не искажая его смысл.
        Если его длина превышает {settings.MAX_PERSON_HISTORY_LENGTH} символов, то нужно его
        укоротить, но также, не теряя смысла. Пересмотри предложения, которые кажутся сухими, неполными и так далее,
        нужно, чтобы текст этот текст был прекрасен. Не приписывай ничего лишнего, только по сути данного фрагмента.
        В своем ответе пришли только готовый текст, без представления, обращений ко мне и тому подобного.
        """
        return template
