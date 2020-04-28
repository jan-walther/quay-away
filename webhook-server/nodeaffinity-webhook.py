from abc import ABC

from flask import Flask, request, jsonify
import base64
import jsonpatch
import multiprocessing
import gunicorn.app.base
import os

admission_controller = Flask(__name__)


@admission_controller.route('/health', methods=['GET'])
def pod_health():
    return "OK"


def admission_response(allowed, message):
    return jsonify({"response": {"allowed": allowed, "status": {"message": message}}})


@admission_controller.route('/mutate', methods=['POST'])
def pod_webhook_mutate():
    request_info = request.get_json()
    containers = request_info['request']['object']['spec']['containers']

    patches = []

    for counter, container in enumerate(containers):
        if container['image'].startswith('quay.io'):
            patches.append({
                'op': 'replace',
                'path': f'/spec/containers/{counter}/image',
                'value': container['image'].replace('quay.io', os.environ['DOCKER_REGISTRY'])
            })

    return admission_response_patch(True, "Adding nodeSelector ", json_patch=jsonpatch.JsonPatch(patches))


def admission_response_patch(allowed, message, json_patch: jsonpatch.JsonPatch):
    base64_patch = base64.b64encode(
        json_patch.to_string().encode("utf-8")).decode("utf-8")
    return jsonify({"response": {"allowed": allowed,
                                 "status": {"message": message},
                                 "patchType": "JSONPatch",
                                 "patch": base64_patch}})


class StandaloneApplication(gunicorn.app.base.BaseApplication, ABC):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


if __name__ == '__main__':
    options = {
        'bind': '0.0.0.0:443',
        'keyfile': '/webhook-ssl/key.pem',
        'certfile': '/webhook-ssl/cert.pem',
        'workers': number_of_workers(),
    }
    admission_controller.logger.info("Hello World!")
    StandaloneApplication(admission_controller, options).run()
