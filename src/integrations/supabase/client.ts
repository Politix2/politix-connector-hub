// This file is automatically generated. Do not edit it directly.
import { createClient } from '@supabase/supabase-js';
import type { Database } from './types';

const SUPABASE_URL = "https://vlacjeyimegjellrepjv.supabase.co";
const SUPABASE_PUBLISHABLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZsYWNqZXlpbWVnamVsbHJlcGp2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIwNDQzNTcsImV4cCI6MjA1NzYyMDM1N30.9xf3FXNG2XMEKcRfHPTI5N6B4qSc1rh-dRcIuEpKYts";

// Import the supabase client like this:
// import { supabase } from "@/integrations/supabase/client";

export const supabase = createClient<Database>(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY);