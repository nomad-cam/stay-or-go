from stayorgo import app

app.debug = True #disable for production servers
app.run(host="0.0.0.0", port=9112)