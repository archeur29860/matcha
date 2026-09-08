CREATE TABLE IF NOT EXISTS users (
  id uuid,
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(50) UNIQUE NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  last_connection TIMESTAMP WITH TIME ZONE,
  is_online BOOLEAN DEFAULT false,
  signaled INTEGER DEFAULT 0
);


INSERT INTO users (email, username, last_name, first_name, password, last_connection, is_online, signaled) VALUES
(
  'julien.v@matcha.fr', 
  'julien_paris', 
  'Vasseur', 
  'Julien', 
  '$2b$10$fictionalhashforjulien', 
  CURRENT_TIMESTAMP,
  true, 
  0
);