'use client';

import { useState, useEffect } from 'react';
import { supabase } from './lib/supabase';
import Auth from './components/Auth';
import Assessment from './components/Assessment';
import { User } from '@supabase/supabase-js';
import LoginPage from './login/page';
import DashboardPage from './dashboard/page';

const Home: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const getSession = async () => {
      const { data } = await supabase.auth.getSession();
      setUser(data.session?.user || null);
    };

    getSession();

    const { data: authListener } = supabase.auth.onAuthStateChange((_, session) => {
      setUser(session?.user || null);
    });

    return () => {
      authListener?.subscription?.unsubscribe();
    };
  }, []);

  return <div>{user ? <DashboardPage /> : <LoginPage />}</div>;
};

export default Home;
