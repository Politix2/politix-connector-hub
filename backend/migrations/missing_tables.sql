-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT NOT NULL UNIQUE,
    name TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_login TIMESTAMPTZ
);

-- Set RLS policies for users
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Create access policies for users
DROP POLICY IF EXISTS "Enable read access for all users" ON public.users;
CREATE POLICY "Enable read access for all users" ON public.users
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Enable insert access for all users" ON public.users;
CREATE POLICY "Enable insert access for all users" ON public.users
    FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Enable update access for own user" ON public.users;
CREATE POLICY "Enable update access for own user" ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- Create topics table
CREATE TABLE IF NOT EXISTS public.topics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    keywords TEXT[] NOT NULL,
    user_id UUID NOT NULL REFERENCES public.users(id),
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Set RLS policies for topics
ALTER TABLE public.topics ENABLE ROW LEVEL SECURITY;

-- Create access policies for topics
DROP POLICY IF EXISTS "Enable read access for own or public topics" ON public.topics;
CREATE POLICY "Enable read access for own or public topics" ON public.topics
    FOR SELECT USING (user_id = auth.uid() OR is_public = true);

DROP POLICY IF EXISTS "Enable insert access for authenticated users" ON public.topics;
CREATE POLICY "Enable insert access for authenticated users" ON public.topics
    FOR INSERT WITH CHECK (user_id = auth.uid());

DROP POLICY IF EXISTS "Enable update access for own topics" ON public.topics;
CREATE POLICY "Enable update access for own topics" ON public.topics
    FOR UPDATE USING (user_id = auth.uid());

-- Create topic_subscriptions table for users to follow topics
CREATE TABLE IF NOT EXISTS public.topic_subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id),
    topic_id UUID NOT NULL REFERENCES public.topics(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(user_id, topic_id)
);

-- Set RLS policies for topic_subscriptions
ALTER TABLE public.topic_subscriptions ENABLE ROW LEVEL SECURITY;

-- Create access policies for topic_subscriptions
DROP POLICY IF EXISTS "Enable read access for own subscriptions" ON public.topic_subscriptions;
CREATE POLICY "Enable read access for own subscriptions" ON public.topic_subscriptions
    FOR SELECT USING (user_id = auth.uid());

DROP POLICY IF EXISTS "Enable insert access for own subscriptions" ON public.topic_subscriptions;
CREATE POLICY "Enable insert access for own subscriptions" ON public.topic_subscriptions
    FOR INSERT WITH CHECK (user_id = auth.uid());

DROP POLICY IF EXISTS "Enable delete access for own subscriptions" ON public.topic_subscriptions;
CREATE POLICY "Enable delete access for own subscriptions" ON public.topic_subscriptions
    FOR DELETE USING (user_id = auth.uid());

-- Create topic_mentions table to track when topics are mentioned
CREATE TABLE IF NOT EXISTS public.topic_mentions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES public.topics(id),
    content_id UUID NOT NULL,
    content_type TEXT NOT NULL,  -- "plenary_session" or "tweet"
    mention_context TEXT,
    detected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_notified BOOLEAN NOT NULL DEFAULT false
);

-- Set RLS policies for topic_mentions
ALTER TABLE public.topic_mentions ENABLE ROW LEVEL SECURITY;

-- Create access policies for topic_mentions
DROP POLICY IF EXISTS "Enable read access for topic mentions" ON public.topic_mentions;
CREATE POLICY "Enable read access for topic mentions" ON public.topic_mentions
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.topics t
            WHERE t.id = topic_id AND (t.user_id = auth.uid() OR t.is_public = true)
        )
    );

DROP POLICY IF EXISTS "Enable insert access for system" ON public.topic_mentions;
CREATE POLICY "Enable insert access for system" ON public.topic_mentions
    FOR INSERT WITH CHECK (true); 