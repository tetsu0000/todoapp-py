#!/usr/bin/env python3
import aws_cdk as cdk

from todoapp_py.todoapp_py_stack import TodoappPyStack


app = cdk.App()
TodoappPyStack(app, "TodoappPyStack")

app.synth()
