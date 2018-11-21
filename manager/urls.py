from django.urls import path
from manager import views


urlpatterns = [
    path('', views.collections, name='home'),
    path('collections/add/', views.collections_add),
    path('collections/edit/<uuid:uuid>/', views.items, name='display_collection'),
    path('collections/edit/<uuid:uuid>/save/', views.collections_edit),
    path('collections/delete/<uuid:uuid>/', views.collections_delete),
    path('collections/<uuid:uuid>/items/add/', views.items_add),
    path('collections/items/<uuid:uuid>/', views.items_value, name='display_value'),
    path('collections/items/<uuid:uuid>/delete/', views.items_delete),
    path('collections/items/<uuid:uuid>/value/add/', views.items_value_add),
    path('collections/items/value/<uuid:uuid>/delete/', views.items_value_del),
    path('collections/items/<uuid:item_uuid>/field/<uuid:field_uuid>/generate/', views.items_value_generate),
    path('collections/<uuid:uuid>/generate/', views.collection_items_generate_selection),
    path('collections/<uuid:uuid>/generate/do/', views.collection_items_generate),
    path('collections/<uuid:uuid>/generate/fix/', views.collection_fix),
    path('collections/<uuid:uuid>/generate/do/fix/', views.collection_items_generate_fix),
    path('collections/duplicate/<uuid:uuid>/', views.collection_duplicate),

    path('types/', views.types, name='types'),
    path('types/add/', views.types_add),
    path('types/edit/<uuid:uuid>/', views.types_detail, name='types_detail'),
    path('types/edit/<uuid:uuid>/save/', views.types_edit),
    path('types/delete/<uuid:uuid>/', views.types_delete),
    path('types/option/<uuid:uuid>/add/', views.option_add),
    path('types/option/<uuid:uuid>/delete/', views.option_remove),
    path('types/subtype/add/', views.subtype_add),
    path('types/subtype/edit/<uuid:uuid>/', views.subtype_detail, name='subtype_detail'),
    path('types/subtype/edit/<uuid:uuid>/save/', views.subtype_edit),
    path('types/subtype/delete/<uuid:uuid>/', views.subtypes_delete),
    path('types/duplicate/<uuid:uuid>/', views.types_duplicate),

    path('exports/', views.exports, name='index_export'),
    path('exports/add/', views.exports_add),
    path('exports/delete/<uuid:uuid>/', views.exports_del),
    path('exports/duplicate/<uuid:uuid>/', views.export_duplicate),
    path('exports/edit/<uuid:uuid>/', views.exports_view, name='display_export'),
    path('exports/edit/<uuid:uuid>/save/', views.exports_update),
    path('exports/<uuid:uuid>/param/add/', views.exports_param_add),
    path('exports/param/<uuid:uuid>/delete/', views.exports_param_del),
    path('collections/<uuid:uuid>/export/', views.export_collection),

    path('tasks/', views.tasks, name='tasks')
]
