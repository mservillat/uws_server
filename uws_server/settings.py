#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (c) 2016 by Mathieu Servillat
# Licensed under MIT (https://github.com/mservillat/uws-server/blob/master/LICENSE)
"""
Settings for the UWS server
"""

import os
import sys
import logging
import logging.config

# Set debug mode, HTTP 500 Errors include traceback
DEBUG = True

# Where is located the code of the web app
APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#'/home/mservillat/CTA/git_voparis/uws_server'

# Where is located the data used/generated by the web app
VAR_PATH = '/var/www/opus'
# This is used to defined the following structure further below:
# /db/' + SQLITE_FILE_NAME
# /logs'
# /jdl'
# /jdl/scripts'
# /jobdata'
# /uploads'
# /temp'

# URL an IP of the web server
BASE_URL = 'http://localhost'
BASE_IP = '127.0.0.1'

# Those servers can have access to /job_event/<jobid_manager> to change the phase or report an error
# The IP can be truncated to allow to refer to a set of IPs
JOB_SERVERS = {
    '::1': 'localhost',
    '127.0.0.1': 'localhost',
    '145.238.151.': 'tycho/quadri12',
}

# The server will allow db and jdl access only from trusted clients (while waiting for an auth system)
# e.g. /db/init, /jdl/validate...
TRUSTED_CLIENTS = {
    '::1': 'localhost',
    '127.0.0.1': 'localhost',
    '145.238.193.69': 'voparis-uws-test.obspm.fr',
    '145.238.168.3': 'savagnin_ucopia',
    '145.238.180.240': 'savagnin_cable',
    '93.15.50.214': 'savagnin_home',
}

# Add the provenance files to the results of the jobs
GENERATE_PROV = True

# Job Description Language (VOTFile, WADLFile)
JDL = 'VOTFile'

# Storage of job information (SQLAlchemy, SQLite, PGSQL)
STORAGE = 'SQLAlchemy'  # define SQLALCHEMY_DB further below
# SQLite storage info
SQLITE_FILE_NAME = 'job_database.db'
# PGSQL storage info
PGSQL_HOST = 'localhost'
PGSQL_PORT = 5432
PGSQL_DATABASE = 'opus'
PGSQL_USER = 'opus'
PGSQL_PASSWORD = 'opus'

# Define a Manager and its properties (Local, SLURM)
MANAGER = 'Local'
# SLURM Manager
SLURM_URL = 'tycho.obspm.fr'  # 'quadri12.obspm.fr'  #
SLURM_USER = 'vouws'
SLURM_USER_MAIL = 'mathieu.servillat@obspm.fr'
SLURM_HOME_PATH = '/obs/vouws'  # '/obs/vouws'
SLURM_JOBDATA_PATH = '/poubelle/vouws/jobdata'
SLURM_WORKDIR_PATH = '/scratch/vouws'
SLURM_SBATCH_DEFAULT = {
    'mem': '200mb',
    'nodes': 1,
    'ntasks-per-node': 1,
    'partition': 'short',  # for tycho...
    # 'account': 'obspm',  # for quadri12...
    # 'partition': 'def',  # for quadri12...'
}
PHASE_CONVERT = {
    # Conversions for SLURM job state codes
    'RUNNING': dict(phase='EXECUTING', msg='Job currently has an allocation.'),
    'PENDING': dict(phase='QUEUED', msg='Job is awaiting resource allocation.'),
    'CONFIGURING': dict(phase='QUEUED', msg='Job has been allocated resources, but are waiting for them '
                                            'to become ready for use'),
    'FAILED': dict(phase='ERROR', msg='Job terminated with non-zero exit code or other failure condition.'),
    'NODE_FAIL': dict(phase='ERROR', msg='Job terminated due to failure of one or more allocated nodes.'),
    'TIMEOUT': dict(phase='ERROR', msg='Job terminated upon reaching its time limit.'),
    'PREEMPTED': dict(phase='ERROR', msg='Job terminated due to preemption.'),
    'CANCELLED': dict(phase='ABORTED', msg='Job was explicitly cancelled by the user or system '
                                           'administrator. The job may or may not have been initiated.'),
    'SUSPENDED': dict(phase='SUSPENDED', msg='Job has an allocation, but execution has been suspended.'),
}

# Default destruction interval
DESTRUCTION_INTERVAL = 30  # in days

# Maximum and default execution duration, 0 implies unlimited execution duration
EXECUTION_DURATION_DEF = 120  # in seconds
EXECUTION_DURATION_MAX = 3600  # in seconds

# Maximum and default wait time (UWS1.1)
WAIT_TIME_DEF = 60  # in seconds
WAIT_TIME_MAX = 60  # in seconds



# ----------
# Internal variables
# ----------


# ISO date format for datetime
DT_FMT = '%Y-%m-%dT%H:%M:%S'

