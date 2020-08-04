# -*- coding: utf-8 -*-

import json
from flask import request, jsonify
from . import docker_control
from tools.docker_control import docker_client


@docker_control.route("/list")
def contains_list():
    """
    :return:
    """
    resp_message = {
        'code': 0,
        'contains': list(),
        'message': 'Empty'
    }

    contains = docker_client.containers.list()
    if contains:
        resp_message['code'] = 1
        resp_message['message'] = "succeed"
        for c in contains:
            resp_message['contains'].append(
                {'name': c.attrs['Name'],
                 'Status': c.attrs['State']['Status'],
                 'id_': c.attrs['Id']}
            )

    return jsonify(resp_message)


@docker_control.route("/start", methods=["POST"])
def contains_start():
    """
    request {
        "contains": [{"id_": "", "status": "", }]
    }
    :return:
    """
    resp_message = {
        'code': 0,
    }

    contains_list = request.json.get('contains')
    try:
        assert isinstance(contains_list, list)
        for c in contains_list:
            assert isinstance(c, dict)
            container = docker_client.containers.get(c.get('id_'))
            if container and c.get('status') != 'running':
                container.start()
        resp_message['code'] = 1
    except Exception as e:
        pass
    return jsonify(resp_message)


@docker_control.route("/stop", methods=["POST"])
def contains_stop():
    """
    request {
        "contains": [{"id_": "", "status": "", }]
    }
    :return:
    """
    resp_message = {
        'code': 0,
    }

    # contains_list = request.json.get('contains')
    # try:
    #     assert isinstance(contains_list, list)
    #     for c in contains_list:
    #         assert isinstance(c, dict)
    #         container = docker_client.containers.get(c.get('id_'))
    #         if container and c.get('status') == 'running':
    #             container.stop()
    #     resp_message['code'] = 1
    # except Exception as e:
    #     pass
    id_list = request.json.get('id')
    try:
        for i in id_list:
            container = docker_client.containers.get(i)
            print(container.status)
            container.stop()
        resp_message['code'] = 1
    except Exception as e:
        pass
    return jsonify(resp_message)