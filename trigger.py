# coding=utf-8
import json
import os
import requests
import logging
from subprocess import call
from flask import Flask, request

app = Flask(__name__)

path = "/root/.jenkins/workspace/"


@app.route('/', methods=['post'])
def build():
    json_payload = json.loads(request.data)
    if json_payload['ref'] != 'refs/heads/master':
        return 'fail'

    repo = json_payload['repository']['name']
    url = json_payload['repository']['url']
    commit_id = json_payload['after']

    actual_path = "%s%s" % (path, repo)

    logging.info("git --git-dir=%s/.git --work-tree=/%s/ pull origin master" % (actual_path, actual_path))

    logging.info("git clone %s %s" % (url, actual_path))

    if os.path.isdir("%s" % actual_path):
        os.system("git --git-dir=%s/.git --work-tree=/%s/ pull origin master" % (actual_path, actual_path))
    else:
        os.system("git clone %s %s" % (url, actual_path))


    requests.post('http://10.15.38.146:8080/jenkins/job/ci-java-job/buildWithParameters',
                  headers={
                      "Jenkins-Crumb": "34dc6325387a674950906eff2c5a3bcc"
                  },
                  data={
                      "branch":"dev",
                      "repo":"git@192.168.0.175:INF/zipkin_test.git",
                      "build_command":"mvn clean install",
                      "notification_emails":"zhugongyi@niwodai.net"
                  })
    return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8090)

