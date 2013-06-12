###############################################################################
##
##  Copyright 2013 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

__all__ = ["PerMessageSnappyMixin",
           "PerMessageSnappyOffer",
           "PerMessageSnappyOfferAccept",
           "PerMessageSnappyResponse",
           "PerMessageSnappyResponseAccept",
           "PerMessageSnappy"]


import snappy

from compress_base import PerMessageCompressOffer, \
                          PerMessageCompressOfferAccept, \
                          PerMessageCompressResponse, \
                          PerMessageCompressResponseAccept, \
                          PerMessageCompress


class PerMessageSnappyMixin:
   """
   Mixin class for this extension.
   """

   EXTENSION_NAME = "permessage-snappy"
   """
   Name of this WebSocket extension.
   """



class PerMessageSnappyOffer(PerMessageCompressOffer, PerMessageSnappyMixin):
   """
   Set of extension parameters for `permessage-snappy` WebSocket extension
   offered by a client to a server.
   """

   @classmethod
   def parse(Klass, params):
      """
      Parses a WebSocket extension offer for `permessage-snappy` provided by a client to a server.

      :param params: Output from :method:`autobahn.websocket.WebSocketProtocol._parseExtensionsHeader`.
      :type params: list

      :returns: object -- A new instance of :class:`autobahn.compress.PerMessageSnappyOffer`.
      """
      ## extension parameter defaults
      ##
      acceptNoContextTakeover = False
      requestNoContextTakeover = False

      ##
      ## verify/parse c2s parameters of permessage-snappy offer
      ##
      for p in params:

         if len(params[p]) > 1:
            raise Exception("multiple occurence of extension parameter '%s' for extension '%s'" % (p, Klass.EXTENSION_NAME))

         val = params[p][0]

         if p == 'c2s_no_context_takeover':
            if val != True:
               raise Exception("illegal extension parameter value '%s' for parameter '%s' of extension '%s'" % (val, p, Klass.EXTENSION_NAME))
            else:
               acceptNoContextTakeover = True

         elif p == 's2c_no_context_takeover':
            if val != True:
               raise Exception("illegal extension parameter value '%s' for parameter '%s' of extension '%s'" % (val, p, Klass.EXTENSION_NAME))
            else:
               requestNoContextTakeover = True

         else:
            raise Exception("illegal extension parameter '%s' for extension '%s'" % (p, Klass.EXTENSION_NAME))

      offer = Klass(acceptNoContextTakeover,
                    requestNoContextTakeover)
      return offer


   def __init__(self,
                acceptNoContextTakeover = True,
                requestNoContextTakeover = False):
      """
      Constructor.

      :param acceptNoContextTakeover: Iff true, client accepts "no context takeover" feature.
      :type acceptNoContextTakeover: bool
      :param requestNoContextTakeover: Iff true, client request "no context takeover" feature.
      :type requestNoContextTakeover: bool
      """
      self.acceptNoContextTakeover = acceptNoContextTakeover
      self.requestNoContextTakeover = requestNoContextTakeover


   def getExtensionString(self):
      """
      Returns the WebSocket extension configuration string as sent to the server.

      :returns: str -- PMCE configuration string.
      """
      pmceString = self.EXTENSION_NAME
      if self.acceptNoContextTakeover:
         pmceString += "; c2s_no_context_takeover"
      if self.requestNoContextTakeover:
         pmceString += "; s2c_no_context_takeover"
      return pmceString


   def __json__(self):
      """
      Returns a JSON serializable object representation.

      :returns: object -- JSON serializable represention.
      """
      return {'extension': self.EXTENSION_NAME,
              'acceptNoContextTakeover': self.acceptNoContextTakeover,
              'requestNoContextTakeover': self.requestNoContextTakeover}


   def __repr__(self):
      """
      Returns Python object representation that can be eval'ed to reconstruct the object.

      :returns: str -- Python string representation.
      """
      return "PerMessageSnappyOffer(acceptNoContextTakeover = %s, requestNoContextTakeover = %s)" % (self.acceptNoContextTakeover, self.requestNoContextTakeover)



class PerMessageSnappyOfferAccept(PerMessageCompressOfferAccept, PerMessageSnappyMixin):
   """
   Set of parameters with which to accept an `permessage-snappy` offer
   from a client by a server.
   """

   def __init__(self,
                offer,
                requestNoContextTakeover = False):
      """
      Constructor.

      :param offer: The offer being accepted.
      :type offer: Instance of :class:`autobahn.compress.PerMessageSnappyOffer`.
      :param requestNoContextTakeover: Iff true, server request "no context takeover" feature.
      :type requestNoContextTakeover: bool
      """
      if not isinstance(offer, PerMessageSnappyOffer):
         raise Exception("invalid type %s for offer" % type(offer))

      self.offer = offer

      if type(requestNoContextTakeover) != bool:
         raise Exception("invalid type %s for requestNoContextTakeover" % type(requestNoContextTakeover))

      if requestNoContextTakeover and not offer.acceptNoContextTakeover:
         raise Exception("invalid value %s for requestNoContextTakeover - feature unsupported by client" % requestNoContextTakeover)

      self.requestNoContextTakeover = requestNoContextTakeover


   def getExtensionString(self):
      """
      Returns the WebSocket extension configuration string as sent to the server.

      :returns: str -- PMCE configuration string.
      """
      pmceString = self.EXTENSION_NAME
      if self.offer.requestNoContextTakeover:
         pmceString += "; s2c_no_context_takeover"
      if self.requestNoContextTakeover:
         pmceString += "; c2s_no_context_takeover"
      return pmceString


   def __json__(self):
      """
      Returns a JSON serializable object representation.

      :returns: object -- JSON serializable represention.
      """
      return {'extension': self.EXTENSION_NAME,
              'offer': self.offer.__json__(),
              'requestNoContextTakeover': self.requestNoContextTakeover}


   def __repr__(self):
      """
      Returns Python object representation that can be eval'ed to reconstruct the object.

      :returns: str -- Python string representation.
      """
      return "PerMessageSnappyAccept(offer = %s, requestNoContextTakeover = %s)" % (self.offer.__repr__(), self.requestNoContextTakeover,)



