from stayorgo import app

app.debug = True #disable for production servers

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9112)