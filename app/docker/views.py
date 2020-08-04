# -*- coding: utf-8 -*-

from flask import request, jsonify
from . import docker_control
from tools.docker_control import docker_client


@docker_control.route("/list")
def contains_list():

    resp_message = {
        'code': 0,
        'message': 'Parameter is invalid'
    }

    contains = docker_client.containers.list()
    print(contains)

    return jsonify(resp_message)
