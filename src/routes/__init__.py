# Blueprint
from flask import Blueprint
routes_bp = Blueprint('routes', __name__, template_folder='templates')

# routes
from .index import index
from .favicon.favicon import favicon
from .results.results import results
from .results.download.download import download

__all__ = (
    "index", "favicon", "results", "download"
)
