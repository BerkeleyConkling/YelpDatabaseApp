CREATE TABLE IF NOT EXISTS Category (
    cat_name VARCHAR(100) PRIMARY KEY NOT NULL
);


CREATE TABLE IF NOT EXISTS ZipCode(
    zip VARCHAR(10) PRIMARY KEY NOT NULL,
    population INT,
    avg_income DECIMAL(10,2),
    median_income DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS Business (
    business_id VARCHAR(200) PRIMARY KEY,
    business_name VARCHAR(200) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    state_name VARCHAR(50) NOT NULL,
    street_address VARCHAR(200) NOT NULL,
    zip VARCHAR(10) NOT NULL,
    review_count INT DEFAULT 0,
    review_rating DECIMAL(2, 1) DEFAULT 5.0,
    popularity_score INT DEFAULT 0,
    success_score INT DEFAULT 0,
    num_checkins INT DEFAULT 0,
    FOREIGN KEY (zip) REFERENCES ZipCode(zip)
);

CREATE TABLE IF NOT EXISTS Review (
    review_id VARCHAR(200) PRIMARY KEY,
    user_id VARCHAR(200) NOT NULL,
    business_id VARCHAR(200) NOT NULL,
    stars INT CHECK (stars BETWEEN 1 AND 5),
    review_date DATE NOT NULL,
    review_text TEXT,
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE IF NOT EXISTS BusinessCategory (
    business_id VARCHAR(200) NOT NULL,
    cat_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (business_id, cat_name),
    FOREIGN KEY (business_id) REFERENCES Business(business_id),
    FOREIGN KEY (cat_name) REFERENCES Category(cat_name)
);

CREATE TABLE IF NOT EXISTS Checkin (
    business_id VARCHAR(200) NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    hour_of_day TIME NOT NULL,
    count INT DEFAULT 0,
    FOREIGN KEY(business_id) REFERENCES Business(business_id),
    PRIMARY KEY(day_of_week, hour_of_day)
);
