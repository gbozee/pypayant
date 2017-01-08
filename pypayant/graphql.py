import requests
import json


def get_value(val):
    if isinstance(val, str):
        return val
    return val.get("value")


def as_valid_graphql(value):
    result = json.dumps(value)
    if type(value) == str:
        return result
    return convert_list(value)


def convert(val, remove_inner=False):
    new_string = json.dumps(val).replace('\\', '')
    for x in val.keys():
        new_string = new_string.replace(json.dumps(x), x)
    # if remove_inner:
    #     return new_string.replace('"','')
    return new_string


def convert_list(val):
    result = {}
    for key, value in val.items():
        if type(value) == list:
            result.update({key: [convert(v, True) for v in value]})
        elif type(value) == dict:
            result.update({key: convert(value)})

        else:
            result.update({key: value})
    return convert(result).replace('["', "[").replace('"]', "]").replace(
        '"{', '{').replace('}"', "}")


def construct_key_value_pair(key, value):
    if type(key) == str:
        return '%s:%s' % (key, as_valid_graphql(value))
    return ",".join(
        construct_key_value_pair(key[x], value[x]) for x, y in enumerate(key))


def resolve_graphql_field(field, value=None):
    if isinstance(field, str):
        return "%s,\n" % field
    # assuming it is a dict
    base = "%s{\n" % field['name']
    if value:
        base = "%s(%s){\n" % (field['name'], construct_key_value_pair(
            field['key'], field['value']))
    for f in field['fields']:
        base += resolve_graphql_field(f, get_value(f))
    base += "}\n"
    return base


def construct_graphql_query(dict_object):
    """
    {"name": "wallet",
    "key": "username",
    "fields": ["owner", "upcoming_earnings",
    {'name': "transactions",
    'key': None,
    "fields": ["display", "type"] }]}
    :returns
        query{
            wallet(username:""){
                total_earned,
                total_withdrawn,
                total_credit_used_to_hire,
                total_used_to_hire,
                total_payed_to_tutor,
                upcoming_earnings,
                transactions{
                    total,
                    type,
                    display,
                    to_string,
                    amount
                }
            }
        }
    """
    base = resolve_graphql_field(dict_object, dict_object.get('value'))
    return "query{\n%s}\n" % base


def construct_graphql_mutation(dict_object):
    # import pdb; pdb.set_trace()
    base = resolve_graphql_field(dict_object, dict_object.get('value'))
    result = "mutation{\n%s}\n" % base
    return result.replace('"', '\"')


def get_field_value(value):
    if isinstance(value, str):
        return value
    return construct_graphql_dict(
        value['name'],
        value['fields'],
        key=value.get('key'),
        value=value.get('value'))


def construct_graphql_dict(name, fields, key=None, value=None):
    options = {
        'name': name,
        'key': key,
        'fields': [get_field_value(x) for x in fields]
    }
    if value:
        options.update(value=value)
    return options


class BaseClient(object):
    def __init__(self, base_url, api_key, implementation="demo"):
        self.base_url = base_url
        self.api_key = api_key
        self.implementation = implementation

    def _response(self, new_query):
        response = requests.post(
            self.base_url, json={'query': new_query,
                                 'variables': None})
        response.raise_for_status()
        return response.json()['data']

    # def _query_graphql_server(self, query):
    #     new_query = construct_graphql_query(query)
    #     return self._response(new_query)

    def _mutation_graphql_server(self, mutation):
        new_query = construct_graphql_mutation(mutation)
        return self._response(new_query)

    def create_invoice_and_send(self, user, booking, name, description):
        """Creat an invoice and send to client
        :param user: the user to send to (an object consisting of
            first_name, email, last_name and primary_phone_no)
        :param booking: a booking object consiting of total_price and 
            last_session which is a datetime object
        :param description: the description on the Invoice
        :param name: The name of the item purchaced"""
        items = [{
            "quantity": "1",
            "description": description,
            "item": name,
            "unit_cost": str(booking.total_price)
        }]
        client = {
            "first_name": user.first_name,
            "email": user.email,
            "last_name": user.last_name,
            "phone": user.primary_phone_no
        }
        query = dict(
            client=client,
            due_date=booking.last_session.strftime("%m/%d/%Y"),
            fee_bearer=json.dumps("client"),
            items=items)
        data = {
            'name': 'createInvoice',
            'key': ['token', 'params', 'implementation'],
            'value': [self.api_key, query, self.implementation],
            'fields': [
                'status', 'message', {
                    'name': 'data',
                    'fields': ['reference_code']
                }
            ]
        }
        new_query = get_field_value(data)
        response = self._mutation_graphql_server(new_query)
        return response['createInvoice']

    def update_invoice_payment(self, user, invoice):
        new_invoice = {}
        for key, value in invoice.items():
            new_invoice.update({key: "%s" % value})
        data = {
            'name': 'updatePayment',
            'key': ["token", "params", "implementation"],
            'value': ["%s" % self.api_key, new_invoice, self.implementation],
            "fields": [
                'status', 'message', {
                    'name': 'data',
                    'fields': [
                        "id", "status", "currency", "message",
                        "transaction_date"
                    ]
                }
            ]
        }
        query = get_field_value(data)
        response = self._mutation_graphql_server(query)
        return response['updatePayment']