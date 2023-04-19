
-- stores information about user
CREATE TABLE users (
	userID int NOT NULL AUTO_INCREMENT,
	username varchar(255) NOT NULL,
	password varchar(255) NOT NULL,
	isAdmin varchar(1) DEFAULT 'N',
	PRIMARY KEY(userID)
)
