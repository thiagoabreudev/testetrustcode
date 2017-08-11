#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api import Api


def main():
    api = Api()
    limpar_registros(api)  # Limpa registros da ultima execucao
    item1(api)  # Criando cliente


def item1(api):
    vals = {
        'name': 'Thiago Abreu Rodrigues',
        'cnpj_cpf': '06896429623',
        'phone': '(31)99130-4223',
        'zip': '35700082'
    }
    cliente_id = api.create('res.partner', vals)
    print U'ITEM 1 - CLIENTE COM CRIADO COM O ID {id}'.format(id=cliente_id)


def limpar_registros(api):
    print u'Deletando orcamentos...'
    print u'Deletando cliente....'
    cliente_id = api.search('res.partner', [('cnpj_cpf', '=', '06896429623')])
    if cliente_id:
        orders = api.search('sale.order', [('partner_id', '=', cliente_id)])
        if orders:
            try:
                api.exec_method('sale.order', 'action_cancel', orders)
            except:
                pass
            api.unlink('sale.order', orders)
        api.unlink('res.partner', cliente_id)

if __name__ == '__main__':
    main()