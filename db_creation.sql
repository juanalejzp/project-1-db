CREATE DATABASE IF NOT EXISTS college_manager;

USE call_center;

CREATE TABLE IF NOT EXISTS campaigns (
  id INT AUTO_INCREMENT PRIMARY KEY,
  campaign_name VARCHAR(255) NOT NULL,
  start_date DATE NOT NULL,
  aim TEXT,
  customer VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS workers (
  code INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  emails VARCHAR(255),
  position VARCHAR(100),
  campaign_id INT,
  FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);