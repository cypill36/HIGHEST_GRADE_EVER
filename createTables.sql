-- file: createTables.sql
-- author: KayLynn Beard

-- stores information about user
CREATE TABLE users (
	userID int NOT NULL AUTO_INCREMENT,
	username varchar(255) NOT NULL,
	password varchar(255) NOT NULL,
	isAdmin varchar(1) DEFAULT 'N',
	PRIMARY KEY(userID)
)

-- stores query history of users for admin access
CREATE TABLE logs (
	logsID int NOT NULL AUTO_INCREMENT,
	userID int NOT NULL,
	query varchar(4095) NOT NULL,
	time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY(userID) REFERENCES users(userID),
	PRIMARY KEY(logsID)
)
