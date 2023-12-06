from django.core.exceptions import FieldDoesNotExist


class RenderField:
    def __init__(self, field_name, admin):
        self.field_name = field_name
        self.admin = admin

        try:
            self.model_field = self.admin.model._meta.get_field(self.field_name)
        except (FieldDoesNotExist, AttributeError):
            self.model_field = None

    @property
    def admin_field(self):
        return getattr(self.admin, self.field_name, None)

    def get_value(self, obj):
        if field := self.admin_field:
            return field(obj) if callable(field) else field
        return getattr(obj, self.field_name)

    def get_field_ordering(self) -> str:
        if self.admin_field and hasattr(self.admin_field, "order_field"):
            return self.admin_field.order_field

        if self.model_field:
            return self.model_field.name

        return ""

    def get_label(self, form=None):
        if self.admin_field and hasattr(self.admin_field, "label"):
            return self.admin_field.label

        form_field = form.fields.get(self.field_name) if form else None

        if form_field:
            return form_field.label

        if self.model_field:
            return self.model_field.verbose_name

        return self.field_name

    def get_tooltip(self, obj):
        if (field := self.admin_field) and hasattr(field, "tooltip"):
            _tooltip = field.tooltip
            return _tooltip(obj) if callable(_tooltip) else _tooltip
        return None

    def __repr__(self):
        return f"{self.__class__.__name__} {self.field_name}"
