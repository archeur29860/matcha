--------------------- ENUM ---------------------

CREATE TYPE gender_type AS ENUM ('Male', 'Female', 'Other');
CREATE TYPE type_of_interaction AS ENUM ('Liked', 'Viewed', 'Blocked', 'Reported', 'Unliked');



--------------------- TABLES ---------------------

--- users ---
CREATE TABLE IF NOT EXISTS users (
  id UUID DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(50) UNIQUE NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  password VARCHAR(255) NOT NULL,
  last_connection DATE,
  is_online BOOLEAN DEFAULT false,
  signaled INTEGER DEFAULT 0,

  --- PK ---
  PRIMARY KEY (id)
);


--- Profiles ---
CREATE TABLE IF NOT EXISTS userProfile(
  user_id UUID UNIQUE,
  age DATE,
  gender gender_type DEFAULT 'Other',
  gender_pref gender_type[] DEFAULT '{Male, Female}',
  bio TEXT,
  picture_profile_index INT,
  popularity INT DEFAULT 0,
  localisation VARCHAR(255) DEFAULT NULL,
  tags INT[],

  --- Constraint --- 
  CONSTRAINT fk_user
    FOREIGN KEY (user_id) 
    REFERENCES users(id) 
    ON DELETE CASCADE
);


--- pictures ---
CREATE TABLE IF NOT EXISTS pictures (
  index INT NOT NULL,
  user_id UUID NOT NULL,
  url VARCHAR(255) NOT NULL,

  --- Constraint ---
  CONSTRAINT fk_user
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);


--- interactions ---
CREATE TABLE IF NOT EXISTS interactions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  from_user_id UUID NOT NULL,
  to_user_id UUID NOT NULL,
  which_interaction type_of_interaction NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  --- Constraint ---
  CONSTRAINT fk_from_user
    FOREIGN KEY (from_user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,
  
  CONSTRAINT fk_to_user
    FOREIGN KEY (to_user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);

---- MATCHES ---- 
CREATE TABLE IF NOT EXISTS matches (
  id UUID DEFAULT gen_random_uuid() UNIQUE,
  user_low_id UUID NOT NULL,
  user_high_id UUID NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  --- PK ---
  PRIMARY KEY (id),

  --- Constraint ---
  CONSTRAINT fk_low_user
    FOREIGN KEY (user_low_id)
    REFERENCES users(id)
    ON DELETE CASCADE,
  
  CONSTRAINT fk_high_user
    FOREIGN KEY (user_high_id)
    REFERENCES users(id)
    ON DELETE CASCADE, 
  
  CONSTRAINT unique_match_relation
    UNIQUE (user_low_id, user_high_id)
);


--- CHAT --- 
CREATE TABLE IF NOT EXISTS chat (
  id UUID NOT NULL,
  from_user_id UUID NOT NULL,
  message VARCHAR,
  sended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_read BOOLEAN DEFAULT false,

  --- Constraint --- 
  CONSTRAINT fk_chat_id
    FOREIGN KEY (id) 
    REFERENCES matches(id) 
    ON DELETE CASCADE
);

---- BLOCKED -----
CREATE TABLE IF NOT EXISTS blocked (
  user_id UUID NOT NULL,
  user_id_blocked UUID NOT NULL,

  --- Constraint ---
  CONSTRAINT fk_user
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,
  
  CONSTRAINT fk_user_blocked
    FOREIGN KEY (user_id_blocked)
    REFERENCES users(id)
    ON DELETE CASCADE,
  
  CONSTRAINT unique_block_relation
    UNIQUE (user_id, user_id_blocked)
);


---- TAGS ----
CREATE TABLE IF NOT EXISTS tags (
  id SERIAL PRIMARY KEY,
  label VARCHAR(25) UNIQUE
);

---- LOCALISATION ----
CREATE TABLE IF NOT EXISTS localisation (
  user_id UUID PRIMARY KEY UNIQUE,
  street VARCHAR(150),
  district VARCHAR(150),
  city VARCHAR(150) NOT NULL,
  postcode VARCHAR(5) NOT NULL,
  department VARCHAR(150) NOT NULL,
  lat FLOAT NOT NULL,
  long FLOAT NOT NULL,
  gps_consent BOOLEAN NOT NULL DEFAULT TRUE,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  
  --- Foreign Key ---
  CONSTRAINT fk_user
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,
  
  --- Validation Constraints ---
  CONSTRAINT chk_user_latitude
    CHECK (lat BETWEEN -90 AND 90),
  
  CONSTRAINT chk_user_longitude
    CHECK (long BETWEEN -180 AND 180)
);