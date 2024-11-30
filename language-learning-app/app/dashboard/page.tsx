import Link from 'next/link'
import React from 'react'

const DashboardPage = () => {
  return (
    <div>
      DashboardPage
      <Link href='/lesson' className='rounded-lg bg-white p-4 text-black'>generate new lesson</Link>
    </div>
    
  )
}

export default DashboardPage