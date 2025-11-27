from app.api import bp

@bp.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    pass

@bp.route('/movies', methods=['GET'])
def get_movies():
    pass

@bp.route('/movies/<int:id>/year', methods=['GET'])
def get_year(id):
    pass

@bp.route('/movies/<int:id>/oscars', methods=['GET'])
def get_oscars(id):
    pass

@bp.route('/movies', methods=['POST'])
def create_movie():
    pass

@bp.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    pass