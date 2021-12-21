from django import forms
from django.db import transaction

from .models import QuestionType as Q_Type, Response


class AssessmentFormFactory(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super().__init__(*args, **kwargs)

        choices = []
        attrs = {
            'class': 'form-control',
            'placeholder': self.question.placeholder,
            'required': self.question.is_required
        }
        field_kwargs = {
            'required': self.question.is_required,
            'label': self.question.name,
            'help_text': self.question.help_text,
        }

        q_type = self.question.type.slug
        if q_type in [Q_Type.CHECKBOX, Q_Type.DROPDOWN, Q_Type.RADIO_BUTTON]:
            if q_type == Q_Type.DROPDOWN and not self.question.is_required:
                choices.append(("", "---------------"))
            for option in self.question.option_set.options.all():
                choices.append(tuple([option.value, option.text]))

        if q_type == Q_Type.CHECKBOX:
            self.fields[f'{self.question.varname}'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                choices=choices,
                **field_kwargs
            )

        if q_type in [Q_Type.DROPDOWN, Q_Type.RADIO_BUTTON]:
            widget = forms.Select if q_type == Q_Type.DROPDOWN else forms.RadioSelect
            self.fields[f'{self.question.varname}'] = forms.ChoiceField(
                widget=widget(attrs=attrs),
                choices=tuple(choices),
                **field_kwargs
            )

        if q_type in [Q_Type.SHORT_TEXT, Q_Type.LONG_TEXT]:
            widget = forms.Textarea if q_type == Q_Type.LONG_TEXT else forms.TextInput
            self.fields[f'{self.question.varname}'] = forms.CharField(
                widget=widget(attrs=attrs),
                **field_kwargs
            )

        if q_type == Q_Type.IMAGE_INPUT:
            self.fields[f'{self.question.varname}'] = forms.ImageField(
                widget=forms.ClearableFileInput(attrs=attrs),
                **field_kwargs
            )

        if q_type == Q_Type.FILE_INPUT:
            self.fields[f'{self.question.varname}'] = forms.FileField(
                widget=forms.ClearableFileInput(attrs=attrs),
                **field_kwargs
            )


class ResponseForm:
    def __init__(self, data=None, files=None, **kwargs):
        self.assessment = kwargs.pop('assessment')
        self.user = kwargs.pop('user', None)
        self.key = kwargs.pop('key', '')
        self.forms = [
            AssessmentFormFactory(
                data=data,
                files=files,
                initial=kwargs.get('initial'),
                question=q,
                prefix=kwargs.get('prefix'),
            ) for q in self.assessment.questions.all()
        ]

    def is_valid(self):
        return all(f.is_valid() for f in self.forms)

    @property
    def errors(self):
        return [f.errors for f in self.forms]

    def has_error(self):
        for f in self.forms:
            if f.errors:
                return True
        return False

    @transaction.atomic
    def save(self):
        for form in self.forms:
            data = form.cleaned_data[form.question.varname]
            Response.objects.update_or_create(
                user=self.user,
                key=self.key,
                assessment=self.assessment,
                question=form.question,
                defaults={
                    'answer': data or '',
                    'image': data if form.question.is_image else None,
                    'file': data if form.question.is_file else None
                }
            )
