#!/usr/bin/python
# -*- encoding: utf-8 -*-
import xmlrpclib


class Api(object):
    def __init__(self):
        self.host = 'http://chocotech.trustcode.com.br'
        self.db = 'chocotech'
        self.user = 'demo'
        self.password = 'demo'
        self.common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.host))
        self.uid = self.common.authenticate(self.db, self.user, self.password, {})
        self.models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.host))

    def create(self, model, vals):
        """
        Servico para consumo do create da Api do odoo
        :param model: O objeto a inserir o registro
        :param vals: Valores a serem inseridos
        :type model: str
        :type vals: dict
        :return: Retorna o id do novo registro criado
        :rtype: bool
        :author: Thiago Abreu Rodrigues <thiago.ar17[at]gmail.com>
        """
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'create', [vals])

    def write(self, model, ids, vals):
        """
        Servico para consumo do write da Api do odoo
        :param model: O objeto a alterar o registro
        :param ids: Lista de ids dos registros a serem alterados
        :param vals: Novos valores do registro
        :type model: str
        :type ids: list
        :type vals: dict
        :return: Booleando informando se o registro foi alterado com sucesso
        :rtype: bool
        :author: Thiago Abreu Rodrigues <thiago.ar17[at]gmail.com>
        """
        self.models.execute_kw(self.db, self.uid, self.password, model, 'write', [ids, vals])

    def search(self, model, args):
        """
        Servico para consumo do search da Api do odoo
        :param model: O objeto a efetuar a pesquisa
        :param args: lista contendo os argumentos para pesquisa
        :type model: str
        :type args: list
        :return: Lista dos ids encontrados
        :rtype: list
        :author: Thiago Abreu Rodrigues <thiago.ar17[at]gmail.com>
        """
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'search', [args])

    def unlink(self, model, ids):
        """
        Servico para consumo do unlink da Api do odoo
        :param model: O objeto a efetuar a exclusao do registro
        :param ids: lista de ids dos registros a serem excluidos
        :type model: str
        :type ids: list
        :return: Booleando se os registros foram excluidos ou nao
        :rtype: bool
        :author: Thiago Abreu Rodrigues <thiago.ar17[at]gmail.com>
        """
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'unlink', ids)

    def search_count(self, model, args):
        """
        Servico para consumo do search_count da Api do odoo
        :param model: O objeto a efetuar a contagem dos registros
        :param args: lista de argumentos para pesquisa
        :type model: str
        :type args: list
        :return: Inteiro informando a quantidade de registros encontrados
        :rtype: int
        :author: Thiago Abreu Rodrigues <thiago.ar17[at]gmail.com>
        """
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'search_count', [args])

    def search_read(self, model, args, values):
        """
        Servico para consumo do search_read da Api do odoo
        :param model: O objeto a efetuar a pesquisa
        :param args: lista de argumentos para efetuar a pesquisa
        :param values: dicionario contendo argumentos adicionais para retorno como campos, limit etc..
        :type model: str
        :type args: list
        :type values: dict
        :return: Lista contendo dicionario dos valores encontrados
        :rtype: list
        :author: Thiago Abreu Rodrigues <thiago.ar17[at]gmail.com>
        """
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'search_read', [args], values)

    def read(self, model, ids, fields):
        """
        Servico para consumo do read da Api do odoo
        :param model: O objeto a efetuar a leitura dos valores
        :param ids: lista de ids para retorno dos seus valores
        :param fields: dicionario contendo argumentos adicionais para retorno como campos, limit etc..
        :type model: str
        :type ids: list
        :type fields: dict
        :return: Lista contendo dicionario dos valores encontrados
        :rtype: list
        :author: Thiago Abreu Rodrigues <thiago.ar17[at]gmail.com>
        """
        return self.models.execute_kw(self.db, self.uid, self.password, model, 'read', [ids], {'fields': fields})

    def exec_method(self, model, method, *args, **kwargs):
        """
        Servico para consumo de metodos adicionais ao orm da Api do odoo
        :param model: O objeto a efetuar a leitura dos valores
        :param method: String contendo o methodo a ser executado
        :param args: lista de argumentos passados como parametro para o metodo
        :param kwargs: dicionario de argumentos passados como parametro para o metodo
        :type model: str
        :type method: str
        :type args: list
        :type kargs: dict
        :return: Depende do retorno do metodo executado
        :author: Thiago Abreu Rodrigues <thiago.ar17[at]gmail.com>
        """
        return self.models.execute_kw(self.db, self.uid, self.password, model, method, args, **kwargs)