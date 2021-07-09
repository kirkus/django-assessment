from django.contrib import admin

from .models import Assessment, Option, OptionSet, Question, QuestionType, Response


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True


class OptionInline(admin.StackedInline):
    model = Option
    extra = 3


@admin.register(OptionSet)
class OptionSetAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    search_fields = ('name',)
    save_on_top = True


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_required', 'order', 'varname', 'type', 'assessment')
    list_filter = ('assessment', 'type')
    model = Question
    search_fields = ('name',)


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'question_name', 'answer', 'assessment')
    list_filter = ('assessment',)
    model = Response

    def question_name(self, obj):
        return obj.question.name[:100]
    question_name.short_description = "Question"
