CREATE TABLE clients (
    id INT AUTO_INCREMENT,
    name VARCHAR(128) NOT NULL,
    DOB DATE NOT NULL,
    address VARCHAR(255) NOT NULL,
    email VARCHAR(128) NOT NULL,
    gender ENUM('M', 'F'),
    phone VARCHAR(128) NOT NULL,
    ordinal_phone VARCHAR(128) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE client_services (
    id INT AUTO_INCREMENT,
    client_id INT NOT NULL,
    service_id INT NOT NULL,
    status ENUM('ACTIVATED', 'DEACTIVATED'),
    start_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    FOREIGN KEY (client_id)
        REFERENCES clients (id)
        ON UPDATE RESTRICT ON DELETE CASCADE,
    FOREIGN KEY (service_id)
        REFERENCES services (id)
        ON UPDATE RESTRICT ON DELETE CASCADE,
    PRIMARY KEY (id)
);

CREATE TABLE services (
    id INT AUTO_INCREMENT,
    service_code ENUM('mem_30_full', 'mem_30_morning', 'mem_15_entries', 'mem_90_full', 'mem_180_full', 'mem_annual',
    'sup_whey_rule_1', 'sup_bcaa',
    'drink_lavie', 'drink_revive',
    'accessory_gloves_cloth', 'accessory_gloves_rubber', 'accessory_gloves_y', 'accessory_bracer', 'accessory_gloves_dot_cs', 'accessory_gloves_aolike',
    'shaker') NOT NULL,
    version VARCHAR(32) NOT NULL DEFAULT '1.0.0',
    price BIGINT NOT NULL,
    description VARCHAR(1024),
    UNIQUE(service_code, version),
    PRIMARY KEY (id)
);

-- Insert services
INSERT INTO services(service_code, price, description)
VALUES ('mem_30_full', 450000, 'Membership 30 full days');
INSERT INTO services(service_code, price, description)
VALUES ('mem_30_morning', 360000, 'Membership 30 morning days');
INSERT INTO services(service_code, price, description)
VALUES ('mem_15_entries', 340000, 'Membership 15 entries in 30 days');
INSERT INTO services(service_code, price, description)
VALUES ('mem_90_full', 1200000, 'Membership 90 full days');
INSERT INTO services(service_code, price, description)
VALUES ('mem_180_full', 1800000, 'Membership 180 full days');
INSERT INTO services(service_code, price, description)
VALUES ('mem_annual', 3000000, 'Membership 365 full days');

ALTER TABLE services ADD COLUMN period INT NOT NULL DEFAULT 30;
ALTER TABLE services ADD COLUMN entries INT NOT NULL DEFAULT 0;

CREATE TABLE checkins (
    id INT AUTO_INCREMENT,
    client_services_id INT NOT NULL,
    version VARCHAR(32) NOT NULL DEFAULT '1.0.0',
    time DATETIME DEFAULT NOW(),
    type ENUM('CHECKIN', 'CHECKOUT'),
    FOREIGN KEY (client_services_id)
        REFERENCES client_services (id)
        ON UPDATE RESTRICT ON DELETE CASCADE,
    PRIMARY KEY (id)
);
