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


@docker_control.route("/control/<cmd>", methods=["POST"])
def contains_control(cmd):
    """
    cmd : start stop restart
    request {"id": ["1e3967531655", "f252c997504d"]}
    :return:
    """
    resp_message = {
        'code': 0,
    }

    id_list = request.json.get('id')
    if id_list:
        for i in id_list:
            container = docker_client.containers.get(i)
            if cmd in ('start', 'stop', 'restart'):
                getattr(container, cmd)()
                resp_message['code'] = 1

    return jsonify(resp_message)
