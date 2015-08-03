import SOAPpy
wsdlFile = 'https://testsystem.globalsign.com/kb/ws/v1/ManagedSSLService?wsdl'
try:
    print soappy_client
except NameError:
    soappy_client = SOAPpy.WSDL.Proxy(wsdlFile)

import suds.client
try:
    print suds_client
except NameError:
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
    args.Request.OrderRequestParameter.OrderKind = 'new'

    # Create option object to specify we need a custom validity period.
    option = suds_client.factory.create('Option')
    option.OptionName = "VPC"
    option.OptionValue = True
    args.Request.OrderRequestParameter.Options.Option.append(option)

    # Let's do 1 month.
    args.Request.OrderRequestParameter.ValidityPeriod.Months = 1
    args.Request.OrderRequestParameter.ValidityPeriod.NotBefore = '2015-08-01T21:02:13.554-05:00'
    args.Request.OrderRequestParameter.ValidityPeriod.NotAfter = '2015-08-31T21:02:13.554-05:00'

    args.Request.OrderRequestParameter.CSR = open('csr/just-testing.sandcats.io.csr').read()
    args.Request.MSSLDomainID = domain_info['MSSLDomainID']
    args.Request.MSSLProfileID = domain_info['MSSLProfileID']
    args.Request.ContactInfo.FirstName = 'Bond'
    args.Request.ContactInfo.LastName = 'James Bond'
    args.Request.ContactInfo.Phone = '+1 585-555-1234'
    args.Request.ContactInfo.Email = 'bond@example.com'
    import ZSI
    #print ZSI.SoapWriter().serialize(args)  #import pdb; pdb.set_trace()
    return suds_client.service.PVOrder(__inject={'msg': s})
#return suds_client.service.PVOrder(args)

s = '''<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soap:Body>
<PVOrder><Request><OrderRequestHeader>

               <AuthToken>



                  <UserName>PAR03383_sandstorm</UserName>

                  <Password>''' + _get_password() + '''</Password>

               </AuthToken>

            </OrderRequestHeader>

            <OrderRequestParameter>

               <ProductCode>PV</ProductCode>

               <OrderKind>new</OrderKind>



             <Options>

                  <Option>

                     <OptionName>VPC</OptionName>

                     <OptionValue>true</OptionValue>

                  </Option>

               </Options>



 <ValidityPeriod>


                  <Months>6</Months>

               <NotBefore>2015-08-04T10:33:10.000-05:00</NotBefore>

               <NotAfter>2015-08-31T21:02:13.554-05:00</NotAfter>


 </ValidityPeriod>


               <CSR>''' + open('csr/just-testing.sandcats.io.csr').read() + '''</CSR>

            </OrderRequestParameter>

            <MSSLProfileID>03383_SMS2_178</MSSLProfileID>

            <MSSLDomainID>DSMS20000000612</MSSLDomainID>



            <ContactInfo>

               <FirstName>Bond</FirstName>

               <LastName>James Bond</LastName>

               <Phone>+1 585-555-1234</Phone>

               <Email>bond@example.com</Email>

            </ContactInfo></Request></PVOrder></soap:Body></soap:Envelope>'''
