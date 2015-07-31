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

def get_mssl_domain_info(domain):
    x = get_mssl_domains()
    for domain_details in x.SearchMsslDomainDetails.SearchMsslDomainDetail:
        if domain_details.MSSLDomainName == domain:
            return {
                'MSSLDomainID': domain_details.MSSLDomainID,
                'MSSLProfileID': domain_details.MSSLProfileID,
            }
    return None

def sign_csr():
    domain_info = get_mssl_domain_info('sandcats.io')

    args = suds_client.factory.create('PVOrder')
    args.Request.OrderRequestHeader.AuthToken.UserName = 'PAR03383_sandstorm'
    args.Request.OrderRequestHeader.AuthToken.Password = _get_password()
    args.Request.OrderRequestParameter.ProductCode = 'PV'
    args.Request.OrderRequestParameter.OrderKind = 'New'
    args.Request.OrderRequestParameter.ValidityPeriod.Months = 1  # FIXME
    args.Request.OrderRequestParameter.CSR = open('csr/just-testing.sandcats.io.csr').read()
    args.Request.MSSLDomainID = domain_info['MSSLDomainID']
    args.Request.MSSLProfileID = domain_info['MSSLProfileID']
    args.Request.ContactInfo.FirstName = 'Bond'
    args.Request.ContactInfo.LastName = 'James Bond'
    args.Request.ContactInfo.Phone = '+1 585-555-1234'
    args.Request.ContactInfo.Email = 'bond@example.com'
    return suds_client.service.PVOrder(args)
