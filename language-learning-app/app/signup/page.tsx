'use client'

import { redirect } from 'next/dist/server/api-utils'
import { signup } from './actions'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function SignUpPage() {
  const router = useRouter()
  return (
    <div className='flex justify-center items-center min-h-screen bg-gray-100'>
      <form className='justify-items-center bg-white p-8 rounded-lg shadow-lg w-full max-w-sm'>
        <h2 className="text-2xl text-gray-700 font-semibold text-center mb-6">Sign Up</h2>
        <div className='justify-items-start space-y-6'>
          <div className='text-gray-700'>
            <label htmlFor="email">Email:</label>
            <input id="email" name="email" type="email" required className='p-1 rounded-md ml-10 border border-black border-opacity-15'/>
          </div>

          <div className='text-gray-700'>
            <label htmlFor="name">Name:</label>
            <input id="name" name="name" type="text" required className='p-1 rounded-md ml-3 border border-black border-opacity-15'/>
          </div>

          <div className='text-gray-700'>
            <label htmlFor="password">Password:</label>
            <input id="password" name="password" type="password" required className='p-1 rounded-md ml-3 border border-black border-opacity-15'/>
          </div>
        </div>
        <div className='mt-8 space-x-7'>
        <button
          className='rounded-full py-2 px-4 m-2 bg-black text-white hover:border hover:bg-white hover:text-black' 
          onClick={() => {router.push('/login')}}
          >Login</button>
          <button formAction={signup} className='rounded-full py-2 px-4 m-2 bg-black text-white hover:border hover:bg-white hover:text-black'>Sign up</button>
        </div>
      </form>
    </div>
  )
}