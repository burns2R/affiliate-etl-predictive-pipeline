-- Relational database schema initialization for PostgreSQL

-- Relational database schema initialization for PostgreSQL

-- Master table for unified, cleansed reporting data across platforms
CREATE TABLE IF NOT EXISTS campaign_performance (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    campaign_id INT NOT NULL,
    campaign_name VARCHAR(255),
    clicks FLOAT DEFAULT 0.0,
    conversions FLOAT DEFAULT 0.0,
    earnings FLOAT DEFAULT 0.0,
    advertiser VARCHAR(100),
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_campaign_perf UNIQUE (date, campaign_id, advertiser)
);

-- Analytical table to capture the optimized traffic configurations from the ML script
CREATE TABLE IF NOT EXISTS traffic_weights_optimization (
    id SERIAL PRIMARY KEY,
    campaign_id INT NOT NULL,
    campaign_name VARCHAR(255),
    category VARCHAR(100),
    optimized_weight FLOAT NOT NULL,
    predicted_epc FLOAT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);