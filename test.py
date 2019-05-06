import click
from network.securitygroup.securityrule import SecurityRule

#from network.networksecuritygroups.securityrule import SecurityRule
#import network.networksecuritygroups.securityrule.SecurityRule

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def doIt(count, name):
    

    s = SecurityRule(1,2,3,4,5,6,7,8,0)
    d = {"user":"reuben", "email":"rcleetus@gmail.com", "id":"100"}
    #SecurityRule.createFromDict(user="reuben", email="rcleetus@gmail.com", id = 1)
    new_s = s.createFromDict(**{"user":"reuben", "email":"rcleetus@gmail.com", "id":"100", "description":"This is a description", "protocol":"https"})
    print(new_s)

    print(s)

doIt()
