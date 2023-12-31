-- Database: crud_flask
--

-- --------------------------------------------------------

--
-- Table structure for table category
--

CREATE TABLE IF NOT EXISTS category_table (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  PRIMARY KEY (id)
);

--
-- Table structure for table conditions
--

CREATE TABLE IF NOT EXISTS condition_table (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  PRIMARY KEY(id)
);

--
-- Table structure for table grant
--
CREATE TABLE IF NOT EXISTS grant_table (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  fain varchar(255),
  federal varchar(255) NOT NULL,
  PRIMARY KEY(id)
);


--
-- Table structure for table location
--

CREATE TABLE IF NOT EXISTS location_table (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  PRIMARY KEY(id)
);

--
-- Table structure for table owner
--

CREATE TABLE IF NOT EXISTS owner_table (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  PRIMARY KEY(id)
);

--
-- Table structure for table equipment
--

CREATE TABLE IF NOT EXISTS equipment_table (
  id int NOT NULL AUTO_INCREMENT,
  wia varchar(255) NOT NULL,
  category varchar(255) NOT NULL,
  cost varchar(255) NOT NULL,
  aquired varchar(255) NOT NULL,
  description_field varchar(255) NOT NULL,
  serial_field varchar(255) NOT NULL,
  owner_field varchar(255) NOT NULL,
  use_field varchar(255) NOT NULL,
  location_field varchar(255) NOT NULL,
  condition_field varchar(255) NOT NULL,
  inspection varchar(255),
  disposition varchar(255),
  notes varchar(255),
  PRIMARY KEY(id)
);

--
-- Table structure for table owner
--

CREATE TABLE IF NOT EXISTS funding_table (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  percentage varchar(255) NOT NULL,
  equipment_id int NOT NULL,
  PRIMARY KEY(id)
);

--
-- Table structure for table users
--

CREATE TABLE IF NOT EXISTS user_table (
  id int NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(10) NOT NULL,
  is_first_login BOOLEAN DEFAULT TRUE,
  PRIMARY KEY(id)
);
