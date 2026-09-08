--------------------- ENUM ---------------------

CREATE TYPE gender_type AS ENUM ('Male', 'Female', 'Other');
CREATE TYPE type_of_interaction AS ENUM ('Liked', 'Viewed', 'Matched');

--------------------- TABLES ---------------------


--- users ---
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


--- Profiles ---
CREATE TABLE IF NOT EXISTS userProfile(
  user_id uuid,
  age DATE,
  gender gender_type DEFAULT 'Other',
  gender_pref gender_type[] DEFAULT '{Male, Female}',
  bio TEXT,
  pictures TEXT[],
  popularity INT DEFAULT 50,
  localisation VARCHAR(255) DEFAULT NULL,
  tags INT[]
);


--- interaction ---
CREATE TABLE IF NOT EXISTS interaction (
  id uuid ,
  from_user_id uuid,
  to_user_id uuid,
  which_interaction type_of_interaction,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---- MATCHES ---- 
CREATE TABLE IF NOT EXISTS matches (
  id uuid,
  user_low_id uuid DEFAULT NOT NULL,
  user_high_id uuid DEFAULT NOT NULL,
  conversation_id uuid DEFAULT NOT NULL,
  created_at TIMESTAMP DEFAULT NOT NULL,
);

CREATE TABLE IF NOT EXISTS chat (
  id uuid DEFAULT NOT NULL,
  from_user_id uuid,
  message string DEFAULT NOT NULL,
  sended_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS blocked (
  user_id uuid,
  user_id_blocked uuid
);

CREATE TABLE IF NOT EXISTS tags (
  index integer PRIMARY KEY,
  label string DEFAULT NOT NULL
);




------ TO START WITH SOME FAKE PROFILES -------

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
) ON CONFLICT DO NOTHING;