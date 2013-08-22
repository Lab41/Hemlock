import web

urls = ("/.*", "test")
app = web.application(urls, globals())

class test:
    def GET(self):
        return 'test'

if __name__ == "__main__":
    app.run()
