# -*- coding: utf-8 -*-

from flask import request, jsonify
from . import docker_control
from tools.docker_control import docker_client


@docker_control.route("/list")
def contains_list():

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


@docker_control.route("/start", methods=["GET", "POST"])
def contains_start():

    resp_message = {
        'code': 0,
        'message': 'Parameter is invalid'
    }

    return jsonify(resp_message)
