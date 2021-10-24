import waitress
from . import main


settings = {}
app = main([], **settings)
waitress.serve(app)
