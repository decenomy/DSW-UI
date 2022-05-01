import React from 'react';
import { Link } from 'react-router-dom'

export function Navbar() {
  return (
    <nav>
    <ul>
      <li><Link to='/'>Home</Link></li>
      <li><Link to='/roster'>Roster</Link></li>
      <li><Link to='/schedule'>Schedule</Link></li>
    </ul>
  </nav>
);
}

export default Navbar;