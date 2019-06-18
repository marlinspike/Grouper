## Grouper
A Python command line tool to manage Azure Network Security Group Rules

## Inspiration
A cutomer I was working with wanted a way to manage all their NSGs through a single (preferrably GUI) tool, so that a network admin/manager could edit them, without the need to know a scripting lanaguage or ARM. Azure NSGs are powerful, but while platform provides versatile traffic rules, it doesn't provide a convenient visual way to manage them across multiple NSGs. I've made Grouper to provide a solution for that.

## Basics
Grouper can:
- Save all the NSG rules in your current Azure subscription to a CSV File, so that you can manage them via Excel or any other CSV editor
- Generate ARM templates from the CSV file, which can be committed to your Source Control System. ARM Templates are idempotent, so it won't matter if you re-run the same template: it will have no more effects than running it a sigle time
- Generate a sample CSV file so you can experiment with Grouper

## Future
Some of the future development ideas I'm toying with:
- Export to CLI, which is also idempotent, and a widely used way to interact programmatically with Azure
- Apply templates rules across NSGs
- Export to PowerShell