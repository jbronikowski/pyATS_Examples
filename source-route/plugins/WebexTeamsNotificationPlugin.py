import logging
import os
import json
import requests
# from requests_toolbelt.multipart.encoder import MultipartEncoder
from ats.log.utils import banner
from pyats.easypy.plugins.bases import BasePlugin
from pyats import configuration as cfg

logger = logging.getLogger("WEBEXTEAMS-NOTIFICATION")

MESSAGE_TEMPLATE = """
## JOB RESULT REPORT

### Job Information

**Total Tasks**    : {results[total]}

**Overall Stats**

Passed     : {results[passed]}\n
Passx      : {results[passx]}\n
Failed     : {results[failed]}\n
Aborted    : {results[aborted]}\n
Blocked    : {results[blocked]}\n
Skipped    : {results[skipped]}\n
Errored    : {results[errored]}\n

"""

class WebExTeamsNotification(BasePlugin):
    '''
    Runs after each task, sends notification upon failure
    '''

    @classmethod
    def configure_parser(cls, parser, legacy_cli = True):
        grp = parser.add_argument_group('WebEx')

        if legacy_cli:
            room = ['-webex_room']
            token = ['-webex_token']
        else:
            room = ['--webex-room']
            token = ['--webex-token']

        grp.add_argument(*token,
                         dest='webex_token',
                         action="store",
                         type=str,
                         metavar='',
                         default = None,
                         help='Webex AUTH Token')

        grp.add_argument(*room,
                         dest='webex_room',
                         action="store",
                         type=str,
                         metavar='',
                         default = None,
                         help='Webex Room to dump to')
        return grp

    def pre_job(self, job):
        self.shared_obj = self.runtime.synchro.dict()

        self.token = self.runtime.args.webex_token or cfg.get('webex.token')
        self.room = self.runtime.args.webex_room or cfg.get('webex.room')

        self.enabled = True
        logger.info(self.token)

        if not self.token and self.room:
            logger.info("SPARK_TOKEN or ROOM_ID not found in env, disabling")
            #self.enabled = False

    def _headers(self, content_type='application/json'):
        headers = {'Authorization': 'Bearer {}'.format(self.token),
                   'Content-Type': content_type}
        return headers

    def _send_msg(self, msg):
        payload = {'roomId': self.room,
                   'markdown': msg}
        url = 'https://api.ciscospark.com/v1/messages'
        if self.enabled:
            logger.info('Sending WebEx Teams notification')
            r = requests.post(url,
                              data=json.dumps(payload),
                              headers=self._headers())
            logger.info(r.text)

    def pre_task(self, task):
        # dict shared
        task.kwargs['webex_dict'] = self.shared_obj

    def post_job(self, job):

        # see if script returned new token or whatever
        self.token = self.shared_obj.get('token', self.token)
        self.room = self.shared_obj.get('room', self.room)

        #print('SIMING is: ', self.shared_obj['SIMING'])

        logger.info('Running post job plugin')
        logger.info(banner("JOB RESULTS"))
        self._send_msg(MESSAGE_TEMPLATE.format(results=job.results))
