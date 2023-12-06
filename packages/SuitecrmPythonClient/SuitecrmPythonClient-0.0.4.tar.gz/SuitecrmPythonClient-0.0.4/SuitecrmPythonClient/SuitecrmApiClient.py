import PythonAPIClientBase
from .SuitecrmLoginSession import SuitecrmLoginSessionBasedOnClientIdAndSecret
import json

api_prefix = '/legacy/Api/V8/meta'

class SuitecrmApiClient(PythonAPIClientBase.APIClientBase):
  refreshAuthTokenIfRequired = None

  def __init__(self, baseURL, mock=None):
    super().__init__(baseURL=baseURL, mock=mock, forceOneRequestAtATime=True)

  def getLoginSessionBasedOnClientIdAndSecret(self, clientId, clientSecret):
    return SuitecrmLoginSessionBasedOnClientIdAndSecret(APIClient=self, clientId=clientId, clientSecret=clientSecret)

  def getModules(self, loginSession):
    result = self.sendGetRequest(
      url=api_prefix + '/modules',
      loginSession=loginSession,
      injectHeadersFn=None
    )
    if result.status_code != 200:
      self.raiseResponseException(result)

    return json.loads(result.text)
