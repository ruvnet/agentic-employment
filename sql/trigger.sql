CREATE TRIGGER sync_human_feedback_trigger
AFTER INSERT OR UPDATE OR DELETE ON human_feedback
FOR EACH ROW
EXECUTE FUNCTION sync_human_feedback();
