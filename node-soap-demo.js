var soap = require('soap');
var url = 'https://testsystem.globalsign.com/kb/ws/v1/ManagedSSLService?wsdl';
var client = null;
soap.createClient(url, function(err, myClient) {
  client = myClient;
});
