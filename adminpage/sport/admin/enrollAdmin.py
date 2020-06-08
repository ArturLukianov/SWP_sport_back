from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin

from sport.models import Enroll, Group

from .mixins import EnrollExportXlsxMixin
from .utils import custom_titled_filter, cache_filter, cache_dependent_filter, custom_order_filter


class TrainerTextFilter(AutocompleteFilter):
    title = "trainer"
    field_name = "trainer"
    rel_model = Group
    parameter_name = "group__trainer"


@admin.register(Enroll)
class EnrollAdmin(admin.ModelAdmin, EnrollExportXlsxMixin):
    autocomplete_fields = (
        "student",
        "group",
    )

    list_filter = (
        # semester filter, resets group sub filter
        (
            "group__semester",
            cache_filter(custom_order_filter(("-start",)), ["group__id"])
        ),
        # group filter, depends on chosen semester
        (
            "group",
            cache_dependent_filter({"group__semester": "semester"}, ("name",))
        ),
        ("group__is_club", custom_titled_filter("club status")),
        ("is_primary", custom_titled_filter("primary status")),
        ("group__sport", admin.RelatedOnlyFieldListFilter),
        TrainerTextFilter,
    )

    list_display = (
        'student',
        'group',
        'is_primary',
    )
    actions = (
        "export_as_csv",
    )

    class Media:
        js = (
            "sport/js/list_filter_collapse.js",
        )