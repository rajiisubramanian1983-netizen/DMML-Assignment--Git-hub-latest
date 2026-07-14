
CREATE TABLE user_features (
    user_id BIGINT PRIMARY KEY,
    user_activity_count INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE item_features (
    product_id BIGINT PRIMARY KEY,
    total_interactions INT NOT NULL,
    total_engagement_score INT NOT NULL,
    avg_engagement_score FLOAT NOT NULL,
    category_code VARCHAR(255),
    brand VARCHAR(255),
    fakestore_category_match VARCHAR(50),
    category_avg_rating_enrichment FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_co_occurrence (
    product_id_a BIGINT NOT NULL,
    product_id_b BIGINT NOT NULL,
    shared_user_count INT NOT NULL,
    PRIMARY KEY (product_id_a, product_id_b),
    FOREIGN KEY (product_id_a) REFERENCES item_features(product_id),
    FOREIGN KEY (product_id_b) REFERENCES item_features(product_id)
);

CREATE TABLE product_catalog (
    product_id BIGINT PRIMARY KEY,
    title VARCHAR(500),
    category VARCHAR(100),
    price FLOAT,
    price_normalized FLOAT,
    rating_rate FLOAT,
    rating_count INT,
    rating_normalized FLOAT,
    source VARCHAR(50) DEFAULT 'FakeStoreAPI',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);