# Table columns defined in database
JOB_ATTRIBUTES = [
    'jobid',
    'jobname',
    'phase',
    'creation_time',
    'start_time',
    'end_time',
    'destruction_time',
    'execution_duration',
    'quote',
    'error',
    'owner',
    'owner_pid',
    'run_id',
    'pid',
]
JOB_PARAMETERS_ATTR = [
    'jobid',
    'name',
    'value',
    'byref',
]
JOB_RESULTS_ATTR = [
    'jobid',
    'name',
    'url',
    'content_type'
]

# Known phases
PHASES = [
    'PENDING',
    'QUEUED',
    'EXECUTING',
    'COMPLETED',
    'ERROR',
    'ABORTED',
    'UNKNOWN',
    'HELD',
    'SUSPENDED',
]

# Active phases (evolution expected for job)
ACTIVE_PHASES = [
    'PENDING',
    'QUEUED',
    'EXECUTING',
]

# Terminal phases (no evolution expected for job)
TERMINAL_PHASES = [
    'COMPLETED',
    'ERROR',
    'ABORTED',
    'HELD',
    # 'SUSPENDED',
]

# suffix to the log file (may be set by test.py of settings_local.py)
LOG_FILE_SUFFIX = ''



# ----------
# Variables may be redefined in a settings_local.py file
# ----------


#--- Include host-specific settings ------------------------------------------------------------------------------------
if os.path.exists(APP_PATH + '/uws_server/settings_local.py'):
    from settings_local import *
#--- Include host-specific settings ------------------------------------------------------------------------------------

#--- If imported from test.py, redefine settings -----------------------------------------------------------------------
main_dict = sys.modules['__main__'].__dict__
if 'test.py' in main_dict.get('__file__', ''):
    print '\nPerforming tests'
    if 'LOG_FILE_SUFFIX' in main_dict:
        LOG_FILE_SUFFIX = main_dict['LOG_FILE_SUFFIX']
    if 'STORAGE' in main_dict:
        STORAGE = main_dict['STORAGE']
    if 'SQLITE_FILE_NAME' in main_dict:
        SQLITE_FILE_NAME = main_dict['SQLITE_FILE_NAME']
    if 'MANAGER' in main_dict:
        MANAGER = main_dict['MANAGER']
#--- If imported from test.py, redefine settings -----------------------------------------------------------------------

#--- Set all _PATH based on APP_PATH or VAR_PATH -----------------------------------------------------------------------
# Path to sqlite db file
SQLITE_FILE = VAR_PATH + '/db/' + SQLITE_FILE_NAME
SQLALCHEMY_DB = 'sqlite:///' + SQLITE_FILE
# Logging
LOG_PATH = VAR_PATH + '/logs'
# Path for JDL files, should probably be accessed through a URL as static files
JDL_PATH = VAR_PATH + '/jdl'
# Path for script files, should probably be accessed through a URL as static files
SCRIPT_PATH = VAR_PATH + '/jdl/scripts'
# Path for job results and logs
JOBDATA_PATH = VAR_PATH + '/jobdata'
# If POST contains files they are uploaded on the UWS server
UPLOAD_PATH = VAR_PATH + '/uploads'
# Path for e.g. SLURM sbatch files created by SLURMManager
TEMP_PATH = VAR_PATH + '/temp'
#--- Set all _PATH based on APP_PATH -----------------------------------------------------------------------------------

# Set logger
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s %(funcName)s: %(message)s'
        },
        'with_user': {
            'format': '[%(asctime)s] %(levelname)s %(funcName)s: %(message)s [%(user)s]'
        },
        'module': {
            'format': '[%(asctime)s] %(levelname)s %(module)s.%(funcName)s: %(message)s'
        },
    },
    'handlers': {
        'file_server': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_PATH + '/server' + LOG_FILE_SUFFIX + '.log',
            'formatter': 'default'
        },
        'file_server_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_PATH + '/server' + LOG_FILE_SUFFIX + '_debug.log',
            'formatter': 'default'
        },
        'file_client': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_PATH + '/client' + LOG_FILE_SUFFIX + '.log',
            'formatter': 'default'
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_PATH + '/debug' + LOG_FILE_SUFFIX + '.log',
            'formatter': 'module'
        },
    },
    'loggers': {
        'uws_server': {
            'level': 'DEBUG',
            'handlers': ['file_server', 'file_server_debug'],
        },
        'uws_client': {
            'level': 'DEBUG',
            'handlers': ['file_client'],
        },
        'beaker': {
            'level': 'DEBUG',
            'handlers': ['file_debug'],
        },
        'cork': {
            'level': 'DEBUG',
            'handlers': ['file_debug'],
        },
        'prov': {
            'level': 'DEBUG',
            'handlers': ['file_debug'],
        },
    }
}

# Add the username to the logs
class CustomAdapter(logging.LoggerAdapter):
    """
    This adapter expects the passed in dict-like object to have a
    'username' key, whose value in brackets is appended to the log message.
    """
    def process(self, msg, kwargs):
        return '{} [{}]'.format(msg, self.extra['username']), kwargs

# Set logger
logging.config.dictConfig(LOGGING)
logger_init = logging.getLogger('uws_server')
logger = logger_init