'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

import { createClient } from '../../utils/supabase/server'
import { cookies } from 'next/headers'

export async function logout() {
    const supabase = await createClient()
  
    const { error } = await supabase.auth.signOut()
  
    if (error) {
      redirect('/error')
    }

    cookies().delete('session_token');
    redirect('/');
  
  }