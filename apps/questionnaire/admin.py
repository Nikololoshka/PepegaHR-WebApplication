from django.contrib import admin

from .models import Questionnaire, SingleChooseQuiz, SingleChooseVariant, \
                    MultiChooseQuiz, MultiChooseVariant, ArbitraryQuiz, \
                    Answer, SingleChooseAnswer, MultiChooseAnswer, \
                    MultiChooseAnswerVariant, ArbitraryAnswer 


admin.site.register(Questionnaire)
admin.site.register(SingleChooseQuiz)
admin.site.register(SingleChooseVariant)
admin.site.register(MultiChooseQuiz)
admin.site.register(MultiChooseVariant)
admin.site.register(ArbitraryQuiz)

admin.site.register(Answer)
admin.site.register(SingleChooseAnswer)
admin.site.register(MultiChooseAnswer)
admin.site.register(MultiChooseAnswerVariant)
admin.site.register(ArbitraryAnswer)
