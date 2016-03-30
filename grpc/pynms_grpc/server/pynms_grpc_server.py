#!/usr/bin/env python

import sys
import os
import time
from pyangbind.lib.xpathhelper import YANGPathHelper
from pyangbind.lib.serialise import pybindJSONEncoder
from pynms_grpc.common import pynms_rpc_pb2
from pynms_grpc.common.nms_grpc.helpers import PyNMSGRPCMethods
from pynms_grpc.common import ybind

class GPRCPyNMSServicer(pynms_rpc_pb2.BetaOCPyNMSServicer):
  def __init__(self, path_helper):
    self._path_helper = path_helper

  def Get(self, request, context):
    response_msg = PyNMSGRPCMethods.service_get_request(request, self._path_helper)
    return response_msg

  def Set(self, request, context):
    response_msg = PyNMSGRPCMethods.service_set_request(request, self._path_helper)
    return response_msg

class PyNMSGRPCServer(object):
  def __init__(self, path_helper, port=50051):
    self._path_helper = path_helper
    self._server = pynms_rpc_pb2.beta_create_OCPyNMS_server(GPRCPyNMSServicer(self._path_helper))
    self._server.add_insecure_port("[::]:%s" % port)

  def serve(self, runtime=86400):
    self._server.start()
    try:
      while True:
        time.sleep(86400)
    except KeyboardInterrupt:
      self._server.stop(0)

if __name__ == '__main__':
  # create a path helper instance to be used by the server
  yph = YANGPathHelper()

  # set up a basic device
  for ymod in ["simple_device"]:
    ymod_cls = getattr(ybind, ymod, None)
    if ymod is None:
      raise AttributeError("Cannot load module %s from bindings" % ymod)
    ymod_cls(path_helper=yph)

  ysys = yph.get_unique("/system")
  ysys.config.hostname = "rtr0"
  ysys.config.domain_name = "lhr.uk"

  netelem = PyNMSGRPCServer(path_helper=yph)
  netelem.serve()