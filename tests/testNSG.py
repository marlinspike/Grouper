import unittest
from network.securitygroup.securityrule import SecurityRule
import json
from collections import defaultdict
from collections import OrderedDict

class Test_NSG(unittest.TestCase):
    #Test create new Security Rule
    def test_securityrule(self):
        rule:SecurityRule = SecurityRule()
        self.assertEqual("",rule.description)
        self.assertEqual("",rule.resourceGroup)
        self.assertEqual("",rule.location)
        self.assertEqual("",rule.nsgname)
        self.assertEqual("",rule.rulename)
        self.assertEqual("",rule.description)
        self.assertEqual("",rule.protocol)
        self.assertEqual("",rule.access)
        self.assertEqual("",rule.priority)
        self.assertEqual("",rule.direction)
        self.assertEqual("",rule.sourcePortRange)
        self.assertEqual("",rule.sourceAddressPrefix)
        self.assertEqual("",rule.destinationAddressPrefix)
        self.assertEqual("",rule.destinationPortRange)
        self.assertEqual([],rule.sourcePortRanges)
        self.assertEqual([],rule.destinationPortRanges)
        self.assertEqual([],rule.sourceAddressPrefixes)
        self.assertEqual([],rule.destinationAddressPrefixes)

    #Test export rule as dict
    def test_securityrule_is_dict(self):
        rule:SecurityRule = SecurityRule()
        self.assertIsInstance(rule.toDict(), dict)

    def test_json_to_rule(self) -> SecurityRule:
        jsonRule = """{
        "access": "Allow",
        "description": null,
        "destinationAddressPrefix": "*",
        "destinationAddressPrefixes": [],
        "destinationApplicationSecurityGroups": null,
        "destinationPortRange": "80",
        "destinationPortRanges": [],
        "direction": "Inbound",
        "name": "HTTP",
        "priority": 300,
        "protocol": "TCP",
        "resourceGroup": "AzureBackupRG_eastus_1",
        "sourceAddressPrefix": "*",
        "sourceAddressPrefixes": [],
        "sourcePortRange": "*",
        "sourcePortRanges": [],
        "location":"xxxxx",
        "nsgname":"xxxxx",
        "rulename":"xxxxx",
        "type": "Microsoft.Network/networkSecurityGroups/securityRules"
        }"""
        JsonDoc = json.loads(jsonRule)
        rule:SecurityRule = SecurityRule().createFromJson(jsonRule)
        dictRule = rule.toOrderedDict()
        self.assertEqual(300, dictRule["priority"])
        self.assertEqual('80', dictRule["destinationPortRange"])
        self.assertEqual('xxxxx', dictRule["rulename"])
        self.assertEqual('TCP', dictRule["protocol"])
        self.assertEqual('AzureBackupRG_eastus_1', dictRule["resourceGroup"])
        self.assertEqual('*', dictRule["sourceAddressPrefix"])
        self.assertIsInstance(dictRule["sourceAddressPrefixes"], list)
        self.assertEqual('xxxxx', dictRule["nsgname"])
        self.assertIsInstance(dictRule["sourcePortRanges"], list)
        return dictRule


    #Test creating a rule from dict
    def test_create_from_dict(self):
        lDict:defaultdict = defaultdict(list)
        lDict["x"].append(self.test_json_to_rule())
        sr:SecurityRule = SecurityRule()
        sr = sr.createFromOrderedDict(lDict["x"][0])
        self.assertAlmostEqual(300,sr.priority)


if __name__ == '__main__':
    unittest.main()