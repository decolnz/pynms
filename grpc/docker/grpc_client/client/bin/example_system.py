#!/usr/bin/env python

from pynms_grpc.client.pynms_grpc_client import PyNMSGRPCClient
from pynms_grpc.client.client_common import PyNMSConfigOperation
from pynms_yang_examples.bindings import simple_device
import sys
import json

def main():
  client = PyNMSGRPCClient('localhost', 50051)
  client.run()


  # An example of getting paths from the remote server via gRPC
  print "Check existing configuration..."
  response = client.get_paths(["/system/config/hostname", "/system/config/domain-name", "/system"], 0)
  for res in response.response:
    print "%s->%s" % (res.path, json.dumps(json.loads(res.value), indent=4))

  # An example of configuring elements from the remote server via gRPC
  s = simple_device()
  s.system.config.hostname = "router42"
  s.system.config.domain_name = "heart-of-gold.beeblebrox"

  config_operation = PyNMSConfigOperation(s.system, 'UPDATE_CONFIG')

  print "Before configuration modification..."
  print "Hostname: %s" % client.get_paths(["/system/config/hostname"], 1).response[0].value
  print "Domain Name: %s" % client.get_paths(["/system/config/domain-name"], 2).response[0].value

  client.set_paths([config_operation])

  print "After configuration modification..."
  print "Hostname: %s" % client.get_paths(["/system/config/hostname"], 3).response[0].value
  print "Domain Name: %s" % client.get_paths(["/system/config/domain-name"], 4).response[0].value

  sys.exit(0)

if __name__ == '__main__':
  main()