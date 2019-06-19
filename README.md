## Grouper
A Python command line tool to manage Azure Network Security Group Rules

## Inspiration
A cutomer I was working with wanted a way to manage all their NSGs through a single (preferrably GUI) tool, so that a network admin/manager could edit them, without the need to know a scripting lanaguage or ARM. Azure NSGs are powerful, but while platform provides versatile traffic rules, it doesn't provide a convenient visual way to manage them across multiple NSGs. I've made Grouper to provide a solution for that.

## Basics
Grouper can:
- Save all the NSG rules in your current Azure subscription to a CSV File, so that you can manage them via Excel or any other CSV editor
- Generate ARM templates from the CSV file, which can be committed to your Source Control System. ARM Templates are idempotent, so it won't matter if you re-run the same template: it will have no more effects than running it a sigle time
- Generate a sample CSV file so you can experiment with Grouper

## Using Grouper
Grouper is an easy to use command line tool. It requires the Azure CLI installed and you must log in to the subscription for which you want to manage Network Security Group rules.

### 1 - Setting up dependencies
- Install python dependencies: python setup.py install
- Install Azure CLI (if you don't already have it installed): https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
- Log in to your Azure subscription using the Azure CLI: az login

### 2 - Getting basic help for Grouper
`python app.py `

This prints basic command help text to console.
![Print basic help](https://raw.githubusercontent.com/marlinspike/grouper/master/readme/grouper-1.png)

### 3 - Serialize Azure Network Security Group (NSG) rules to a local CSV file
Grouper will use the Azure CLI to query your subscription for NSG rules, and then parse the response to create a CSV file in the root of the Grouper application. This CSV file can become your management plane for editing or creating new NSG Rules, or simply a single pane of glass to see all the NSG rules in your subscription.

`python app.py aznsg --csvfile azure-nsg.csv`

![alt text](https://raw.githubusercontent.com/marlinspike/grouper/master/readme/grouper-aznsg.png)

### 4 - Edit the CSV file in your favorite editor
You can then use Excel, Numbers, or any other editor to view or make edits to your NSG Rules, including adding rules, or modifying existing ones. Once you're done, use Grouper to create ARM Templates from your CSV file.

![Edit CSV File](https://raw.githubusercontent.com/marlinspike/grouper/master/readme/grouper-edit-csv.png)

### 5 - Create ARM templates from your CSF File
Editing your NSGs via CSV File is just the first step; Grouper allows you to export your CSV files as ARM Tempalates, which you can then check into your source control as valid and complete rules that can be applied manually via PowerShell/CI, in the Portal, or via your CI/CD pipeline. In that way, your exported ARM templates now become your Infrastructure as Code, while still maintaining an easy to use control plane (your CSV editor).

`python app.py csvtoarm --csvfile azure-nsg.csv`
![Convert CSV File to ARM Template](https://raw.githubusercontent.com/marlinspike/grouper/master/readme/grouper-csvtoarm.png)

The resulting ARM templates are exported to the *output* folder, as shown below:
![ARM Templates in Output folder](https://raw.githubusercontent.com/marlinspike/grouper/master/readme/grouper-armtemplates.png)

### 6 Generate a sample CSV to experiment and test editing and exporting ARM Templates
Grouper can generate a sample CSV file so that you can experiment with editing the CSV File, and then generate ARM templates. The sample NSG Rules provide a nice playground to see how edits are converted to ARM templates.

`python app.py generatecsv`
![Generate Sample CSV File](https://raw.githubusercontent.com/marlinspike/grouper/master/readme/grouper-generatecsv.png)


## Future
Some of the future development ideas I'm toying with:
- Export to CLI, which is also idempotent, and a widely used way to interact programmatically with Azure
- Apply templates rules across NSGs
- Export to PowerShell