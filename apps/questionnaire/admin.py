from django.contrib import admin

from .models import Questionnaire, SingleChooseQuiz, SingleChooseVariant, \
                    MultiChooseeQuiz, MultiChooseeVariant, ArbitraryQuiz


admin.site.register(Questionnaire)
admin.site.register(SingleChooseQuiz)
admin.site.register(SingleChooseVariant)
admin.site.register(MultiChooseeQuiz)
admin.site.register(MultiChooseeVariant)
admin.site.register(ArbitraryQuiz)
