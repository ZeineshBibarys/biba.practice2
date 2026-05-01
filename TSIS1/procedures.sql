-- procedures.sql

-- 1. Upsert процедурасы (Практика 8): Бар болса жаңарту, жоқ болса қосу
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_email VARCHAR, p_birthday DATE)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET email = p_email, birthday = p_birthday WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, email, birthday) VALUES(p_name, p_email, p_birthday);
    END IF;
END;
$$;

-- 2. Жаңа телефон қосу (TSIS 1)
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
    IF v_contact_id IS NOT NULL THEN
        INSERT INTO phones(contact_id, phone, type) VALUES(v_contact_id, p_phone, p_type);
    ELSE
        RAISE EXCEPTION 'Контакт табылмады: %', p_contact_name;
    END IF;
END;
$$;

-- 3. Контактіні топқа жылжыту (TSIS 1): Топ жоқ болса, оны құрады
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
BEGIN
    -- Топты іздеу немесе құру
    INSERT INTO groups (name) VALUES (p_group_name)
    ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
    RETURNING id INTO v_group_id;

    -- Контактіні жаңарту
    UPDATE contacts SET group_id = v_group_id WHERE name = p_contact_name;
END;
$$;

-- 4. Кеңейтілген іздеу функциясы (TSIS 1): Аты, email немесе телефоны бойынша
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(contact_name VARCHAR, email VARCHAR, phone_numbers TEXT, group_name VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        c.name, 
        c.email, 
        string_agg(p.phone || ' (' || p.type || ')', ', ') as phones,
        g.name as g_name
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE c.name ILIKE '%' || p_query || '%' 
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END;
$$ LANGUAGE plpgsql;

-- 5. Пагинация (Практика 8)
-- procedures.sql ішіндегі функцияны жаңарту
-- procedures.sql ішінде осы бөлікті тексеріңіз:
-- Ескі функцияны толық өшіру (міндетті түрде қосыңыз)
DROP FUNCTION IF EXISTS get_paginated_contacts(int, int);

-- Жаңа функцияны құру
CREATE OR REPLACE FUNCTION get_paginated_contacts(p_limit INT, p_offset INT)
RETURNS TABLE(name VARCHAR, email VARCHAR, phones TEXT, group_name VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        c.name, 
        c.email, 
        string_agg(p.phone || ' (' || p.type || ')', ', ') as phones,
        g.name as group_name
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    GROUP BY c.id, g.id
    ORDER BY c.name
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;