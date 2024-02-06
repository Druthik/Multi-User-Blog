CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
);

CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- title VARCHAR(255) NOT NULL,
    image_path VARCHAR NOT NULL,
    text_data VARCHAR(255), -- Assuming storing image URLs
    -- date_published DATETIME,
    -- comment_enabled BOOLEAN,
    username VARCHAR(255) NOT NULL,
    FOREIGN KEY (username) REFERENCES users(username)
);

CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT,
    user_id INT,
    comment_text TEXT NOT NULL,
    date_posted DATETIME,
    -- anonymous BOOLEAN,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (username) REFERENCES users(username)
);

-- Additional tables will be added as needed, e.g., for likes, user sessions, etc.
