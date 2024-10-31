'use client';

import { useState } from 'react';
import { signUpWithEmail, signInWithEmail } from '../lib/auth';

const Auth: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [isLogin, setIsLogin] = useState<boolean>(true);
  const [message, setMessage] = useState<string>('');

  const handleAuth = async () => {
    const action = isLogin ? signInWithEmail : signUpWithEmail;
    const { error } = await action(email, password);
    setMessage(error ? error.message : isLogin ? 'Logged in!' : 'Account created!');
  };

  return (
    <div>
      <h2>{isLogin ? 'Login' : 'Sign Up'}</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleAuth}>{isLogin ? 'Login' : 'Sign Up'}</button>
      <button onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? 'Switch to Sign Up' : 'Switch to Login'}
      </button>
      <p>{message}</p>
    </div>
  );
};

export default Auth;
