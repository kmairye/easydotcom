from django.conf import settings

from google.cloud import translate_v2 as translate

# Google translate api
translate_client = translate.Client()
text = "Dette er et forsøg på oversættelse fra google cloud"
target = "en"
result = translate_client.translate(text, target_language=target)
print(u'Text: {}'.format(result['input']))
print(u'Translation: {}'.format(result['translatedText']))
print(u'Detected source language: {}'.format(result['detectedSourceLanguage']))


# Middleware
class LanguageDetectorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.supported_languages = settings.LANGUAGES

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        try:
            accepted = request.META["HTTP_ACCEPT_LANGUAGE"]
            accepted = accepted.split(",")
            print(accepted)
            print(accepted[0])
            if accepted[0] in self.supported_languages:
                response.context_data["supported_languages"] = self.supported_languages[accepted[0]]
                return response
        except:
            pass

        return response
