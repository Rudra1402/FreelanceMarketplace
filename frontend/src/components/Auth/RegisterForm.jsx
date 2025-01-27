import React from 'react';

const RegisterForm = () => {
  return (
    <form>
      <h2>Register</h2>
      <input type="text" placeholder="Username" />
      <input type="email" placeholder="Email" />
      <input type="password" placeholder="Password" />
      <label>
        <input type="checkbox" /> I am a client
      </label>
      <button type="submit">Register</button>
    </form>
  );
};

export default RegisterForm;
