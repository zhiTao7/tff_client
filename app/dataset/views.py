# -*- coding: utf-8 -*-

import os
from flask import request, jsonify
from flask import current_app
from . import dataset


@dataset.route("/upload", methods=["POST"])
def dataset_upload():
    """

    :return:
    """

    resp_message = {'code': 0}

    file_obj = request.files.get('file_path')
    if file_obj:
        _file_path = os.path.join(current_app.config['BASE_DATASET_DIR'], file_obj.filename)
        if not os.path.exists(_file_path):
            with open(_file_path, 'wb') as f:
                f.write(file_obj.read())
            resp_message["code"] = 1

    return jsonify(resp_message)


@dataset.route("/delete")
def dataset_delete():

    resp_message = {'code': 0}

    file_name = request.args.get('dataset')
    if file_name:
        _file_path = os.path.join(current_app.config['BASE_DATASET_DIR'], file_name)
        if os.path.exists(_file_path):
            try:
                os.remove(_file_path)
            except FileNotFoundError:
                pass
            resp_message['code'] = "1"

    return jsonify(resp_message)
