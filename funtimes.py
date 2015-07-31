import SOAPpy
wsdlFile = 'https://testsystem.globalsign.com/kb/ws/v1/ManagedSSLService?wsdl'
soappy_client = SOAPpy.WSDL.Proxy(wsdlFile)

import suds.client
suds_client = suds.client.Client(wsdlFile)

import commands
def _get_password():
    s, o = commands.getstatusoutput('pass globalsigntest')
    if s != 0:
        import sys
        sys.exit(1)
    return o

def get_mssl_domains():
    ### Let's make a call to GetMSSLDomains(), which should be a
    ### read-only action.
    args = suds_client.factory.create('BmV1GetMsslDomainListRequest')
    args.QueryRequestHeader.AuthToken.UserName = 'PAR03383_sandstorm'
    args.QueryRequestHeader.AuthToken.Password = _get_password()
    return suds_client.service.GetMSSLDomains(args)

def check_domain_in_list(domain):
    x = get_mssl_domains()
    for domain_details in x.SearchMsslDomainDetails.SearchMsslDomainDetail:
        if domain_details.MSSLDomainName == domain:
            return True
    return False
