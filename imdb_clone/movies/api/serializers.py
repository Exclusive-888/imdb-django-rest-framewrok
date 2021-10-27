"""All model fields are put here for educational/experimental purpose"""

from rest_framework import serializers

from movies.models import Movie




class MovieSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Movie
        fields = (
            'url', 'id',
            'name', 'slug', 'name', 'original_name',
            'is_featured',
            'release_date', 'duration', 'imdb_rating',
            'content', 'content_source', 'trailer', 'trailer_info',
            'image', 'image_credit',
            'age', 'trailer_video', 'duration_humanize',
            )
        lookup_field = 'slug'
        #add Extra keyword arguments
        extra_kwargs = {
            'url': {
                'view_name': 'movies:movie-detail',
                'lookup_field': 'slug'}
        }


