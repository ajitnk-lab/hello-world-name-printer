from aws_cdk import App
from stack import HelloWorldNamePrinterStack

app = App()
HelloWorldNamePrinterStack(app, "HelloWorldNamePrinterStack")
app.synth()