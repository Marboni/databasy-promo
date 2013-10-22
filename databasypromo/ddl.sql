CREATE TABLE visit (
    uri VARCHAR(1024),
    netloc VARCHAR(1024),
    path VARCHAR(1024),
    time TIMESTAMP
);

CREATE TABLE email (
    email VARCHAR(255),
    time TIMESTAMP
);