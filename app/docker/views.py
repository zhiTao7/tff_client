# -*- coding: utf-8 -*-

import json
import docker
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

    contains = docker_client.containers.list(all=True)
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


@docker_control.route("/control/<cmd>")
def contains_control(cmd):
    """
    cmd : stop restart
    :return:
    """
    resp_message = {
        'code': 0,
    }
    id_list = request.args.get('_id')
    if cmd in ('stop', 'restart'):
        try:
            container = docker_client.containers.get(id_list)
        except docker.errors.NotFound:
            pass
        else:
            getattr(container, cmd)()
            resp_message['code'] = 1

    return jsonify(resp_message)
