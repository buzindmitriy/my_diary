def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from entries.models import Entry

    user_group, _ = Group.objects.get_or_create(name='Пользователь')
    editor_group, _ = Group.objects.get_or_create(name='Редактор')
    admin_group, _ = Group.objects.get_or_create(name='Администратор')

    content_type = ContentType.objects.get_for_model(Entry)

    view_permission = Permission.objects.get(codename='view_entry', content_type=content_type)
    add_permission = Permission.objects.get(codename='add_entry', content_type=content_type)
    change_permission = Permission.objects.get(codename='change_entry', content_type=content_type)
    delete_permission = Permission.objects.get(codename='delete_entry', content_type=content_type)

    user_group.permissions.set([view_permission, add_permission])
    editor_group.permissions.set([view_permission, add_permission, change_permission])
    admin_group.permissions.set([view_permission, add_permission, change_permission, delete_permission])