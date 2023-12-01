from garpix_utils.logs.enums.get_enums import Action
from garpix_utils.logs.services.logger_iso import LoggerIso, ActionResult


class CreateLogMixin:
    log_msg_delete = None
    log_msg_create = None
    log_msg_change = None

    @staticmethod
    def log_delete(logger, request, obj, action):

        obj_title = getattr(obj, 'title', getattr(obj, 'name', None))

        title = f' и с названием {obj_title}' if obj_title else ''

        msg = CreateLogMixin.log_msg_delete if CreateLogMixin.log_msg_delete else f'Объект {obj.__class__.__name__} c id={obj.pk}{title} был удален'
        return logger.create_log(action=action,
                                 obj=obj.__class__.__name__,
                                 obj_address=request.path,
                                 result=ActionResult.success,
                                 sbj=request.user.username,
                                 sbj_address=LoggerIso.get_client_ip(request),
                                 msg=msg)

    @staticmethod
    def log_change_or_create(logger, request, obj, change, action_change=None, action_create=None):
        obj_title = getattr(obj, 'title', getattr(obj, 'name', None))

        title = f' с названием {obj_title}' if obj_title else ''

        if change:
            old_obj = obj.__class__.objects.get(pk=obj.pk) if change else None
            changed_fields = ''
            fields = obj._meta.fields
            for field in fields:
                field_name = field.name
                old_value = getattr(old_obj, field_name)
                new_value = getattr(obj, field_name)
                if old_obj and old_value != new_value:
                    changed_fields += f'{field.verbose_name}: {old_value} -> {new_value};'
            params = changed_fields
            action = action_change or Action.any_entity_change.value
            msg = CreateLogMixin.log_msg_change if CreateLogMixin.log_msg_change else f'Объект {obj.__class__.__name__} c id={obj.pk}{title} был изменен'
        else:
            action = action_create or Action.any_entity_create.value
            msg = CreateLogMixin.log_msg_create if CreateLogMixin.log_msg_create else f'Объект {obj.__class__.__name__} {title} был добавлен'
            params = None

        return logger.create_log(action=action,
                                 obj=obj.__class__.__name__,
                                 obj_address=request.path,
                                 result=ActionResult.success,
                                 sbj=request.user.username,
                                 params=params,
                                 sbj_address=LoggerIso.get_client_ip(request),
                                 msg=msg)
