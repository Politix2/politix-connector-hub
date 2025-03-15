-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create plenary_sessions table
CREATE TABLE IF NOT EXISTS public.plenary_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    date TIMESTAMPTZ NOT NULL,
    content TEXT NOT NULL,
    source_url TEXT,
    collected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    analyzed BOOLEAN NOT NULL DEFAULT false,
    analysis_result JSONB
);

-- Set RLS policies for plenary_sessions
ALTER TABLE public.plenary_sessions ENABLE ROW LEVEL SECURITY;

-- Create access policies for plenary_sessions
DROP POLICY IF EXISTS "Enable read access for all users" ON public.plenary_sessions;
CREATE POLICY "Enable read access for all users" ON public.plenary_sessions
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Enable insert access for all users" ON public.plenary_sessions;
CREATE POLICY "Enable insert access for all users" ON public.plenary_sessions
    FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Enable update access for all users" ON public.plenary_sessions;
CREATE POLICY "Enable update access for all users" ON public.plenary_sessions
    FOR UPDATE USING (true);

-- Create tweets table
CREATE TABLE IF NOT EXISTS public.tweets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tweet_id TEXT NOT NULL UNIQUE,
    user_handle TEXT NOT NULL,
    user_name TEXT,
    content TEXT NOT NULL,
    posted_at TIMESTAMPTZ NOT NULL,
    collected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    analyzed BOOLEAN NOT NULL DEFAULT false,
    analysis_result JSONB
);

-- Set RLS policies for tweets
ALTER TABLE public.tweets ENABLE ROW LEVEL SECURITY;

-- Create access policies for tweets
DROP POLICY IF EXISTS "Enable read access for all users" ON public.tweets;
CREATE POLICY "Enable read access for all users" ON public.tweets
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Enable insert access for all users" ON public.tweets;
CREATE POLICY "Enable insert access for all users" ON public.tweets
    FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Enable update access for all users" ON public.tweets;
CREATE POLICY "Enable update access for all users" ON public.tweets
    FOR UPDATE USING (true);

-- Create topic_analyses table
CREATE TABLE IF NOT EXISTS public.topic_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id TEXT NOT NULL,
    content_type TEXT NOT NULL,
    topics TEXT[] NOT NULL,
    sentiment TEXT,
    keywords TEXT[],
    analysis_date TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Set RLS policies for topic_analyses
ALTER TABLE public.topic_analyses ENABLE ROW LEVEL SECURITY;

-- Create access policies for topic_analyses
DROP POLICY IF EXISTS "Enable read access for all users" ON public.topic_analyses;
CREATE POLICY "Enable read access for all users" ON public.topic_analyses
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Enable insert access for all users" ON public.topic_analyses;
CREATE POLICY "Enable insert access for all users" ON public.topic_analyses
    FOR INSERT WITH CHECK (true); 