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
    item5(api)  # Utilizando a api busque os dados da maior venda feita (mostre os dados do cliente, e valor total)
    item6(api)  # lista juntamente os produtos que foram comprados na mairo venda e o valor total de cada.
    item7(api)  # valor total de possíveis vendas (orçamentos) com o valor total de vendas feitas (vendas confirmadas)
    item8(api)  # Vamos ajudar o financeiro agora, você deve mostrar qual o valor total de faturas (notas fiscais) do mês de junho de 2017.
    item9(api)  # Para o cliente que você criou, você deve criar um orçamento para o mesmo com pelo menos um produto


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


def item5(api):
    maior_venda = api.search_read('sale.order', [],
                                  {'fields': ['partner_id', 'amount_total'],
                                   'order': 'amount_total desc',
                                   'limit': 1})
    print u'ITEM 5 - A maior venda realizada foi no valor de R${valor} para o cliente {cliente}.' \
        .format(valor=maior_venda[0].get('amount_total'), cliente=maior_venda[0].get('partner_id')[1])


def item6(api):
    maior_venda = api.search_read('sale.order', [],
                                  {'fields': ['partner_id', 'amount_total', 'order_line', 'total_tax'],
                                   'order': 'amount_total desc',
                                   'limit': 1})
    produto_ids = maior_venda[0].get('order_line')
    imposto = maior_venda[0].get('total_tax')
    print u'ITEM 6 - IMPOSTOS E PRODUTOS'
    print u'\tPagou o valor de R${imposto} em impostos'.format(imposto=imposto)
    produtos = api.read('sale.order.line', produto_ids, ['product_id', 'price_subtotal'])
    for produto in produtos:
        print u'\tProduto: {produto} no valor de R$: {valor}'.format(produto=produto.get('product_id')[1],
                                                                     valor=produto.get('price_subtotal'))


def item7(api):
    ordens_confirmadas = sum(map(lambda i: i.get('amount_total'),
                                 api.search_read('sale.order', [('state', '=', 'sale')], {'fields': ['amount_total']})))
    orcamentos = sum(map(lambda i: i.get('amount_total'),
                         api.search_read('sale.order', [('state', 'in', ('draft', 'sent'))],
                                         {'fields': ['amount_total']})))
    percentual = (100 - (orcamentos * 100) / ordens_confirmadas)

    print u'ITEM 7 - VENDAS CONFIRMADAS: R$ {vendas} | ORCAMENTOS EM ABERTO: {orcamentos} | PERCENTUAL DE FECHAMENTO' \
          u' {fechamento} %'.format(vendas=ordens_confirmadas, orcamentos=orcamentos, fechamento=percentual)


def item8(api):
    fatura = sum(map(lambda i: i.get('amount_total'), api.search_read('account.invoice',
                             [('date_invoice', '>=', '2017-06-01'), ('date_invoice', '<=', '2017-06-30')],
                             {'fields': ['amount_total']})))

    print u'ITEM 8 - O VALOR TOTAL DAS FATURAS DO MES DE JUNHO DE 2017 FOI DE R${fatura}'.format(fatura=fatura)


def item9(api):
    cliente_id = api.search('res.partner', [('cnpj_cpf', '=', '06896429623')])
    values = {
        'partner_id': cliente_id[0],
        'pricelist_id': 1,
        'order_line': [
            [0, False, {'product_id': 270, 'product_uom_qty': 1}]
        ]
    }
    orcamento_id = api.create('sale.order', values)
    print u'ITEM 9 - FOI CRIADO UM ORCAMENTO COM O ID {id}'.format(id=orcamento_id)



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
