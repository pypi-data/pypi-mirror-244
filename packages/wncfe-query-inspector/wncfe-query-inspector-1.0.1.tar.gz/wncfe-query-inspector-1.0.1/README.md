SQL Tools
=================
Simple middleware tool for analyzing Django ORM SQL execution. 

# Usage
Add the follow line of code to your middleware in your project settings.py file
```
'wncfe-sql-tools.middleware.new_middleware'
```

# How it works
The tool uses Django built in features to inspect the SQL generated from queries executed by the application. 3rd party tools are used to format and highlight the SQL presented in the terminal window.