class PerMessageSnappyResponse(PerMessageCompressResponse, PerMessageSnappyMixin):
   """
   Set of parameters for `permessage-snappy` responded by server.
   """

   @classmethod
   def parse(Klass, params):
      """
      Parses a WebSocket extension response for `permessage-snappy` provided by a server to a client.

      :param params: Output from :method:`autobahn.websocket.WebSocketProtocol._parseExtensionsHeader`.
      :type params: list

      :returns: object -- A new instance of :class:`autobahn.compress.PerMessageSnappyResponse`.
      """
      c2s_no_context_takeover = False
      s2c_no_context_takeover = False

      for p in params:

         if len(params[p]) > 1:
            raise Exception("multiple occurence of extension parameter '%s' for extension '%s'" % (p, Klass.EXTENSION_NAME))

         val = params[p][0]

         if p == 'c2s_no_context_takeover':
            if val != True:
               raise Exception("illegal extension parameter value '%s' for parameter '%s' of extension '%s'" % (val, p, Klass.EXTENSION_NAME))
            else:
               c2s_no_context_takeover = True

         elif p == 's2c_no_context_takeover':
            if val != True:
               raise Exception("illegal extension parameter value '%s' for parameter '%s' of extension '%s'" % (val, p, Klass.EXTENSION_NAME))
            else:
               s2c_no_context_takeover = True

         else:
            raise Exception("illegal extension parameter '%s' for extension '%s'" % (p, Klass.EXTENSION_NAME))

      response = Klass(c2s_no_context_takeover,
                       s2c_no_context_takeover)
      return response


   def __init__(self,
                c2s_no_context_takeover,
                s2c_no_context_takeover):
      self.c2s_no_context_takeover = c2s_no_context_takeover
      self.s2c_no_context_takeover = s2c_no_context_takeover



class PerMessageSnappyResponseAccept(PerMessageCompressResponseAccept, PerMessageSnappyMixin):
   """
   Set of parameters with which to accept an `permessage-snappy` response
   from a server by a client.
   """

   def __init__(self,
                response):
      """
      Constructor.

      :param response: The response being accepted.
      :type response: Instance of :class:`autobahn.compress.PerMessageSnappyResponse`.
      """
      if not isinstance(response, PerMessageSnappyResponse):
         raise Exception("invalid type %s for response" % type(response))

      self.response = response


   def __json__(self):
      """
      Returns a JSON serializable object representation.

      :returns: object -- JSON serializable represention.
      """
      return {'extension': self.EXTENSION_NAME,
              'response': self.response.__json__()}


   def __repr__(self):
      """
      Returns Python object representation that can be eval'ed to reconstruct the object.

      :returns: str -- Python string representation.
      """
      return "PerMessageSnappyResponseAccept(response = %s)" % self.response.__repr__()



class PerMessageSnappy(PerMessageCompress, PerMessageSnappyMixin):
   """
   `permessage-snappy` WebSocket extension processor.
   """

   @classmethod
   def createFromResponseAccept(Klass, isServer, accept):
      pmce = Klass(isServer,
                   accept.response.s2c_no_context_takeover,
                   accept.response.c2s_no_context_takeover)
      return pmce


   @classmethod
   def createFromOfferAccept(Klass, isServer, accept):
      pmce = Klass(isServer,
                   accept.offer.requestNoContextTakeover,
                   accept.requestNoContextTakeover)
      return pmce


   def __init__(self,
                isServer,
                s2c_no_context_takeover,
                c2s_no_context_takeover):

      self._isServer = isServer
      self._compressor = None
      self._decompressor = None

      self.s2c_no_context_takeover = s2c_no_context_takeover
      self.c2s_no_context_takeover = c2s_no_context_takeover


   def __json__(self):
      return {'extension': self.EXTENSION_NAME,
              's2c_no_context_takeover': self.s2c_no_context_takeover,
              'c2s_no_context_takeover': self.c2s_no_context_takeover}


   def __repr__(self):
      return "PerMessageSnappy(isServer = %s, s2c_no_context_takeover = %s, c2s_no_context_takeover = %s)" % (self._isServer, self.s2c_no_context_takeover, self.c2s_no_context_takeover)


   def startCompressMessage(self):
      if self._isServer:
         if self._compressor is None or self.s2c_no_context_takeover:
            self._compressor = snappy.StreamCompressor()
      else:
         if self._compressor is None or self.c2s_no_context_takeover:
            self._compressor = snappy.StreamCompressor()


   def compressMessageData(self, data):
      return self._compressor.add_chunk(data)


   def endCompressMessage(self):
      return ""


   def startDecompressMessage(self):
      if self._isServer:
         if self._decompressor is None or self.c2s_no_context_takeover:
            self._decompressor = snappy.StreamDecompressor()
      else:
         if self._decompressor is None or self.s2c_no_context_takeover:
            self._decompressor = snappy.StreamDecompressor()


   def decompressMessageData(self, data):
      return self._decompressor.decompress(data)


   def endDecompressMessage(self):
      pass