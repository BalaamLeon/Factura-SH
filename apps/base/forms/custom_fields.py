from crispy_forms.layout import Field
from crispy_forms.utils import TEMPLATE_PACK, render_field
from django.utils.html import conditional_escape


class PrependedAppendedText(Field):
    template = "custom_fields/prepended_appended_text_custom.html"

    def __init__(self, field, prepended_text=None, appended_text=None, input_size=None, *args, **kwargs):
        self.field = field
        self.appended_text = appended_text
        self.prepended_text = prepended_text
        if "active" in kwargs:
            self.active = kwargs.pop("active")

        self.input_size = input_size
        css_class = kwargs.get("css_class", "")

        # Bootstrap 3
        if "input-lg" in css_class:
            self.input_size = "input-lg"
        if "input-sm" in css_class:
            self.input_size = "input-sm"

        super().__init__(field, *args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        extra_context = extra_context.copy() if extra_context is not None else {}
        extra_context.update(
            {
                "crispy_appended_text": self.appended_text,
                "crispy_prepended_text": self.prepended_text,
                "input_size": self.input_size,
                "active": getattr(self, "active", False),
            }
        )
        if hasattr(self, "wrapper_class"):
            extra_context["wrapper_class"] = self.wrapper_class
        template = self.get_template_name(template_pack)
        return render_field(
            self.field,
            form,
            form_style,
            context,
            template=template,
            attrs=self.attrs,
            template_pack=template_pack,
            extra_context=extra_context,
            **kwargs,
        )


class AppendedText(PrependedAppendedText):
    def __init__(self, field, text, *args, **kwargs):
        kwargs.pop("appended_text", None)
        kwargs.pop("prepended_text", None)
        self.text = text
        super().__init__(field, appended_text=text, **kwargs)


class PrependedText(PrependedAppendedText):
    def __init__(self, field, text, *args, **kwargs):
        kwargs.pop("appended_text", None)
        kwargs.pop("prepended_text", None)
        self.text = text
        super().__init__(field, prepended_text=text, **kwargs)


class CustomInlineCheckboxes(Field):
    """
    Layout object for rendering checkboxes inline::

        InlineCheckboxes('field_name')
    """

    template = "custom_fields/checkboxselectmultiple_inline_custom.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return super().render(
            form, form_style, context, template_pack=template_pack, extra_context={"inline_class": "inline"}
        )


class CustomFloatingField(Field):
    template = "custom_fields/floating_field_custom.html"


class CustomFloatingFieldWithIcon(Field):
    template = "custom_fields/floating_field_with_icon_custom.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = list(args)

        if not hasattr(self, "attrs"):
            self.attrs = {}
        else:
            # Make sure shared state is not edited.
            self.attrs = self.attrs.copy()

        if "css_class" in kwargs:
            if "class" in self.attrs:
                self.attrs["class"] += " %s" % kwargs.pop("css_class")
            else:
                self.attrs["class"] = kwargs.pop("css_class")

        self.wrapper_class = kwargs.pop("wrapper_class", None)
        self.icon = kwargs.pop("icon", None)
        self.template = kwargs.pop("template", self.template)

        # We use kwargs as HTML attributes, turning data_id='test' into data-id='test'
        self.attrs.update({k.replace("_", "-"): conditional_escape(v) for k, v in kwargs.items()})

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        if extra_context is None:
            extra_context = {}
        if hasattr(self, "wrapper_class"):
            extra_context["wrapper_class"] = self.wrapper_class

        if hasattr(self, "icon"):
            extra_context["icon"] = self.icon

        template = self.get_template_name(template_pack)

        return self.get_rendered_fields(
            form,
            form_style,
            context,
            template_pack,
            template=template,
            attrs=self.attrs,
            extra_context=extra_context,
            **kwargs,
        )
