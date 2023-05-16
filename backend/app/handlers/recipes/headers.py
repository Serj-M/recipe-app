events_header = {
    'name': {
        'title': 'Название мероприятия',
        'type': 'string',
        'can_sort': True,
        'filter': {
            'type': 'string'
        }
    },
    'participant_department': {
        'title': 'Участники',
        'type': 'list',
        'can_sort': False,
        "filter": {
            "name": "departments",
            "type": "multiselect",
            "data_route": {
                "url": "/nsi/departments/list",
                "method": "POST"
            }
        }
    },
    'object_name': {
        'title': 'Объекты',
        'type': 'list',
        'can_sort': False,
        'filter': {
            'name': 'objects',
            'type': 'multiselect',
            'data_route': {
                'url': '/nsi/localization_objects/list',
                'method': 'POST'
            }
        }
    },
    'date_start': {
        'title': 'Дата начала',
        'type': 'date',
        'can_sort': True,
        'filter': {
            'type': 'date'
        }
    },
    'date_end': {
        'title': 'Дата завершения',
        'type': 'date',
        'can_sort': True,
        'filter': {
            'type': 'date'
        }
    },
    'event_status_name': {
        'title': 'Статус',
        'type': 'string',
        'can_sort': True,
        'filter': {
            'name': 'status_id',
            'type': 'multiselect',
            'data_route': {
                'url': '/nsi/event_status/list',
                'method': 'POST'
            }
        }
    },
    'event_type_name': {
        'title': 'Тип',
        'type': 'string',
        'can_sort': True,
        'filter': {
            'name': 'type_id',
            'type': 'multiselect',
            'data_route': {
                'url': '/nsi/event_type/list',
                'method': 'POST'
            }
        }
    },
    'cost': {
        'title': 'Стоимость тыс. руб.',
        'type': 'doubledValue',
        'can_sort': True
    },
    'responsible_department_id': {
        'title': 'Ответственное подразделение',
        'type': 'string',
        'can_sort': True
    },
    'actions': {
        'title': 'Действия',
        'type': 'actions'
    }
}