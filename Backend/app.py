from fms import create_app

app = create_app()

def run():
    app.run(port=5000,debug=True)

if __name__ == '__main__':
    run()