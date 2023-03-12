from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService

from setup_db import db


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    movie1 = Movie(id=1, title='Йеллоустоун', description='description1',
                   trailer='trailer1', year=2018, rating=8.6,
                   genre_id=1, director_id=1)
    movie2 = Movie(id=2, title='Омерзительная восьмерка', description='description2',
                   trailer='trailer2', year=2015, rating=7.8,
                   genre_id=2, director_id=2)
    movie3 = Movie(id=3, title='Вооружен и очень опасен', description='description3',
                   trailer='trailer3', year=1978, rating=6,
                   genre_id=3, director_id=3)

    movie_dao.get_one = MagicMock(return_value=movie1)
    movie_dao.get_all = MagicMock(return_value=[movie1, movie2, movie3])
    movie_dao.create = MagicMock(return_value=Movie(id=3, title='Вооружен и очень опасен'))
    movie_dao.update = MagicMock()
    movie_dao.delete = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id == 1
        assert movie.title == 'Йеллоустоун'

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) == 3

    def test_create(self):
        movie_data = {
            'title': 'Вооружен и очень опасен'
        }
        movie = self.movie_service.create(movie_data)
        assert movie.id is not None
        assert movie.title == movie_data['title']

    def test_update(self):
        movie_data = {
            'id': 3,
            'title': 'Вооружен и очень опасен'
        }
        self.movie_service.update(movie_data)

    def test_delete(self):
        movie = self.movie_service.delete(1)
        assert movie is None
