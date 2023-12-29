from db import User,Todo,Base,engine


print("Creating database......")


Base.metadata.create_all(bind=engine)