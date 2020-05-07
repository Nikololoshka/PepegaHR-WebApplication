from django.contrib import admin

from .models import Questionnaire, SingleChooseQuiz, SingleChooseVariant, \
                    MultiChooseQuiz, MultiChooseVariant, ArbitraryQuiz


admin.site.register(Questionnaire)
admin.site.register(SingleChooseQuiz)
admin.site.register(SingleChooseVariant)
admin.site.register(MultiChooseQuiz)
admin.site.register(MultiChooseVariant)
admin.site.register(ArbitraryQuiz)
