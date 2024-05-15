CREATE OR REPLACE FUNCTION sync_human_feedback()
RETURNS TRIGGER AS $$
BEGIN
    -- Handle INSERT event
    IF TG_OP = 'INSERT' THEN
        INSERT INTO human_feedback_sync (id, tenant_id, created_at, agent, task, feedback_type, feedback_details)
        VALUES (NEW.id, NEW.tenant_id, NEW.created_at, NEW.agent, NEW.task, NEW.feedback_type, NEW.feedback_details);
    -- Handle UPDATE event
    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE human_feedback_sync
        SET tenant_id = NEW.tenant_id, created_at = NEW.created_at, agent = NEW.agent, task = NEW.task, feedback_type = NEW.feedback_type, feedback_details = NEW.feedback_details
        WHERE id = OLD.id;
    -- Handle DELETE event
    ELSIF TG_OP = 'DELETE' THEN
        DELETE FROM human_feedback_sync WHERE id = OLD.id;
    END IF;
    RETURN NEW;
END;
$$
 LANGUAGE plpgsql;
