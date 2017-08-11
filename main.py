#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api import Api


def main():
    api = Api()
    limpar_registros(api)  # Limpa registros da ultima execucao
    item1(api)  # Criando cliente
    item2(api)  # Alterando cliente
    item3(api)  # Quantidade de clientes na base
    item4(api)  # Listar os 10 primeiros clientes por ordem alfabética (Nome e Cidade que mora)


def item1(api):
    vals = {
        'name': 'Thiago Abreu Rodrigues',
        'cnpj_cpf': '06896429623',
        'phone': '(31)99130-4223',
        'zip': '35700082'
    }
    cliente_id = api.create('res.partner', vals)
    print U'ITEM 1 - CLIENTE COM CRIADO COM O ID {id}'.format(id=cliente_id)


def item2(api):
    cliente_id = api.search('res.partner', [('cnpj_cpf', '=', '06896429623')])
    api.write('res.partner', cliente_id, {'rg_fisica': 'MG-12.896.140'})
    print U'ITEM 2 - O CLIENTE DE ID {id} FOI ALTERADO COM SUCESSO'.format(id=cliente_id[0])


def item3(api):
    clientes = api.search_count('res.partner', [])
    print u'ITEM 3 - ESTA BASE POSSUI {clientes} CLIENTES.'.format(clientes=clientes)


def item4(api):
    clientes_ordenado = api.search_read('res.partner', [], {'fields': ['name', 'city'], 'order': 'name', 'limit': 10})
    print u'ITEM 4 - OS 10 PRIMEIROS CLIENTES EM ORDEM ALFABETICA'
    for cliente in clientes_ordenado:
        print u'\tNome: {nome} | Cidade: {cidade}'.format(nome=cliente.get('name'),
                                                          cidade=cliente.get('city') or U'NAO INFORMOU')


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
