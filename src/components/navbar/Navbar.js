import React from 'react';
import { Link } from 'react-router-dom'

import logo from 'logo.svg';

export function Navbar() {
  return (

<nav className="navbar" role="navigation" aria-label="main navigation">
  <div className="navbar-brand">
    <a className="navbar-item" href="#">
      <img src={logo} width="112" height="28" />
    </a>

    <a role="button" className="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div id="navbarBasicExample" className="navbar-menu">
    <div className="navbar-start">
     
      <Link className="navbar-item" to='/dash'>Dashboard</Link>
      <Link className="navbar-item" to='/receive'>Receive</Link>
      <Link className="navbar-item" to='/send'>Send</Link>
      <Link className="navbar-item" to='/mymn'>My masternodes</Link>

      <div className="navbar-item has-dropdown is-hoverable">
        <a className="navbar-link">
          Utilities
        </a>

        <div className="navbar-dropdown">
        <Link className="navbar-item" to='/bootstrap'>Bootstrap</Link>
        <Link className="navbar-item" to='/updatewallet'>Update wallet</Link>
          
        </div></div>
      <div className="navbar-item has-dropdown is-hoverable">
        <a className="navbar-link">
          Advanced
        </a>

        <div className="navbar-dropdown">
        <Link className="navbar-item" to='/raw'>Create raw transaction</Link>
        </div></div>

      <div className="navbar-item has-dropdown is-hoverable">
        <a className="navbar-link">
          Info
        </a>

        <div className="navbar-dropdown">
        <Link className="navbar-item" to='/mnexplorer'>Masternodes explorer</Link>
        </div></div>
     
    </div>

    <div className="navbar-end">
      <div className="navbar-item">
        <div className="buttons">
          <a className="button is-primary" href="#">
            <strong>Logout</strong>
          </a>
        </div>
      </div>
    </div>
  </div>
</nav>



);
}

export default Navbar;