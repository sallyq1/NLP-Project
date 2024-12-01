import { cookies } from 'next/headers';  // to access cookies on the server
import { createClient } from '../utils/supabase/server';  // supabase server-side client
import LoginPage from './login/page'; 
import DashboardPage from './dashboard/page'; 
import { redirect } from 'next/navigation';

export default async function Home() {
  const supabase = await createClient();
  
  // get session cookie to check if the user is logged in
  const cookieStore = cookies();
  const token = cookieStore.get('sb:token')?.value;  // 'sb:token' cookie is used by Supabase
  
  // check if the user is authenticated
  const { data, error } = await supabase.auth.getUser(token);
  
  if (error || !data?.user) {
    // if user isn't authenticated
    console.log('redirected')
    return <LoginPage/>
  }

  // if the user is authenticated, go to dashboard
  return <DashboardPage />;

}