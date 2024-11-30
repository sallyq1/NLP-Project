'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

import { createClient } from '../../utils/supabase/server'

export async function login(formData: FormData) {
  const supabase = await createClient()

  const senddata = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  }

  const { data, error } = await supabase.auth.signInWithPassword(senddata)

  if (error) {
    redirect('/error');
  }

  console.log("Session Token: ", data.session.access_token); // Get the token

  revalidatePath('/', 'layout')
  redirect('/')
}

// export async function signup(formData: FormData) {
//   const supabase = await createClient()
  
//   const data = {
//     email: formData.get('email') as string,
//     password: formData.get('password') as string,
//   }

//   const { error } = await supabase.auth.signUp(data)

//   if (error) {
//     redirect('/error')
//   }

//   revalidatePath('/', 'layout')
//   redirect('/')
// }