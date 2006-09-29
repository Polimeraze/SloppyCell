import cPickle
import logging
import smtplib
from email.MIMEText import MIMEText

import scipy

from scipy import linspace, logspace

import random
import copy

def send_email(to_addr, from_addr=None, subject='', message=''):
    """
    Send a plain-text email to a single address.
    """
    if from_addr is None:
        from_addr = to_addr

    # Create a text/plain message
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['To'], msg['From'] = to_addr, from_addr

    # From the documentation for email... Not sure what it means. :-)
    ## Send the message via our own SMTP server, but don't include the
    ## envelope header.
    s = smtplib.SMTP()
    s.connect()
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.close()

def save(obj, filename):
    """
    Save an object to a file
    """
    f = file(filename, 'wb')
    cPickle.dump(obj, f, 2)
    f.close()

def load(filename):
    """
    Load an object from a file
    """
    f = file(filename, 'rb')
    obj = cPickle.load(f)
    f.close()
    return obj

def eig(mat):
    """
    Return the sorted eigenvalues and eigenvectors of mat.
    """
    e, v = scipy.linalg.eig(mat)
    order = scipy.argsort(abs(e))[::-1]
    e = scipy.take(e, order)
    v = scipy.take(v, order, axis=1)

    return e, v

def bootstrap(data,num_iterates=100):
    """
    Use sampling with replication to calculate variance in estimates.
    """
    len_data = len(data)
    sampled_data = []
    for ii in range(num_iterates):
        sampled_data.append([random.choice(data) for ii in range(len_data)])

    return sampled_data
        
def enable_debugging_msgs(filename=None):
    """
    Enable output of debugging messages.

    If filename is None messages will be sent to stderr.
    """
    logging.root.setLevel(logging.DEBUG)

    if filename is not None:
        # Remove other handlers
        for h in logging.root.handlers:
            logging.root.removeHandler(h)

        # We need to add a file handler
        handler = logging.FileHandler(filename)
        # For some reason the default file handler format is different.
        # Let's change it back to the default
        formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        handler.setFormatter(formatter)
        logging.root.addHandler(handler)
    logging.debug('Debug messages enabled.')

def disable_debugging_msgs():
    """
    Disable output of debugging messages.
    """
    logging.root.setLevel(logging.WARN)
    # Remove all other handlers
    for h in logging.root.handlers:
        logging.root.removeHandler(h)
    # Restore basic configuration
    logging.basicConfig()

def disable_warnings():
    logging.root.setLevel(logging.CRITICAL)

def enable_warnings():
    logging.root.setLevel(logging.WARNING)

class SloppyCellException(Exception):
    pass

import Redirector_mod
Redirector = Redirector_mod.Redirector

