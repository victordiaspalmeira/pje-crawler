import requests

if __name__ == "__main__":
    request = '''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://www.cnj.jus.br/servico-intercomunicacao-2.2.2/" xmlns:tip="http://www.cnj.jus.br/tipos-servico-intercomunicacao-2.2.2">
        <soapenv:Header/>
        <soapenv:Body>
        <ser:consultarProcesso>
        <tip:idConsultante>75293730215</tip:idConsultante>
        <tip:senhaConsultante>admin123</tip:senhaConsultante>
        <tip:numeroProcesso>0032470-55.2016.2.00.0000</tip:numeroProcesso>
        <!--  Opcional - Data para restringir a pesquisa   -->
        <tip:dataReferencia>?</tip:dataReferencia>
        <!--  Opcional - Se true exibe a estrutura com lista de movimentos do processo   -->
        <tip:movimentos>false</tip:movimentos>
        <!--  Opcional - Se true exibe o cabecalho com os dados básico do processo   -->
        <tip:incluirCabecalho>false</tip:incluirCabecalho>
        <!--  Opcional - Se true exibe a estrutura com a lista de documentos do processo   -->
        <tip:incluirDocumentos>false</tip:incluirDocumentos>
        </ser:consultarProcesso>
        </soapenv:Body>
        </soapenv:Envelope>
        <!--  0030244-77.2016.2.00.0000  -->
    '''.encode('utf-8')
    headers = {'Content-Type': 'text/xml'}
    req = requests.Request('POST', 'https://consultarProcesso/ConsultaPJe?wsdl',
                   headers=headers,
                   data=request)

    prepped_requ = req.prepare()
    s = requests.Session()
    http_response = s.send(prepped_requ)
    print(http_response)