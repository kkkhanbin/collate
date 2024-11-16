from flask import render_template, redirect
from werkzeug.exceptions import BadRequest

from src_temp.parsers import MapParser
from src_temp.routes import routes_bp
from src_temp.forms import SearchForm, EditMapForm
from src_temp.api import Static


@routes_bp.route('/', methods=['GET', 'POST'])
def index():
    form = EditMapForm()

    if form.validate_on_submit():
        # Если на эту страницу перешли с формы, то пересылаем на эту же
        # страницу, но с параметром l в адресной строке. Нужно для того, чтобы
        # пользователь мог обновлять страницу без посылания новой формы
        l = form.L_TYPES_CONVERT[form.l.data]
        lon, lat = form.longitude.data, form.latitude.data
        z = form.z.data

        return redirect(
            Static.create_url(
                '/', params={'l': l, 'lon': lon, 'lat': lat, 'z': z})
        )

    try:
        map_args = MapParser().parse_args()
    except BadRequest:
        map_params = DEFAULT_MAP_PARAMS
    else:
        map_params = {
            'l': map_args.l,
            'll': f'{map_args.lon},{map_args.lat}',
            'z': map_args.z,
            'pt': map_args.pt
        }

    world_map = Static.get(params=map_params)
    if not world_map:
        world_map = Static.get(params=DEFAULT_MAP_PARAMS)
    url = world_map.url if world_map is not None else ''

    return render_template(
        'index.html', title=TITLE, search_form=SearchForm(),
        world_map=url, form=form, map_params=map_params)
