from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from itemscatalog import Category, Base, Items, Description, User

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


user1 = User(name="", email="")


session.add(user1)
session.commit()

category1 = Category(name="Soccer", user=user1)

session.add(category1)
session.commit()

items1 = Items(name="Soccer Cleats",  category=category1, user=user1)

session.add(items1)
session.commit()

description1 = Description(content="Soccer shoes, soccer cleats,"
                                   "soccer boots whatever the name, most of"
                                   "the time a soccer shoe is a firm ground"
                                   "soccer shoe",
                           items=items1, user=user1)

session.add(description1)
session.commit()


items2 = Items(name="Shin Guards", category=category1, user=user1)

session.add(items2)
session.commit()

description2 = Description(content="A shin guard or shin pad is a piece"
                                   "of equipment worn on the front of a"
                                   "player's shin to protect them from"
                                   "injury.",
                           items=items2, user=user1)

session.add(description2)
session.commit()


items3 = Items(name="Uniform", category=category1, user=user1)

session.add(items3)
session.commit()

description3 = Description(content="In association football, kit"
                                   "also referred to as strip or soccer"
                                   "uniform is the standard equipment and"
                                   "attire worn by players. The sport's Laws"
                                   "of the Game specify the minimum kit which"
                                   "a player must use, and also prohibit the"
                                   "use of anything that is dangerous to"
                                   "either the player or another participant.",
                           items=items3, user=user1)


session.add(description3)
session.commit()


category2 = Category(name="Basket Ball", user=user1)

session.add(category2)
session.commit()


items1 = Items(name="Basket Ball Hoop", category=category2, user=user1)

session.add(items1)
session.commit()

description1 = Description(content="A Basket Ball hoop is a raised vertical"
                                   "board with a basket attached.A basketball"
                                   "hoop is mounted to a basketball backboard"
                                   "via a flexible connection between the"
                                   "backboard and the connection sroble the"
                                   "hoop.",
                           items=items1, user=user1)

session.add(description1)
session.commit()

items2 = Items(name="Basket Ball Shoes", category=category2, user=user1)

session.add(items2)
session.commit()

description2 = Description(content="Basketball shoes are all created with the"
                                   "same basic type of construction that"
                                   "includes an upper, a midsole, and an"
                                   "outsole. Each of these key components is"
                                   "designed to provide basketball players"
                                   "with the best playing experience.",
                           items=items2, user=user1)


session.add(description2)
session.commit()

category3 = Category(name="Base Ball", user=user1)

session.add(category3)
session.commit()

items1 = Items(name="Base Ball Cleats", category=category3, user=user1)

session.add(items1)
session.commit()

description1 = Description(content="Baseball cleats are designed to give"
                                   "athletes the traction, support, and"
                                   "comfort they need to perform on the"
                                   "diamond. Tons of technology is built into"
                                   "the outsole of these cleats and there are"
                                   "generally two options: metal or molded.",
                           items=items1, user=user1)

session.add(description1)
session.commit()

items2 = Items(name="Base Ball Bat", category=category3, user=user1)

session.add(items2)
session.commit()

description2 = Description(content="A baseball bat is a smooth wooden or metal"
                                   "club used in the sport of baseball to hit"
                                   "the ball after it is thrown by the"
                                   "pitcher.By regulation it may be no more"
                                   "than 2.75 inches (70 mm) in diameter at"
                                   "the thickest part and no more than 42"
                                   "inches (1,100 mm) long.",
                           items=items2, user=user1)

session.add(description2)
session.commit()

category4 = Category(name="Frisbee", user=user1)

session.add(category4)
session.commit()

items1 = Items(name="Frisbee Disc", category=category4, user=user1)

session.add(items1)
session.commit()

description1 = Description(content="A frisbee (also called a flying disc or"
                                   "simply a disc) is a gliding toy or"
                                   "sporting item that is generally plastic"
                                   "and roughly 20 to 25 centimetres (8 to 10"
                                   "in) in diameter with a lip, used"
                                   "recreationally and competitively for"
                                   "throwing and catching.",
                           items=items1, user=user1)

session.add(description1)
session.commit()

print "list created"
