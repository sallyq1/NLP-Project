'use client'

import { logout } from './actions'; // Import the logout function
import { useRouter } from 'next/navigation';

const LogoutPage: React.FC = () => {
  const router = useRouter();

  const handleLogout = async () => {
    await logout(); // Call the logout function
    router.push('/'); // Redirect to the home page after logout
  };

  return (
    <div className='flex justify-center items-center min-h-screen bg-gray-100'>
      <div className='bg-white p-8 rounded-lg shadow-lg w-full max-w-sm'>
        <h2 className="text-2xl text-gray-700 font-semibold text-center mb-6">Logout</h2>
        <p className="text-gray-700 text-center mb-6">Are you sure you want to log out?</p>
        <div className='flex justify-center'>
          <button
            onClick={handleLogout}
            className='rounded-full py-2 px-4 bg-black text-white hover:bg-gray-800'
          >
            Log out
          </button>
        </div>
      </div>
    </div>
  );
};

export default LogoutPage;
