# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import proxy_pb2 as proxy__pb2


class ProxyServiceStub(object):
  """service, encode a plain text 
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Predict = channel.unary_unary(
        '/proxytest.ProxyService/Predict',
        request_serializer=proxy__pb2.input.SerializeToString,
        response_deserializer=proxy__pb2.response.FromString,
        )
    self.Return = channel.unary_unary(
        '/proxytest.ProxyService/Return',
        request_serializer=proxy__pb2.input.SerializeToString,
        response_deserializer=proxy__pb2.response.FromString,
        )
    self.SetModel = channel.unary_unary(
        '/proxytest.ProxyService/SetModel',
        request_serializer=proxy__pb2.modelinfo.SerializeToString,
        response_deserializer=proxy__pb2.response.FromString,
        )
    self.SetDAG = channel.unary_unary(
        '/proxytest.ProxyService/SetDAG',
        request_serializer=proxy__pb2.dag.SerializeToString,
        response_deserializer=proxy__pb2.response.FromString,
        )
    self.Ping = channel.unary_unary(
        '/proxytest.ProxyService/Ping',
        request_serializer=proxy__pb2.hi.SerializeToString,
        response_deserializer=proxy__pb2.response.FromString,
        )


class ProxyServiceServicer(object):
  """service, encode a plain text 
  """

  def Predict(self, request, context):
    """request a service of encode
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Return(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetModel(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetDAG(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Ping(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ProxyServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Predict': grpc.unary_unary_rpc_method_handler(
          servicer.Predict,
          request_deserializer=proxy__pb2.input.FromString,
          response_serializer=proxy__pb2.response.SerializeToString,
      ),
      'Return': grpc.unary_unary_rpc_method_handler(
          servicer.Return,
          request_deserializer=proxy__pb2.input.FromString,
          response_serializer=proxy__pb2.response.SerializeToString,
      ),
      'SetModel': grpc.unary_unary_rpc_method_handler(
          servicer.SetModel,
          request_deserializer=proxy__pb2.modelinfo.FromString,
          response_serializer=proxy__pb2.response.SerializeToString,
      ),
      'SetDAG': grpc.unary_unary_rpc_method_handler(
          servicer.SetDAG,
          request_deserializer=proxy__pb2.dag.FromString,
          response_serializer=proxy__pb2.response.SerializeToString,
      ),
      'Ping': grpc.unary_unary_rpc_method_handler(
          servicer.Ping,
          request_deserializer=proxy__pb2.hi.FromString,
          response_serializer=proxy__pb2.response.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'proxytest.ProxyService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
