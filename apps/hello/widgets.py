from django import forms
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.safestring import mark_safe


class DatePickerWidget(forms.DateInput):
    class Media:
        css = {
            'all': (staticfiles_storage.url('css/jquery-ui.min.new.css'),)
        }
        js = (
            staticfiles_storage.url('js/jquery-1.11.1.min.js'),
            staticfiles_storage.url('js/jquery-ui.min.js'),
            staticfiles_storage.url('js/jquery.form.min.js'),
            staticfiles_storage.url('js/form.js'),
        )

    def __init__(self, params='', attrs=None):
        self.params = params
        super(DatePickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(DatePickerWidget, self).render(name, value,
                                                        attrs=attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $('#id_%s').datepicker({%s});
            </script>''' % (name, self.params,))
