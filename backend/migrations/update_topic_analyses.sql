-- Update topic_analyses table to better store LLM analysis results
ALTER TABLE IF EXISTS public.topic_analyses
    ADD COLUMN IF NOT EXISTS topic_id UUID REFERENCES public.topics(id),
    ADD COLUMN IF NOT EXISTS analysis_data JSONB,
    ADD COLUMN IF NOT EXISTS relevant_extracts JSONB,
    ADD COLUMN IF NOT EXISTS summary TEXT,
    ADD COLUMN IF NOT EXISTS sentiment TEXT,
    ADD COLUMN IF NOT EXISTS analyzed_at TIMESTAMPTZ DEFAULT now();

-- Create index for topic_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_topic_analyses_topic_id ON public.topic_analyses(topic_id);

-- Comment on table and columns
COMMENT ON TABLE public.topic_analyses IS 'Stores LLM analysis results for topics from plenary sessions and tweets';
COMMENT ON COLUMN public.topic_analyses.topic_id IS 'Reference to the topic being analyzed';
COMMENT ON COLUMN public.topic_analyses.analysis_data IS 'Complete analysis data from LLM in JSON format';
COMMENT ON COLUMN public.topic_analyses.relevant_extracts IS 'Extracted relevant text from sessions and tweets';
COMMENT ON COLUMN public.topic_analyses.summary IS 'Summary of the overall discourse on the topic';
COMMENT ON COLUMN public.topic_analyses.sentiment IS 'Overall sentiment analysis (positive, negative, neutral, mixed)';
COMMENT ON COLUMN public.topic_analyses.analyzed_at IS 'Timestamp when the analysis was performed'; 