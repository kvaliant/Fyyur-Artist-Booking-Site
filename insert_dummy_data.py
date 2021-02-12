from app import db, Venue, venue_genres, Artist, artist_genres, Genres, PastShows, UpcomingShows, Area

genresJazz = Genres(name='Jazz')
genresReggae = Genres(name='Reggae')
genresSwing = Genres(name='Swing')
genresClassical = Genres(name="Classical")
genresFolk = Genres(name="Folk")
genresRnB = Genres(name="R&B")
genresHipHop = Genres(name="Hip-Hop")
genresRocknRoll = Genres(name="Rock n Roll")

area1 = Area(
    city = "San Francisco",
    state = "CA",
)
area2 = Area(
    city = "New York",
    state = "NY",
)

pastshows1 = PastShows(
    start_time = "2019-05-21T21:30:00.000Z"
)
pastshows2 = PastShows(
    start_time = "2019-06-15T23:00:00.000Z"
)
upcomingshows3 = UpcomingShows(
    start_time = "2035-04-01T20:00:00.000Z"
)

venue1 = Venue(
    name = "The Musical Hop",
    address = "1015 Folsom Street",
    city = "San Francisco",
    state = "CA",
    phone = "123-123-1234",
    website = "https://www.themusicalhop.com",
    facebook_link = "https://www.facebook.com/TheMusicalHop",
    seeking_talent = True,
    seeking_description = "We are on the lookout for a local artist to play every two weeks. Please call us.",
    image_link = "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    past_shows_count = 1,
    upcoming_shows_count = 0,
)
venue1.genres = [genresJazz, genresReggae, genresSwing, genresClassical, genresFolk]
venue1.past_shows = [pastshows1]
venue1.upcoming_shows = []


venue2 = Venue(
    name = "The Dueling Pianos Bar",
    address = "335 Delancey Street",
    city = "New York",
    state = "NY",
    phone = "914-003-1132",
    website = "https://www.theduelingpianos.com",
    facebook_link = "https://www.facebook.com/TheMusicalHop",
    seeking_talent = False,
    seeking_description = "",
    image_link = "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    past_shows_count = 0,
    upcoming_shows_count = 0,
)
venue2.genres = [genresClassical, genresRnB, genresHipHop]
venue2.past_shows = []
venue2.upcoming_shows = []    

venue3 = Venue(
    name = "Park Square Live Music & Coffee",
    address = "34 Whiskey Moore Ave",
    city = "San Francisco",
    state = "CA",
    phone = "415-000-1234",
    website = "https://www.parksquarelivemusicandcoffee.com",
    facebook_link = "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    seeking_talent = False,
    seeking_description = "",
    image_link = "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    past_shows_count = 1,
    upcoming_shows_count = 1,
)
venue3.genres = [genresRocknRoll, genresJazz, genresClassical, genresFolk]
venue3.past_shows = [pastshows2]
venue3.upcoming_shows = [upcomingshows3]

artist1 = Artist(
    name = "Guns N Petals",
    city = "San Francisco",
    state = "CA",
    phone = "326-123-5000",
    website = "https://www.gunsnpetalsband.com",
    facebook_link = "https://www.facebook.com/GunsNPetals",
    seeking_venue = True,
    seeking_description = "Looking for shows to perform at in the San Francisco Bay Area!",
    image_link = "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    past_shows_count = 1,
    upcoming_shows_count = 0,
)
artist1.genres = [genresRocknRoll]
artist1.past_shows = [pastshows1]
artist1.upcoming_shows = []

artist2 = Artist(
    name = "Matt Quevedo",
    city = "New York",
    state = "NY",
    phone = "300-400-5000",
    facebook_link = "https://www.facebook.com/mattquevedo923251523",
    seeking_venue = False,
    image_link = "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    past_shows_count = 1,
    upcoming_shows_count = 0,
)
artist2.genres = [genresJazz]
artist2.past_shows = [pastshows2]
artist2.upcoming_shows = []

artist3= Artist(
    name = "The Wild Sax Band",
    city = "San Francisco",
    state = "CA",
    phone = "432-325-5432",
    seeking_venue = False,
    image_link = "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    past_shows_count = 0,
    upcoming_shows_count = 3,
)
artist3.genres = [genresJazz, genresClassical]
artist3.past_shows = []
artist3.upcoming_shows = [upcomingshows3]

area1.venue = [venue1, venue3]
area2.venue = [venue2]

db.session.add(genresJazz)
db.session.add(genresReggae)
db.session.add(genresSwing)
db.session.add(genresClassical)
db.session.add(genresFolk)
db.session.add(genresRnB)
db.session.add(genresHipHop)
db.session.add(genresRocknRoll) 

db.session.add(area1)
db.session.add(area2)

db.session.add(venue1)
db.session.add(venue2)
db.session.add(venue3)

db.session.add(artist1)
db.session.add(artist2)
db.session.add(artist3)

db.session.commit()