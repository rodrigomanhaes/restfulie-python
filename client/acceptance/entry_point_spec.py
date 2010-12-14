import unittest
import urllib
from should_dsl import should
from fake_server import start_server, stop_server
from restfulie import Restfulie

class EntryPoint(unittest.TestCase):

    def it_gets_raw_data_from_an_entry_point(self):
        uri = 'http://localhost:8081/myresource'
        content = "<item><name>Rich Rock Sunshine</name></item>"
        self.server_content(content)

        resource = Restfulie.at(uri).raw().get()
        resource.response.code |should| be(200)
        resource.response.body |should| equal_to(content)

    def it_retrieves_content_as_xml(self):
        uri = 'http://localhost:8081/myresource'
        content = '''<items>
                        <item>
                            <name>product</name>
                            <price>2</price>
                        </item>
                        <item>
                            <name>another product</name>
                            <price>5</price>
                        </item>
                    </items>'''

        for content_type in ('application/xml', 'text/xml'):
            self.server_content(content, content_type)

            resource = Restfulie.at(uri).get()
            resource.items[0].name |should| equal_to('product')
            resource.items[0].price |should| be(2)
            resource.items[1].name |should| equal_to('another product')
            resource.items[1].price |should| be(5)

    def it_retrieves_content_as_json(self):
        uri = 'http://localhost:8081/myresource'
        content = '''{"item": {"name": "product", "price": 2}}'''
        self.server_content(content, 'application/json')

        resource = Restfulie.at(uri).get()
        resource.item.name |should| equal_to('product')
        resource.item.price |should| be(2)

    def setUp(self):
        start_server()

    def tearDown(self):
        stop_server()

    def server_content(self, content, content_type=None):
        data = urllib.urlencode({'content': content})
        urllib.urlopen('http://localhost:8081/set_content', data)
        if content_type:
            data = urllib.urlencode({'content_type': content_type})
            urllib.urlopen('http://localhost:8081/set_content_type', data)

