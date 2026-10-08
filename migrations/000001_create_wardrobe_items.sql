CREATE TABLE IF NOT EXISTS wardrobe_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    color TEXT,
    season TEXT DEFAULT 'all',
    style_tags TEXT DEFAULT '[]',
    image_url TEXT,
    times_worn INTEGER DEFAULT 0,
    created_at TEXT
);

INSERT INTO wardrobe_item (name, category, color, season, style_tags, image_url, times_worn, created_at) VALUES
    ('White Cotton Tee',      'top',       '#f4f4f5', 'summer', '["casual","sport"]',              '', 4, '2026-01-10 08:00:00'),
    ('Navy Oxford Shirt',     'top',       '#1e3a5f', 'all',    '["corporate","smart-casual"]',    '', 2, '2026-01-11 08:00:00'),
    ('Black Silk Blouse',     'top',       '#18181b', 'all',    '["formal","date","corporate"]',   '', 1, '2026-01-12 08:00:00'),
    ('Blue Denim Jeans',      'bottom',    '#3b5b7c', 'all',    '["casual","smart-casual"]',       '', 6, '2026-01-10 08:00:00'),
    ('Charcoal Trousers',     'bottom',    '#374151', 'all',    '["corporate","formal"]',          '', 3, '2026-01-13 08:00:00'),
    ('Beige Chino Shorts',    'bottom',    '#d8c7a8', 'summer', '["casual","sport"]',              '', 5, '2026-01-14 08:00:00'),
    ('Floral Summer Dress',   'dress',     '#e8a0bf', 'summer', '["casual","date"]',               '', 2, '2026-01-15 08:00:00'),
    ('Little Black Dress',    'dress',     '#0a0a0a', 'all',    '["formal","date"]',               '', 1, '2026-01-16 08:00:00'),
    ('White Sneakers',        'shoes',     '#fafafa', 'all',    '["casual","sport","smart-casual"]','', 8, '2026-01-10 08:00:00'),
    ('Black Leather Heels',   'shoes',     '#111111', 'all',    '["formal","date","corporate"]',   '', 2, '2026-01-16 08:00:00'),
    ('Brown Chelsea Boots',   'shoes',     '#6b4423', 'winter', '["smart-casual","casual"]',       '', 3, '2026-01-17 08:00:00'),
    ('Wool Overcoat',         'jacket',    '#4b5563', 'winter', '["corporate","formal","smart-casual"]','', 1, '2026-01-18 08:00:00'),
    ('Denim Jacket',          'jacket',    '#5b7a9c', 'all',    '["casual","smart-casual"]',       '', 4, '2026-01-18 08:00:00'),
    ('Silver Watch',          'accessory', '#c0c0c0', 'all',    '["corporate","formal","smart-casual","date"]','', 0, '2026-01-19 08:00:00'),
    ('Canvas Tote Bag',       'accessory', '#c9b99b', 'all',    '["casual","sport"]',              '', 0, '2026-01-19 08:00:00');
