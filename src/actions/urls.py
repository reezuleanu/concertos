from django.urls import path
from . import views


urlpatterns = [
    path("", views.post_action, name="post_action"),
    # path("download/", views.download_test, name="download_test"),
    # path("all/", views.get_all_actions, name="get_all_actions"),
    path("triggers/", views.get_trigger_types, name="get_trigger_types"),
    path(
        "variables/global/",
        views.get_all_global_variables,
        name="get_all_global_variables",
    ),  # todo work on this
    path(
        "variables/personal/",
        views.get_all_personal_variables,
        name="get_all_personal_variables",
    ),
    # path("<str:action_name>/", views.get_action, name="specific_action"),
    path(
        "variables/global/<str:variable_name>",
        views.global_variable,
        name="global_variable",
    ),
    path(
        "variables/personal/<str:variable_name>/<int:user_id>",
        views.personal_variable,
        name="personal_variable",
    ),
    path("variables/create", views.post_variable, name="post_variable"),
    # path("html/", views.get_html, name="get_html"),  # ! deprecated
    path("functions/<int:deviceid>/", views.get_funcs, name="get_funcs"),
    path("captain/<str:button_name>/", views.captain_trigger, name="captain_trigger"),
    path("captain/", views.get_captain_buttons, name="get_captain_buttons"),
    path("<str:action_name>/", views.get_action, name="specific_action"),
]
