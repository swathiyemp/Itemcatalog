from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

from itemscatalog import Category, Base, Items, Description, User

engine = create_engine("postgresql://catalog:topsecret@localhost/catalogdb")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


user1 = User(name="swathi yemperala", email="swatz2006@gmail.com")


session.add(user1)
session.commit()

category1 = Category(name="Soccer", user_id=1)

session.add(category1)
session.commit()

items1 = Items(name="Soccer Cleats",  category=category1, user_id=1)

session.add(items1)
session.commit()

description1 = Description(content="Soccer shoes, soccer cleats,"
                                   "soccer boots whatever the name, most of"
                                   "the time a soccer shoe is a firm ground"
                                   "soccer shoe",
                           items=items1, user_id=1)

session.add(description1)
session.commit()


items2 = Items(name="Shin Guards", category=category1, user_id=1)

session.add(items2)
session.commit()

description2 = Description(content="A shin guard or shin pad is a piece"
                                   "of equipment worn on the front of a"
                                   "player's shin to protect them from"
                                   "injury.",
                           items=items2, user_id=1)

session.add(description2)
session.commit()


items3 = Items(name="Uniform", category=category1, user_id=1)

session.add(items3)
session.commit()

description3 = Description(content="In association football, kit"
                                   "also referred to as strip or soccer"
                                   "uniform is the standard equipment and"
                                   "attire worn by players.",
                           items=items3, user_id=1)


session.add(description3)
session.commit()


category2 = Category(name="Basket Ball", user_id=1)

session.add(category2)
session.commit()


items1 = Items(name="Basket Ball Hoop", category=category2, user_id=1)

session.add(items1)
session.commit()

description1 = Description(content="A Basket Ball hoop is a raised vertical"
                                   "board with a basket attached.A basketball"
                                   "hoop is mounted to a basketball backboard",
                           items=items1, user_id=1)

session.add(description1)
session.commit()

items2 = Items(name="Basket Ball Shoes", category=category2, user_id=1)

session.add(items2)
session.commit()

description2 = Description(content="Basketball shoes are all created with the"
                                   "same basic type of construction that"
                                   "includes an upper, a midsole, and an"
                                   "outsole.",
                           items=items2, user_id=1)


session.add(description2)
session.commit()

category3 = Category(name="Base Ball", user_id=1)

session.add(category3)
session.commit()

items1 = Items(name="Base Ball Cleats", category=category3, user_id=1)

session.add(items1)
session.commit()

description1 = Description(content="Baseball cleats are designed to give"
                                   "athletes the traction, support, and"
                                   "comfort they need to perform on the"
                                   "diamond.",
                           items=items1, user_id=1)

session.add(description1)
session.commit()

items2 = Items(name="Base Ball Bat", category=category3, user_id=1)

session.add(items2)
session.commit()

description2 = Description(content="A baseball bat is a smooth wooden or metal"
                                   "club used in the sport of baseball to hit"
                                   "the ball after it is thrown by the"
                                   "pitcher.",
                           items=items2, user_id=1)

session.add(description2)
session.commit()

category4 = Category(name="Frisbee", user_id=1)

session.add(category4)
session.commit()

items1 = Items(name="Frisbee Disc", category=category4, user_id=1)

session.add(items1)
session.commit()

description1 = Description(content="A frisbee (also called a flying disc or"
                                   "simply a disc) is a gliding toy or"
                                   "sporting item used for throwing and"
                                   "catching.",
                           items=items1, user_id=1)

session.add(description1)
session.commit()

print "list created"
