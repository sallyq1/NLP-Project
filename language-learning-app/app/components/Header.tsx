import React from 'react'
import { useRouter } from 'next/navigation';
import Image from 'next/image';

const Header = () => {
    const router = useRouter();

    const handleLogout = () => {
        router.push('/logout'); 
      };
  return (
    <div className='flex items-center justify-between bg-white w-full py-5 px-20 '>   

<Image src="/fluently-logo.svg" alt="logo" width={200} height={100}/>

    <button
      onClick={handleLogout}
      className=" px-8 py-3 text-lg rounded-full bg-[#23AAA7]/20 text-[#23AAA7] font-semibold hover:bg-[#23AAA7]/40 transition-all"
    >
      Logout
    </button></div>
  )
}

export default Header

